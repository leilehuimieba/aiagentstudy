# 领域情报学习系统 — 产品路线图

> 更新时间：2026-05-19  
> 状态：**长期路线图；当前执行以 `PRODUCT_NOW.md` 为准**

> 2026-06-18 提醒：本文档中部分早期基线数字已经过期。当前知识库事实以 `.\kb.ps1 status`、`knowledge/catalog/current-coverage.md`、`PROJECT_BOARD.md` 和 `PRODUCT_NOW.md` 为准。最近一次状态为：592 条 catalog rows、561 条 BestBlogs rows、最新 BestBlogs ID `BB-2026-05-01-573`、6888 个 FTS chunks。

---

## 零、开发前准备工作（必须全部完成才能开始写代码）

> 本章节是实际检查结果，不是假设。每项有真实验证命令。

### 0-A 环境核查结论

| 项目 | 状态 | 实际情况 |
|---|---|---|
| Python | ✅ | 3.8.0，路径 `D:\Grammar\python38\python.exe`，命令用 `python`（不是 `python3`） |
| Node.js | ✅ | v24.14.0 |
| pip | ✅ | 25.0.1 |
| flask | ✅ | 3.0.3 已安装 |
| requests | ✅ | 已安装 |
| anthropic SDK | ❌ | **未安装，需要执行准备步骤** |
| feedparser | ❌ | **未安装，需要执行准备步骤** |
| python-dateutil | ❌ | **未安装，需要执行准备步骤** |
| ANTHROPIC_API_KEY | ❌ | **未配置，用户必须手动填入 .env** |
| SQLite FTS5 trigram | ⚠️ | SQLite 3.28，不支持 trigram tokenizer（需要 3.35+），**已有索引无法使用** |

### 0-B SQLite 版本问题的解决方案

**问题：** 现有 `kb.sqlite` 的 FTS5 索引使用了 `trigram` tokenizer，但当前 SQLite 3.28 不支持，查询会报错。

**解决方案（不升级 SQLite，不破坏现有文件）：**
- 现有 `kb.sqlite` 保持只读，不动
- 搜索改用 **JSON 内存搜索**：启动时加载 `articles-meta.json`（165条，约 2MB），Python 内存过滤
- 新建的 `product.sqlite` 使用默认 FTS5 tokenizer（无 trigram），避免此问题
- 等后续有需要再升级 SQLite 或引入向量搜索

### 0-C 现有数据实际情况（与文档其他地方的假设不同，以此为准）

```
知识库实际状态：
  文章数量：165 篇（不是 228，部分未完整索引）
  日期范围：2026-04-27 ~ 2026-05-05（约 10 天）
  存储位置：knowledge/items/<topic>/<id>/
  数据表名：items（不是 articles）
  元数据文件：knowledge/retrieval/articles-meta.json
  编码：UTF-8（终端显示乱码是 Windows 终端问题，数据本身正常）

Topic 分布：
  01-context-memory:     53 篇
  02-tools-actions:      43 篇
  03-control-loop:       20 篇
  04-evaluation-guardrails: 16 篇
  06-frontier-radar:     33 篇

Python 命令：
  用 python（不是 python3）
  用 pip（不是 pip3）
```

### 0-D 准备工作执行清单（按顺序执行）

#### 步骤 1：安装缺失的 Python 依赖
```bash
pip install anthropic feedparser python-dateutil
```
验证：
```bash
python -c "import anthropic, feedparser, dateutil; print('all ok')"
```

#### 步骤 2：配置 API Key（用户必须手动完成）
在 `D:/newwork/aiagentstudy/product/` 目录创建 `.env` 文件：
```
ANTHROPIC_API_KEY=sk-ant-你的真实key
```
⚠️ 没有这个 key，M4 问答功能无法运行。

#### 步骤 3：创建 product/ 目录结构
执行脚本自动创建（见下方 migrate_db.py）

#### 步骤 4：创建初始配置文件
- `product/config/sources.json`：采集源配置
- `product/config/domains.json`：领域配置

#### 步骤 5：初始化 product.sqlite
运行 `python product/scripts/migrate_db.py`

#### 步骤 6：冒烟测试
运行 `python product/scripts/smoke_test.py` 确认全部通过

### 0-E 准备工作验收

所有以下命令都必须成功（无报错），才能开始写业务代码：

```bash
# 1. 依赖检查
python -c "import anthropic, feedparser, dateutil, flask, requests; print('deps ok')"

# 2. 数据库检查
python -c "
import sqlite3, json
db = sqlite3.connect('D:/newwork/aiagentstudy/knowledge/retrieval/kb.sqlite')
count = db.execute('SELECT COUNT(*) FROM items').fetchone()[0]
print(f'kb.sqlite ok: {count} items')
db.close()
with open('D:/newwork/aiagentstudy/knowledge/retrieval/articles-meta.json', encoding='utf-8') as f:
    meta = json.load(f)
print(f'articles-meta.json ok: {len(meta)} items')
"

# 3. 内存搜索测试
python -c "
import json
with open('D:/newwork/aiagentstudy/knowledge/retrieval/articles-meta.json', encoding='utf-8') as f:
    items = json.load(f)
results = [i for i in items if 'checkpoint' in i.get('retrieval_text', '').lower()]
print(f'search ok: checkpoint found in {len(results)} items')
"

# 4. API key 检查
python -c "
import os
from pathlib import Path
env_path = Path('D:/newwork/aiagentstudy/product/.env')
if env_path.exists():
    content = env_path.read_text()
    has_key = 'ANTHROPIC_API_KEY=sk-ant-' in content
    print('API key configured:', has_key)
else:
    print('ERROR: .env file not found')
"

# 5. product.sqlite 检查
python -c "
import sqlite3
db = sqlite3.connect('D:/newwork/aiagentstudy/product/data/product.sqlite')
tables = [r[0] for r in db.execute(\"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()]
print('product.sqlite tables:', tables)
db.close()
"
```

