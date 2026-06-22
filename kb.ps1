param(
  [Parameter(Position = 0)]
  [ValidateSet("search", "pack", "brief", "evidence", "rebuild", "build-item-metadata", "verify", "audit", "health", "repair-audit", "eval", "coverage", "weekly-review", "obsidian-card", "capture", "capture-arxiv", "capture-rss", "capture-browser", "watch", "bulk", "promote", "reject", "defer", "restore", "sources", "source-health", "probe-sources", "discover-sources", "doctor", "status", "help")]
  [string]$Command = "help",

  [Parameter(Position = 1, ValueFromRemainingArguments = $true)]
  [string[]]$Rest
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Show-Help {
  @"
AI Agent Study knowledge-base helper

Usage:
  .\kb.ps1 search "Claude" [--limit 5] [--topic 01-context-memory]
  .\kb.ps1 pack "智能体评估" [--limit 5] [--topic 04-evaluation-guardrails]
  .\kb.ps1 pack "Claude Code auto mode 原文 来源" --profile auto
  .\kb.ps1 pack "Harness Engineering 权限 日志 验证" --profile deep --grouped
  .\kb.ps1 brief "browser use agents" [--limit 5]
  .\kb.ps1 evidence "Claude Code auto mode 原文 来源" [--limit 5]
  .\kb.ps1 rebuild
  .\kb.ps1 build-item-metadata [--execute]
  .\kb.ps1 verify
  .\kb.ps1 audit
  .\kb.ps1 health [--json]
  .\kb.ps1 repair-audit [--fix summary-index] [--execute]
  .\kb.ps1 eval
  .\kb.ps1 coverage [--write] [--date YYYY-MM-DD]
  .\kb.ps1 weekly-review [--eval] [--write] [--date YYYY-MM-DD]
  .\kb.ps1 weekly-review --write [--date YYYY-MM-DD]
  .\kb.ps1 obsidian-card BB-2026-05-01-564 [--module control-loop] [--write] [--force] [--vault-root D:\webstudy\Notes\obsidian\黑曜石]
  .\kb.ps1 obsidian-card BB-2026-05-01-564 --register-existing "D:\webstudy\Notes\obsidian\黑曜石\学习笔记\AI-Agent\03-控制循环与编排\2026-06-18-生产级Agent循环.md" --module control-loop
  .\kb.ps1 doctor
  .\kb.ps1 status
  .\kb.ps1 capture [--page 1] [--page-size 20] [--profile qmvqcrb8] [--discovery-date YYYY-MM-DD]
  .\kb.ps1 capture-arxiv [--query 'all:"AI agent"'] [--max-results 10] [--limit 5]
  .\kb.ps1 capture-rss --ids simon-willison langchain-blog [--limit 5]
  .\kb.ps1 capture-browser --ids openai-news github-trending [--profile qmvqcrb8]
  .\kb.ps1 watch [--limit 20] [--ids openai-news anthropic-news] [--group-by source] [--summary] [--json]
  .\kb.ps1 bulk --action show --ids anthropic-news --limit 5
  .\kb.ps1 bulk --action defer --ids anthropic-news --limit 2 --reason "review later" --execute
  .\kb.ps1 bulk --action reject --type product --limit 2 --reason "low-value product radar" --execute
  .\kb.ps1 promote CAND-2026-0001 [--dry-run] [--method browser --profile qmvqcrb8]
  .\kb.ps1 reject CAND-2026-0001 --reason "duplicate"
  .\kb.ps1 defer CAND-2026-0001 --reason "review later" [--until 2026-06-16]
  .\kb.ps1 restore CAND-2026-0001 [--from-bucket deferred] [--reason "ready to review"]
  .\kb.ps1 sources
  .\kb.ps1 source-health [--limit 20] [--ids openai-news anthropic-news]
  .\kb.ps1 probe-sources [--profile qmvqcrb8] [--ids arxiv openai-news]
  .\kb.ps1 discover-sources [--arxiv-query 'all:"AI agent"'] [--rss huggingface-blog google-deepmind]

Read START_HERE.md for the repository workflow.
"@
}

function Invoke-Query([string]$Mode) {
  if (-not $Rest -or $Rest.Count -eq 0) {
    throw "Missing query. Example: .\kb.ps1 $Mode `"Claude`""
  }
  & python "knowledge\raw\query-kb.py" @Rest --mode $Mode
}

function Show-Status {
  $indexPath = Join-Path $Root "knowledge\catalog\articles-index.md"
  $buildReportPath = Join-Path $Root "knowledge\retrieval\build-report.json"
  $ftsReportPath = Join-Path $Root "knowledge\retrieval\fts-report.json"
  $indexRows = Select-String -Path $indexPath -Pattern '^\| [A-Z][A-Z0-9-]+-' -ErrorAction Stop
  $bestBlogsRows = Select-String -Path $indexPath -Pattern '^\| BB-' -ErrorAction SilentlyContinue
  $arxivRows = Select-String -Path $indexPath -Pattern '^\| ARXIV-' -ErrorAction SilentlyContinue
  $rssRows = Select-String -Path $indexPath -Pattern '^\| RSS-' -ErrorAction SilentlyContinue
  $browserRows = Select-String -Path $indexPath -Pattern '^\| BROWSER-' -ErrorAction SilentlyContinue
  $ids = foreach ($row in $bestBlogsRows) {
    if ($row.Line -match 'BB-2026-05-01-(\d{3})') { [int]$Matches[1] }
  }
  $lastId = if ($ids) { "BB-2026-05-01-{0:000}" -f (($ids | Measure-Object -Maximum).Maximum) } else { "none" }

  Write-Output "Knowledge base status"
  Write-Output "  Catalog rows: $($indexRows.Count)"
  Write-Output "  Latest catalog ID: $lastId"
  Write-Output "  BestBlogs rows: $($bestBlogsRows.Count)"
  Write-Output "  arXiv rows: $($arxivRows.Count)"
  Write-Output "  RSS rows: $($rssRows.Count)"
  Write-Output "  Browser snapshot rows: $($browserRows.Count)"

  $itemsRoot = Join-Path $Root "knowledge\items"
  if (Test-Path -LiteralPath $itemsRoot) {
    Write-Output "  Topic items:"
    Get-ChildItem -LiteralPath $itemsRoot -Directory |
      Sort-Object Name |
      ForEach-Object {
        $count = (Get-ChildItem -LiteralPath $_.FullName -Directory -ErrorAction SilentlyContinue).Count
        Write-Output ("    {0}: {1}" -f $_.Name, $count)
      }
  }

  if (Test-Path -LiteralPath $buildReportPath) {
    $reportText = Get-Content -LiteralPath $buildReportPath -Raw
    $report = $reportText | ConvertFrom-Json
    $generatedAt = if ($reportText -match '"generated_at"\s*:\s*"([^"]+)"') { $Matches[1] } else { $report.generated_at }
    Write-Output "  Retrieval items: $($report.items)"
    Write-Output "  Retrieval generated_at: $generatedAt"
  } else {
    Write-Output "  Retrieval: missing; run .\kb.ps1 rebuild"
  }

  if (Test-Path -LiteralPath $ftsReportPath) {
    $ftsReport = Get-Content -LiteralPath $ftsReportPath -Raw | ConvertFrom-Json
    Write-Output "  FTS chunks: $($ftsReport.chunks)"
  }

  $candidatesRoot = Join-Path $Root "knowledge\candidates"
  if (Test-Path -LiteralPath $candidatesRoot) {
    $candidateFiles = @("inbox.jsonl", "promoted.jsonl", "deferred.jsonl", "rejected.jsonl")
    Write-Output "  Candidates:"
    foreach ($file in $candidateFiles) {
      $path = Join-Path $candidatesRoot $file
      $count = 0
      if (Test-Path -LiteralPath $path) {
        $count = (Get-Content -LiteralPath $path | Where-Object { $_.Trim() }).Count
      }
      Write-Output ("    {0}: {1}" -f $file, $count)
    }
  }
}

function Invoke-WeeklyReview {
  if ($Rest -contains "--write") {
    & python "knowledge\raw\generate-weekly-review.py" @Rest
    return
  }

  Write-Output "Weekly project review"
  Write-Output "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
  Write-Output ""

  Show-Status
  Write-Output ""

  Write-Output "Health"
  & python "knowledge\raw\audit-summary.py"
  Write-Output ""

  Write-Output "Candidate summary"
  & python "knowledge\raw\manage_candidates.py" watch --summary
  Write-Output ""

  Write-Output "Source health focus"
  & python "knowledge\raw\source-health.py" --limit 10
  Write-Output ""

  Write-Output "Management files"
  Write-Output "  - PROJECT_BOARD.md"
  Write-Output "  - PRODUCT_NOW.md"
  Write-Output "  - knowledge\catalog\current-coverage.md"
  Write-Output ""
  Write-Output "Refresh coverage: .\kb.ps1 coverage --write"

  if ($Rest -contains "--eval") {
    Write-Output ""
    Write-Output "Search eval"
    & python "knowledge\raw\eval-search.py"
  } else {
    Write-Output "Run search eval when needed: .\kb.ps1 weekly-review --eval"
  }
}

switch ($Command) {
  "search" {
    Invoke-Query "search"
  }
  "pack" {
    Invoke-Query "pack"
  }
  "brief" {
    if (-not $Rest -or $Rest.Count -eq 0) {
      throw "Missing query. Example: .\kb.ps1 brief `"browser use agents`""
    }
    & python "knowledge\raw\brief-kb.py" @Rest
  }
  "evidence" {
    if (-not $Rest -or $Rest.Count -eq 0) {
      throw "Missing query. Example: .\kb.ps1 evidence `"Claude Code auto mode`""
    }
    & python "knowledge\raw\evidence-kb.py" @Rest
  }
  "rebuild" {
    & node "knowledge\raw\build-kb-retrieval.js"
    & python "knowledge\raw\build-kb-fts.py"
  }
  "build-item-metadata" {
    & python "knowledge\raw\build-item-metadata.py" @Rest
  }
  "verify" {
    & node "knowledge\raw\verify-batch.js"
  }
  "audit" {
    & node "knowledge\raw\audit-kb.js"
  }
  "health" {
    & python "knowledge\raw\audit-summary.py" @Rest
  }
  "repair-audit" {
    & python "knowledge\raw\repair-audit.py" @Rest
  }
  "eval" {
    & python "knowledge\raw\eval-search.py" @Rest
  }
  "coverage" {
    & python "knowledge\raw\generate-current-coverage.py" @Rest
  }
  "weekly-review" {
    Invoke-WeeklyReview
  }
  "obsidian-card" {
    & python "knowledge\raw\generate-obsidian-card.py" @Rest
  }
  "doctor" {
    & opencli doctor -v
    & opencli profile list
  }
  "status" {
    Show-Status
  }
  "capture" {
    & python "knowledge\raw\capture-opencli-latest-page.py" @Rest
  }
  "capture-arxiv" {
    & python "knowledge\raw\capture-arxiv-papers.py" @Rest
  }
  "capture-rss" {
    & python "knowledge\raw\capture-rss-sources.py" @Rest
  }
  "capture-browser" {
    & python "knowledge\raw\capture-browser-sources.py" @Rest
  }
  "watch" {
    & python "knowledge\raw\manage_candidates.py" watch @Rest
  }
  "bulk" {
    & python "knowledge\raw\manage_candidates.py" bulk @Rest
  }
  "promote" {
    & python "knowledge\raw\manage_candidates.py" promote @Rest
  }
  "reject" {
    & python "knowledge\raw\manage_candidates.py" reject @Rest
  }
  "defer" {
    & python "knowledge\raw\manage_candidates.py" defer @Rest
  }
  "restore" {
    & python "knowledge\raw\manage_candidates.py" restore @Rest
  }
  "sources" {
    Get-Content -LiteralPath "knowledge\sources\README.md"
    Write-Output ""
    Write-Output "Source registry: knowledge\sources\source-registry.json"
    Write-Output "Capture strategy: knowledge\sources\capture-strategy.md"
    Write-Output "Paper sources: knowledge\sources\paper-sources.md"
  }
  "source-health" {
    & python "knowledge\raw\source-health.py" @Rest
  }
  "probe-sources" {
    & python "knowledge\raw\probe-ai-sources-opencli.py" @Rest
  }
  "discover-sources" {
    & python "knowledge\raw\discover-ai-source-candidates.py" @Rest
  }
  default {
    Show-Help
  }
}
