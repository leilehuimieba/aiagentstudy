# Security Review - 2026-06-18

Scope: `product/` Flask knowledge-management application.

This review focuses on issues that matter if the local app is exposed beyond a single trusted desktop user, or if it becomes a test harness for exploit samples.

## Findings

### High: Admin endpoints had no authorization

Affected routes:

- `POST /api/admin/reload`
- `POST /api/admin/collect`
- `POST /api/profile/infer`
- `POST /api/report/weekly`

Impact:

- Trigger background collection jobs.
- Trigger LLM calls and cost-bearing work.
- Reload in-memory state.
- Write report files.
- If the Flask server is exposed to LAN or public interfaces, these become unauthenticated management actions.

Fix applied:

- Added `_require_admin()`.
- If `ADMIN_TOKEN` is configured, admin routes require `X-Admin-Token`.
- If no token is configured, admin routes only allow loopback + same-origin/no-origin development requests.
- Frontend API client can send `X-Admin-Token` from `localStorage.ADMIN_TOKEN`.

### High: Debug mode was enabled by default

Previous default:

```text
FLASK_DEBUG=true
```

Impact:

- Flask debug mode is unsafe if the app is exposed beyond localhost.
- Debug consoles and detailed tracebacks increase exploitation risk.

Fix applied:

- Runtime default changed to `false`.
- `.env.template` changed to `FLASK_DEBUG=false`.

### Medium: Browser cross-site POSTs were not rejected

Impact:

- A malicious page could attempt to trigger local or LAN admin-like POST actions from the user's browser.
- Modern browser private-network protections help but should not be the only boundary.

Fix applied:

- Added `request_guard()` to reject unsafe methods when `Origin` or `Referer` does not match the app origin.

### Medium: Request and field sizes were unbounded

Affected inputs:

- `question`
- `query`
- `note_text`
- `article_id`
- `event_type`
- `week`

Impact:

- Memory/cost DoS.
- Excessive LLM prompt cost.
- Large database writes.

Fix applied:

- Added `MAX_REQUEST_BYTES`.
- Added `_bounded_text()` checks on high-impact input fields.
- Added `days` range check.

### Medium: Article body path read was not constrained to knowledge items

Affected function:

- `product/api/db.py::_read_article_text`

Impact:

- If `articles-meta.json` is ever polluted, `article_path` could point outside the intended article corpus.

Fix applied:

- Resolve the final path with `abspath`.
- Require `commonpath([ITEMS_DIR, full]) == ITEMS_DIR`.

### Low: Smoke test had an overly narrow domain assertion

Impact:

- Existing config had 5 subtopics across 2 domains, but the smoke test required 5 under the first domain only.

Fix applied:

- Smoke test now checks total subtopic count and validates that each domain has `subtopics`.

## Remaining Recommendations

- Add rate limiting for LLM endpoints: `/api/qa`, `/api/articles/<id>/summary`, `/api/reviews/enqueue`, `/api/report/weekly`.
- Add structured audit logs for admin actions and LLM calls.
- Store secret values only in `.env`; never log them. Log env key names only.
- Consider adding a simple `APP_AUTH_TOKEN` if the whole app is ever exposed beyond localhost.
- Replace raw `innerHTML` rendering of article, recommendation, and QA data with DOM construction or a strict sanitizer.
- Add tests for the new admin/origin guard.
- Keep real exploit payloads outside static web paths and outside this repository unless encrypted/restricted.

## Verification

Commands run:

```powershell
python -m py_compile product\api\app.py product\api\db.py product\scripts\smoke_test.py
python product\scripts\smoke_test.py
```

Result:

```text
15 PASS / 0 FAIL
```