---

## 文档导读

| 章节 | 内容 | 用途 |
|---|---|---|
| 一 | 产品定位 | 每次迷失方向时回来看 |
| 二 | **整体验收标准** | 每个阶段结束时对照 |
| 三 | 现有资产 | 开始前确认不重复造轮子 |
| 四 | **技术栈决策** | 遇到技术选型问题时参考 |
| 五 | **项目目录结构** | 写代码前确认放哪里 |
| 六 | 模块架构总图 | 理解整体结构 |
| 七 | 模块详细规划（M1-M10） | 做每个模块前仔细阅读 |
| 八 | **第一阶段任务拆解** | 直接开始执行的依据 |
| 九 | 执行顺序 | 阶段划分和里程碑 |
| 十 | 不做什么 | 防止功能蔓延 |
| 十一 | 阶段自检 | 每阶段结束时问自己 |

---

## 一、产品定位

**一句话：** 你在某个领域积累的时间越长，它就越懂你在研究什么。

**核心差异化：**
- BestBlogs / TrendRadar：告诉你今天发生了什么（信息流）
- Perplexity / GPT Researcher：帮你做一次性深度研究（单次搜索）
- Khoj：你上传文档，它帮你问答（手动知识库）
- **我们：自动采集 + 时间复利积累 + 让你真正学到（不只是看过）**

**目标用户（起点）：** 需要持续跟踪某个专业领域的独立研究者、AI 从业者、技术创业者。

---

## 二、整体验收标准（计划完成的判断依据）

> 这是整个产品"做完了"的定义。每个阶段结束后对照此表。

### 阶段一验收（第 1-2 周完成）
- [ ] 用自然语言问一个跨时间问题，得到带引用和日期的回答
- [ ] 回答能区分"1个月内的新观点"和"3个月前的旧观点"
- [ ] 采集新文章后，下次问答能包含新内容
- [ ] 知识库为空时，明确告知而不是胡编

### 阶段二验收（第 3-4 周完成）
- [ ] 切换到"工程师视角"和"产品视角"，同一篇文章摘要有明显不同
- [ ] 系统能识别"这个用户更关注技术实现还是商业应用"
- [ ] 能追踪第二个领域（不只是 AI agent，换一个领域能跑起来）

### 阶段三验收（第 5-6 周完成）
- [ ] 读完文章有"一句话总结"入口，写的内容能在"我的笔记"里查到
- [ ] 3 天后收到一篇已读文章的复习提醒，提示有效（不是废话）
- [ ] 周一收到"上周学到了什么"报告，内容是关于我的理解变化，不是文章列表

### 阶段四验收（第 7-8 周完成）
- [ ] 一眼看出自己在哪个子话题上覆盖薄弱
- [ ] 系统推荐的文章，80% 我认为是我确实应该读的
- [ ] 每条推荐都有"为什么推荐给你"的说明，说明是准确的

### 整体产品验收（第 8 周末）
- [ ] 我自己每天都在用，而不是部署好就不碰了
- [ ] 能向一个陌生人在 2 分钟内说清楚"这个产品和 BestBlogs/TrendRadar 有什么不同"
- [ ] 至少有 1 个不是我的人在用，且用了 2 周以上没有放弃

---

## 三、现有资产（不要重复造轮子）

| 资产 | 位置 | 状态 | 价值 |
|---|---|---|---|
| 228 篇 AI agent 文章 | `knowledge/items/` | 完整 | 启动弹药，冷启动解决方案 |
| FTS5 全文检索 | `knowledge/retrieval/kb.sqlite` | 可用 | 语义检索基础 |
| 文章元数据索引 | `retrieval/articles-meta.json` | 可用 | 分类、标签、摘要 |
| BestBlogs 采集脚本 | `knowledge/raw/*.js` | 可用 | 采集 pipeline |
| 6 维分类体系 | catalog | 可用 | 领域分类基础 |

**结论：** 采集层、存储层、基础检索层已经存在。**不要重写，要包装成产品。**

---

## 四、技术栈决策

> 每个选择都有明确理由，不随意更换。

| 层级 | 技术选择 | 理由 |
|---|---|---|
| 采集脚本 | **Node.js**（现有） | 现有脚本全是 Node.js，不重写 |
| 存储 | **SQLite**（现有） | 轻量，本地，已有 FTS5 索引，零运维 |
| 后端 API | **Python + Flask** | Python 3.8 已有，LLM SDK 生态最好，Flask 比 FastAPI 对 3.8 更友好 |
| LLM 调用 | **OpenAI SDK + DeepSeek** | 日常任务用 deepseek-v4-flash（快）；复杂推理用 deepseek-v4-pro（推理模型，慢但准） |
| **间隔复习算法** | **`supermemo2` 库**（✅ 已决策） | 直接 pip install，不自实现 SM-2；Python 3.8 兼容，零依赖 |
| **知识图谱可视化** | **Cytoscape.js CDN**（✅ 已决策） | 无构建步骤，CDN 引入；力导向布局 `cose`；不用 D3.js（过复杂）|
| **报告模板** | **Jinja2**（✅ 已决策） | Flask 已附带，render_template_string() 直接用；不引入 reportAI 等重库 |
| **关键词提取** | **正则 + 停用词**（✅ 已决策） | 165 篇文章规模，不引入 jieba/spaCy（依赖重，3.8 兼容有坑）|
| **向量检索** | **暂缓**（≥ 500 篇文章后引入） | 当前 FTS5 已够；届时选 sentence-transformers+FAISS 或 sqlite-vec |
| 前端 | **HTML + 原生 JS**（MVP） | 不引入构建工具，直接打开 index.html 即可用 |
| 定时任务 | **Windows 任务计划程序 / cron** | 系统级，不依赖进程常驻 |
| 包管理 | **pip + requirements.txt** | 简单，Python 3.8 兼容 |

