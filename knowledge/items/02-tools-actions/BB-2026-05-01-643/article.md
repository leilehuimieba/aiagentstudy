# Codex Logs Are Burning Your SSD

- BestBlogs URL: https://www.bestblogs.dev/article/58fb6bc9
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzIzNjE2NTI3NQ==&mid=2247492103&idx=1&sn=13991140d0353c1da41da421ad61bf0d
- Source: BestBlogs / 浮之静
- Publish time: 2026-06-22 21:04:00
- Capture route: article discovered from OpenCLI Browser Bridge profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 16661

---

这不是“日志文件有点大”的小毛病。Codex 正在把 TRACE 级网络事件、遥测镜像和依赖库噪声写进一个持久化 SQLite 库；文件可能只显示几百 MB，SSD 背后承受的写入却可能高得多。

  

  世界真就是一个大草台班子，看来 Codex 确实是 Vibe 出来的...

  

  Codex 能做的事越来越多，有点像当年 Chrome 要吞噬一切的意思（你的电脑里可能安装了 N 个基于 Chromium 内核开发的 Electron 应用，Codex 就是代表之一）。Chrome 是出了名的烧 CPU，占内存，Codex 现在是烧硬盘，可真是新时代下的卧龙凤雏...

  

  截图还是太保守了，很多时候，CPU 轻松打到 150%+，Codex 也是各种僵尸进程（比如用完的 subagent 不关闭），类似的问题太多太多，已无力吐槽...

  如果你在用 OpenAI Codex，无论是 CLI、桌面端，还是编辑器扩展，可以先看一眼这个文件族：

  ls -lh ~/.codex/logs_2.sqlite*

  

  你大概率会看到三个文件：

  logs_2.sqlite
logs_2.sqlite-wal
logs_2.sqlite-shm

  主库是 SQLite 数据库，-wal 是 SQLite 的 write-ahead log，-shm 是 WAL 模式下的共享内存辅助文件。它们不是你的项目文件，也不是会话历史的规范存储。Codex 的线程、会话、索引、目标等状态还存在其他 SQLite 库和 rollout/session 文件里。

  但 logs_2.sqlite 也不是可随手清理的临时文件。它是 Codex 的本地诊断日志库，其中 feedback_log_body 会被反馈/报 bug 流程读取。更麻烦的是，多个 issue 指出它可能包含 websocket/SSE 的原始 payload，也就是可能夹带对话片段或请求内容。换句话说，它既不该被当成会话历史保留，也不该被当成无风险缓存随便上传、备份或公开。

  要判断它是不是在烧盘，先得把五层问题分开：

  
   logs_2.sqlite 在 Codex 里承担什么角色；

   为什么一个看似不大的 SQLite 文件可能对应很高的真实写入量；

   GitHub 上几个 issue 到底证明了什么；

   网上流传的触发器、tmpfs、机械盘等做法分别能解决什么、不能解决什么；

   用户现在怎么止血，上游真正该怎么修。

  

  问题边界

  日志增长本来不是新闻。真正异常的是：Codex 把一个面向诊断和反馈的 SQLite 库，当成了几乎全量 TRACE 事件的持久化出口。

  本文核对的 openai/codex commit 中，app-server[1] 和 TUI[2] 都会启动 SQLite log DB layer：

  letlog_db = state_db.clone().map(log_db::start);
letlog_db_layer = log_db
    .clone()
    .map(|layer| layer.with_filter(Targets::new().with_default(Level::TRACE)));

  也就是说，这个 sink 默认允许所有 target 的 TRACE 级别日志进入 SQLite。RUST_LOG=warn 可以影响 stderr 这类普通输出，但这里的 SQLite sink 有自己的过滤链。#17320 的报告者也正是这样复现的：进程环境里已经有 RUST_LOG=warn，但 logs_2.sqlite 里仍然持续出现 TRACE 行。

  源码里确实已经有一个小修补：在 state/src/log_db.rs[3] 里，opentelemetry_sdk 的 TRACE/DEBUG 会被丢弃。这个补丁能减少一类 OpenTelemetry SDK 噪声，但它不是全局修复。websocket、SSE、log target、codex_otel.*、codex_client::transport 等来源仍然可以进入持久化日志。

  所以更准确的病因不是 “Codex 写日志”，而是：

  
   Codex 的持久化 SQLite 日志 sink 默认接收过宽的 TRACE 来源，而且没有和用户可见的 RUST_LOG=warn 形成同一条过滤边界。

  

  这件事的副作用有三个：

  
   空间副作用：主库和 WAL 可能快速增长；

   写入副作用：即使保留行数不变，持续 insert-prune 也会制造大量物理写入；

   隐私副作用：低层协议 payload 被落盘后，日志不再只是“无害诊断文本”。

  

  写放大机制

  这个问题容易被低估，是因为 SQLite 的文件大小不是 SSD 实际写入量。

  普通人看文件大小时，通常看的是：

  ls -lh ~/.codex/logs_2.sqlite*
