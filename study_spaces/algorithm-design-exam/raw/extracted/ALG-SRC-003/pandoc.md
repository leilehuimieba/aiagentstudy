**《算法分析与设计》期末试题及参考答案**

**二、复杂性分析**

1.  MERGESORT(low，high)

if low\<high；

then mid←(low，high)/2；

MERGESORT(low，mid)；

MERGESORT(mid+1，high)；

MERGE(low，mid，high)；

endif

end MERGESORT

答![](media/image1.png){width="5.7625in" height="2.05in"}

2.  procedure S1(P，W，M，X，n)

> i←1; a←0
>
> while i≤ n do
>
> if W(i)\>M then return endif
>
> a←a+i
>
> i←i+1 ;
>
> repeat
>
> end
>
> 解：![](media/image2.png){width="3.2493055555555554in"
> height="1.46875in"}
>
> 3.procedure PARTITION(m,p)
>
> Integer m,p,i;global A(m:p-1)
>
> v←A(m);i←m

loop

loop i←i+1 until A(i) ≥v repeat

loop p←p-1 until A(p) ≤v repeat

if i\<p

then call INTERCHANGE(A(i),A(p))

else exit

endif

repeat

A(m) ←A(p);A(p) ←v

End PARTITION

3解：、最多的查找次数是p-m+1次

4.procedure F1(n)

if n\<2 then return(1)

else return(F2(2,n,1,1))

endif

end F1

procedure F2(i,n,x,y)

if i≤n

then call F2(i+1,n,y,x+y)

endif

return(y)

end F2

4、解：F2（2，n,1,1）的时间复杂度为：

T(n)=O(n-2); 因为i≤n时要递归调用F2，一共是n-2次

当n＝1时F1(n)的时间为 O(1)

当n\>1时F1(n)的时间复杂度与F2(2,n,1,1)的时间复杂度相同即为为 O(n)

5.procedure MAX(A,n,j)

xmax←A(1);j←1

for i←2 to n do

if A(i)\>xmax then xmax←A(i); j←i;endif

repeat

end MAX

答案

5、

> xmax←A(1);j←1 时间为：O(1)

for i←2 to n do 循环最多n-1次

> 所以 总时间为:

T(n)=O(1)+ (n-1)O(1)= O(n)

6.procedure BINSRCH(A,n,x,j)

integer low,high,mid,j,n;

low←1;high←n

while low≤high do

mid←\|\_(low+high)/2\_\|

case

:x\<A(mid):high←mid-1

:x\>A(mid):low←mid+1

:else:j←mid; return

endcase

repeat

j←0

end BINSRCH

答案

6、log2n+1

**三、算法理解**

> 1、写出多段图最短路经动态规划算法求解下列实例的过程，并求出最优值。
>
> 各边的代价如下：
>
> C(1,2)=3， C(1,3)=5 ，C(1,4)=2
>
> C(2,6)=8 ，C(2,7)=4 ，C(3,5)=5 ，C(3,6)=4， C(4,5)=2，C(4,6)=1

C(5,8)=4， C(6,8)=5 ，C(7,8)=6

答案：

> 1、
>
> Cost(4,8)=0
>
> Cost(3,7)= C(7,8)+0=6 ，D\[5\]=8
>
> Cost(3,6)= C(6，8)+0=5, D\[6\]=8
>
> Cost(3,5)= C(5，8)+0=4 D\[7\]=8
>
> Cost(2,4)= min{C(4，6)+ Cost(3,6), C(4，5)+ Cost(3,5)}
>
> = min{1+ 5, 2+4}=6 D\[4\]=6
>
> Cost(2,3)= min{C(3，6)+ Cost(3,6) }
>
> = min{4+5}=9 D\[3\]=5
>
> Cost(2,2)= min{C(2，6)+ Cost(3,6), C(2，7)+ Cost(3,7)}
>
> = min{8+5, 4+6}=10 D\[2\]=7
>
> Cost(1,1)= min{C(1,2)+ Cost(2,2), C(1,3)+ Cost(2,3), C(1,4)+
> Cost(2,4)}
>
> = min{3+10, 5+9,2+6}= 8
>
> D\[1\]=4

1→4→6→8

2.  写出maxmin算法对下列实例中找最大数和最小数的过程。

数组 A=(48,12,61,3,5,19,32,7)

答案

2.  写出maxmin算法对下列实例中找最大数和最小数的过程。

数组 A=()

1、 48,12,61,3, 5,19,32,7

2、48,12 61,3 5,19 32,7

3、 48～61, 12～3 19～32，5～7

4、 61～32 3～5

5、 61 3

