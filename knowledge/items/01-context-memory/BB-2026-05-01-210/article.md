# [Issue 3697] Claude Code Auto-Memory Feature Explained: Say Goodbye to Repeated Instructions, Let AI Remember Your Project

- BestBlogs URL: https://www.bestblogs.dev/en/article/4d48937e
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 6050
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MjM5MTA1MjAxMQ==&mid=2651279074&idx=1&sn=b2e523cedefdde4cc76c44101be80210

---

前言

每次开启新会话都要重复交代项目背景？Anthropic 为 Claude Code 推出的自动记忆功能彻底解决了这一痛点。本文详解 MEMORY.md 的工作原理、与 CLAUDE.md 的区别、记忆层级机制，并通过实战演示展示如何配置与控制这一功能。

本文由 5 分钟新知精选，今日前端早读课文章由 @Youssef Hosni 分享，@飘飘编译。

译文从这开始～～

你再也不用担心在 Claude Code 中丢失会话上下文了。全新的自动记忆功能解决了工作流中最令人头疼的问题之一。如果你之前用过 Claude Code，一定对这个痛点深有体会 —— 关掉会话，第二天回来，Claude 就像失忆了一样从零开始。这往往意味着你得重复交代同样的项目细节、偏好设置和决策过程，才能回到之前的进度。

【图书】Claude Code 实战：Harness工程之道

Anthropic 现在为 Claude Code 引入了自动记忆功能，目标很简单：让会话之间的衔接更加顺畅。Claude 现在能够在与你协作的过程中自行构建和维护记忆。随着工作的推进，它会默默记录项目相关的有用上下文，比如构建命令、编码偏好、架构决策，甚至你们一起攻克的疑难 bug。

当你开启新会话时，这些上下文已经就位，你可以从上次中断的地方继续，而不必从头来过。这个功能尤其出色的一点在于，你完全不需要手动管理它，Claude 会自主完成这一切。

大多数 Claude Code 用户对 CLAUDE.md 已经不陌生了 —— 这是用来给 Claude 下达指令的文件。自动记忆在此基础上新增了一层，引入了一个名为 MEMORY.md 的文件。与 CLAUDE.md 不同的是，这个文件由 Claude 自行编写和更新，相当于一个跨会话的持续性草稿本。

我在一个真实项目中测试了 Claude Code 的新自动记忆功能，想深入了解 Claude 会选择记住哪些内容、这些信息存储在哪里，以及在进入全新会话时它的记忆有多可靠。在这篇文章中，我将详细解析自动记忆的工作原理，厘清 CLAUDE.md 和 MEMORY.md 之间的区别，分享我的测试结果，并展示如何在需要时对这项功能进行控制。

【第3692期】告别基础设施焦虑：用Claude托管代理轻松构建代码审查工具

一、Claude Code 的自动记忆是如何工作的？

自动记忆功能在你更新 Claude Code 后即默认开启，无需额外安装或配置，开箱即用。在你工作的过程中，Claude 会默默观察当前的操作并做好笔记，自行判断哪些信息值得为后续会话保留。

以下是 Claude 会存储的信息类型：

-

项目模式，例如构建命令、测试工作流，以及代码库的组织结构

-

调试心得，包括疑难问题的解决方案和特定错误的根本原因

-

架构笔记，如关键文件、模块间的依赖关系和核心抽象层

-

个人偏好，比如沟通风格、工作流习惯和工具选择

关键在于，这一切都不依赖手动输入。Claude 自行判断哪些内容重要，并自动记录下来。

自动记忆存储在哪里？

每个项目都有独立的记忆目录，存储路径为：~/.claude/projects/<project>/memory/

其中 <project> 路径基于 Git 仓库的根目录，这意味着同一仓库下的所有子目录共享同一个记忆位置。

【第1864期】手撕Git，告别盲目记忆

如果你使用的是 Git worktree，每个 worktree 会拥有各自独立的记忆目录。若不在 Git 仓库中，Claude 则会回退到当前工作目录。

该文件夹内部的结构通常如下：

~/.claude/projects/<project>/memory/
├── MEMORY.md # 主索引文件，每次会话开始时加载
├── debugging.md # 调试历史和反复出现的问题的笔记
└── ... # Claude 按需创建的其他主题文件

MEMORY.md 是主入口文件，相当于 Claude 所有存储内容的索引，也是每次会话开始时唯一自动加载的记忆文件。

理解 200 行限制

有一个重要细节需要注意：新会话启动时，Claude 只会将 MEMORY.md 的前 200 行加载到系统提示中。

