"""Lazy-start, resident embedding daemon for the dense retrieval channel.

Loading BAAI/bge-m3 costs ~9s (torch + 2.27GB weights). The CLI search path
(`kb.ps1 search`) spawns a fresh python per call and `eval-search.py` spawns one
*per query*, so without a daemon every query re-pays that 9s. This module keeps
the model loaded once in a background process and answers query-encode requests
over a 127.0.0.1 socket, turning the per-query cost from ~10s to <1s.

Design goals (see the conversation that motivated this):
  * Lazy start: the daemon comes up on the FIRST query after boot, not before.
    `client_encode()` auto-spawns it, waits for the model to load, then queries.
  * No boot autostart: there is no Task Scheduler / registry / startup entry.
    The daemon is just a detached child of whatever first queried it; after a
    reboot nothing runs until the next query spawns it again.
  * Graceful degrade: any daemon failure falls back to in-process encoding, so
    search never breaks because the daemon is down.
  * Manual control: `kb.ps1 daemon status|stop|restart` (and an optional idle
    timeout via KB_DAEMON_IDLE_SEC) let the user reclaim the ~2.5GB at will.

Protocol: one JSON request per connection, newline-terminated, JSON reply.
  {"op":"ping"}             -> {"ok":true, "pid":..., "model":..., "uptime":...}
  {"op":"encode","text":s} -> {"ok":true, "vector_b64": <base64 float32 LE>}
  {"op":"shutdown"}        -> {"ok":true}; daemon exits after replying.
"""

import base64
import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RETRIEVAL_DIR = ROOT / "knowledge" / "retrieval"
LOCK_PATH = RETRIEVAL_DIR / ".embed-daemon.json"
LOG_PATH = RETRIEVAL_DIR / ".embed-daemon.log"

HOST = "127.0.0.1"
# How long client_encode() waits for a cold daemon to load the model before it
# gives up and falls back to in-process encoding. Cold disk + torch import can be
# slow, so keep this generous.
SPAWN_TIMEOUT_SEC = float(os.environ.get("KB_DAEMON_SPAWN_TIMEOUT", "90"))
# Per-request socket timeout for an already-running daemon (encode is fast).
REQUEST_TIMEOUT_SEC = float(os.environ.get("KB_DAEMON_REQUEST_TIMEOUT", "30"))
# Auto-shutdown after this many idle seconds (0 = stay resident until reboot or
# manual stop). Default 0 to honor the "常驻" intent; set e.g. 1800 to reclaim RAM.
IDLE_TIMEOUT_SEC = float(os.environ.get("KB_DAEMON_IDLE_SEC", "0"))


# --------------------------------------------------------------------------- #
# Shared helpers
# --------------------------------------------------------------------------- #
def _read_lock():
    try:
        return json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def _send(port, request, timeout):
    """Open a fresh connection, send one JSON request, return the JSON reply."""
    with socket.create_connection((HOST, port), timeout=timeout) as sock:
        sock.settimeout(timeout)
        sock.sendall((json.dumps(request) + "\n").encode("utf-8"))
        buf = bytearray()
        while b"\n" not in buf:
            chunk = sock.recv(65536)
            if not chunk:
                break
            buf.extend(chunk)
    line = bytes(buf).split(b"\n", 1)[0]
    return json.loads(line.decode("utf-8"))


def ping(timeout=2.0):
    """Return the daemon's status dict if a healthy daemon is reachable, else None."""
    lock = _read_lock()
    if not lock or "port" not in lock:
        return None
    try:
        reply = _send(int(lock["port"]), {"op": "ping"}, timeout)
        if reply.get("ok"):
            return {**lock, **reply}
    except Exception:
        return None
    return None


# --------------------------------------------------------------------------- #
# Client side: used by embed_lib.encode_query
# --------------------------------------------------------------------------- #
def _spawn_daemon():
    """Launch the daemon as a detached background process (no console window)."""
    RETRIEVAL_DIR.mkdir(parents=True, exist_ok=True)
    creationflags = 0
    if os.name == "nt":
        DETACHED_PROCESS = 0x00000008
        CREATE_NEW_PROCESS_GROUP = 0x00000200
        CREATE_NO_WINDOW = 0x08000000
        creationflags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW
    log = open(LOG_PATH, "ab", buffering=0)
    subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve()), "serve"],
        stdin=subprocess.DEVNULL,
        stdout=log,
        stderr=log,
        cwd=str(ROOT),
        creationflags=creationflags,
        close_fds=True,
    )


def ensure_daemon(timeout=SPAWN_TIMEOUT_SEC):
    """Return a live daemon's port, spawning and waiting for it if needed."""
    status = ping()
    if status:
        return int(status["port"])

    # Stale or missing lock: spawn a fresh daemon and wait for it to load.
    _spawn_daemon()
    deadline = time.monotonic() + timeout
    delay = 0.25
    while time.monotonic() < deadline:
        time.sleep(delay)
        status = ping()
        if status:
            return int(status["port"])
        delay = min(delay * 1.5, 2.0)
    return None


