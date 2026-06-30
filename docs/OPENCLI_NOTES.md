# OpenCLI Notes

OpenCLI turns websites, browser sessions, Electron apps, and local tools into deterministic CLI interfaces for humans and AI agents.

## Local Usage

```powershell
opencli doctor -v
opencli profile list
opencli browser qmvqcrb8 tab new "https://www.bestblogs.dev/explore"
opencli browser qmvqcrb8 state --tab <targetId>
opencli browser qmvqcrb8 extract --selector "#bbArticleContent" --tab <targetId>
```

`qmvqcrb8` is the default local Browser Bridge profile currently used for logged-in browser work. Generic browser/login-state usage is documented in the local Codex skill `opencli-browser-bridge`.

## Agent Model Mapping

- Tools/Actions: stable browser and website operations.
- Context/State: logged-in browser state.
- Evaluation/Guardrails: deterministic commands and exit codes.
- Deliverable: article exports, summaries, adapters.