### 需要安装的依赖

```bash
# Python 依赖（第一次执行前安装）
pip install flask openai requests feedparser python-dateutil supermemo2

# Node.js 依赖（已有，确认即可）
cd D:/newwork/aiagentstudy
npm install  # 如果有 package.json
```

### 环境变量

```
# .env 文件（放在 product/ 目录，不提交 git）
LLM_BASE_URL=https://api.deepseek.com/v1
LLM_API_KEY=sk-你的key
LLM_MODEL=deepseek-v4-pro
COLLECT_QUALITY_THRESHOLD=6
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
```

---

## 五、项目目录结构

```
aiagentstudy/
│
├── knowledge/                    ← 现有，不动
│   ├── items/                    ← 228 篇文章
│   ├── retrieval/kb.sqlite       ← 现有 FTS5 库
│   └── raw/                      ← 采集脚本
│
├── product/                      ← 新建，所有新代码在这里
│   ├── api/                      ← Python Flask 后端
│   │   ├── app.py                ← Flask 入口
│   │   ├── db.py                 ← 数据库操作封装
│   │   ├── collect.py            ← 采集 pipeline
│   │   ├── qa.py                 ← 问答逻辑
│   │   ├── user_model.py         ← 用户模型更新
│   │   ├── personalize.py        ← 个性化摘要生成
│   │   ├── learning.py           ← 学习机制（压缩/复习）
│   │   ├── recommend.py          ← 推荐逻辑
│   │   └── report.py             ← 周报生成
│   │
│   ├── web/                      ← 前端（纯 HTML/JS）
│   │   ├── index.html            ← 主界面（文章列表 + 问答入口）
│   │   ├── article.html          ← 文章详情页
│   │   ├── graph.html            ← 知识图谱页
│   │   ├── profile.html          ← 用户画像页
│   │   └── js/
│   │       ├── api.js            ← 统一 API 调用封装
│   │       ├── reader.js         ← 阅读行为埋点
│   │       └── ui.js             ← 通用 UI 组件
│   │
│   ├── scripts/                  ← 独立运行的脚本
│   │   ├── daily_collect.py      ← 每日采集入口
│   │   ├── weekly_report.py      ← 周报生成入口
│   │   └── migrate_db.py         ← 数据库迁移
│   │
│   ├── config/
│   │   ├── sources.json          ← 信息源配置
│   │   └── domains.json          ← 领域配置
│   │
│   ├── data/
│   │   └── product.sqlite        ← 新增的用户行为库（和现有 kb.sqlite 分开）
│   │
│   ├── requirements.txt
│   ├── .env                      ← 不提交 git
│   └── README.md                 ← 启动说明
│
├── PRODUCT_ROADMAP.md            ← 本文件
└── AGENTS.md                     ← 现有，不动
```

**关键设计决策：**
- 新代码全部在 `product/` 目录下，不污染现有 `knowledge/`
- 用两个 SQLite 文件：`kb.sqlite`（现有，只读）和 `product.sqlite`（新建，读写）
- 前期不需要起服务，`daily_collect.py` 直接命令行运行即可

---

## 七、模块架构总图

```
┌─────────────────────────────────────────────────────────────────┐
│  M1 采集层          M2 存储层          M3 领域配置层              │
│  自动抓取            结构化存储          用户定义领域               │
│  质量过滤            向量 + FTS          信息源管理                 │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  M4 对话问答层       M5 用户模型层       M6 个性化呈现层           │
│  跨时间问答           行为信号采集         同文章不同角度            │
│  引用溯源             兴趣图谱             深度通道                  │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  M7 学习机制层       M8 知识图谱层       M9 推荐层                │
│  主动压缩             概念关系图           知识盲点推荐              │
│  间隔复习             覆盖热力图           推荐理由可见              │
│  矛盾冲突             时间轴演化                                    │
└──────────────────────────────┬──────────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────────┐
│  M10 输出层                                                       │
│  周报（学到了什么）/ 变化提醒 / API                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 八、模块详细规划

---

### M1 — 采集层

**解决什么问题：** 自动、持续地从可配置信息源采集高质量内容，不依赖用户手动导入。

---

#### M1 最小闭环

**目标：** 用户配置一个信息源，系统自动定时采集，内容入库。

**实现方案：**

```
信息源类型（MVP 只做这三种）：
  1. RSS URL（覆盖 90% 的技术博客）
  2. BestBlogs 分类页（现有脚本基础上）
  3. 手动粘贴 URL（用户发现好文章，一键导入）

采集流程：
  URL / RSS → 抓取全文 → LLM 质量评分（0-10）→
  评分 < 6 丢弃 → 生成摘要 + 标签 → 写入 SQLite

定时策略：
  每天 08:00 自动运行一次（cron / 系统任务）