du -sh ~/.codex

  

  但 SQLite 在 WAL 模式下写入时，新数据通常先进入 logs_2.sqlite-wal，随后 checkpoint 到主库。期间还会更新 B-tree、索引页、页缓存、事务元数据。删除旧行也不是“把写入抵消掉”，删除本身也要写 WAL，也会更新索引。

  Codex 这张 logs 表还有多个索引。当前 logs migration[4] 中能看到这些索引：

  CREATE INDEX idx_logs_ts ON logs(ts DESC, ts_nanos DESC, id DESC);
CREATE INDEX idx_logs_thread_id ON logs(thread_id);
CREATE INDEX idx_logs_thread_id_ts ON logs(thread_id, ts DESC, ts_nanos DESC, id DESC);
CREATE INDEX idx_logs_process_uuid_threadless_ts
ON logs(process_uuid, ts DESC, ts_nanos DESC, id DESC)
WHERE thread_id ISNULL;

  也就是说，每插入一行日志，不是只写一段文本。它还可能更新多个索引结构。然后保留策略又会删掉超限的旧行，删除也要更新这些结构。

  当前源码里的保留策略大致是：

  
   日志内容保留 10 天[5]，启动维护时删除更旧的行；

   每个 thread partition 限制约 10 MiB 或 1000 行[6]；

   threadless 日志按 process UUID 单独限制；

   启动维护会跑 PRAGMA wal_checkpoint(PASSIVE)[7]。

  

  这些机制控制的是“最终留下多少日志”，不是“为了留下这些日志，磁盘被写了多少次”。PASSIVE checkpoint 也不会强行截断所有 WAL，它会避开活跃 reader/writer。

  所以你可能看到这样的现象：

  保留行数: 几乎不变
