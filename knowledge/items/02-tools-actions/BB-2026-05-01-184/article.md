# Kimi WebBridge: Let AI Operate Your Browser

- BestBlogs URL: https://www.bestblogs.dev/en/article/31884d93
- Extraction: BestBlogs API proxy content endpoint + rendered rich text body
- Extracted chars: 2258
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=Mzk0NDU1MDkyNg==&mid=2247488449&idx=1&sn=8f670f00b26eedc5de9ec6a66fc4aefa

---

今天，我们推出 Kimi WebBridge。

一个面向 Kimi Code、Claude Code、Cursor、Codex、Hermes Agent、OpenClaw 等 AI Agent 的浏览器插件，让 AI 真正像你一样操作浏览器。

Kimi WebBridge 会带着你的登录状态、你的 Cookie、你的账号，去点击、滑动、输入，填写表单、提取信息、跨站点整合内容。换句话说，在目标网站看来，Kimi WebBridge 等同于你在操作。

了解更多 kimi.com/zh-cn/features/webbridge

Kimi WebBridge 运行时会标记出正在操作的浏览器标签页，如上图的 gmail 和 mailchimp 页面。但它不会占用我们的鼠标键盘，我们依然可以使用电脑和浏览器。

它能帮你做什么？

大部分基于网页的重复性繁琐操作或定时任务，现在都可以通过 Kimi WebBridge 自动化完成。

从 Kimi WebBridge 内部测试到最终上线，Kimi 很多内部员工用它做了很多有意思的事情，下面分享两个搭配 Kimi Code 使用的案例，希望给大家带来启发。

示例一：自动化信息整理

自动采集多个笔记类APP的应用商店宣传素材，让 AI 分析设计风格差异并写入在线文档。

示例二：复杂操作自动化

一键接管量化研究模拟平台，自动抓取金融数据、多策略迭代回测、撰写量化报告。

现在开始使用

如果你的电脑上已经安装了支持 Skill 的本地 AI Agent，比如 Kimi Code、Claude Code、Cursor、Codex、OpenClaw、Hermes Agent 等，那么只需两步就可以开始使用 Kimi WebBridge。

第一步

在 Chrome 或 Edge 浏览器的应用商店搜索安装「Kimi WebBridge」扩展插件。

如遇网络连接问题，也可以参考这里的教程手动下载安装扩展插件。

第二步

把下面的命令发送给你的本地 AI Agent，让它帮你安装 Kimi WebBridge 的本地守护程序和技能（Skill）。

安装 KimiWebBridge：curl -fsSL https://kimi-web-img.moonshot.cn/webbridge/install.sh | bash。装完后即可用我的浏览器做任何网页操作。

接下来，可能需要重启一下你的 Kimi Code 等本地 AI Agent 来加载 Kimi WebBridge 技能。

重启后，输入这个命令来测试一下，如果打开了 kimi.com 标签页并且出现 agent:kimi 的提示，就代表安装成功了。

使用 kimi-webbridge 帮我打开 kimi.com

如果你通过 Kimi 电脑客户端在本地电脑上部署了 Kimi Claw Desktop，就不需要第二步了，Kimi Claw Desktop 系统已内置 Kimi WebBridge，直接发送指令开始使用即可。

云端部署的 Kimi Claw 目前暂不支持，我们后续会为其推出专门的浏览器实现类似能力。

探索进阶能力

AI Agent 通过 Kimi WebBridge 操作浏览器时，每次都需要探索、迭代和调教一段时间，才能学到任务应该怎么高效完成。

如果你的任务非常具体，流程已经固定。比如在已登录状态下，让 Kimi WebBridge 帮你打开 chatgpt.com 使用自己的会员额度生成一张图片，并放到下载目录中。那么，就可以创建一个不消耗大模型 Token 的专用 CLI 工具，将其安装到本地电脑系统中，之后直接调用这个 CLI 工具来执行重复任务。

你可以在开源社区中找到更多某网站专用 CLI 工具来安装使用，比如 Twitter-cli、Xiahongshu-cli、boss-cli……等等。也可以自己创建某个网站某项功能专用的 CLI 工具，推荐为你的 AI Agent 安装这个的 Skill(https://github.com/better-world-ai/x-cli)，然后让 AI Agent 帮你创建专属 CLI 工具。

快速开始

Kimi WebBridge：kimi.com/zh-cn/features/webbridge

Kimi Code：kimi.com/code

🎁 期待在评论区分享更多你的探索！我们会挑选 3 位最有启发的分享，分别送上 199 元 Kimi 月度会员。

最近更新

Kimi K2.6 发布并开源，全面精进代码和 Agent 集群能力

Kimi K2.6「Agent 集群」现已支持 300 个成员并行协作

和 Kimi 一起投身 AGI，穿越成长周期

服务全球1/5网站的Cloudflare选择Kimi K2.5，降低77%成本

Kimi 杨植麟「2026 中关村论坛」演讲全文（附视频）

Kimi API：用90%缓存命中率，把价格打到25%

你可以来 Kimi 使用 OpenClaw 了

技术报告：Kimi K2.5 如何实现文本和视觉能力互相增强？

不只PPT，Kimi K2.5 Agent可以帮你做Excel、Word和PDF了

Kimi 发布并开源 K2.5 模型，带来全新视觉理解、代码和 Agent 集群能力
