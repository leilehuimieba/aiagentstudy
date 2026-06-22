# DongSQL V1.2.0 Released: Deepening the Retail Database Kernel with Dual Leaps in Performance and Stability

- BestBlogs URL: https://www.bestblogs.dev/article/bb9fd95c
- Original publisher URL: https://mp.weixin.qq.com/s?__biz=MzU1MzE2NzIzMg==&mid=2247502298&idx=1&sn=a0266d36073457f2716c803cddbf4a09
- Source: BestBlogs / 京东技术
- Publish time: 2026-05-27 19:27:00
- Capture route: article discovered from logged-in Chrome/OpenCLI profile `qmvqcrb8` latest article feed page 4; page/content captured from BestBlogs resource APIs
- Extracted chars: 12226

---

继京东自研电商数据库内核DongSQL V1.1.0在2025年9月发布后，京东零售数据库团队持续深耕数据库内核技术，经过半年的打磨，正式推出DongSQL V1.2.0版本。新版本在热点行更新优化、主从复制性能、执行计划缓存、带量压测支持、海量表启动速度、SIMD加速等多个维度实现了重大突破，为零售高性能数据库需求提供了更强大的内核支撑能力。

  
   
    本文将深度解析DongSQL V1.2.0的核心技术升级，以及在各种场景下的性能表现。

    

    图1：DongSQL V1.2.0架构总览（★标注为V1.2.0新增特性）

    
     
      
       
        

        一、组提交性能优化

        

       

      

     

     1.1 组提交单播通知

     ▶︎ 优化背景：在DongSQL组提交过程中，follower线程需要等待leader完成binlog刷盘后才能继续执行。传统方式使用单一条件变量（COND_done）广播唤醒所有等待的follower线程，当并发线程数较多时，广播唤醒会导致严重的锁竞争，成为性能瓶颈。

     ▶︎ 技术方案：DongSQL V1.2.0为每个线程分配独立的条件变量（THD::COND_wakeup_ready），将广播唤醒改为逐个单播唤醒。leader线程完成刷盘后，遍历follower队列逐个唤醒，大幅减少对共享条件变量的锁竞争。

     ▶︎ 核心优势：

     
      
       适用于所有开启主从复制的场景

      

      
       每个线程独立等待，避免广播唤醒的惊群效应

      

      
       高并发写入场景效果显著，低并发场景性能持平

      

     

     ▶︎ 测试环境：16C32G，sysbench 16张表每张1000万行

     ▶︎ 性能测试数据：

     

     oltp_insert详细数据：
    

    

    oltp_update_non_index详细数据：

    

    oltp_delete详细数据：

    

   

   

   

   -- 启用组提交单播通知（默认开启）
SET GLOBAL binlog_group_commit_unicast_mode = ON;

   

   
    

    
     图2：组提交单播通知性能对比（开启单播通知后，高并发写入场景性能显著提升）

    

    
     
      
       
        
         

         二、半同步复制性能优化

         

        

       

      

     

    

    
     
      
       
        
         
          
           
            ▶︎ 在刷盘后更新binlog end position：优化binlog位点更新时机，在刷盘完成后立即更新end position，减少从库等待延迟。

            ▶︎ ACK时刷新中继日志：半同步复制在收到从库ACK时立即刷新中继日志，确保数据一致性同时优化复制性能。

            ▶︎ 事务侧和日志侧双重优化：从中继日志侧和事务侧两个维度进行优化，全面提升复制效率。

            ▶︎ 性能测试数据：

            基于sysbench oltp_write_only场景测试（20张表，每张1000万行，主从半同步架构）：

            

            DongSQL 8.0 性能提升：
           

           

          

         

        

        DongSQL 5.7 性能提升：

        

       

      

     

     

     

     -- 相关系统变量