1.  给出5个数(3,6,9,1,7),M=13，用递归树描述sumofsub算法求和数=M的一个子集的过程。

    ![](media/image3.png){width="5.686805555555556in"
    height="2.6729166666666666in"}

2.  快速排序算法对下列实例排序，算法执行过程中，写出数组A第一次被分割的过程。

    A=(65,70,75,80,85,55,50,2)

    ![](media/image4.png){width="5.7625in"
    height="2.1458333333333335in"}

3.  归并排序算法对下列实例排序，写出算法执行过程。

A=(48,12,61,3,5,19,32,7)

> 5、

48,12,61,3 5,19,32,7

48,12 61,3 5,19 32,7

12,48 3,61 5,19 7,32

3, 12, 48, 61 5, 7, 19，32

3,5, 7,12，19，32，48,61

4.  写出图着色问题的回溯算法的判断X\[k\]是否合理的过程。

6、

i←0

while i\<k do

if G\[k,i\]=1 and X\[k\]= X\[i\] then

return false

i←i+1

repeat

if i= k then return true

5.  对于下图，写出图着色算法得出一种着色方案的过程。

> 7、
>
> K←1
>
> X\[1\] ←1 , 返回 true
>
> X\[2\]←1,返回false; X\[2\]←X\[2\]+1=2, 返回 true
>
> X\[3\]←1 ,返回false; X\[3\]←X\[3\]+1=2, 返回false;X\[3\]←X\[3\]+1=3,
> 返回 true
>
> X\[4\]←1, 返回false; X\[4\]←X\[4\]+1=2, 返回false;X\[4\]←X\[4\]+1=3,
> 返回 true
>
> 找到一个解 （1，2，3，3）

6.  写出第7题的状态空间树。

    ![](media/image5.png){width="2.895138888888889in"
    height="2.8180555555555555in"}

7.  写出归并排序算法对下列实例排序的过程。

> (6,2,9,3,5,1,8,7)
>
> 9、
>
> 调用第一层次 6,2,9,3 5,1,8,7 分成两个子问题
>
> 调用第二层次 6,2 9,3 5,1 8,7 分成四个子问题
>
> 调用第三层次 6 2 9 3 5 1 8 7 分成八个子问题
>
> 调用第四层次 只有一个元素返回上一层

第三层归并 2 ,6 3, 9 1,5 7,8 返回上一层

第二层归并 2 ,3,6, 9 1,5,7,8 返回上一层

第一层归并 1, 2 ,3, 5 ,6, 7, 8,9 排序结束，返回主函数

8.  写出用背包问题贪心算法解决下列实例的过程。

P=(18,12,4,1)

W=(12,10,8,3)

M=25

10、实例符合P(i)/W(i)≥P(i+1)/W(i+1)的顺序。

CU←25,X←0

W\[1\]\< CU: x\[1\]←1; CU←CU-W\[1\]=13;

W\[2\]\< CU: x\[2\]←1; CU←CU-W\[2\]=3;

W\[3\]\>CU: x\[3\]←CU/ W\[3\]=3/8;

实例的解为：（1，1，3/8，0）

11、有一个有序表为{1，3，9，12，32，41，45，62，75，77，82，95，100}，当使用二分查找值为82的结点时，经过多少次比较后查找成功并给出过程。

解 一共要要执行四次才能找到值为82的数。

12、使用prim算法构造出如下图G的一棵最小生成树。

dist(1,2)=6;dist(2,5)=3;dist(5,6)=6;dist(6,4)=2;dist(4,1)=5;

dist(1,3)=1;dist(2,3)=5;dist(3,4)=5;dist(3,6)=4;dist(5,3)=6

13、有如下函数说明

int f(int x,int y)

{

f=x Mod y +1;

}

已知a=10,b=4,c=5
则执行k=f(f(a+c,b),f(b,c))后，k的值是多少并写出详细过程。

K的值是5

14、McCathy函数定义如下：

当x\>100时 m(x)=x-10;

当x\<=100时 m(x)=m(m(x+11));

编写一个递归函数计算给定x的m(x)值。

int m(int x)

{

int y;

if(x\>100) return(x-100);

else

{

y=m(x+11);

return (m(y));

}

}

15、 设计一个算法在一个向量A中找出最大数和最小数的元素。

解

Void maxmin(A,n)

Vector A;

int n;

{

int max,min,i;

max=A\[0\];min=A\[0\];

for(i=0;i\<=n;i++)

if(A\[i\]\>max)max=A\[i\];

else if(A\[i\]\<min)min=A\[i\];

printf("max=%d,min=%d\\n",max,min);

}

**参考答案**

**三、算法理解**

12．使用普里姆算法构造出如下图G的一棵最小生成树。