MAX(id): 快速增加
WAL: 持续写
SSD: 真实写入增加

  这就是 insert-prune 循环：表面像轮转，底层是在持续写入、建索引、删除、checkpoint。空间被控制住了，写入没有。

  证据链

  #17320：过滤失效

  #17320 的标题是：Excessive SQLite WAL writes during streaming due to TRACE logs ignoring RUST_LOG

  这个 issue 开于 2026-04-10，截至 2026-06-22 仍是 Open。

  报告者在 Linux/VSCodium 环境下测到，模型流式输出时，app-server 进程向 ~/.codex/logs_2.sqlite-wal 写入约 5 MiB/s，峰值约 16 MiB/s。关键证据有三类：

  
   进程环境确认 RUST_LOG=warn；

   strace 看到持续 pwrite64 写 WAL；

   SQLite 查询看到一次约 50 token 的回复后，MAX(id) 增加约 5000，但总行数保持稳定。

  

  这说明两件事：

  
   TRACE 日志确实绕过了用户以为的 warn 级别；

   大量日志在短时间内被插入，随后又被保留策略修剪。

  

  报告中的级别分布也很直观：

  

  如果 RUST_LOG=warn 真被这个持久化 sink 遵守，理论上 WARN 之外的大量行本不该进库。

  #28224：寿命外推

  #28224 的标题是：Codex SQLite feedback logs can write ~640 TB/year and rapidly consume SSD endurance

  这个 issue 开于 2026-06-14，截至 2026-06-22 仍是 Open，标签包括 CLI、bug、performance。

  它把问题从“日志库很大”推进到“持续写入可能消耗 SSD TBW”。报告者给出的样本是：

  
   21 天机器写入约 37 TB；

   外推约 640 TB/年；

   保留行约 68 万行；

   保留日志内容约 1 GiB；

   TRACE 占保留字节约 70.7%；

   codex_otel.log_only 和 codex_otel.trace_safe 又占约 25.3%；

   15 秒样本中 MAX(id) 增加约 3.6 万，保留行数不变。

  

  这里最重要的不是 640 TB/年这个数字人人都会遇到。它显然取决于使用强度、线程数、模型输出、工具调用、运行时长和平台。真正重要的是机制：

  
   保留数据很小，但写入 churn 很大。文件净增长不能代表 SSD 实际写入。

  

  这也是很多人误判的地方。看到主库只有几百 MB，会以为问题不大。但在 WAL 模式和 insert-prune 循环下，净增长和底层写入之间可以差很多。

  相关症状

  围绕 logs_2.sqlite 和 WAL，还有一串相关 issue：

  
   #22444：logs_2.sqlite-wal 增长到数百 GB，删除后空间仍不释放，因为 stale/suspended Codex TUI 进程仍持有已删除 WAL 的文件描述符；

   #28997：logs_2.sqlite-wal 在默认风格的本地使用中增长到几十 GB；

   #27741：logs_2.sqlite 变大后，桌面端启动可能因为 app-server SQLite pool timeout 失败；

   #24275：Codex Desktop 正常使用时 logs_2.sqlite / WAL 快速增长；

   #16886：另一个文本日志 ~/.codex/log/codex-tui.log 不轮转，这是相邻问题，但不是同一个 SQLite sink；

   #23787、#23863、#23917：涉及升级后 logs_2.sqlite 的 sqlx migration checksum、损坏或启动失败。

  

  最后这组迁移 issue 要谨慎理解。它们能说明 logs_2.sqlite 在升级路径上确实影响启动稳定性，但不能证明任何用户手动 trigger 一定会导致 checksum drift。sqlx 校验的是迁移记录和迁移 SQL，不是你额外创建了一个 trigger 就必然改 checksum。

  风险分层

  “用了 Codex 你的 SSD 一年必死”这个说法有传播力，但不能当成精确结论。

  SSD 的 TBW 是保修写入量指标，不是达到后立刻坏掉的硬阈值。不同容量、不同 NAND、不同控制器、不同预留空间、不同写放大，都会影响实际寿命。macOS 的 APFS、系统 swap、Spotlight、浏览器缓存、Docker、虚拟机也都在写盘。

  但也不建议轻描淡写成“只是一个日志文件”。原因有三点：

  
   这类写入缺少用户价值：用户运行 Codex，是为了执行任务，不是为了长期保存 websocket TRACE、inotify 噪声和遥测镜像。

   Mac 的风险权重更高：很多 Mac 的 SSD 焊在主板上。即便它不会明天坏，无意义的高频写入也比可替换硬盘更值得警惕。

   副作用不止寿命：大 WAL 会拖慢备份、同步、启动、迁移，还可能导致磁盘空间被 stale 进程占着不释放。

  

  更平衡的判断是：

  

  会不会烧同一小块

  通常不会。SSD 和机械硬盘不一样，主机反复写同一个文件，不等于 NAND 闪存中同一批存储单元被原地反复擦写。

  原因在于 SSD 控制器通过 FTL（Flash Translation Layer）维护逻辑地址和物理位置的映射。主机看到的是 LBA，控制器真正写的是 NAND 物理页。对现代 SSD 来说，更新数据通常是异地更新（out-of-place update）：新数据写到新的物理位置，映射表改到新位置，旧位置标记为无效，之后交给垃圾回收擦除。磨损均衡会尽量把这些擦写分摊到更多物理块上，而不是让某个文件路径或某段 LBA 长期对应同一批物理单元。

  所以，“反复写 logs_2.sqlite-wal” 更准确的风险不是烧穿同一小片，而是持续制造大量主机写入。主机写入越多，经过 SQLite、文件系统、FTL、垃圾回收和写放大后，NAND 实际写入也越多。

  这里也有两个现实放大因素：

  
   盘越满，可轮换的空闲块越少，垃圾回收越吃力，写放大越高；

   低端或老旧主控的静态磨损均衡可能较弱，热数据区短期内会比冷数据区更快磨损。

  

  因此，真正危险的组合不是“同一个文件名被反复写”，而是“高频写入、盘接近写满、长时间运行”叠加。保留足够空闲空间，本质上也是在给 SSD 留预留空间（over-provisioning）和磨损均衡余地。

  我更愿意把它定义为一个持久化边界 bug，而不是单纯的 SSD 焦虑：诊断日志可以存在，但它必须有清晰的级别、采样、脱敏、保留和大小边界。

  止血方案复盘

  触发器止血

  流传的命令是：

  sqlite3 ~/.codex/logs_2.sqlite \