rpl_update_binlog_end_pos_after_flush = ON  -- 主库生效
rpl_semi_sync_flush_relay_log_on_ack = ON   -- 从库生效

     

     
      

      图3：半同步复制优化性能对比（低并发场景显著提升，8.0 最高提升25%）
      
       
        
         
          
           

           三、执行计划缓存

           

          

         

        

       

      

      3.1 功能概述

      ▶︎ 技术痛点：之前版本DongSQL每次执行SQL语句时都需要重新生成执行计划，对于频繁执行的相同SQL，重复生成执行计划会消耗大量CPU资源。

      ▶︎ 解决方案：DongSQL V1.2.0引入执行计划缓存（Plan Cache）功能，缓存SELECT语句的执行计划，避免重复生成执行计划，显著提升查询性能。

     

     

     

     -- 开启执行计划缓存
SET GLOBAL plan_cache_enabled = ON;
-- 查看缓存状态
SHOW STATUS LIKE 'plan_cache%';

     

     
      3.2 性能提升

      ▶︎ 测试场景：基于sysbench标准测试（8C16G，10张表每张100万行），对比开启和关闭执行计划缓存的性能差异。

      ▶︎ 性能测试数据：

      

      select_random_ranges 详细数据：
     

     

     select_random_points 详细数据：

     

     ▶︎ 最佳实践：执行计划缓存特别适用于以下场景：

     
      
       频繁执行相同SQL模式的查询

      

      
       OLTP类型的高并发短查询

      

      
       预编译语句和参数化查询

      

     

     

     图4：执行计划缓存开启前后QPS对比（select_random_ranges与select_random_points场景）

    

   

   
    
     
      
       

       四、单点查询优化增强

       

      

     

    

   

  

  4.1 功能扩展

  ▶︎ V1.1.0回顾：DongSQL V1.1.0首次引入单点查询bypass功能，针对主键等值查询绕过部分SQL层处理逻辑，直接访问存储引擎。

  ▶︎ V1.2.0增强：新版本大幅扩展了单点查询优化的支持范围：

  
   
    索引类型扩展：新增支持唯一索引（Unique Index）

   

   
    数据类型扩展：新增支持VARCHAR、CHAR类型

   

  

  

  

  -- 支持主键查询优化
SELECT * FROM orders WHERE order_id = 1001;  -- 主键INT类型
-- 支持唯一索引查询优化
SELECT * FROM users WHERE email = 'user@example.com';  -- 唯一索引VARCHAR类型
-- 支持CHAR类型
SELECT * FROM products WHERE product_code = 'ABC123';  -- 唯一索引CHAR类型

  

  ▶︎ 注意事项：

  
   
    应用条件：单表主键/唯一索引查询

   

  

  4.2 性能提升

  ▶︎ 测试环境：8C16G，16张表每张100万行，sysbench oltp_point_select场景

  DongSQL 8.0 性能测试数据：

  

  DongSQL 5.7 性能测试数据：

  

  整型主键查询详细数据（DongSQL 8.0）：

  

  

  图5：单点查询优化QPS对比（多维度性能提升汇总）

  
   
    
     
      
       

       五、海量表极速启动

       

      

     

    

   

   5.1 技术痛点

   ▶︎ 问题背景：DongSQL在启动时需要扫描所有表空间文件来获取space id信息，传统方式是读取每个文件的第一个页。当实例中存在大量表（数十万甚至百万级别）时，启动时间会显著延长。

   ▶︎ 典型场景：DongDAL的分库分表架构，单实例可能包含数十万张表，启动时间可达数十秒甚至分钟级别。

   5.2 解决方案

   ▶︎ 技术创新：DongSQL V1.2.0使用文件扩展属性（xattr）保存表空间文件的space id信息，启动时直接从文件属性读取，无需解析每个文件的第一个页。

  

  

  

  -- 系统变量
