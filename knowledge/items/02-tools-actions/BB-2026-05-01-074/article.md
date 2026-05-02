# Claude Code 创始人首次公开：我的 13 个使用技巧！

- BestBlogs URL: https://www.bestblogs.dev/article/dd8025cf
- Extraction: DOM text from BestBlogs page via OpenCLI browser bridge
- Extracted chars: 2336
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzIyNjM2MzQyNg==&mid=2247717240&idx=1&sn=dfd0b8b79fb18e53d17d62ef149aa392

---

 Datawhale干货 

作者：Boris Cherny，Claude Code创始人

昨晚，Claude Code 创始人 Boris Cherny 在X上首次公开了他的个人Claude Code使用技巧。

以下是 Boris 的原文，Datawhale团队翻译：

我是 Boris，Claude Code 的创造者。不少人问起我是如何使用 Claude Code 的，那我就来展示一下我的设置吧。

我的配置可能会让你大吃一惊，因为它极其朴素。Claude Code 能够完美地开箱即用，所以我个人并没有做太多的定制化修改。

使用 Claude Code 并没有所谓的唯一正解：我们在构建它时就特意设计成这样，你可以按照自己喜欢的方式去使用、定制，甚至大肆改造它。事实上，Claude Code 团队里的每一位成员，用法也都截然不同。

那么，开始吧。

Claude Code 创始人的 13 个使用技巧

1. 我会在终端里并行运行 5 个 Claude 实例。我把标签页按 1-5 编号，并利用系统通知功能来提醒我什么时候某个 Claude 需要人工输入。

2. 我同时还会在网页端运行 5-10 个 Claude 会话，与本地的 Claude 并行协作。在终端写代码时，我经常用 & 将本地会话推送到网页端，或直接在 Chrome 里开启新会话，有时还会用 --teleport 命令在两者间反复横跳。每天早晨和工作中，我也会通过手机（Claude iOS 应用）开启几个会话，之后再回头查看进度。

3. 我所有工作都用带有“思考过程（thinking）”的 Opus 4.5。 这是我用过最好的编程模型。虽然它比 Sonnet 更大、更慢，但因为它更听劝（需要引导的地方少）且更擅长使用工具，从结果来看，它几乎总是比用小模型效率更高。

4. 我们团队共用一个 CLAUDE.md 文件。我们把它提交到 git 仓库中，全员每周都会多次更新。每当我们发现 Claude 做错了什么，就会记录进 CLAUDE.md，这样它下次就知道该怎么做了。其他团队也有各自维护的 CLAUDE.md，保持更新是每个团队的职责。

5. 在代码审查期间，我经常在同事的 PR 上 @.claude， 要求将某些内容作为 PR 的一部分添加到 CLAUDE.md 中。我们使用了 Claude Code 的 Github Action（/install-github-action）来实现这一点。

6. 大多数会话从“计划模式（Plan mode）”开始（双击 shift+tab）。如果目标是写一个 PR，我会先用计划模式，和 Claude 来回沟通直到我满意它的方案。接着，我切换到“自动接受修改模式”，Claude 通常就能一次性搞定。一份好的计划至关重要！

7. 对于每天都要重复多次的“内循环”工作流，我都会使用斜杠命令（slash commands）。这省去了重复输入 Prompt 的麻烦，也让 Claude 自己能调用这些工作流。这些命令都提交在 git 里的 .claude/commands/ 目录下。

例如：我和 Claude 每天会用几十次 /commit-push-pr 命令。它通过内联 bash 预先计算 git 状态等信息，让运行飞快，避免了与模型之间不必要的来回确认。

8. 我经常使用几个“子智能体（subagents）”：code-simplifier 用于在完成后简化代码；verify-app 包含端到端测试 Claude Code 的详细指令。和斜杠命令类似，我认为子智能体是将大多数 PR 中最常见的流程自动化。

9. 我们使用 PostToolUse 钩子来格式化 Claude 生成的代码。虽然 Claude 本身生成的代码格式就很不错，但这个钩子能搞定最后 10% 的细节，避免之后在 CI（持续集成）中报错。

10. 我不使用 --dangerously-skip-permissions。相反，我用 /permissions 预先批准那些在我的环境中已知的安全 bash 命令。这些配置大多保存在 .claude/settings.json 中并全队共享。

11. Claude Code 会帮我操作所有工具。它经常通过 MCP 服务器在 Slack 上搜索或发帖，使用 bq 命令行运行 BigQuery 查询来回答分析性问题，或是从 Sentry 抓取错误日志。Slack 的 MCP 配置定义在 .mcp.json 中并全队共享。

12. 对于超长时间运行的任务，我有三种方案：

(a) 提示 Claude 在完成后用后台智能体验证工作；

(b) 使用智能体的 Stop 钩子更确定地执行验证；

(c) 使用 ralph-wiggum 插件。 我还会配合使用 --permission-mode=dontAsk 或在沙箱里开启危险跳过模式，这样 Claude 就能在不被打断的情况下自主大展身手。

13. 最后一个秘诀（可能也是让 Claude Code 产出高质量结果最重要的事）：给 Claude 一个验证工作的方法。只要有反馈闭环，最终结果的质量会提升 2-3 倍。

Claude 会使用 Chrome 扩展程序测试我提交到网页端的每一个改动。它会打开浏览器，测试 UI，不断迭代直到代码运行正常且交互体验良好。

不同领域的验证方式不同：可能只是运行一个 bash 命令、一套测试集，或是在模拟器里测试。务必投入精力把这个验证环节做扎实。

希望这些对你们有帮助！