技术选择：
  - 现有 Node.js 脚本改造（不重写）
  - 加一个 sources.json 配置文件
  - 加一个采集日志表（每次跑了什么，结果如何）
```

**验收标准：**
- [ ] 用户编辑 `sources.json` 加入一个 RSS 地址
- [ ] 手动触发 `node collect.js`，内容进入数据库
- [ ] 重复文章不重复入库（URL 去重）
- [ ] 日志文件记录：采集了几篇，过滤了几篇，入库了几篇

**不做（MVP 阶段明确排除）：**
- 不做 UI 配置界面（直接编辑 JSON）
- 不做爬虫反反爬（先用 RSS，规避问题）
- 不做实时采集（定时批量足够）

---

#### M1 优化路径

```
优化 1（有 10 个用户后）：
  加 Web UI 管理信息源（添加/删除/测试连通性）

优化 2（发现质量问题后）：
  优化质量评分 prompt，加领域相关性过滤
  （不只是"质量高"，还要"和用户领域相关"）

优化 3（用户反馈后）：
  加 GitHub Trending、arXiv、Hacker News 适配器
  这三个覆盖技术领域 90% 的高价值内容

优化 4（规模化后）：
  加增量采集（只抓新内容，不重跑全量）
  加采集失败重试机制
```

---

### M2 — 存储层

**解决什么问题：** 文章、用户行为、知识关系的持久化存储，支撑上层所有功能。

---

#### M2 最小闭环

**目标：** 一个 SQLite 数据库，能存文章、能全文检索、能按时间查询。

**现有基础：** `kb.sqlite` 已存在，FTS5 已建好。

**MVP 需要补充的表：**

```sql
-- 文章表（现有，确认字段完整）
articles (
  id, url, title, source, domain,
  published_at, collected_at,
  summary, full_text, tags,
  quality_score, embedding_id
)

-- 用户行为表（新增）
user_events (
  id, article_id, event_type,
  -- event_type: view_start / view_end / highlight /
  --             feedback_useful / feedback_known / feedback_dive
  payload,   -- JSON，存额外数据（高亮的文字等）
  created_at
)

-- 用户笔记表（新增，存"一句话压缩"）
user_notes (
  id, article_id, note_text,
  note_type,  -- compression / question / insight
  created_at
)

-- 复习队列表（新增，间隔复习用）
review_queue (
  id, article_id, concept,
  next_review_at, ease_factor,
  review_count, last_result
)
```

**验收标准：**
- [ ] 四张表能正常写入读出
- [ ] FTS5 能按关键词搜索文章
- [ ] 按 `domain` 和 `published_at` 过滤文章
- [ ] `user_events` 能记录一次"阅读开始/结束"事件

---

#### M2 优化路径

```
优化 1（问答功能上线后）：
  加向量嵌入（embedding）存储
  用 sqlite-vec 或迁移到 LanceDB
  支持语义相似搜索（不只是关键词匹配）

优化 2（用户量增加后）：
  加全量备份机制（每日 .sqlite 备份到指定目录）
  加数据导出（用户可以把自己的知识库导出为 JSON）

优化 3（多领域支持后）：
  加 domains 表（用户定义的领域列表）
  文章和领域多对多关联
```

---

### M3 — 领域配置层

**解决什么问题：** 让用户能定义"我要追踪什么"，而不是只能追踪固定的 AI agent 领域。

---

#### M3 最小闭环

**目标：** 用户创建一个"领域"，配置关键词和信息源，系统自动把采集内容归类到这个领域。

**实现方案：**

```
domain_config.json 示例：
{
  "domains": [
    {
      "id": "ai-agent",
      "name": "AI Agent",
      "keywords": ["agent", "MCP", "LangGraph", "harness", "tool use"],
      "sources": ["bestblogs-ai", "arxiv-cs.AI", "hn-ai"],
      "exclude_keywords": ["chatbot", "画图"]
    }
  ]
}

归类逻辑：
  文章入库时，对 title + summary 做关键词匹配
  命中 keywords 且不命中 exclude_keywords → 归入此领域
  命中多个领域 → 都归入（多对多）
```

**验收标准：**
- [ ] 修改 `domain_config.json` 不需要改代码
- [ ] 新采集的文章自动打上领域标签
- [ ] 能按领域过滤查看文章列表
- [ ] 有一个"未分类"桶，收集没有命中任何领域的文章

---

#### M3 优化路径

```
优化 1（用户反馈分类不准后）：
  改用 LLM 判断相关性（比关键词匹配准确，但慢一些）
  关键词匹配作为 pre-filter，LLM 做最终判断

优化 2（多用户场景）：
  领域配置移到数据库，支持 UI 编辑
  加"领域模板"功能（选一个预设领域快速开始）

优化 3（领域理解加深后）：
  自动发现领域内的子话题
  给用户展示："你的 AI Agent 领域下有这些子话题"
```

---

### M4 — 对话问答层

**解决什么问题：** 用户能用自然语言问关于自己知识库的问题，得到有时间维度的答案。

**这是 MVP 最核心的差异化功能。**

---

#### M4 最小闭环

**目标：** 用户问一个关于领域的问题，系统从知识库检索相关文章，生成带引用的回答。

**实现方案：**

```
问答流程：
  用户问题
    → FTS5 关键词搜索（找相关文章）
    → 取 top 5-8 篇文章的摘要
    → 拼入 context，调 LLM 生成回答
    → 回答中标注来源（文章标题 + 日期）