innodb_fast_initial_fil_scan = ON  -- 默认开启
-- 查看文件的xattr属性
getfattr ./t1.ibd -n user.dongsql.space_id

  

  
   ▶︎ 技术特点：

   
    
     自动写入xattr：创建表时自动写入space id到文件扩展属性

    

    
     兼容性保证：旧版本升级后首次启动会自动补全xattr

    

    
     安全机制：检测到xattr冲突或错误时自动修复

    

    
     动态开关：支持运行时动态开启/关闭

    

   

   5.3 性能突破

   ▶︎ 测试环境：8C16G128G DongSQL实例

   表空间扫描时间对比：

   

   整体启动时间对比：
  

  

  ▶︎ 业务价值：

  
   
    大幅缩短故障恢复时间，提升系统可用性

   

   
    加速容器化部署和弹性扩容场景

   

   
    特别适用于分库分表架构下的海量表实例

   

  

  

  图6：表空间扫描与启动时间对比（20万/100万张表场景）

  
   
    
     
      
       

       六、SIMD性能优化

       

      

     

    

   

  

  6.1 SQL摘要SIMD加速

  ▶︎ 技术背景：SQL摘要（Digest Hash）是数据库性能分析和监控的核心功能，用于识别相同模式的SQL语句。在高并发场景下，SQL摘要计算成为性能瓶颈之一。尤其是之前版本发布的限流功能，也高度依赖SQL摘要计算。

  ▶︎ AVX2指令集优化：DongSQL V1.2.0使用AVX2指令集优化DIGEST_HASH_TO_STRING函数，利用SIMD（单指令多数据）并行计算能力，显著提升SQL摘要转换性能。

  

  

  -- 系统变量（默认开启）
enable_digest_hash_to_string_avx2 = ON

  

  6.2 性能测试数据

  ▶︎ 测试环境：8C 16G，DongSQL 8.0，16张表每张100万行

  ▶︎ 测试场景对比：

  

  详细数据对比（oltp_point_select场景）：

  

  ▶︎ 适用条件：CPU需支持AVX2指令集（Intel Haswell及以后、AMD Excavator及以后）

  

  图7：AVX2指令集优化性能对比（oltp_point_select场景详细数据与多场景对比）

  
   
    
     
      
       

       七、Statement Outline（5.7版本）

       

      

     

    

   

  

  7.1 功能移植

  ▶︎ 背景：DongSQL V1.1.0在8.0版本引入了Statement Outline功能，用于固化SQL执行计划。为满足存量业务需求，V1.2.0将该功能移植到DongSQL 5.7版本。

  ▶︎ 核心能力：

  
   
    执行计划固化：绑定特定SQL到固定执行计划

   

   
    Hint注入：动态为SQL添加优化提示

   

   
    应急干预：快速解决线上SQL性能问题

   

  

  

  

  -- 为特定SQL添加索引提示