"CREATE TRIGGER IF NOT EXISTS block_log_inserts
   BEFORE INSERT ON logs BEGIN SELECT RAISE(IGNORE); END;"

  它的行为很简单：每次应用想向 logs 表插入新行时，SQLite 触发器执行 RAISE(IGNORE)，这次插入被忽略，应用侧通常不会收到错误。

  它有效吗？对阻断 logs 表新增行很有效。

  如果目标只是立刻减少 logs_2.sqlite 的主要持久化写入，trigger 是三个偏方里最直接的。没有新增日志行，就不会持续写入那些日志 payload，也不会继续为这些新行更新索引和触发后续 prune。

  但要把它的边界说清楚：

  
   它不是真正的源码修复：Codex 仍然会生成日志事件、格式化字段、走 tracing layer、入队、尝试 INSERT。你只是让 SQLite 在最后一步忽略插入。

   它会让反馈日志变空：feedback_log_body 是反馈/报 bug 时的重要诊断来源。阻断后，反馈功能大概率仍能打开，但日志附件会缺失或价值下降。

   它不是 sqlx checksum drift 的直接原因：额外 trigger 不会自动进入 sqlx migration checksum。真正的问题是，后续版本如果重建 logs 表、替换库、迁移 schema，这个 trigger 可能被无声删除。升级后需要复查。

   它不回收旧文件体积：trigger 只止血。旧的 logs_2.sqlite 和 WAL 需要在 Codex 完全退出后再清理或 VACUUM。

  

  更准确的结论是：trigger 是止血钳，不是修复。它适合临时阻断写入，不适合作为长期运行策略。

  软链误区

  网上常见命令类似：

  mv ~/.codex/logs_2.sqlite ~/.codex/logs_2.sqlite.bak
ln -s /tmp/logs_2.sqlite ~/.codex/logs_2.sqlite

  这个思路是把 SQLite 库放到内存盘，让高频写入不落 SSD。

  问题在于，这条经验严重依赖平台。

  macOS 的 /tmp

  macOS 的 /tmp 通常是指向 /private/tmp 的路径，在 APFS 系统盘上，不是 tmpfs。你可以自己验证：

  readlink /tmp
