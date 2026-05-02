# OpenCLI Notes

OpenCLI turns websites, browser sessions, Electron apps, and local tools into deterministic CLI interfaces for humans and AI agents.

## Local Usage

```powershell
opencli doctor -v
opencli browser tab new "https://www.bestblogs.dev/explore"
opencli browser state --tab <targetId>
opencli browser extract --selector "#bbArticleContent" --tab <targetId>
```

## Agent Model Mapping

- Tools/Actions: stable browser and website operations.
- Context/State: logged-in browser state.
- Evaluation/Guardrails: deterministic commands and exit codes.
- Deliverable: article exports, summaries, adapters.