dist(1,2)=6;dist(2,5)=3;dist(5,6)=6;dist(6,4)=2;dist(4,1)=5;

dist(1,3)=1;dist(2,3)=5;dist(3,4)=5;dist(3,6)=4;dist(5,3)=6

**四、设计算法**

1\. 1. 设有n项独立的作业{1,2,...,
n},由m台相同的机器加工处理。作业i所需要的处理时间为t~i~。约定：任何一项作业可在任何一台机器上处理，但未完工前不准中断处理；任何作业不能拆分更小的子作业。

多机调度问题要求给出一种调度方案，使所给的n个作业在尽可能短的时间内由m台机器处理完。设计算法，并讨论是否可获最优解。

解：对于处理机j，用S\[j\]
表示处理机j已有的作业数，用P\[j,k\]表示处理机j的第k个作业的序号 。

1）将作业按照t\[1\]≥t\[2\]≥......≥t\[n\]排序

2）S\[1:m\]清零 j←0 //从第一个处理机开始安排

3\) for i←1 to n do //安排n个作业

j←j mod m +1 //选下一个处理机

S\[j\]←S\[j\]+1;

P\[j,S\[j\]\]←i ；

Repeat

2.2. 设有n种面值为:

d~1~≥d~2~≥......≥d~n~的钱币，需要找零钱M，如何选择钱币d~k~，的数目X~k~，满足

d~1~×X~i~＋......d~n~×X~n~=M ，使得

X~i~＋......X~n~ 最小

请选择贪心策略，并设计贪心算法。

贪心原则：每次选择最大面值硬币。

CU←M;i←1;X←0 // X为解向量

While CU≠0 do

X\[i\]←CU div d\[i\] // X\[i\]为第i中硬币数

CU←CU-d\[i\]\*X\[i\]

i←i+1;

repeat

3、3. 有n个物品，已知n=7,
利润为P=(10,5,15,7,6,18,3)，重量W=(2,3,5,7,1,4,1)，背包容积M=15,物品只能选择全部装入背包或不装入背包，设计贪心算法，并讨论是否可获最优解。

定义结构体数组G，将物品编号、利润、重量作为一个结构体：例如G\[k\]={1,10,2}

求最优解，按利润/重量的递减序，有

{5,6,1,6} {1,10,2,5}{6,18,4,9/2} {3,15,5,3} {7,3,1,3}{2,5,3,5/3}
{4,7,7,1}

算法

procedure KNAPSACK(P，W，M，X，n)

//P(1：n)和W(1；n)分别含有按

**P(i)/W(i)≥P(i+1)/W(i+1)排序**的n件物品的效益值

和重量。M是背包的容量大小，而x(1：n)是解向量//

real P(1：n)，W(1：n)，X(1：n)，M，cu；

integer i，n；

X←0 //将解向量初始化为零//

cu←M //cu是背包剩余容量//

for i←1 to n do

if W(i)\>cu then exit endif

X(i) ←1

cu←cu-W(i)

repeat

end GREEDY-KNAPSACK

根据算法得出的解：

X=（1,1,1,1,1,0,0）获利润52， 而解

（1,1,1,1, 0, 1,0）可获利润54

因此贪心法不一定获得最优解。

4． 4. 设计只求一个哈密顿环的回溯算法。

Hamiltonian(n)

{k←1; x\[k\] ←0;

While k\>0 do

x\[k\] ← x\[k\]+1;

while B(k)=false and x\[k\]≤n do

x\[k\] ← x\[k\]+1; repeat

If x\[k\]≤n then

if k=n then {print x; return}

else {k← k+1; x\[k\]←0;} endif

else k← k-1

endif

repeat

end

procedure B(k)

{ G\[x\[k-1\],x\[k\] \]≠1 then return false;

for i←1 to k-1 do

if x\[i\]=x\[k\] then return false;endif

repeat

return true;

}

5．利用对称性设计算法，求n为偶数的皇后问题所有解。

**procedure** NQUEENS1(n)

a←0 //计数器清零

X(1)←0；k←1 //k是当前行；X(k)是当前列//

**While** k\>0 **do** //对所有的行执行以下语句//

1\) { X(k)←X(k)+1 //移到下一列//

**While** X(k)≤n **and not** PLACE(k) **do**

2\) X(k)←X(k)十l

**if** X(k)≤n

**then if** k=n /

**then**

**{print**(X)，a←a+1 //找到一个解计数器a加1//

if a=n/2 then return // 找到n/2个解算法结束

3\) **else {**k←k+1；X(k)←0；**}**

4\) **else** k←k－1 //回溯//

**　 }**

**end** NQUEENS
