# 考前速记卡

- Title: 算法设计与分析考前速记卡
- Source: local exam corpus synthesis
- Date: 2026-05-11
- Domain: algorithm-design-exam
- Type: 速记卡

## 一页速记

### 1. 算法四特性

- 有穷性
- 确定性
- 可行性
- 输入 / 输出

### 2. 复杂度顺序

`O(1) < O(logn) < O(n) < O(nlogn) < O(n^2) < O(2^n)`

### 3. 分治

- 核心：分解、递归求解、合并
- 典型题：二分搜索、归并排序、快速排序、棋盘覆盖、循环赛日程表、Strassen

### 4. 动态规划

- 两大性质：最优子结构、重叠子问题
- 步骤：定义状态 -> 写转移 -> 求最优值 -> 必要时构造解
- 典型题：LCS、矩阵连乘、编辑距离、0-1 背包

### 5. 贪心

- 核心：贪心选择性质
- 和 DP 共同点：都有最优子结构
- 典型题：哈夫曼、最优装载、最小生成树、Dijkstra

### 6. 回溯

- 核心：深度优先 + 剪枝
- 树类型：子集树 / 排列树
- 典型题：N 皇后、m 着色、TSP

### 7. 分支限界

- 核心：活结点表 + 界函数
- 组织形式：FIFO 队列 / 优先队列
- 典型题：最大团、TSP、背包

### 8. NP / 随机算法

- 记住：`P ⊆ NP`
- 常见名字：蒙特卡罗、拉斯维加斯、舍伍德

## 高频判断题 / 选择题陷阱

- **贪心法不能解 0-1 背包**
- **动态规划通常自底向上**
- **回溯法通常深度优先**
- **分支限界法不等于深度优先**
- **哈夫曼编码可用贪心法**
- **LCS 是动态规划经典题**
- **N 皇后不是贪心问题**
- **二分搜索属于分治法**

## 考前最后 10 分钟看什么

只看这些：

1. 分治 / DP / 贪心 / 回溯 / 分支限界 的区别
2. 每种方法各 2~3 个经典题
3. O、Ω、常见复杂度
4. P / NP / NP 完全
5. 常见题型关键词：
   - 子集树
   - 排列树
   - 最优子结构
   - 重叠子问题
   - 贪心选择性质
   - 活结点表
   - 剪枝函数

## 证据说明

证据主要来自以下抽取文件：
- `D:\newwork\aiagentstudy\study_spaces\algorithm-design-exam\raw\extracted\ALG-SRC-006\pandoc.md`
- `D:\newwork\aiagentstudy\study_spaces\algorithm-design-exam\raw\extracted\ALG-SRC-010\pandoc.md`
- `D:\newwork\aiagentstudy\study_spaces\algorithm-design-exam\raw\extracted\ALG-SRC-008\pandoc.md`
- `D:\newwork\aiagentstudy\study_spaces\algorithm-design-exam\raw\topic-analysis.md`
- `D:\newwork\aiagentstudy\study_spaces\algorithm-design-exam\raw\topic-analysis.json`