CALL dbms_outln.add_index_outline(
  'ecommerce_db', '', 1, 
  'USE INDEX', 'idx_status', '', 
  'SELECT * FROM orders WHERE status = "PAID"'
);
-- 为问题SQL添加限流Hint
CALL dbms_outln.add_optimizer_outline(
  'ecommerce_db', '', 1, 
  '/*+ ccl_queue_digest(5) */', 
  'SELECT * FROM hot_products WHERE status = 1'
);

  

  7.2 应用场景

  ▶︎ 执行计划不稳定：防止因数据变化、统计信息更新导致的执行计划劣化

  ▶︎ 应急限流：突发流量场景下快速对问题SQL进行限流

  ▶︎ 性能基线保护：为核心SQL绑定最优执行计划，确保性能稳定

  
   
    
     
      
       

       八、热点行更新优化

       

      

     

    

   

  

  8.1 功能背景

  ▶︎ 业务痛点：在余额扣减、库存秒杀、高并发发号器等典型业务场景中，短时间内会出现针对同一数据行的海量更新操作，即热点行更新问题。海量并发的单行UPDATE语句同时争夺同一行数据的修改权限，导致数据库内部产生大量锁等待与锁竞争。

  ▶︎ 核心瓶颈：

  
   
    行锁冲突：UPDATE遵循两阶段加锁协议，同一时间只有一个事务能更新某一行，其他事务需串行等待

   

   
    半同步复制延迟：事务提交阶段必须等待备库ACK响应后才能释放行级排他锁(X锁)，网络延迟进一步延长锁持有时间

   

   
    B+树索引高频遍历：每次查找行数据需从根节点自顶向下遍历B+树，单表数据量越大耗时越长

   

   
    死锁检测开销：热点行更新场景下锁等待关系图急剧膨胀，死锁检测消耗大量CPU，DongSQL 5.7中每次加锁失败都需检测死锁并持全局锁

   

  

  ▶︎ 传统方案局限：此前DongSQL第一版优化通过Hint排队限流+快速提交，虽能减少死锁检测开销，但未改变UPDATE串行执行的本质。在半同步复制环境下，单热点行理论TPS上限仅约500-1000，无法满足高并发业务需求。

  8.2 技术方案

  ▶︎ 核心思路：摒弃"串行等锁"传统思路，引入SQL层缓存的更新批量合并机制，从根本上打破UPDATE串行执行和网络延迟的物理瓶颈。

  ▶︎ 更新批量合并机制：

  
   
    SQL层行缓存：在SQL层维护InnoDB行数据完整缓存，配备互斥锁保障并发安全

   

   
    双更新单元：每行数据配备两个交替执行的更新单元，确保同一时间只有一个单元持有行级排他锁(X锁)

   

   
    Leader-Follower模式：

   

  

  
   
    Leader线程进入InnoDB获取X锁，完成数据更新后写入SQL层缓存，等待收集Follower

   

   
    Follower线程直接从SQL层缓存读取数据、执行更新、写回缓存，无需进入InnoDB

   

   
    Leader统一处理Redo Log与Binlog落盘，完成后唤醒所有Follower

   

  

  ▶︎ 关键优化点：

  
   
    减少B+树遍历：仅Leader线程需遍历B+树，Follower直接从缓存获取数据

   

   
    减少死锁检测：更新合并大幅降低并发挂起线程数量，缩减锁等待关系图规模

   

   
    平摊网络延迟：单次半同步复制ACK被整个更新单元共享，降低每条UPDATE平均等待时间

   

   
    Crash Recovery安全：通过Binlog完整性标记机制，将更新单元绑定为逻辑整体，确保异常重启后主备数据一致

   

  

  

  

  -- 使用热点行更新（必须包含 COMMIT_ON_SUCCESS Hint）
