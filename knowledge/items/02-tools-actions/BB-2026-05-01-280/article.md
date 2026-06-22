# VAPD AgentKit: A Composable Frontend General-Purpose Library for Agents

- BestBlogs URL: https://www.bestblogs.dev/article/811c9a29
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzI4NjY4MTU5Nw==&mid=2247506363&idx=1&sn=9e119a46ba72217d90045a16aa27967c
- Source: BestBlogs / vivo互联网技术
- Publish time: 2026-05-20 20:00:00
- Capture route: article discovered from logged-in Edge/OpenCLI latest page 4 feed; page/content captured from BestBlogs resource APIs
- Extracted chars: 8049

---

围绕三大业务场景（笔记、知识库、项目管理）统一了一套可组合的 AI Agent 能力。

  
   
    
     作者：vivo 互联网项目团队- Ding Junjie

    

   

   
    
     
      
       
        
         目录

        

       

      

     

     
      
       01. 背景与目标

       02. 设计原则

       03. 架构总览

       04. 事件流与消息模型：把一切都还原成消息

       05. Agent 回合循环（loop）与工具调用（tools）

       06. UI 交互与建议（Suggestions）

       07. 最小上手：3 步把 Chat 接入到任一页面

       08. 与业务的契合

       09. 面向知识库问答与集成流程智能的演进设想

       10. 下一步需完善

       11. 结  语

      

     

     
      
       
        
         我们围绕三大业务场景（笔记、知识库、项目管理）统一了一套可组合的 AI Agent 能力。

         本文聚焦一期「Chat 模式」落地：强调 Runtime Adapter 的“协议无关、面向任意后端流”特性——只要后端能够以流式输出事件，前端即可通过统一的 Adapter 转为标准消息模型进行渲染与编排。我们以“统一消息模型 + Runtime Adapter + 前端编排”的方式，将工具调用、Agent 回合循环、事件流与 UI 交互组合在一起，并为后续历史与检查点能力预留 threadId/runId。

        

       

      

     

    

   

   
    1分钟看图掌握核心观点👇

   

   
    
     
      
       
        
         
          
           
            
             

            

           

           
            
             

            

           

          

         

         
          
           
            左右滑动查看

           

          

         

        

       

      

     

     
      图 1 VS 图 2，您更倾向于哪张图来辅助理解全文呢？欢迎在评论区留言。

     

    

   

   
    
     
      01

     

    

   

   
    背景与目标

   

   
    
     
      

      
       
        业务诉求：笔记、知识库、项目管理三类场景都需要“对话式”AI 能力，并逐步演进到多轮、工具调用、上下文增强与可追溯。

       

       
        统一入口：不希望每条业务线重复造轮子；期待用同一套可组合 Hook 即插即用。

       

       
        一期范围：先完成 Chat 模式打底，但保留可扩展的“多消息一回合”“工具调用”“历史/检查点”能力。

       

      

      

     

    

   

   在产品体验上，我们遵循主流 Agent 设计范式（消息驱动、工具调用、上下文注入、可回放、可评测），并结合过往的实现风格，将复杂性交由“消息模型 + 运行时适配 + 前端编排”三段式来解耦。

   
    
     
      02

     

    

   

   
    设计原则

   

   

   
    
     消息即协议：把后端回传的事件统一解码为前端消息模型，UI 只消费消息，不关心来源细节。

    

   

   
    
     运行时可插拔：只要后端能以“流”的形式输出（SSE、GraphQL、WebSocket、Fetch ReadableStream 等均可），Adapter 都会转为相同的 AgentStreamEvent，前端逻辑零差异。

    

   

   
    
     前端可编排：用 Hook/Context 管理上下文、工具、重试/变体、回调，形成稳定的胶水层。

    

   

   
    
     渐进增强：一期只做 Chat，但保留 threadId/runId，为“历史/检查点/回放/评测”留出Agent能力口。

    

   

   

   
    
     
      03

     

    

   

   
    架构总览

   

   

   只列出 Chat 模式强相关的核心模块（更多细节见项目架构文档）：

   
    ① 统一消息模型

    
     
      覆盖 UserMessage、AssistantMessage、Thinking-Message、ActionExecution-

      Message、ResultMessage 等类型，含 status 与可选 parentMessageId，可扩展图片、状态消息。

     

    

    ② Runtime Adapter 接口

    
     
      generateResponse(params) / retry(params) 返回 ReadableStream<AgentStreamEvent>，sendFeedback 统一正/负反馈。

     

    

    
     
      可对接多种后端“流”：内置 VAPD 适配示例，也可扩展 GraphQL/WebSocket/自定义 Fetch 流；无论来源如何，都会标准化为 AgentStreamEvent。

     

    

    ③ 前端编排（Orchestration）

    
     
      AgentKit 作为 Provider 暴露上下文，统一注入 runtime、actions、上下文树、消息与加载状态、重载完成回调等。

     

     
      useAgentChat 组合 useChat，提供 append-

      Message、reloadMessages、stop-

      Generation、threadId、runId 等能力。

     

     
      useChat 串接 Runtime 流式事件，处理工具调用与 Agent 循环，并维护 AbortController。

     

    

    ④ Vue UI 组件

    
     
      Chat 容器封装输入/消息区/操作/建议项，借助 useCopilotChatLogic 与 Core 同步。

     

    

   

   
    
     
      04

     

    

   

   
    事件流与消息模型：把一切都还原成消息

   

   

   

   
    后端返回的是“事件”，前端消费的是“消息”。我们把差异收敛在 Adapter 层：

    
     
      增量累加：把分片 token 聚合为 Thinking-

      Message / AssistantMessage。

     

     
      工具事件：tool_call → ActionExecution-

      Message，tool_result → ResultMessage。

     

     
      统一标识：维护 threadId（会话）与 runId（本轮 loop），为历史/检查点铺路。

     

     
      精确收束：依据服务端“回合结束”信号或本地规则，准确结束本轮流。

     

    

    

   

   上层只看到标准的 AgentStreamEvent：

   

   

   export type AgentStreamEvent = {
  threadId?: string | null
  runId?: string | null
  messages?: Message[]
  guardrailsFailureReason?: string
}

   

   UI 组件无须关心消息从哪里来，只负责渲染消息序列。

   
    
     
      05

     

    

   

   
    Agent 回合循环（loop）与工具调用（tools）

   

   Chat 模式不仅是“生成一条回复”，而是“一轮内可能包含多条消息”：思考、工具调用、结果回注、继续生成……我们把“回合循环”放在 useChat 中集中处理：

   
    
     
      

      
       
        串接流式事件，按顺序追加消息；

       

       
        捕获 ActionExecutionMessage 触发前端工具 handler，并把结果回注为 ResultMessage；

       

       
        当一轮结束，返回最终 AssistantMessage 并可进入下一轮；

       

       
        在“重载/变体”场景中，保留既有候选并追加新候选，形成多变体集合。

       

      

      

     

    

   

   与传输方式无关：只要后端发出等价事件，Adapter 统一映射，工具消息即可完整往返。

   
    
     工具调用的前端形态：useAgentAction

    

   

   为了让“工具”在页面内即可声明与注册，我们提供了 useAgentAction：

   
    
     
      

      
       
        描述：name/description/parameters；

       

       
        处理：handler(args) 返回值会被打包成 ResultMessage 回注对话；

       

       
        可选渲染：render 可将工具调用或结果以内嵌卡片形式展示（不影响文本流）；

       

       
        幂等：同一执行 ID 只会触发一次 handler（去重）。

       

       
        与运行时的关系：Adapter 负责把后端的工具事件统一映射为前端消息，UI 不需要关注具体协议与传输方式。

       

      

      

     

    

   

   
    
     
      06

     

    

   

   
    UI 交互与建议（Suggestions）

   

   Chat 作为容器，暴露了消息渲染插槽与输入区控制，默认行为：

   
    
     渲染 Thinking、Assistant、User、Error 等消息类型；

    

    
     支持复制、停止、重新生成、建议点击；

    

    
     useCopilotChatLogic 负责把 Core 能力（useAgentChat）与 UI 事件连起来，并提供节流后的建议刷新入口。

    

   

   
    
     
      07

     

    

   

   
    最小上手：3 步把 Chat 接入到任一页面

   

   

   

   // 1) 在根组件用 AgentKit 包裹，并选择 Runtime
