# AI Agent 情报站

本地运行的 AI Agent 领域知识管理系统。自动积累 → 跨时间问答 → 帮你真正学到而不只是看过。

## 快速启动

```powershell
# 在项目根目录运行
.\product\start.ps1
```

浏览器自动打开 `http://127.0.0.1:5000/`

---

## 手动启动

```powershell
# 1. 安装依赖（首次）
pip install -r product/requirements.txt

# 2. 初始化数据库（首次）
python product/scripts/migrate_db.py

# 3. 启动服务
cd product/api
python app.py
```

访问：
- 主界面：`http://127.0.0.1:5000/`
- 知识图谱：`http://127.0.0.1:5000/graph`

---

## 每日采集

```powershell
python product/scripts/daily_collect.py
```

Dry-run（不写入）：
```powershell
python product/scripts/daily_collect.py --dry-run --limit 5
```

## 生成周报

```powershell
python product/scripts/weekly_report.py
# 指定某周
python product/scripts/weekly_report.py --week 2026-W20
```

报告保存在 `product/data/reports/`

---

## 目录结构

```
product/
├── api/
│   ├── app.py           # Flask 服务入口（同时服务前端）
│   ├── db.py            # 知识库查询
│   ├── qa.py            # 智能问答
│   ├── learning.py      # 间隔复习（SM-2）
│   ├── personalize.py   # 三角度摘要
│   ├── recommend.py     # 推荐 + 知识图谱数据
│   └── user_model.py    # 用户行为推断
├── web/
│   ├── index.html       # 主界面（Flask 服务，支持 ES modules）
│   ├── graph.html       # 知识图谱（Cytoscape.js）
│   └── js/api.js        # API 客户端
├── scripts/
│   ├── migrate_db.py    # 数据库初始化
│   ├── daily_collect.py # 每日采集
│   └── weekly_report.py # 周报生成
├── config/
│   ├── sources.json     # 信息源配置
│   └── domains.json     # 领域配置
├── data/
│   ├── product.sqlite   # 用户行为数据库
│   └── reports/         # 生成的周报
├── .env                 # API Key（不提交 git）
└── requirements.txt
```

## 关键技术决策

| 问题 | 决策 |
|---|---|
| 间隔复习算法 | `supermemo2` 库，不自实现 SM-2 |
| 知识图谱可视化 | Cytoscape.js CDN，无构建步骤 |
| 前端 ES module | Flask 服务 web/ 目录，解决 file:// CORS |
| 向量检索 | 暂缓，FTS5 内存搜索够用（165篇规模） |
| 报告模板 | Jinja2（Flask 自带） + DeepSeek |