一旦 MEMORY.md 变得过长，Claude 会将更详细的笔记拆分到独立的主题文件中，例如 debugging.md 或 api-conventions.md，同时保持主文件简洁实用。这些额外的主题文件在启动时不会被加载，Claude 只会在会话过程中需要特定上下文时才去读取。

因此，整个工作流程如下：

-

新会话启动，MEMORY.md 的前 200 行被加载

-

Claude 需要某段调试历史，便按需读取 debugging.md

-

Claude 学到新内容后，更新 MEMORY.md 或某个主题文件

我在测试中注意到一点：这个过程并非在后台静默执行 —— 这与我最初的预期不同。你实际上可以在会话中实时看到 Claude 读取和写入记忆目录的操作。

CLAUDE.md 和 MEMORY.md 有什么区别？

很多开发者可能会问同样的问题：既然已经有了 CLAUDE.md，为什么还需要 MEMORY.md？让我们来厘清这一点。

CLAUDE.md 一直是 Claude Code 的组成部分，你在其中编写希望 Claude 遵循的指令、规则和偏好。

MEMORY.md 的运作方式则截然不同。

你不需要自己编写 MEMORY.md，Claude 会自动创建并更新它。

最简单的理解方式是：CLAUDE.md 是你下达的指令，而 MEMORY.md 是 Claude 自己的备忘录。在 MEMORY.md 中，Claude 会记录与你协作过程中积累的有用上下文，例如：

-

你的偏好习惯

-

反复出现的项目模式

-

哪些命令能正常运行

-

哪些命令会报错

-

过往会话中的有价值笔记

重要的是，这些内容完全由 Claude 随时间自主积累，无需你手动干预。所以两者的区别很简单：

-

CLAUDE.md：你告诉 Claude 该怎么做的地方

-

MEMORY.md：Claude 为自己做笔记的地方

这两个文件协同配合，为 Claude 在会话开始时提供更完善的上下文。

一个告诉 Claude 你希望它如何行事，另一个帮助它记住关于你项目已经学到的一切。

【第3524期】无需 CRDT 或 OT 的协同文本编辑

理解 Claude Code 的记忆层级

Claude Code 并非仅依赖 CLAUDE.md 和 MEMORY.md，它实际上通过一套分层记忆系统运作。每一层扮演不同的角色，具体取决于指令的适用对象和作用范围。

核心逻辑很简单：越具体的指令，优先级越高。

这意味着项目级的 CLAUDE.md 优先级高于全局的用户级记忆。自动记忆同样位于项目层级，也就是说它的作用范围限定在你个人以及你正在参与的特定项目。

还有一个实用细节：CLAUDE.local.md。这个文件会被自动添加到 .gitignore 中，因此非常适合存放私有的本地配置，例如沙箱 URL、本地测试笔记，或者其他不需要与团队共享的内容。

会话启动时 Claude 加载了什么？

当你开启一个新的 Claude Code 会话时，Claude 会从多个层级加载上下文。

通常包括：

-

你所在组织的策略（如果存在的话）

-

项目级的 CLAUDE.md，包含团队共享指令

-

你个人的 ~/.claude/CLAUDE.md 偏好设置

-

MEMORY.md 的前 200 行，即 Claude 保存的笔记内容

因此，在你输入第一条提示之前，Claude 已经对你的项目规范、个人偏好，以及从以往会话中积累的上下文有了初步的认知。

【第3693期】从提示词到工程框架：AI工程的成长之路

二、Claude Code 自动记忆实战演练

让我们从零开始创建一个项目，亲身体验自动记忆的实际运作方式。

1. 更新 Claude Code

首先，为了确保自动记忆功能可用，你需要确认已安装最新版本的 Claude Code。

claude update

然后检查当前版本，版本号应在 2.1.76 之后：

claude --version

2. 搭建测试项目

接下来，创建一个测试项目并在该文件夹中初始化 Git：

mkdir test-claude-memory && cd test-claude-memory
git init

运行 git init 这一步至关重要，因为 Claude Code 依赖 Git 仓库根目录来确定记忆文件的存储位置。如果你的项目不是 Git 仓库，项目级的记忆配置将无法正常工作。

现在，我们可以在这个测试项目中启动 Claude Code 了：

claude

3. 初探 Claude 记忆功能

自动记忆不会仅仅因为你打开了一个会话就创建文件。Claude 需要先与你协作完成一些工作，才会开始做笔记。我让 Claude Code 构建了一个基于 LangChain 的 RAG 管道：