关键 prompt 设计：
  "你只能基于以下 {N} 篇文章回答，文章均来自 {domain} 领域，
   时间跨度 {start} 到 {end}。
   如果这些文章不足以回答，明确说明。
   回答时注明哪个观点来自哪篇文章（日期）。"

时间维度问题（特殊处理）：
  检测 trigger 词：最近/上个月/这周/变化/趋势/演化
  触发时间范围过滤：只检索对应时间段的文章
  结构化输出：{时间段前} vs {时间段后} 的对比
```

**验收标准：**
- [ ] 问"AI agent 可靠性现状"能得到有引用的答案
- [ ] 问"这个月有什么新变化"能限定到最近 30 天的文章
- [ ] 回答中每个引用都能点击跳到原文
- [ ] 知识库里没有相关内容时，明确说"我的知识库里没有这方面的信息"

---

#### M4 优化路径

```
优化 1（FTS 召回质量差后）：
  加向量语义搜索（embedding + cosine similarity）
  混合检索：FTS + 向量，rerank 合并结果

优化 2（用户问跨领域问题后）：
  支持跨领域检索（"AI agent 和量化交易有什么交叉？"）

优化 3（时间轴分析需求出现后）：
  专门的"演化分析"模式
  输出：概念 X 在过去 N 个月的观点演变时间线

优化 4（问答质量稳定后）：
  加对话记忆（同一 session 内的上下文连贯）
  "你刚才问的那篇文章里还有一个细节..."
```

---

### M5 — 用户模型层

**解决什么问题：** 系统理解这个用户是谁、关注什么、处于什么学习阶段，驱动个性化。

---

#### M5 最小闭环

**目标：** 被动采集阅读行为，推断用户的关注角度和专业深度。

**实现方案：**

```
信号采集（前端埋点，3 种最轻的）：
  1. 阅读时长：页面进入/离开时间戳差值
     > 30 秒 = 认真读
     < 10 秒 = 扫了一眼
  2. 显式反馈按钮（界面上三个按钮）：
     💡 有用  /  ✓ 已知道  /  🔍 想深入了解
  3. 滚动深度：读到文章的百分之几

用户模型字段（存入 user_profile 表）：
  expertise_level: beginner / intermediate / expert
    （根据"已知道"点击率推断：点多了说明基础扎实）
  primary_angle: engineer / product / researcher
    （根据哪类文章读得久推断）
  active_topics: [字符串数组]
    （读了 3 篇以上且时长 > 30s 的 tag）
  weak_topics: [字符串数组]
    （相关领域但几乎没读过的 tag）

推断规则（可以先硬编码，不用 ML）：
  读了 5 篇以上带 "implementation" tag 的 → engineer
  读了 5 篇以上带 "product" / "business" tag 的 → product
  "已知道"点击率 > 40% → expert
  "已知道"点击率 < 10% → beginner
```

**验收标准：**
- [ ] 阅读 10 篇文章后，`user_profile` 表有数据
- [ ] `expertise_level` 和 `primary_angle` 有值
- [ ] 能查看自己的"用户画像"页面（简单展示即可）

---

#### M5 优化路径

```
优化 1（有足够行为数据后）：
  加对话信号：从问答对话中提取兴趣关键词
  "用户问了什么类型的问题" 比 "用户读了什么" 更准确

优化 2（个性化需求明确后）：
  用户可以主动编辑自己的画像（校正系统推断）
  "系统认为我是工程师视角，但我更关注产品侧" → 一键修正

优化 3（多用户后）：
  加用户偏好的显式设置
  第一次使用引导：让用户粘贴一篇他觉得写得好的文章
  从这篇文章推断初始用户模型
```

---

### M6 — 个性化呈现层

**解决什么问题：** 同一篇文章，不同用户看到不同角度的摘要，而不是千篇一律的原文摘要。

---

#### M6 最小闭环

**目标：** 根据用户的 `primary_angle` 字段，用对应角度重新生成文章摘要。

**实现方案：**

```
三种角度 prompt（MVP 先做这三种）：

工程师角度：
  "用 3 句话总结这篇文章的技术要点：
   关键实现细节是什么？和现有方案相比技术上有什么不同？
   有什么坑或限制？"

产品角度：
  "用 3 句话总结这篇文章的产品洞察：
   解决了什么用户问题？对竞争格局有什么影响？
   给产品决策者的 takeaway 是什么？"

初学者角度：
  "用简单的语言解释这篇文章讲了什么：
   用一个生活中的类比帮助理解核心概念。
   读完这篇应该知道哪三件事？"

触发时机：
  文章入库时，预生成三个角度的摘要（异步，不影响采集速度）
  存入 article_summaries 表（article_id + angle + summary_text）
  展示时根据 user_profile.primary_angle 选择对应摘要
```

**验收标准：**
- [ ] 同一篇文章，切换"工程师/产品/初学者"模式，摘要内容不同
- [ ] 首次加载不慢（摘要已预生成，不是实时生成）
- [ ] 用户可以手动切换角度查看

---

#### M6 优化路径

```
优化 1（用户反馈摘要质量后）：
  优化各角度 prompt
  加摘要评分（用户点"没用"时触发重新生成）

优化 2（用户模型精细化后）：
  从 3 种角度扩展到更细粒度
  例如：工程师里细分"架构师" vs "实现工程师"

优化 3（深度通道）：
  用户划选文章中的某个词/句子
  弹出：这个概念在你的知识库里有 N 篇相关内容
         [查看这个概念的完整上下文]
         [帮我用更简单的语言解释]
         [这个观点有没有反对意见]
