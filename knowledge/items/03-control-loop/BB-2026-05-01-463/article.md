# NVIDIA: Leading the PC, Reforging the PC | Hard Philosophy

- BestBlogs URL: https://www.bestblogs.dev/article/2f366f79
- Original publisher URL: https://www.ifanr.com/1668041?utm_source=rss&utm_medium=rss&utm_campaign=
- Source: BestBlogs / 爱范儿
- Publish time: 2026-06-08 19:59:44
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 2; page/content captured from BestBlogs resource APIs
- Extracted chars: 5314

---

爱范儿关注「明日产品」，硬哲学栏目试图剥离技术和参数的外衣，探求产品设计中人性的本源。

  

  过去 48 小时，对于 Windows 电脑市场来说可谓地震不断——

  不是微软要发 Win 12 了，也不是苹果重新内置 BootCamp 了，而是英伟达要造消费级 CPU 了。

  

  图｜Microsoft

  更重要的是，老黄插手 CPU（SoC）领域，可不是来和英特尔、AMD 和苹果分蛋糕的……

  他是来掀桌子的。

  

  图｜YouTube @Nvidia

  在刚结束的微软 Build 与英伟达 GTC 显卡技术大会开幕式上，我们见到了来自英伟达的「终极 PC 解决方案」： RTX Spark N1X 处理器。

  老黄期望通过 RTX Spark 打造的电脑很简单：

  造出目前最全能、最智能、最面向未来十年甚至二十年 AI 潮流的终极 Windows 全能本。

  支撑英伟达这一设计的根本逻辑，是老黄在 GTC 开幕演讲上的一个大胆判断——

  
   面向人类用户设计计算产品的时代已经结束，未来我们应该面向智能体（intelligent agent）的需求设计计算硬件。

  

  

  图｜YouTube @Nvidia

  下一个 AI 时代属于智能体

  开场不久，介绍过 AI 技术如何塑造了当下的产业经济之后，老黄就拿出了他本次演讲的核心观点：

  
   相比单独使用某个 LLM（大语言模型），智能体将是下一个阶段我们使用算力的主要方式（a new kind of computing pattern）。

  

  这个核心观点如此重要，以至于老黄在演讲的前中后期反反复复提起这一页 keynote，将它重复播放了很多遍。

  整个演讲上公布的新硬件——比如正式投产的 Vera Rubin 计算平台、企业级 AI 工具包、底层模型等等，全都是围绕着这个核心理论而设计的。

  

  图｜YouTube @Nvidia

  根据老黄的介绍，智能体之所以能够成为下一阶段的核心算力使用方式，原因主要有 4 个——

  1：解放用户生产力

  过去几年里，单纯的生成式 AI（Generative AI）虽然能力得到了很大的提升，但并没有拓展出非常多的使用场景。

  即使它可以画图、做视频、直接制作各种文件，但本质交互方式依然是用户问一句、AI 答一句。

  智能体则不然——它的运作模式中包含「观察、推理、规划、使用工具」的闭环能力，这种模式让人类用户从工具操作者进化成了工具指挥者，可以被看作是一种形式的生产力解放。

  2：减少隐性资源消耗

  除了自身的运行模式之外，智能体还会彻底改变过去半个多世纪中，人类与计算机的核心人机交互模式。

  换言之，智能体将曾经需要手动打开程序、点击工具和操作的流程后置了一步，让人的工作从「动手」变成了「动口」，用解释意图（intents）取代具体的操作。

  这种变化的意义，在于它结束了「人学习和适应软件」的时代。而一个「软件学习和适应人」的阶段，将会节省大量人类学习和练习使用软件所需的时间资源。

  3：无视物理数量限制

  最「大力出奇迹」的优点是，智能体不会像人类一样，受到各种原因导致的数量限制。

  在演讲中，老黄列举了几个例子：AI 编码智能体的出现，让 GitHub 上的代码提交量在 2026 年初同比近乎翻了三倍。

  英伟达内部也计划通过部署「数十万个 Cadance 超级智能体」，将芯片设计验证的耗时从数周缩短到数小时。

  换言之：只要算力资源允许，智能体就可以将单个人类的能力「超级加倍」，让生产力获得指数级放大。

  4：比 LLM 更万能

  相比传统 LLM，智能体还拥有一个非常具体的优势——普适性。

  智能体的运作模式（模型 + 外壳 + 工具 + 运行环境）在所有应用场景中都是通配的，这种强大的通用性让它可以无孔不入。

  比如大规模的云端 SaaS 服务、个人电脑部署、自动驾驶和人形机器人底层系统等等。

  也就是说，智能体是 LLM 的一个「万能接口」，它自己就是完整的工具组件、可以直接嵌入具体的生产环节里，不需要人类在中间辛苦地做「回答搬运工」。

  

  图｜YouTube @Nvidia

  基于以上四点论据，老黄指出了一种「面向智能体」的算力设计思路：

  过去四十多年，所有计算硬件都是围绕人类的需求设计的，但智能体的世界以纳秒计算、对于各种资源（比如内存和电力）的需求模式和人类截然不同。

  在这样的大背景下，老黄宣布了新一代全栈 POD 超级计算平台「Vera Rubin」的正式投产：

  

  图｜YouTube @Nvidia

  相比年初在 CES 上首次介绍 Vera Rubin 平台，老黄在演讲中再次强调了这一代架构「专门为智能体设计」的属性。

  尤其最新的 Vera CPU，就直接打上了「CPU for Agents」的标签——这颗 88 核心 176 线程的处理器的主要工作，用老黄的话说，是一位「指挥家」。

  换言之，Vera CPU 主要控制智能体的调度、工具调用、内存和上下文管理，负责将 Rubin GPU 的巨量算力以最高效率、最低空置、最快速度的方式调度起来：

  

  图｜YouTube @Nvidia

  在此基础上，其他机柜组件—— BlueField-4 DPU、NVL72 交换机、ConnectX-9 SuperNIC 网卡、Spectrum-6 以太网交换机等等，才能和 Vera Rubin 共同构成这套「面向智能体」的算力解决方案。

  

  图｜YouTube @Nvidia

  但就像前面说的，老黄除了公布 Vera Rubin 投产之外，同时也将这个「AI 的未来属于智能体」的观点投向了一个更偏向消费电子的领域—— PC。

  给智能体设计的电脑

  之前提到，老黄今年 GTC 开幕演讲的主旨其实就一句话：

  
   给人类用户设计硬件的时代结束了，我们下一步要面向智能体设计硬件。

  

  但智能体的使用者不止 Oracle、OpenAI、Anthropic、AWS 这些企业巨头，个人 AI 用户的数量同样不可忽视。

  为了占住极为分散但规模庞大的 C 端市场，老黄在今年的演讲中公布了英伟达首款面向个人消费市场的 CPU 产品—— RTX Spark 超级芯片。

  

  图｜YouTube @Nvidia

  老黄对 RTX Spark 首型号 N1X 的介绍相当动情：「它集合了我们 33 年来的全部技术经验，因为它支持所有英伟达已有的技术栈」。

  与苹果的 Apple Silicon 思路类似，RTX Spark N1X 是一块集成 CPU、GPU 和统一内存的 ARM 架构 SoC，采用台积电 3nm 工艺制造，CPU 与联发科共同设计。

  

  图｜Nvidia

  尽管用着上一代 Grace Blackwell 平台，而非最新的 Vera Rubin，RTX Spark N1X 依然可以实现最高 1 PFLOPS（一千万亿次浮点）的 AI 算力。

  根据英伟达工程师的介绍，N1X 的整体性能与 RTX 5070 笔记本接近，相比早期泄露的「与 M3 Max 跑分近似」又有了一些提升：

  

  图｜YouTube @Nvidia

  在产品形态方面，RTX Spark 最主要的平台将会是 14-16 寸的笔记本，合作方也是那几个熟悉的巨头——联想、微软、惠普、华硕等等。

  其中当属英伟达与微软的合作最为密切，毕竟 RTX Spark 是要运行 Windows on ARM 的。

  而老黄的 ARM 处理器能否追上苹果，微软是其中不可或缺的因素。

  相应的，微软也在演讲后更新了搭载 RTX Spark 的 Surface Laptop Ultra 预告片：

  

  图｜YouTube @Microsoft Surface

  而相比高通的 ARM 架构笔记本，RTX Spark 还有一个得天独厚的优势：它支持所有英伟达已经有的技术，从光线追踪到 DLSS，再到 Cuda 加速和 TensorRT。

  换言之，RTX Spark 笔记本不仅有 Win on ARM 上相对优秀的游戏体验，更是能够在本地 AI 工具加速之类的严肃场合提供「货真价实的生产力」。

  

  图｜YouTube @Nvidia

  更重要的是——按照老黄的说法—— RTX Spark 所驱动的笔记本、小型主机和台式机都是「为智能体操作而设计」的。

  除了 Windows 本身和软件商之外，甚至连 Adobe 都宣布将会为 RTX Spark 彻底重构 Premiere 和 Photoshop：

  

  图｜YouTube @Nvidia

  就拿 Premiere 来说，Adobe 将会在 RTX Spark 电脑上带来一套全新的、以指挥智能体为主的交互模式，以及更多的 MCP 支持。

  再大胆一点设想，所有剪辑师都熟悉的「时间轴式 UI」很有可能在智能体时代被一个多模态指令框所替代——

  听起来很酷，也很可怕。

  

  在 RTX Spark 笔电上运行 Premiere Pro｜Tom’s Guide

  换言之，AI 不仅重塑了硬件的设计方式，也终于开始重塑一些已成定局十多年的软件 UI 交互规范了。

  RTX Spark 的应用场景也不止笔电，在老黄的 GTC 开幕演讲与当天稍晚些的微软开发者 Build 大会上，我们看到了很多以此为基础的小型主机平台。

  就比如这个长得神似 Xbox 的微软 RTX Spark Dev Box：

  

  图｜Microsoft

  AI 需求塑造物理世界

  纵观老黄的整个 GTC 演讲，以及同期召开的 COMPUTEX 和微软 Build 大会，我们可以明显地感受到：

  AI 从「生成式」向「智能体」的转变，将会重塑人们使用计算机的主要方式，并且这种重塑也反过来影响了计算硬件上下游的设计和形态。

  换言之，英伟达不仅定义了下一个 AI 时代的核心问题：「什么是生产力 – 是智能体」，更是为自己的观点拿出了一套相当具有说服力的配套产品。

  

  图｜YouTube @Nvidia

  而 RTX Spark 的目标，是让新时代的全能本既要本地跑模型，又要兼顾生产力和娱乐——

  毕竟支持 RTX 和 Cuda 对于 Windows on ARM 一直是个老大难问题，直到英伟达亲自下场。

  只不过在为下一个 AI 时代催生新硬件感到兴奋的同时，我们也需要理性地看待 RTX Spark N1X 处理器：因为它并不是一个非常新鲜的东西。

  

  还记得去年的 DGX Spark 吗？里面的「GB10 超级芯片」基本上就是 N1X 的先行版本。

  从芯片刻字上看，老黄在 COMPUTEX 上展示的 N1X 生产周期甚至是 2024 年，早期泄露跑分接近 2023 年的 M3 Max 也就不意外了。

  

  图｜YouTube @High Yield

  虽然所有消费级产品都要等到今年秋天，但看到 RTX Spark N1X 的这些零星信息，也很难不让人微微担心——

  
   一颗 CPU 两年前、GPU 一年前且不满血的 SoC，真能为未来 10 年 20 年的智能体需求准备好吗？

  

  尽管 N1X 既没用上最新的 Vera Rubin 架构，也不如今年的骁龙 X2 Elite Extreme 甚至去年的 AMD Strix HALO，但它标志着一个开端：

  一个芯片优先考虑智能体需求、并顺势开始影响操作系统、软件程序，直至硬件商品形态的时代的开端。

  至于究竟谁能代表 AI 时代的操作系统，微软选择和英伟达联手，「再给 Win on ARM 一个机会」，明显是意识到了自己被 macOS 和 Linux 夹攻的困境。

  

  图｜Microsoft

  然而成也 Win on ARM，败也 Win on ARM —— RTX Spark 主动带来全套的英伟达技术适配，并不能解决 Win on ARM 在其他体验上的长期瘸腿。

  毕竟一个足够好的面向 AI 的操作系统（比如 macOS），即使它自己不倾向于开放，也会有用户通过逆向工程的方式帮它开放。

  而在这一层上，RTX Spark + Win on ARM 所以立足的基点，就显得不是那么稳固了。