UPDATE /*+ COMMIT_ON_SUCCESS */ t1 SET val = val + 1 WHERE id = 1;
-- 系统变量
SET GLOBAL hotspot = ON;                          -- 开启热点行更新
SET GLOBAL hotspot_for_autocommit = ON;           -- 对autocommit模式的UPDATE也启用
SET GLOBAL hotspot_for_trigger = ON;              -- 允许有UPDATE Trigger的表启用
SET GLOBAL hotspot_update_max_wait_time = 5000000; -- Leader等待Follower的最大时间(微秒)

  

  8.3 性能测试数据

  ▶︎ 测试环境：8C 16G，DongSQL 8.0，单表10条数据，针对id=1的行做热点更新

  ▶︎ 测试SQL：

  

  

  UPDATE /*+ COMMIT_ON_SUCCESS */ sbtest1 SET k = k + 1 WHERE id = 1;

  

  热点行更新性能对比：

  

  ▶︎ 测试结论：

  
   
    低并发场景（≤2线程）：开启hotspot后性能下降约10%-30%，因合并机制引入额外开销

   

   
    高并发场景（≥4线程）：性能显著提升，128线程达到峰值34,127 TPS，相比基线提升约9倍

   

   
    开启hotspot后，高并发下平均延迟从72.69ms降至3.78ms，降低95%

   

   
    峰值性能后（128+线程），因CPU饱和，TPS略有回落但维持3万+

   

  

  ▶︎ 最佳实践：

  
   
    适用于高并发热点行更新场景（库存扣减、余额更新、发号器等）

   

   
    低并发场景不建议启用，可能引入额外开销

   

   
    必须配合/*+ COMMIT_ON_SUCCESS */ Hint使用

   

   
    确保满足使用限制条件（主键/唯一索引等值查询、非分区表等）

   

  

  

  图8：热点行更新开启前后TPS对比（高并发下性能提升显著，128线程峰值达34,127 TPS）

  
   
    
     
      
       

       九、带量压测支持

       

      

     

    

   

  

  9.1 功能背景

  ▶︎ 业务痛点：在业务侧原有的压测流程中，需要新建一个压测实例，并把所有数据复制一份到新建的压测实例中，所有压测流量接入到独立的压测实例。为了降本增效，业务侧推进带量压测项目——直接在原实例上新建压测表（以_bak_bak为后缀），压测流量打到压测表上，业务SQL仍操作原表。

  ▶︎ 核心问题：由于压测流量巨大，而压测期间业务的普通用户SQL量较少，数据库会被压测SQL大量占用CPU时间片，导致普通用户SQL出现超时、饿死或执行延迟过高的问题。

  ▶︎ 解决方案：DongSQL V1.2.0在线程池中新增低优先级队列，通过DONGSQL_LOW_PRIO Hint标识压测SQL，将其路由到低优先级队列执行，业务SQL保持普通优先级，确保业务SQL优先得到执行。

  9.2 技术实现

  ▶︎ 架构设计：带量压测的实现由三个模块组成：

  
   
    自动开启模块：每次带有压测Hint的SQL进入DongSQL时，在执行期间识别到Hint后自动打开流量检测开关

   

   
    流量检测模块：线程池检测到流量检测开关打开后，在SQL任务进入线程池任务队列之前，通过MSG_PEEK技术预读网络包前N个字节，识别SQL是否包含压测Hint，若包含则放入低优先级队列

   

   
    自动关闭模块：后台监控线程周期性检测，当检测到当前不在压测状态时，自动关闭流量检测开关，降低流量检测对非压测期间数据库性能的影响

   

  

  ▶︎ 核心创新：

  
   
    MSG_PEEK预读技术：在网络包阶段（尚未解析SQL）即可提前获取SQL前缀，不影响后续网络包的正常处理

   

   
    自动开关机制：压测流量进来时第一时间开启检测，压测流量消失后30秒内自动关闭检测，确保非压测期间零性能开销

   

  

  

  

  -- 压测SQL示例（带有DONGSQL_LOW_PRIO Hint的SQL会被放入低优先级队列）
SELECT /*+ DONGSQL_LOW_PRIO */ id, name FROM user WHERE age > 18;
UPDATE /*+ DONGSQL_LOW_PRIO */ user SET age = 21 WHERE id = 1;
-- 业务正常SQL（不带Hint，保持普通优先级，优先执行）
SELECT id, name FROM user WHERE age > 18;
UPDATE user SET age = 21 WHERE id = 1;

  

  ▶︎ 相关系统变量：

  
   
    enable_high_volume_testing：带量压测功能开关（默认ON）

   

   
    load_testing_disable_cycle_period：自动关闭检测的周期间隔（默认30秒）

   

  

  9.3 性能测试数据

  ▶︎ 测试环境：8C 16G，DongSQL 8.0开启线程池，sysbench 16张表每张100万行，oltp_read_write场景

  ▶︎ 测试方式：固定用户流量并发数，逐步增加压测流量并发数（32-512），对比开启/关闭低优先级Hint时用户流量的TPS和延迟表现。

  用户并发数=8，压测并发数递增：

  

  用户并发数=32，压测并发数递增：

  

  

  图9：带量压测功能性能对比（开启LOW_PRIO后用户流量TPS保持稳定，512并发下提升9~11倍）

  ▶︎ 测试结论：

  
   
    压测并发越高，用户流量TPS提升幅度和延迟降低幅度越显著

   

   
    512并发压测场景下，用户流量TPS提升高达911倍，平均延迟降低90%，tp99延迟降低66～71%

   

   
    开启功能后，无论压测流量多大，用户流量TPS和延迟始终保持稳定

   

  

  ▶︎ 最佳实践：

  
   
    压测时为所有压测SQL添加/*+ DONGSQL_LOW_PRIO */ Hint

   

   
    需开启线程池功能（thread_handling=pool-of-threads）

   

   
    功能默认开启，无需额外配置

   

  

  
   
    
     
      
       

       十、其他重要优化

       

      

     

    

   

  

  10.1 监控表增强

  ▶︎ 新增监控表：performance_schema.dongsql_statement_summary

  ▶︎ 采集指标：SQL执行全链路的各项性能指标，包括解析时间、优化时间、执行时间、锁等待时间等。

  ▶︎ 门控参数：dongsql_query_time，支持通过门控参数控制是否写入监控数据。

  

  

  -- 查看SQL执行全链路指标