```

---

### M7 — 学习机制层

**解决什么问题：** 让用户真正"学到"，而不只是"看过"。核心反人性但高价值。

---

#### M7 最小闭环

**目标：** 实现"读完压缩"和"间隔复习"两个最基础的学习机制。

**实现方案：**

```
机制 1：读完压缩（Read → Compress）

  用户读完文章，底部弹出：
  ┌──────────────────────────────────────────┐
  │ 用一句话写下：这篇文章改变了你什么想法？   │
  │ _________________________________________ │
  │ [跳过]                      [保存 →]      │
  └──────────────────────────────────────────┘

  - 用户写的句子存入 user_notes 表
  - 不强制（有跳过按钮），但统计跳过率
  - 跳过 5 次以上时轻提醒一次

机制 2：间隔复习（Spaced Repetition）

  触发条件：用户在某篇文章上停留 > 30s，或点了"有用"
  → 将这篇文章加入 review_queue，next_review_at = now + 3 days

  复习时的呈现：
  ┌──────────────────────────────────────────┐
  │ 3 天前你读了「LangGraph 1.0 新特性」       │
  │                                          │
  │ 不翻回去，回答一个问题：                  │
  │ checkpoint/resume 解决了什么核心问题？    │
  │                                          │
  │ [我来想想]  [已忘记，给我提示]  [我记得]  │
  └──────────────────────────────────────────┘

  - [我来想想] → 展开答案（用文章摘要生成）
  - [已忘记]   → next_review_at = now + 1 day（ease_factor--）
  - [我记得]   → next_review_at = now + 7 days（ease_factor++）

  复习问题生成：
  文章入库时，用 LLM 生成 1 个"核心考查点"问题
  存入 articles 表的 review_question 字段
```

**验收标准：**
- [ ] 读完一篇文章，底部弹出压缩框
- [ ] 输入的句子能在"我的笔记"页面看到
- [ ] `review_queue` 里有数据，到时间后推送复习提醒
- [ ] 完成一次复习，根据结果更新 `next_review_at`

---

#### M7 优化路径

```
优化 1（有复习数据后）：
  加矛盾冲突检测：
  当新文章观点与用户已读文章矛盾时，主动提示
  "你上周读的文章说 X，今天这篇说 Y，你怎么看？"

优化 2（用户有笔记积累后）：
  "教我"模式：用户用自己的话解释一个概念
  系统评估并指出盲点

优化 3（学习数据足够后）：
  个人知识报告：
  "你已经能解释的概念 / 还在理解中的 / 还没触及的"
  四层知识状态可视化
```

---

### M8 — 知识图谱层

**解决什么问题：** 让用户能看到领域的结构和自己的覆盖状况，不只是一个文章列表。

---

#### M8 最小闭环

**目标：** 一个覆盖热力图，显示用户在各个子话题上的文章数量和学习深度。

**实现方案：**

```
子话题定义（先手动定义，不用 AI 自动发现）：
  AI Agent 领域下：
    - 控制流与编排
    - 记忆与上下文
    - 工具与 MCP
    - 多 Agent 协作
    - 评估与可靠性
    - 安全与权限
    - 产品与商业

  这些用 keywords 映射到 tags，和 M3 的标签体系对齐

热力图展示：
  每个子话题显示：
    文章数量（采集深度）
    用户实际读过的比例（覆盖深度）
    最近更新时间（活跃度）

  颜色编码：
    深色 = 覆盖充分
    浅色 = 覆盖稀薄 → 推荐补充
    灰色 = 没有采集到内容
```

**验收标准：**
- [ ] 页面展示 AI Agent 领域的 7 个子话题
- [ ] 每个格子显示：文章数 / 读过数 / 最近更新
- [ ] 点击格子，进入该子话题的文章列表

---

#### M8 优化路径

```
优化 1（子话题数据充分后）：
  加时间轴维度：
  某个子话题的文章数量趋势图（这个方向是在变热还是变冷）

优化 2（概念提取能力成熟后）：
  AI 自动发现子话题（不再手动定义）
  从文章中提取高频概念，自动聚类

优化 3（用户量增加后）：
  概念关系图（力导向图）
  节点 = 概念，边 = 共同出现 / 引用关系 / 矛盾关系
  这是完整的知识图谱，作为高级功能
```

---

### M9 — 推荐层

**解决什么问题：** 不是"你可能喜欢"，而是"根据你的知识状态，你应该读这篇"。

---

#### M9 最小闭环

**目标：** 基于知识覆盖热力图，推荐用户薄弱区域的文章，并说明推荐理由。

**实现方案：**

```
推荐逻辑（规则式，不用 ML）：

  数据来源：
    M8 的覆盖热力图 + M5 的用户模型

  规则：
    1. 找出覆盖率 < 30% 的子话题
    2. 在这些子话题里，找最近 14 天内的文章
    3. 排序：质量分 * 相关性分 * 时新性权重
    4. 取 top 3

  推荐卡片格式：
  ┌───────────────────────────────────────┐
  │ 推荐给你                              │
  │                                       │
  │ 「Agent 评估方法：三层决策框架」        │
  │                                       │
  │ 推荐理由：                            │
  │ 你在"评估与可靠性"方向只读过 2 篇，    │
  │ 但这个方向最近 2 周有 5 篇新文章，     │
  │ 这篇是其中质量分最高的。              │
  └───────────────────────────────────────┘
