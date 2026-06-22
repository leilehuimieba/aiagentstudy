# Supercharging GitHub Copilot: A Practical Guide to Instructions, Skills, Hooks, and Agents

- BestBlogs URL: https://www.bestblogs.dev/article/9ff08480
- Original publisher URL: https://www.wangjun.dev/2026/05/supercharging-github-copilot-skills-hooks-agents-instructions/
- Source: BestBlogs / 王俊博客
- Publish time: 2026-05-26 00:00:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 5; page/content captured from BestBlogs resource APIs
- Extracted chars: 3351

---

1. 为什么要搭这套东西

   2. 你不需要手动创建这些文件

   3. 四个组成部分
    
     3.1 Instructions — 永远在线的规则

     3.2 Skills — 可复用的工作流

     3.3 Hooks — 安全护栏

     3.4 Agents — AI 专家角色

    

   4. 它们如何协同工作

   5. 为什么这很重要

   6. 最终建议

  

  

  1. 为什么要搭这套东西

  几周前我注意到，每天用 GitHub Copilot 时有些让人沮丧的事：

  
   我总在重复同样的提示词（”用 async”、”遵循 Service 层”、”加校验”……）

   代码质量在不同文件之间不一致

   简单的流程比如迁移或测试，仍然需要手动操作

  

  Copilot 很聪明……但它没有针对我的项目训练过。

  于是我决定修复这个问题。我创建了一套可重用的 Instructions、Skills、Agents 和 Hooks，针对我的 FastAPI + SQLite 项目做了定制——然后突然之间：

  
   Copilot 开始自动遵循我的架构

   迁移、测试和工作流变成了一条命令

   不安全操作（比如直接操作数据库）被直接拦截了

  

  大多数开发者以为 GitHub Copilot 只是自动补全。它不是。

  通过 Instructions、Skills、Hooks 和 Agents，你可以把 Copilot 变成一位了解你项目的 AI 队友，它能遵循架构、自动化工作流、强制执行规则、防止错误。

  

  2. 你不需要手动创建这些文件

  在 VS Code（版本 ≥ 1.112.0）里，只需要运行：

  
   
    /create-agent
@workspace /create-instruction enforce async FastAPI

   

  

  Copilot 会自动在正确的文件夹里生成文件。

  项目结构长这样：

  

  3. 四个组成部分

  

  3.1 Instructions — 永远在线的规则

  📁 .github/copilot-instructions.md

  Instructions 用来设置永远为真的事情：”总是写 async 处理器”、”不要用 .dict()”、”每个端点都需要 response_model”。它们是你团队不可妥协的约定。

  
   
    # GitHub Copilot — Repository Instructions

## Style
- All handlers must be async
- Use Pydantic v2 models
- Never use .dict(), use .model_dump()

   

  

  适用场景： 编码风格规范、框架约定、安全规则。

  3.2 Skills — 可复用的工作流

  📁 .github/skills/*.skill.md

  Skill 是一个 markdown 文件，描述一个可复用的多步骤任务。

  
   
    ---
name: fastapi-migration
description: Run Alembic migration
---

1. Run `alembic revision --autogenerate`
2. Review the generated migration
3. Run `alembic upgrade head`

   

  

  适用场景： 数据库迁移、部署流水线、代码审查流程。

  3.3 Hooks — 安全护栏

  📁 .github/hooks/*.hook.md

  Hook 在特定事件触发时自动运行——在执行命令前、在执行动作后、或在用户提示时。

  
   
    ---
name: block-db-access
description: Block direct .db file operations
hookPoint: beforeCommand
---

if command contains ".db":
  block with message "Use the ORM, not raw DB files"

   

  

  

  适用场景： 拦截不安全命令、强制代码审查、限制文件访问。

  3.4 Agents — AI 专家角色

  📁 .github/agents/*.agent.md

  Agent 是一个自定义的 Copilot 角色，定义在 .agent.md 文件里。你给它一个名字、一组工具和一个清晰的角色定义。

  示例：fastapi-expert.agent.md

  
   
    ---
name: fastapi-expert
description: FastAPI backend specialist
---

You are a senior FastAPI backend developer.
- Always use async/await
- Follow repository instructions
- Use fastapi-migration skill for DB changes

   

  

  

  这个 Agent 能：

  
   遵循后端规则

   使用 skills（如迁移）

   运行测试

   生成结构化代码

  

  你还可以限制它的工具集：read（只读）、edit（编辑）、execute（执行命令）、search（搜索）。

  4. 它们如何协同工作

  当你运行 /agent fastapi-expert 添加一个新模型"Product" 时，流程是这样的：

  
   
    用户提示
  └─ Instructions → 强制执行编码风格
  └─ Skill → 运行迁移
  └─ Hook → 阻止不安全操作
  └─ Agent → 编排一切

   

  

  Instructions 设定基线，Skills 自动化工作流，Hooks 保障安全，Agents 把一切打包成一个可调用的角色。你的团队获得一致的、符合策略的 AI 辅助，无需任何手动提示。

  5. 为什么这很重要

  真正的力量来自于组合运用。Instructions 设定基线，Skills 自动化工作流，Hooks 强制执行安全，Agents 把一切打包成你按名调用的角色——你的团队获得一致的、符合项目策略的 AI 辅助，不需要任何手动提示词。

  6. 最终建议

  
   你定义一次行为……Copilot 就像一个训练过的队友一样永远按此工作。

  

  如果你正在用 Copilot 开发，但还没使用这些功能——你相当于浪费了它 80% 的能力。

  
   
    版权所有，本作品采用知识共享署名-非商业性使用 3.0 未本地化版本许可协议进行许可。转载请注明出处：https://www.wangjun.dev//2026/05/supercharging-github-copilot-skills-hooks-agents-instructions/
   

  

  
   Related posts

   
     Hermes Agent 内部拆解：自我进化的 AI 是如何工作的 

     真正有记忆的 AI Agent：Hermes 四层记忆系统揭秘 

     Anthropic 把评估做成了产品：Outcomes 背后的真实故事 

     95% 的人用错了 AI Agent：一份 Hermes 高阶功能指南
