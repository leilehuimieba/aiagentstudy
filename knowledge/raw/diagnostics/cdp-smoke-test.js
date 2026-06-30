const fs = require('fs');
const http = require('http');
const { spawn } = require('child_process');

const EDGE = 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';
const USER_DATA_DIR = 'E:\\yuyan\\edge-cdp-bestblogs';
const PORT = 9223;
const TEST_URL = 'https://www.bestblogs.dev/article/b79e265b';

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function requestJson(url, method = 'GET') {
  return new Promise((resolve, reject) => {
    const req = http.request(url, { method }, (res) => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (chunk) => { body += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (err) {
          reject(new Error(`${method} ${url} returned non-JSON: ${body.slice(0, 200)}`));
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function waitForEndpoint() {
  for (let i = 0; i < 30; i += 1) {
    try {
      return await requestJson(`http://127.0.0.1:${PORT}/json/version`);
    } catch (_) {
      await sleep(500);
    }
  }
  throw new Error('CDP endpoint did not become ready');
}

function cdpClient(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let nextId = 1;
  const pending = new Map();
  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  };
  return new Promise((resolve, reject) => {
    ws.onerror = () => reject(new Error('WebSocket error'));
    ws.onopen = () => {
      resolve({
        send(method, params = {}) {
          const id = nextId++;
          ws.send(JSON.stringify({ id, method, params }));
          return new Promise((res, rej) => pending.set(id, { resolve: res, reject: rej }));
        },
        close() {
          ws.close();
        },
      });
    };
  });
}

async function main() {
  fs.mkdirSync(USER_DATA_DIR, { recursive: true });
  const child = spawn(EDGE, [
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${USER_DATA_DIR}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-networking',
    'about:blank',
  ], { detached: true, stdio: 'ignore', windowsHide: true });
  child.unref();

  await waitForEndpoint();
  const target = await requestJson(`http://127.0.0.1:${PORT}/json/new?${encodeURIComponent(TEST_URL)}`, 'PUT');
  const client = await cdpClient(target.webSocketDebuggerUrl);
  await client.send('Runtime.enable');
  await client.send('Page.enable');
  await sleep(9000);
  const result = await client.send('Runtime.evaluate', {
    returnByValue: true,
    expression: `(() => {
      const root = document.querySelector('#bbArticleContent') || document.querySelector('article') || document.querySelector('main') || document.body;
      return {
        url: location.href,
        title: document.title,
        chars: root ? root.innerText.length : 0,
        text: root ? root.innerText.slice(0, 3000) : '',
        links: Array.from(document.querySelectorAll('a[href]')).slice(0, 50).map(a => ({ text: (a.innerText || '').trim(), href: a.href }))
      };
    })()`,
  });
  fs.writeFileSync('knowledge/raw/cdp-smoke-test-result.json', `${JSON.stringify(result.result.value, null, 2)}\n`, 'utf8');
  console.log(JSON.stringify(result.result.value, null, 2));
  client.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