SELECT * FROM performance_schema.dongsql_statement_summary 
WHERE digest_text LIKE '%orders%' 
ORDER BY timer_wait DESC LIMIT 10;
-- 设置门控参数
SET GLOBAL dongsql_query_time = 0.1;  -- 只记录执行时间超过100ms的SQL

  

  10.2 Jemalloc Profiling

  ▶︎ 功能描述：支持jemalloc性能分析功能，添加malloc_stats_print函数用于内存分析。

  ▶︎ 应用场景：内存泄漏排查、内存使用优化、性能调优。

  10.3 fdatasync优化

  ▶︎ 技术方案：使用fdatasync替代fsync加速文件系统访问，减少不必要的元数据刷盘。

  ▶︎ 性能提升：sysbench write_only场景下提升5%，延迟降低5%。

  
   
    
     
      
       

       十一、性能基准测试汇总

       

      

     

    

   

  

  11.1 新特性性能提升汇总

  

  11.2 版本整体性能对比

  ▶︎ 测试环境：一主一从半同步架构，16C32G，sysbench 16张表每张100万行

  DongSQL 8.0版本对比（V1.2.0 vs V1.1.2）

  

  oltp_insert详细对比：

  

  DongSQL 5.7版本对比（V1.2.0 vs V1.1.4）

  

  ▶︎ 性能提升分析：

  DongSQL V1.2.0相比V1.1.x版本，在所有测试场景均有显著提升：

  
   
    写入密集型场景受益于组提交单播通知和半同步复制优化，性能提升最为显著

   

   
    读取密集型场景受益于单点查询优化和SIMD加速

   

   
    混合读写场景综合各项优化，整体性能提升约40%

   

  

  

  图10：版本性能提升汇总（V1.2.0相比V1.1.x版本各测试场景提升幅度）

  注：1.2.0 版本基准性能测试基于常规sysbench场景，热点行优化及带量压测功能需结合特定hint实现，因此基准测试数据不包含这两个场景性能优化带来的性能提升

  
   
    
     
      
       

       十二、未来规划

       

      

     

    

   

  

  1.持续性能优化：深入优化核心执行引擎，持续提升OLTP场景性能

  2.智能运维增强：完善监控诊断能力，提供更丰富的性能分析工具

  3.云原生演进：推进存算分离架构，打造高性能低成本云原生数据库

  
   
    
     
      
       

       十三、结语

       

      

     

    

   

   从V1.1.0到V1.2.0，DongSQL在热点行更新优化、主从复制性能、执行计划缓存、带量压测支持、海量表启动、SIMD加速等多个维度实现了重大突破。这些优化不仅提升了系统性能，更重要的是为京东零售场景提供了更坚实的技术底座。
  

  京东零售数据库团队始终以“业务价值驱动技术创新”为核心理念，持续深耕数据库内核技术。未来，我们将继续围绕电商场景的核心需求，打造更强大、更稳定、更高效的数据库产品。
