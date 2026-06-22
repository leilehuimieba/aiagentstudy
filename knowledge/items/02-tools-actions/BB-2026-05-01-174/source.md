# Source Evidence

- Title: Building a safe， effective sandbox to enable Codex on Windows
- BestBlogs URL: https://www.bestblogs.dev/en/article/36e502e0
- Original publisher URL: https://openai.com/codex/
- Original link text: Codex⁠

## Captured Page Metadata

- Browser title: Building a safe， effective sandbox to enable Codex on Windows
- Description: This engineering blog post from OpenAI describes the process of implementing a secure and effective sandbox for their coding agent, Codex, on the Windows operating system. The author explains that Windows lacked a suitable out-of-the-box isolation primitive for an open-ended agentic workload, leading them to evaluate and reject options like AppContainer, Windows Sandbox, and Mandatory Integrity Control. The first prototype, an 'unelevated sandbox,' used synthetic SIDs and write-restricted tokens to control file writes and environment variables to limit network access. While functional, its network suppression was merely advisory and easily bypassed. To achieve strong network isolation, the team redesigned the sandbox to require an elevated setup step. The final 'elevated sandbox' creates dedicated Windows users (CodexSandboxOffline/Online) and applies Windows Firewall rules to them, alongside a dedicated command-runner binary to spawn restricted processes. The post highlights the trade-offs between safety and usability, and the necessity of composing multiple Windows primitives to build a coherent solution for a coding agent.
- Date: Yesterday

## Evidence Links Captured

- Codex⁠: https://openai.com/codex/
- Try it out⁠: https://openai.com/codex/