def client_encode(text):
    """Encode a single query via the daemon. Returns float32[dim] or None.

    None signals the caller to fall back to in-process encoding. Disabled when
    KB_NO_DAEMON is set (e.g. for debugging the pure in-process path).
    """
    if os.environ.get("KB_NO_DAEMON"):
        return None
    port = ensure_daemon()
    if port is None:
        return None
    try:
        reply = _send(port, {"op": "encode", "text": text}, REQUEST_TIMEOUT_SEC)
    except Exception:
        return None
    if not reply.get("ok") or "vector_b64" not in reply:
        return None
    raw = base64.b64decode(reply["vector_b64"])
    return np.frombuffer(raw, dtype=np.float32).copy()


def stop_daemon():
    """Ask a running daemon to shut down. Returns True if one was contacted."""
    lock = _read_lock()
    if not lock or "port" not in lock:
        return False
    try:
        _send(int(lock["port"]), {"op": "shutdown"}, 3.0)
    except Exception:
        pass
    # Confirm it is gone; clean up the lock either way.
    gone = ping(timeout=1.0) is None
    try:
        LOCK_PATH.unlink()
    except Exception:
        pass
    return gone


# --------------------------------------------------------------------------- #
# Server side: `python embed_daemon.py serve`
# --------------------------------------------------------------------------- #
def _log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}", flush=True)


def run_daemon():
    # If a healthy daemon already owns the lock, do nothing (prevents a race
    # where two near-simultaneous queries both spawn a server).
    if ping(timeout=1.0):
        _log("another healthy daemon already running; exiting")
        return

    import embed_lib as E

    _log(f"loading model {E.model_ref()} ...")
    t0 = time.monotonic()
    E.get_model()  # one-time cold load
    _log(f"model loaded in {time.monotonic() - t0:.1f}s")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, 0))
    server.listen(8)
    port = server.getsockname()[1]
    server.settimeout(5.0)  # so the idle check can run between accepts

    started = time.time()
    LOCK_PATH.write_text(
        json.dumps(
            {"pid": os.getpid(), "port": port, "model": E.model_ref(), "started": started},
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    _log(f"listening on {HOST}:{port} (pid {os.getpid()})")

    last_activity = time.monotonic()
    try:
        while True:
            try:
                conn, _ = server.accept()
            except socket.timeout:
                if IDLE_TIMEOUT_SEC and (time.monotonic() - last_activity) > IDLE_TIMEOUT_SEC:
                    _log(f"idle for {IDLE_TIMEOUT_SEC:.0f}s; shutting down")
                    break
                continue

            with conn:
                conn.settimeout(REQUEST_TIMEOUT_SEC)
                try:
                    buf = bytearray()
                    while b"\n" not in buf:
                        chunk = conn.recv(65536)
                        if not chunk:
                            break
                        buf.extend(chunk)
                    if not buf:
                        continue
                    request = json.loads(bytes(buf).split(b"\n", 1)[0].decode("utf-8"))
                    op = request.get("op")

                    if op == "ping":
                        reply = {"ok": True, "pid": os.getpid(), "port": port,
                                 "model": E.model_ref(), "uptime": round(time.time() - started, 1)}
                    elif op == "encode":
                        vec = E.encode_query_local(request.get("text") or "")
                        vec = np.ascontiguousarray(vec, dtype=np.float32)
                        reply = {"ok": True, "vector_b64": base64.b64encode(vec.tobytes()).decode("ascii")}
                    elif op == "shutdown":
                        conn.sendall((json.dumps({"ok": True}) + "\n").encode("utf-8"))
                        _log("shutdown requested")
                        break
                    else:
                        reply = {"ok": False, "error": f"unknown op {op!r}"}

                    conn.sendall((json.dumps(reply, ensure_ascii=False) + "\n").encode("utf-8"))
                    last_activity = time.monotonic()
                except Exception as exc:  # never let one bad request kill the daemon
                    _log(f"request error: {exc!r}")
                    try:
                        conn.sendall((json.dumps({"ok": False, "error": str(exc)}) + "\n").encode("utf-8"))
                    except Exception:
                        pass
    finally:
        server.close()
        # Only remove the lock if it still points at us.
        lock = _read_lock()
        if lock and lock.get("pid") == os.getpid():
            try:
                LOCK_PATH.unlink()
            except Exception:
                pass
        _log("stopped")


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "serve"
    if cmd == "serve":
        run_daemon()
    elif cmd == "status":
        status = ping()
        if status:
            print(json.dumps(status, ensure_ascii=False, indent=2))
        else:
            print("daemon: not running")
            sys.exit(1)
    elif cmd == "stop":
        print("daemon: stopped" if stop_daemon() else "daemon: not running")
    else:
        print(f"unknown command {cmd!r}; use serve|status|stop", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv)