df -h /tmp /
mount | grep -Ei 'tmpfs|ramdisk' || echo"无 tmpfs/ramdisk 挂载"

  

  在现代 macOS 上，df -h /tmp / 常见结果是：/tmp 落在 /System/Volumes/Data，/ 落在只读系统卷。它们可能显示成不同 APFS volume，但仍在同一个 APFS container 或同一块内置 SSD 上。只要 mount 没有显示 tmpfs 或 RAM disk，把日志软链到 /tmp 就只是从 SSD 的一个目录挪到另一个目录。对 SSD 写入没有实质帮助。

  macOS 真要内存盘，需要单独创建 RAM disk，例如用 hdiutil。但 RAM disk 易失、吃内存，内存压力大时还可能诱发 swap，最后仍可能回写 SSD。对普通用户并不优雅。

  如果只是临时验证，可以这样创建一个约 1 GiB 的 RAM disk：

  DISK=$(hdiutil attach -nomount ram://2097152 | awk 'NR==1 {print $1}')
diskutil erasevolume HFS+ CodexRAM "$DISK"
mkdir -p /Volumes/CodexRAM/codex-sqlite

  这里要先用 awk 取第一列。hdiutil attach -nomount 的输出可能带尾随空白，$(...) 只会去掉尾随换行，不会自动去掉空格或 tab；如果把未裁剪的 "$DISK" 传给 diskutil，可能出现找不到磁盘的错误。

  然后把 Codex 的 SQLite home 临时指过去：

  CODEX_SQLITE_HOME=/Volumes/CodexRAM/codex-sqlite codex

  注意：CODEX_SQLITE_HOME[8] 指向的是 Codex 的整个 SQLite home，不只是 logs_2.sqlite。把它放到 RAM disk 上，会让 state、logs、goals、memories[9] 等 SQLite 状态都变成易失数据。原始 rollout/session 文件通常仍在 CODEX_HOME，但索引和恢复链路可能错配。因此这个方案只适合临时验证或一次性空状态实验，不适合作为日常配置。

  用完后先退出 Codex，再卸载：

  hdiutil detach /Volumes/CodexRAM

  这里的 2097152 是 512 字节扇区数量，约等于 1 GiB。这个大小对临时验证通常够用，但不适合长期承载整个 SQLite home。RAM disk 重启会消失，空间占用的是内存；如果机器内存紧张，系统可能通过 swap 把压力转回 SSD。

  Linux 的 tmpfs

  有些发行版会把 /tmp 挂成 tmpfs，有些不会。先查：

  findmnt /tmp
findmnt /dev/shm

  /dev/shm 通常是 tmpfs，但容量有限，重启清空。你要接受诊断日志丢失。

  句柄陷阱

  #22444 的关键教训是：删除或移动 WAL 文件时，如果 Codex 进程仍持有文件描述符，空间不会立刻释放。du 可能看起来降了，df 却不降，因为旧 inode 还被进程占着。

  所以任何软链、移动、删除、VACUUM 前都要先停掉 Codex：

  pgrep -fl 'Codex|codex|app-server'
lsof -nP | grep -E '\.codex/.+logs_2\.sqlite'

  结论：软链到内存盘只是在特定平台和特定挂载条件下有效。macOS 上软链到 /tmp 基本没有保护 SSD 的意义。

  迁移介质

  这个方向比 /tmp 软链更诚实。Codex 本身支持配置 sqlite_home，也支持环境变量 CODEX_SQLITE_HOME。例如：

  # ~/.codex/config.toml
sqlite_home = "/Volumes/ExternalDisk/codex-sqlite"

  或者临时启动：

  CODEX_SQLITE_HOME=/Volumes/ExternalDisk/codex-sqlite codex

  这会把 Codex 的 SQLite 状态库整体迁到另一个目录，包括 logs DB，不只是 logs_2.sqlite。

  它的优点：

  
   不需要改 schema；

   不需要 trigger；

   比软链单个文件更符合 Codex 配置模型；

   如果外置盘或第二块盘不是内置 SSD，确实能减少内置 SSD 的写入。

  

  它的代价：

  
   只是换位置，不是减少日志量；

   外置盘断开、休眠或变慢会影响 Codex；

   HDD 对小块同步写、checkpoint、SQLite lock 更敏感；

   对 Mac 笔记本用户，长期挂一块外置盘并不现实。

  

  结论：sqlite_home 是比文件级软链更干净的迁移手段，但它仍然是搬运，不是治疗。

  看似开关

  下面这些设置能改变一部分行为，但关不掉真正的 SQLite 写入路径。

  RUST_LOG=warn

  值得试，但不能依赖。#17320 的核心就是 extension 已经设置了 RUST_LOG=warn，SQLite sink 仍然写 TRACE。本文核对的源码中 app-server / TUI 的 SQLite layer 也确实使用了独立的 Targets::new().with_default(Level::TRACE)。

  所以：

  RUST_LOG=warn codex

  可能减少 stderr 或部分普通日志，但不能保证停止 logs_2.sqlite 的 TRACE 写入。

  [feedback] enabled = false

  配置里确实有：

  [feedback]
enabled = false

  但这表示禁用反馈提交流程，不是禁用 SQLite log DB layer。源码中 feedback_enabled[10] 会被解析进配置，feedback processor[11] 会检查它，但 app-server / TUI 启动时仍会挂 log_db_layer。

  所以它不是这个写放大的完整开关。

  清理不等于限流

  这能回收当前体积，但不能阻止未来继续写：

  DELETEFROM logs WHERE ts < strftime('%s','now') -3*86400;
VACUUM;

  而且不要在 Codex 还开着库时乱跑。更安全的流程是：

  
   完整退出 Codex；

   备份 logs_2.sqlite*；

   再执行 checkpoint、delete、vacuum。

  

  这属于清理，不是 cap。真正的 cap 应该由应用在写入前或数据库维护策略里实现。

  处理路径

  1. 确认增速

  看文件大小：

  ls -lh ~/.codex/logs_2.sqlite*

  看级别分布：

  sqlite3 ~/.codex/logs_2.sqlite \
"SELECT level, COUNT(*) FROM logs GROUP BY level ORDER BY COUNT(*) DESC;"

  看最大来源：

  sqlite3 ~/.codex/logs_2.sqlite <<'SQL'
SELECT target, level, COUNT(*) AS n
FROM logs
GROUP BY target, level
ORDER BY n DESC
LIMIT 20;
SQL

  

  如果 TRACE 占大头，并且 codex_api::endpoint::responses_websocket、codex_api::sse::responses、codex_client::transport、log、codex_otel.* 出现在前列，就和相关 issue 的症状一致。

  2. 安全清理

  完整退出 Codex 后：

  pgrep -fl 'Codex|codex|app-server'
lsof -nP | grep -E '\.codex/.+logs_2\.sqlite'

  确认没有进程占用后：

  BACKUP="$HOME/.codex/logs-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP"
mv"$HOME/.codex"/logs_2.sqlite* "$BACKUP"/ 2>/dev/null

  不要删除整个 ~/.codex。那里面还有登录、配置、会话索引和其他状态。

  3. Mac 处理

  macOS 上推荐顺序是：

  
   先退出所有 Codex 进程；

   清理或备份 logs_2.sqlite*；

   如果只是空间问题，定期清理即可；

   如果是 SSD 写入焦虑，优先考虑外置盘上的 sqlite_home；

   如果你明确接受丢诊断，再考虑 trigger；

   不要以为 /tmp 是内存盘。

  

  4. 临时止血

  先退出 Codex，再执行：

  sqlite3 ~/.codex/logs_2.sqlite <<'SQL'
CREATE TRIGGER IF NOT EXISTS block_log_inserts
BEFORE INSERT ON logs
BEGIN
  SELECT RAISE(IGNORE);
END;
SQL

  回滚：

  sqlite3 ~/.codex/logs_2.sqlite \
"DROP TRIGGER IF EXISTS block_log_inserts;"

  加完后建议检查：

  sqlite3 ~/.codex/logs_2.sqlite \
"SELECT name FROM sqlite_master WHERE type='trigger';"

  再次强调：这是临时止血，会牺牲反馈日志。升级后也要确认 trigger 是否还在。

  5. 备份排除

  如果你同步 ~/.codex 或多个 profile 目录，至少排除 SQLite sidecar：

  --exclude='*.sqlite-wal'
--exclude='*.sqlite-shm'

  WAL 和 SHM 是运行时文件。把几十 GB 的 WAL 同步到另一台机器，多数情况下只是在复制问题。

  真正的修复点

  真正的修复不该让用户在 trigger、RAM disk、外置盘之间做选择。

  上游应该修的是持久化日志边界：

  
   SQLite log sink 不应默认全局 TRACE：持久化日志应该有比开发调试更严格的默认级别。

   持久化过滤应该明确且可见：启动时至少记录 effective DB log filter，让用户知道什么会落盘。

   websocket/SSE 原始 payload 不应默认落盘：更合理的是存 event kind、状态、耗时、字节数、错误摘要、token usage，而不是完整 payload。

   低价值依赖噪声应丢弃或采样：target=log、hyper_util、tokio-tungstenite internals、inotify spam、低层 OpenTelemetry SDK 事件不应持续持久化。

   codex_otel.log_only / codex_otel.trace_safe 需要重新评估：如果它们只是遥测镜像，就不该占据 feedback log 的大头。

   增加全局大小/WAL 上限：per-thread 或 per-process partition cap 不够。WAL 也需要可观测、可截断、可告警。

   提供明确 escape hatch：比如 sqlite_logs_enabled = false 或更细粒度的 sqlite_log_level = "warn"。这比用户自己写 trigger 安全。

  

  从当前源码形态看，这不是大重构才做得到的事。最小可行修复是收窄 app-server / TUI 挂 SQLite layer 时的默认 filter，并在 state/src/log_db.rs 写入前丢弃已知高频低价值 target。更完整的修复则要补上大小预算、payload 脱敏、WAL 维护和配置开关。

  结语：持久化必须有边界

  诊断日志本身不是坏东西。问题在于，一个面向用户机器的本地优先工具，把 TRACE、协议 payload、依赖库噪声和遥测镜像一起写进持久化 SQLite，再靠事后 prune 来控制“最终留下多少”。

  这违反了一个很基本的工程边界：调试信息可以很多，但默认持久化的信息必须少、稳、可解释、可控制。

  如果一次 50 token 的回复能让 MAX(id) 跳几千行，如果设置了 RUST_LOG=warn 仍然写 TRACE，如果文件看起来只涨了几百 MB 但底层持续写 WAL，那就不是用户太焦虑，而是日志系统的默认边界错了。

  止血可以靠 trigger、sqlite_home 迁移、清理 WAL。治病只能在 Codex 自己的 SQLite log sink 里做。

  参考 issues

  截至本文核对时（2026-06-22），下面提到的核心 issue 中 #17320、#28224、#22444、#24275、#27741、#28997 仍是 Open。

  
   #17320[12]: Excessive SQLite WAL writes during streaming due to TRACE logs ignoring RUST_LOG

   #28224[13]: Codex SQLite feedback logs can write ~640 TB/year and rapidly consume SSD endurance

   #22444[14]: logs_2.sqlite-wal grows indefinitely and remains allocated after deletion

   #28997[15]: logs_2.sqlite-wal grows without bound into tens of GB

   #27741[16]: Desktop launch can fail when logs_2.sqlite grows large

   #24275[17]: Codex Desktop rapidly grows logs_2.sqlite / WAL during normal active use

   #16886[18]: Codex tui logs keeps growing and not getting rotated

   #23787[19]: Recovery tool for Codex App 0.130 to 0.131 startup crash

   #23863[20]: Desktop App startup crash due to sqlx migration checksum mismatch on logs_2.sqlite

   #23917[21]: Upgrading to the latest version corrupted logs_2.sqlite and codex app would not restart

   xdifu/codex-repair[22]: Fix the "Codex cannot access its local database" crash on Codex Desktop after the 0.130 → 0.131 auto-update — without losing any conversations.

  

  References

  [1]

  app-server:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/app-server/src/lib.rs#L666-L669

  [2] 
   TUI:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/tui/src/lib.rs#L1231-L1234
[3] 
   state/src/log_db.rs:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/src/log_db.rs#L190-L201
[4] 
   logs migration:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/logs_migrations/0002_logs_feedback_log_body.sql#L49-L53
[5] 
   日志内容保留 10 天:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/src/runtime/logs.rs#L296-L302
[6] 
   每个 thread partition 限制约 10 MiB 或 1000 行:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/src/runtime.rs#L91-L98
[7] 
   PRAGMA wal_checkpoint(PASSIVE):https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/src/runtime/logs.rs#L303-L307
[8] 
   CODEX_SQLITE_HOME:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/core/src/config/mod.rs#L265-L276
[9] 
   state、logs、goals、memories:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/state/src/runtime.rs#L139-L147
[10] 
   feedback_enabled:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/core/src/config/mod.rs#L3911-L3915
[11] 
   feedback processor:https://github.com/openai/codex/blob/c03742ca0a78a8e54cd881032a2327363678b5aa/codex-rs/app-server/src/request_processors/feedback_processor.rs#L49-L52
[12] 
   #17320:https://github.com/openai/codex/issues/17320
[13] 
   #28224:https://github.com/openai/codex/issues/28224
[14] 
   #22444:https://github.com/openai/codex/issues/22444
[15] 
   #28997:https://github.com/openai/codex/issues/28997
[16] 
   #27741:https://github.com/openai/codex/issues/27741
[17] 
   #24275:https://github.com/openai/codex/issues/24275
[18] 
   #16886:https://github.com/openai/codex/issues/16886
[19] 
   #23787:https://github.com/openai/codex/issues/23787
[20] 
   #23863:https://github.com/openai/codex/issues/23863
[21] 
   #23917:https://github.com/openai/codex/issues/23917
[22] 
   xdifu/codex-repair:https://github.com/xdifu/codex-repair
