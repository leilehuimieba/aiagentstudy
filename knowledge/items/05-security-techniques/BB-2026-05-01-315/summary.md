# [BB-2026-05-01-315] Summary

## Article

- Title: Introducing SignSaboteur: forge signed web tokens with ease
- Source: PortSwigger Research
- URL: https://portswigger.net/research/introducing-signsaboteur-forge-signed-web-tokens-with-ease
- Date: 05-22
- Topic: `05-security-techniques`
- Tags: signed-tokens, hmac-bypass, authz-bypass, brute-force, flask-express-django

## Model Mapping

- Blocks: Tools/Actions, Evaluation
- Layer: domain knowledge

## Core Takeaway

虽然 SignSaboteur 讲的是 signed token，而不是严格意义上的 filename + filehash 下载参数，但它给出了同类“hash / signature 守门”问题的系统化利用路径：发现 token、识别框架、搜 secret / salt、尝试默认密钥、再做 claims 篡改与权限绕过。对 FlagHunter 来说，这正好可以抽象成一类 hash-guarded 资源访问策略，而不是把这类题都硬编码成某种特定 payload。文章还特别强调 Unknown signed tokens 的检测与 brute-force 模式，对 CTF 中自定义 filehash / sessionhash 结构很有启发。

## Reusable Principle

- 先识别签名对象和框架，再决定 hash / key / salt 的猜测策略。
- 签名类问题的第一阶段不是 exploit，而是 token census 和 format inference。
- 当结构未知时，优先做 unknown token 模式识别与小词表验证。

## FlagHunter Relevance

- `strategy_registry.web.hash_guarded_access`：抽象出 token-discovery -> key-guess -> claim-mutate -> access-check 流水线。
- `HypothesisEngine`：把默认密钥 / 配置泄露 / 文档泄露 / error 泄露作为独立假设分支。
- `FlagProof`：签名伪造成功时记录原 token、修改字段、重签结果和授权变化。