// App.vue
<template>
  <AgentKit:runtime="runtime">
    <MyChat />
  </AgentKit>

</template>
<scriptlang="ts">
import { AgentKit, VapdRuntimeAdapter } from '@vapd-agentkit/vue-core'

exportdefault {
  components: { AgentKit },
  setup() {
    const runtime = new VapdRuntimeAdapter({
      // 可选：自定义 url/headers/agentId/appId/extendParams
    })
    return { runtime }
  }
}
</script>
// 2) 页面里直接用 Chat（或自定义渲染
<template>
  <AgentChat:labels="{ placeholder: '问点什么' }" />

</template>
<scriptsetuplang="ts">
import { AgentChat } from '@vapd-agentkit/vue-ui'
</script>
// 3) （可选）注册工具，供模型调用
// 任一组件 setup 中：
import { useAgentContext } from '@vapd-agentkit/vue-core'

const ctx = useAgentContext()
ctx.setAction('searchDocs', {
  name: 'searchDocs',
  description: '搜索知识库',
  parameters: [{ name: 'q', type: 'string' }],
  handler: async ({ q }) => {
    const result = await fetch(`/api/search?q=${encodeURIComponent(q)}`).then(r => r.json())
    return { hits: result.items }
  }
})

   

   
    
     
      08

     

    

   

   
    与业务的契合

   

   笔记/知识库/项目管理：前端可把当前选中文段/标签/页面结构通过 addContext 合并入 agentArgs，无需更改 Runtime。

   

   知识库agent文档/集成流程智能Agent（未来规划）：把检索与聚合能力抽象为 FrontendAction，回注 ResultMessage，让 Agent 循环自动推进。

   
    
     
      09

     

    

   

   
    面向知识库问答与集成流程智能的演进设想

   

   
    
     知识库问答 Agent（RAG）

    

   

   
    
     
      

      
       
        支持互联网检索，结合站内知识完成回答；

       

       
        提供关键字检索、内容获取与语义检索（向量）；

       

       
        后续将支持直接帮你编辑、 新增文档等操作；

       

       
        让 AI 准确看到你正在关注的内容，与你的上下文保持一致，帮助你更高效地思考、写作与创造。

       

      

      

      

     

    

   

   2. 集成流程，自动配置，添加节点，配置节点，验证节点，一句话帮你完成流程配置

   

   
    
     
      

      
       
        面向非开发同学，解决流程编排困难和语法复杂的问题；

       

       
        支持从自然语言自动生成流程与节点参数

       

       
        节点配置表单化，参数智能补全与校验，自动化验证每一步并给出修复建议；

       

       
        支持逐步验证与仿真运行，输出日志与每步结果检查。

       

      

      

     

    

   

   
    
     
      10

     

    

   

   
    下一步需完善

   

   
    
     历史记录：当前未做持久化回放；已通过 threadId 预埋会话键，后续可依此查询并复原消息序列。

    

    
     检查点：runId 用于标记本轮 loop，未来可以支持检查点能力，在“继续/撤回/回滚”中复用，是Agent交互中必不可少的能力。

    

    
     工具事件：实现HumanInTheLoop能力，工具调用需要用户确认，或者需要用户填写表单等内容与Agent协同。

    

   

   
    
     
      11

     

    

   

   
    结  语

   

   用“消息模型 + Runtime Adapter + 前端编排”的方式，我们把 Chat 模式做成了可以“拼”的底座：

   
    
     
      

      
       
        UI 只面向消息，不关心来源；

       

       
        运行时可替换，协议差异被屏蔽；

       

       
        工具/上下文/重试等交互都在编排层实现；

       

       
        threadId/runId 为历史/检查点打好地基。

       

      

      

     

    

   

   这让三类业务都能在同一套基建上继续演进。接下来，我们会补齐历史与工具事件、完善多变体交互，并把“回合对齐/评测”纳入流水线。
