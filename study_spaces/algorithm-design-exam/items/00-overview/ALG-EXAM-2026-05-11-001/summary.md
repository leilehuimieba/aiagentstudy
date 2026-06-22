# 算法考试资料空间总览

- Title: 算法设计与分析考试复习空间初始化
- Source: local exam files
- Date: 2026-05-11
- Domain: algorithm-design-exam
- Location: `study_spaces/algorithm-design-exam/`

## 当前判断

你担心的“知识库污染”判断是对的。

现有 `knowledge/` 目录已经围绕 AI agent 做了目录、检索、审计和总结流程。
如果把算法题库直接塞进 `knowledge/items/`，后续：

- agent 检索结果会混入考试资料
- 相关性审计会失真
- `knowledge/retrieval/kb.sqlite` 的召回会变脏

所以这次采用了**分空间管理**：

- `knowledge/`：只保留 AI agent 主知识库
- `study_spaces/algorithm-design-exam/`：专门给算法考试复习

## 已登记的外部题库来源

来源目录：`D:\BaiduNetdiskDownload\算法设计与分析题库`

当前已发现 11 份资料，涵盖：

- 复习题纲
- 期末复习题
- 学生版练习题
- 试卷与参考答案
- 汇总版 / 合并版资料

## 现在最适合你的复习方式

不是立刻全量精读所有文件，而是按下面顺序推进：

1. 先用“题纲 / 复习题”确定范围
2. 再用“学生版 / 练习题”刷题
3. 再做“试卷 / 期末题”
4. 最后只保留高频模板和错题冲刺

## 下一步建议

如果你让我继续，最有价值的下一步是：

- 把这些 PDF / Word 题库抽取成文本
- 按“动态规划 / 贪心 / 分治 / 图算法 / NP 完全”等模块整理
- 直接给你生成一版“算法考试高频考点 + 常见题模板 + 冲刺背诵卡”