Build a simple rag pipeline with langchain

此时，如果你运行 /memory 命令，可以看到自动记忆已开启，并且有三个记忆选项。

选项一：用户记忆

此选项会在系统编辑器中直接打开全局文件 ~/.claude/CLAUDE.md。

这是你的个人记忆文件，包含跨所有项目通用的指令和偏好设置。比如你偏好的编码风格、常用工具，或者你希望 Claude 在任何项目中都遵循的习惯。

这个文件由你自己管理。

选项二：项目记忆

此选项会打开当前项目中的 CLAUDE.md 文件。

这是共享的项目文件，通常存放团队级别的上下文信息，例如编码规范、架构决策和团队共同遵循的工作流。如果项目在版本控制之下，这个文件可以提交到仓库中，让整个团队都能从中受益。

这同样是一个由你编写和维护的文件。Claude 会读取它，但不会对其进行修改。

选项三：打开自动记忆文件夹

这部分才是由 Claude 管理的。

选择此选项会打开 Claude 存储自身笔记的记忆目录，其中包括 MEMORY.md 以及它在多次会话中创建的各类主题文件。这就是我们在本文中一直讨论的那个文件夹。

在 Windows 上，该文件夹可能无法自动打开。如果遇到这种情况，可以在终端中手动导航：

ls $env:USERPROFILE\.claude\projects\<your-project-path>\memory\

4. 自动记忆开关

当你输入 /memory 命令时，会看到：

Auto-memory: on

你可以直接在这里切换开关，无需修改任何配置文件。只需停留在 Auto-memory: on 这一行按下回车，即可切换为 Auto-memory: off。

如果你即将进行一些不希望 Claude 记住的探索性工作，或者只是临时跑一次性任务，这是暂停当前项目记忆功能最快捷的方式。

建议在每个新项目开始时运行一下 /memory 命令，确认开关已打开，同时熟悉文件的存储位置，以免记忆内容积累后才手忙脚乱。

5. 冷启动会话测试

现在让我们完全关闭 Claude Code，在同一个项目中重新开启一个新会话，不提供任何上下文，直接发送以下消息，看看 Claude 的记忆能否在冷启动中存活：

What do you know about this project?

Claude 读取了新会话的记忆内容，给出了一份关于我项目的详细概述：

所有这些信息都是从上一次会话中的 MEMORY.md 回忆出来的。这正是 Claude Code 自动记忆按照设计预期运行的效果。

三、控制 Claude 自动记忆

自动记忆默认处于开启状态，在大多数情况下，这个默认设置是合理的。

但总有一些场景需要你将其关闭。Claude Code 提供了多种方式来实现这一点，具体取决于你需要的控制粒度。

针对单个项目关闭自动记忆

如果你只想为某一个项目禁用自动记忆，可以在该项目的配置文件中添加以下设置：

// .claude/settings.json
{
"autoMemoryEnabled": false
}

这只会禁用该项目的自动记忆，其他项目不受影响。

全局关闭自动记忆

如果你想在所有项目中禁用自动记忆，将同样的设置添加到用户级配置文件中即可：

// ~/.claude/settings.json
{
"autoMemoryEnabled": false
}

这会在全局范围内生效，Claude 将在所有项目中停止使用自动记忆。

在 CI 环境中强制关闭

如果你在 CI 流水线或其他托管环境中运行 Claude Code，最稳妥的做法是使用环境变量：

export CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 # 强制关闭
export CLAUDE_CODE_DISABLE_AUTO_MEMORY=0 # 强制开启

这个环境变量会覆盖 /memory 开关以及 settings.json 中的所有相关配置。

因此，它是确保自动记忆在自动化环境中绝不运行的最可靠手段 —— 你肯定不希望 Claude 把 CI 会话中的内容记录下来。

编辑记忆文件

记忆文件本质上就是 Markdown 文件，你随时可以打开并编辑它们。

最便捷的方式是在 Claude Code 中使用 /memory 命令。它会打开记忆文件选择器，让你直接跳转到系统编辑器中的任意记忆文件。

当你需要删除过时的笔记、清理不再相关的条目，或者随着项目演进重新整理记忆内容时，这个功能非常实用。

你也可以直接从终端打开这些文件：

open ~/.claude/projects/<your-project>/memory/MEMORY.md

关于本文
译者：@飘飘
作者：@Youssef Hosni
原文：https://levelup.gitconnected.com/claude-code-memory-md-everything-you-need-to-know-how-to-get-started-8ac99e161153