```

**验收标准：**
- [ ] 每天推荐 3 篇文章（不多，精不滥）
- [ ] 每篇推荐都有"为什么推荐给你"的说明
- [ ] 用户点"不感兴趣"后，这篇不再出现，且对应子话题优先级降低

---

#### M9 优化路径

```
优化 1（用户反馈推荐不准后）：
  加对话驱动的推荐：
  用户在对话中说了某个词，主动推荐相关文章
  "你刚才问到了 durable execution，我这里有 3 篇相关内容"

优化 2（数据足够后）：
  加"连接两个你已知概念的桥梁文章"推荐
  "你已经理解了 A 和 B，这篇文章解释了 A 和 B 的关系"

优化 3（多用户后）：
  加"和你学习路径相似的人也读了"
  （轻度协同过滤，保护隐私）
```

---

### M10 — 输出层

**解决什么问题：** 给用户一个持续的"成长感"，让他们看到知识在积累，而不只是信息在流逝。

---

#### M10 最小闭环

**目标：** 每周一早上，给用户发一份"上周你学到了什么"的报告（不是"上周发布了什么"）。

**实现方案：**

```
周报内容结构：

  📈 本周你深化的理解（来自复习记录和笔记）
     · 概念 A：从"听说过"升级到"能解释"
     · 概念 B：补充了 2 个新细节

  🆕 本周新出现的概念（你之前没见过的）
     · 列出 3-5 个

  ❓ 还悬而未决的矛盾（你标记了但没解决的）
     · "大厂入场是否让小工具失去差异化" ← 第 2 周了

  💡 你本周写的句子（"一句话压缩"汇总）
     · 列出 3 条你自己写的

  📊 知识覆盖变化
     · 上周：231 篇 / 本周新增：12 篇
     · 最活跃子话题：评估与可靠性（+5 篇新文章）

生成方式：
  每周日 23:00 定时脚本跑
  从数据库聚合本周数据
  用 LLM 把数据转成自然语言段落
  存为 HTML/Markdown，发送方式 MVP 先用终端打印或写文件
```

**验收标准：**
- [ ] 手动运行 `node weekly-report.js`，生成一份报告
- [ ] 报告包含上述 5 个部分（数据为空时有提示）
- [ ] 报告内容是关于"用户学到了什么"，不是文章列表

---

#### M10 优化路径

```
优化 1（报告有读者后）：
  加推送渠道：邮件 / 企业微信 / Telegram
  （参考 TrendRadar 的推送架构，借用思路）

优化 2（报告内容稳定后）：
  加"变化提醒"（不等周报）：
  当某个你关注的子话题在 24 小时内出现 3 篇以上新文章，
  发一条即时提醒："评估方向今天突然活跃，有重要进展"

优化 3（用户有积累后）：
  加"月度洞察"：
  "这个月，AI agent 领域的共识发生了一次明显偏移"
  时间轴可视化 + 代表性文章引用
```

---

## 九、第一阶段详细任务拆解（第 1-2 周，可直接执行）

> 这一层是"计划"和"执行"之间的桥梁。每个任务明确到"写什么文件、做什么事"。

### 任务 1：初始化 product/ 目录和数据库 schema
**预计时间：** 2 小时  
**输出文件：** `product/scripts/migrate_db.py`、`product/data/product.sqlite`

```
建表清单：
  user_events       ← 阅读行为
  user_notes        ← 一句话压缩
  review_queue      ← 间隔复习队列
  article_summaries ← 多角度摘要缓存
  user_profile      ← 用户模型
  sources           ← 信息源配置

验收：
  运行 python migrate_db.py 无报错
  用 sqlite3 查看表结构正常
```

---

### 任务 2：封装现有 kb.sqlite 的查询接口
**预计时间：** 3 小时  
**输出文件：** `product/api/db.py`

```
封装以下函数：
  search_articles(query, domain=None, days=None, limit=10)
    → FTS5 全文检索，支持按领域和时间过滤

  get_article_by_id(article_id)
    → 返回完整文章信息

  get_recent_articles(domain, days=7, limit=20)
    → 最近 N 天的文章

  get_articles_by_subtopic(subtopic_tag, limit=10)
    → 按子话题获取文章

验收：
  单独运行 db.py 中的测试函数
  search_articles("checkpoint") 返回 > 3 篇相关文章
```

---

### 任务 3：问答核心逻辑
**预计时间：** 4 小时  
**输出文件：** `product/api/qa.py`

```
函数：answer_question(question, domain="ai-agent")

流程：
  1. 检测时间关键词（最近/上个月/这周 → 设置 days 参数）
  2. 调 search_articles() 取 top 6 篇
  3. 拼 context prompt（文章标题 + 日期 + 摘要）
  4. 调 claude-haiku-4-5 生成回答
  5. 回答格式：结论 → 依据（带[文章标题, 日期]引用）

特殊情况处理：
  检索结果 < 2 篇 → 回答"我的知识库在这方面内容不足"
  问题涉及时间对比 → 分段：{早期观点} vs {近期观点}

验收：
  python qa.py 交互模式
  问"AI agent 可靠性现状" → 有带日期引用的回答
  问"这周有什么新变化" → 只引用最近 7 天的文章
  问"量子计算" → 回答"知识库里没有相关内容"
```

---

### 任务 4：最简 Flask API
**预计时间：** 2 小时  
**输出文件：** `product/api/app.py`

```
接口清单（MVP 只做这 4 个）：

  GET  /api/articles
       参数：domain, days, page, limit
       返回：文章列表（id/title/date/summary/tags）

  GET  /api/articles/:id
       返回：单篇文章完整信息

  POST /api/qa
       body: { question, domain }
       返回：{ answer, sources: [{title, date, id}] }

  POST /api/events
       body: { article_id, event_type, payload }
       返回：{ ok }（记录阅读行为）

