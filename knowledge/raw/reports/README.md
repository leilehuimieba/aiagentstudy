# reports/

Batch reports and capture-run / discovery snapshots, moved out of `knowledge/raw/`
to keep the script root scannable. Read-only provenance — useful when auditing why
an item was or was not captured. Not an active interface.

Families:

- `batch-*-report.json` — historical capture batch reports
- `opencli-latest-batch-*.json` — OpenCLI latest-list capture batches
- `edge-featured-batch-*.json`, `edge-latest-batch-*.json` — older Edge capture runs
- `current-opencli-latest-page*-<date>.json` — dated list-API snapshots
- `current-edge-*.json` — Edge list snapshots
- `*-candidates*.json`, `latest-scan-*.json`, `recent-days-scan.json`,
  `explore-links-*.json`, `today-*.json`, `weekly-picks-*.json` — discovery scans