验收：
  python app.py 启动无报错
  curl POST /api/qa 返回正确格式
  curl GET /api/articles 返回文章列表
```

---

### 任务 5：最简前端界面
**预计时间：** 4 小时  
**输出文件：** `product/web/index.html`、`product/web/js/api.js`

```
页面布局（极简，不追求好看）：

  左侧：文章列表
    - 按时间排序
    - 每条显示：标题 + 日期 + 领域标签
    - 点击进入详情

  右侧：问答框
    - 输入问题 → Enter 发送
    - 回答显示在下方
    - 引用的文章标题可点击跳转

  顶部：领域选择器（下拉菜单，MVP 只有 ai-agent）

行为埋点（reader.js）：
  进入文章详情 → 记录 view_start 事件
  离开文章详情 → 记录 view_end 事件（带停留时长）
  点击"有用"按钮 → 记录 feedback_useful 事件

验收：
  直接打开 index.html 不需要构建步骤
  能看到文章列表，点击进入详情
  输入问题后显示回答和引用
  F12 Network 面板里能看到事件被正确发送
```

---

### 任务 6：采集 pipeline 改造（配置化）
**预计时间：** 3 小时  
**输出文件：** `product/config/sources.json`、`product/scripts/daily_collect.py`

```
sources.json 格式：
{
  "sources": [
    {
      "id": "bestblogs-ai",
      "type": "bestblogs_category",
      "category": "ai",
      "enabled": true
    },
    {
      "id": "hn-ai",
      "type": "rss",
      "url": "https://hnrss.org/newest?q=AI+agent&points=50",
      "enabled": true
    }
  ]
}

daily_collect.py 流程：
  读 sources.json → 逐个采集 → 质量过滤（score < 6 丢弃）→
  去重检查（URL 是否已在 kb.sqlite）→ 入库 → 输出采集日志

验收：
  python daily_collect.py 运行完成，打印：
    "采集: 23篇 | 过滤: 8篇 | 入库: 12篇 | 重复跳过: 3篇"
  再跑一次，重复文章不会重复入库
  关掉一个 source 的 enabled=false，不再采集它
```

---

### 第一阶段完成检查清单

```
□ migrate_db.py 建表成功
□ db.py 的 search_articles() 能返回正确结果
□ qa.py 能回答带时间范围的问题
□ app.py 启动后 4 个接口都正常响应
□ index.html 直接打开可用（不需要 npm/构建）
□ 阅读行为事件能正确写入 product.sqlite
□ daily_collect.py 可手动运行，有日志输出
□ 以上 6 个任务全部完成，总用时 < 3 天
```

---

## 十、执行顺序

```
第 1 阶段（第 1-2 周）：能用的核心

  M1 MVP  → 采集 pipeline 可配置化
  M2 MVP  → 数据库补充用户行为表
  M4 MVP  → 最基础的问答（FTS + LLM 回答）

  里程碑：能问"这个月 AI agent 可靠性有什么新进展？"得到有引用的答案

---

第 2 阶段（第 3-4 周）：个性化基础

  M3 MVP  → 领域配置化（换一个领域能跑）
  M5 MVP  → 阅读行为采集 + 基础用户模型
  M6 MVP  → 三种角度摘要

  里程碑：切换到"产品角度"，同一篇文章展示不同侧重点

---

第 3 阶段（第 5-6 周）：学习机制

  M7 MVP  → 读完压缩 + 间隔复习
  M10 MVP → 每周学习报告

  里程碑：用了 2 周后，能看到"上周你学到了什么"，而不是"上周发布了什么"

---

第 4 阶段（第 7-8 周）：可视化与推荐

  M8 MVP  → 覆盖热力图
  M9 MVP  → 基于知识盲点的推荐

  里程碑：一眼能看出自己在哪个子话题上薄弱，系统自动推荐补充

---

第 5 阶段（第 9 周起）：持续深化

  M4 优化  → 加向量语义搜索
  M7 优化  → 矛盾冲突检测
  M8 优化  → 时间轴 + 概念关系图
  M10 优化 → 推送渠道接通
```

---

## 十一、不做什么（同样重要）

- **不做用户账号系统（前 3 个月）**：单用户本地运行，不要为多用户过早设计
- **不做漂亮 UI（第 1 阶段）**：命令行 + 最简单的 Web 页面，功能优先
- **不做移动端（前 6 个月）**：先 Web，移动端是后期
- **不做爬虫反爬（优先 RSS）**：RSS 覆盖 90% 需求，爬虫带来维护成本
- **不做实时推送（前 3 个月）**：定时批量足够，实时是锦上添花
- **不做社交功能**：这不是社区产品

---

## 十二、每个阶段结束的自检问题

第 1 阶段结束后问自己：
> "我自己每天用这个问答功能吗？如果不用，为什么？"

第 2 阶段结束后问自己：
> "切换到产品角度看文章，我真的感觉不一样吗？"

第 3 阶段结束后问自己：
> "上周的学习报告，有没有让我感到'我真的在进步'？"

第 4 阶段结束后问自己：
> "推荐给我的文章，有没有让我意识到自己的盲点？"

如果任何一个问题的答案是否定的，不要继续往下走，先修复这个阶段。

---

*文档维护：每完成一个 MVP 模块，在对应位置标记完成日期和实际与预期的差异。*
