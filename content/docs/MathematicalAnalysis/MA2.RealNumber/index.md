---
title: "MA 2. RealNumber"
date: 2024-12-15
tags: ["Docs","MA"]
math: mathjax
showWordCount: false
---
> Last Edit: 12/15/24

## Real Number 实数

### Rational Number 有理数

- 整数，有限位小数，无限循环小数，分数
- 只要是能被表达为
$$\frac{p}{q},p,q\in \mathbb z,q\neq 0$$
- 的数都叫做Rational Number
- 也就是说可以被任意两个Nature Number通过加减乘除所得到的数都被称为Rational Number（做除法的时候分母不能为零）

### Irrational Number 无理数

#### Pythagoras Theorem 毕达哥拉斯定理

- 在一个直角三角形中，直角边对面的斜边（最长边）的平方等于两个直角边的平方和

#### Contradiction

- 在当时并没有Irrational Number的定义，但是表示一个两个直角边长度为一的直角三角形的斜边的时候却出现了问题，即\\(1^2+1^2=x^2\\)，无法通过一个Rational Number，也就是两个Nature Number的任意四则运算求出这个x

#### Proof that sqrt 2 isn't Rational Number

- Proof By Contradiction
- 假设\\(\sqrt 2\\)是一个Rational Number，则有\\(2=(\frac{p}{q})^2\\)，其中p和q是互素的
- 即\\(p^2=2q^2\\)，已知\\(2q^2\\)为一个Even Number，则等号另一边的\\(p\\)也必为一个Even Number（Odd Number的平方为Odd Number）
- 既然p是一个Even Number，则他可以被2整除，即\\(p^2\\)可以被4整除，同理可以得到\\(2|q^2\\)
- 那既然p和q都是偶数，很明显他们不可能互素，Contradict，故假设不成立
- 于是证明了Irrational Number的存在

### Define Real Number

- 首先要知道的是，根号的本质是一个服务幂而创造出的代数运算，其能表达出的Irrational Number的个数几乎可以忽略不计
- 所以定义实数的第一步就是构造出所有Irrational Number，第二步则是定义全序列关系，第三步为定义代数运算，第四步研究拓扑结构（稠密性）

### Dedekind Cut

- 设数集的一个划分\\(\{\alpha,\beta \}\\)，其中
- \\(\alpha,\beta\neq \emptyset\\)，即两个划分必须为有元素
- 向下封闭：\\(\forall x,y\in k, x<y,y\in \alpha \Rightarrow x\in \alpha\\)
- \\(\alpha\\)中无最大元素：\\(\forall x\in \alpha,\exists y\in \alpha~ st.~y>x\\)
- 满足以上条件的Cut则称为k上的一个Dedekind Cut，记做\\(\alpha|\beta\\) ，其中\\(\alpha,\beta\\)分别称为Dedekind Cut的Lower Set和Upper Set
- 每一个Dedekind Cut都确定了一个Real Number，其为一个存在无限过程的集合，具体来说有对于一个Set，其无最大元素的定义便是一个无限的过程，所以即使Dedekind Cut的Lower Set是一个集合，其实际上表示的是一个Real Number
- 再次对于上面的\\(x^2=2\\)做分析，假设其正根为\\(x_0\\)，令
$$\alpha = \{a \in \mathbb{Q} : a < x_0\}~~~~~
\beta = \{a \in \mathbb{Q} : a > x_0\}$$
![[MA2.RealNumber.png]]

- 则集合\\(\alpha\\)便就是一个表达\\(\sqrt2\\)的方法

### Real Number Set Definition

- 有理数集\\(\mathbb Q\\)上的所有Dedekind Cut的Lower Set的Set称为Set of Real Numbers，记做\\(\mathbb R\\)
- 其中的每一个Dedekind Cut的Lower Set表示一个Real Number

### Sequence Relationship

- 定义了Real Number后，需要将他们排列，具体来说需要将由Dedekind Cut所确定的Lower Sets做排列，有
$$\alpha_1\leq\alpha_2=\alpha1\subseteq\alpha _2$$
- 但是左边是一个全序集，而右边是偏序集
- 证明右边是全序集可以通过向下封闭的性质，即
$$\forall \alpha_1\leq \alpha_2~\exists\forall x\in\alpha_1\Rightarrow x \in\alpha_2$$
- 则可以证明出Real Number Set\\(\mathbb R\\)是一个全序集

### Summation

- 通过两个Dedekind Cut相加定义出一个新的Dedekind Cut
$$\alpha+\beta=\{a+b,a\in\alpha,b\in\beta\}$$
- 现在需要证明这个定义Well-defined

#### Proof

- 只需证明\\(\alpha + \beta\\)是一个 **Dedekind Cut**的Lower Set，也就是证明其1.向下封闭，2.没有最大元素 
- (i) 显然\\(\alpha + \beta \neq \emptyset\\)。任取\\(c \in (\alpha + \beta)\\)，令\\(c = a + b\\)，其中\\(a \in \alpha, b \in \beta\\)。若\\(c' < c\\)，则存在\\(d > 0\\)满足\\(c' = c - d = (a + b) - d = (a - d) + b\\)，由于\\(a - d < a\\)，故\\(a - d \in \alpha\\)。这表明\\(c' \in (\alpha + \beta)\\)，于是可知\\(\alpha + \beta\\)向下封闭
- (ii) 由于\\(\alpha\\)和\\(\beta\\)中都没有最大元素，因此一定存在\\(a' \in \alpha, b' \in \beta\\)满足\\(a' > a, b' > b\\)，于是\\((a' + b') \in (\alpha + \beta)\\)且\\(a' + b' > a + b\\)，于是可知\\(\alpha + \beta\\)中也没有最大元素。
- 综上可述\\(\alpha+\beta\in \mathbb R\\)

### Law of Operation

#### 加法结合律

- 对任意的\\(\alpha, \beta, \gamma \in \mathbb{R}\\)，有\\((\alpha + \beta) + \gamma = \alpha + (\beta + \gamma)\\)

#### 加法交换律

- 对任意的\\(\alpha, \beta \in \mathbb{R}\\)，有\\(\alpha + \beta = \beta + \alpha\\)

#### 加法零元  

- 对于任意的\\(\alpha \in \mathbb{R}\\)，存在一个零元\\(0^*\\)使得\\(\alpha + 0^* = 0^* + \alpha = \alpha\\)

#### 加法负元

- 对于任意的\\(\alpha \in \mathbb{R}\\)，存在一个负元\\(\beta\\)使得\\(\alpha + \beta = \beta + \alpha = 0^*\\)


 # Completeness of Real Number Field 实数域的完备性

###  Dense 稠密

设S是一个集合，X是一个包含S的更大的空间。我们说S在X中稠密，如果对于X中任意的点x，在x的任意小的邻域中，总能找到至少一个属于S的点
$$\forall x \in X, \forall \epsilon > 0, \exists s \in S \ \text{st.} \ |s - x| < \epsilon$$

#### Real Number Field's Density 实数域的稠密性

- 对于任意𝛼,𝛽∈R,若𝛼< 𝛽,则一定存在𝛾∈R满足\\(\alpha < \gamma <\beta\\)

 ### Proof
 
- 令𝛾=(𝛼+𝛽)/2.由于𝛼 < 𝛽,故 
$$2𝛼 < 𝛼+𝛽 <2𝛽 ⇐⇒ 𝛼< \frac{𝛼+𝛽} {2} <𝛽 ⇐⇒ 𝛼<𝛾<\beta$$
### Dedekind Theorem In Rational Number Field 有理数的戴德金分割

有理数域\\(\mathbb Q\\)上的Dedekind Cut可能会出现Upper Set中无最小元素的情况.这说明有理数域存在空隙

#### ex. sqrt{2} 在 Q中的分割

考虑实数\\(\sqrt{2}\\)（它是无理数，不属于\\(\mathbb{Q}\\)），我们定义：

- \\(A = \{ q \in \mathbb{Q} \mid q^2 < 2 \}\\) （所有小于\\(\sqrt{2}\\) 的有理数）
- \\(B = \{ q \in \mathbb{Q} \mid q^2 > 2 \}\\) （所有大于\\(\sqrt{2}\\) 的有理数）

可以验证：

1. \\(A \cup B = \mathbb{Q}\\)且\\(A \cap B = \emptyset\\)
2. \\(a < b\\) 对于任意\\(a \in A, b \in B\\)

但是Upper Set B中**不存在最小元素**，因为对于任意\\(b \in B\\)，都可以找到一个更小的\\(b' \in B\\)

这说明在\\(\mathbb{Q}\\)中，\\(\sqrt{2}\\)这样的点无法被有理数表示，导致了“**空隙**”的存在。

### Dedekind Theorem in Real Number Field 实数的戴德金分割

- 对于实数域R上的任一Dedekind Cut \\(𝐴| 𝐵\\), Upper Set 𝐵中都有最小元素

#### Proof

简单来说，给定实数域上的一个Dedekind Cut(A|B)。

1. 若A有最大元，则这个最大元即属于B，因此B有最小元。
2. 若A无最大元，则A中可找出一列有理数向上递增逼近分割点。若该分割点存在于A中，则逼近过程能产生一个最大元与分割矛盾；若分割点不在A中，就会落在B中，从而成为B的最小元。

总而言之，无论A是否有最大元，B中总能找到一个最小元

### The limit principle 界

Dedekind Cut  𝐴 | 𝐵 中, Lower Set 𝐴的任一元素都小于𝐵中任一元素，从直观上看, 𝐴是有‘‘上界的”,而𝐵是有‘‘下界的”.

#### Bounded 有界的

- 设非空集合𝐸⊆R.若存在𝑀>0使得|𝑥|<𝑀 (∀𝑥∈𝐸),则称𝐸是有界的(bounded)

#### Supremum 上确界

集合E的一个数M被称为其上确界（supremum），如果满足以下两个条件

- M是E的上界 Upper bound：
$$\forall x \in E, \quad x \leq M$$
- M是所有上界中的最小值，也就是上确界 Supremum： 
- 对于任意\\(\varepsilon > 0\\)，都存在\\(x_\varepsilon \in E\\)，使得\\(M - \varepsilon < x_\varepsilon \leq M\\)

#### Infimum 下确界

集合E的一个数m被称为其**下确界（infimum）**，如果满足以下两个条件：

- m是E的下界（lower bound）：
$$\forall x \in E, \quad m \leq x$$
2. m是所有下界中的最大值： 对于任意\\(\varepsilon > 0\\)，都存在\\(x_\varepsilon \in E\\)，使得\\(m\leq x_\varepsilon < m + \varepsilon\\)

#### Existence of Supremum & Infimum 上，下确界的存在性

- 对于一个实数集的子集\\(E\subseteq\mathbb R\\)，其根据Real  Number的 Completeness一定存在确界

#### ex. Supremum & Infimum
$$E =\{ \frac{1}{n} : n \in \mathbb{N}^* \}$$
- 对于E来说，\\(supE=1,infE=0\\)

### Least-upper-bound property, LUB 最小上界性

**定义**：如果一个非空的实数集合S在实数集中有上界，那么S必定在实数集中有最小的上界（简称为**确界**）

- Dedekind Theorem和确界原理是等价的

### Heine-Borel Theorem

- 有限闭区间的任一开覆盖都存在一个有限子覆盖

#### Open Cover 开覆盖

- 设Set \\(E\subseteq \mathbb R\\)和一族开区间\\(\{I_\lambda:\lambda\in \Lambda \}\\)，\\(\Lambda\\)是一个指标集，若
$$E \subseteq \bigcup_{\lambda \in \Lambda} I_\lambda.$$
- 则\\(\{I_\lambda:\lambda\in \Lambda \}\\)是E的一个Open Cover，也就是一个开区间的集合的并集能够覆盖满整个集合E，记作\\(C_E\\)
- 若E有一个Open Cover \\(C_E'\subseteq C_E\\)，则称\\(C_E'\\)为\\(C_E\\)的Subcover 子覆盖
- 过这个Cover里只有有限个Open Set，则称他为Finite Subcover 有限子覆盖


## Set's Cardinality 集合的基数

### Cardinality 基数

- 对于一个Finite Set A来说，他的基数是一个可以数出来的数字，即可以在\\(\mathbb Z\\)中找到一个数表示他的Cardinality，计作cardA或是\\(|A|\\)
- 我们约定\\(card \emptyset =0\\)
- 同时也可以发现两个Card相同的Set之间一定存在一个Bijective
- 对于一个Infinite Set，即使无法直接数出他的Card，但可以通过Bijective的角度刻画

### Equivalency of Set 集合的对等

- 设集合A，B若存在一个A到B的双射 , 则称A与B对等 (equivalent), 记作A ∼ B

### Finite Set 有限集

- 设集合A. 若A= ∅ , 或存在\\(n∈ N^∗\\), 使得集合 \\(\{ 1 , 2 , · · · , n\}\\) ∼ A , 则称集合A为有限集 (finite set)
- Finite Set的任一Subset仍是一个Finite Set

### Equivalency of Integer Set and Nature Number Set 整数集和自然数集的对等

- 考虑以下问题，自然数集和整数集的Cardinality是否相等？
- 从直觉上看\\(\mathbb N \subset \mathbb Z\\)，看似自然数的总数比整数少，但并非如此
- 前面说明了，如果两个Set之间可以建立一个Bijective的关系，则说明两个Set是Equivalent的，现在把Integer Set的所有元素排成一列
$$0,1,-1,2,-2,3,-3,\cdots$$
- 通过以下函数建立\\(f:\mathbb N\rightarrow \mathbb Z\\)
$$f(n) = 
\begin{cases} 
-\frac{n}{2}, & \text{n is Even} \\
\frac{n+1}{2}, & \text{n is Odd}
\end{cases}$$
- 可以发现
$$n = 1 \to 0,n = 2 \to -n,n = 3 \to 1,n = 4 \to -2,n = 5 \to 2,n = 6 \to -3
$$
- 于是可知\\(\mathbb N\\) ~ \\(\mathbb Z\\)

### Countable Set 可数集

- 设Infinite Set A，若\\(A\\) ~ \\(\mathbb N\\)，集存在一个**A到N的Bijective Relationship**，则称A为**Countable 可数的**，这样的Set也被称为**Countable Set**
- Countable Set的Cardinality称为**Countable Cardinality 可数基数**，记做\\(\aleph_0\\)
> Aleph 阿列夫

### Rational Number Set is a Countable Set

- 同理只要将Rational Number通过\\(\frac{p}{q}\\)那样排成一排然后和\\(\mathbb N\\)建立Bijective Relationship就行
$$
\left[
\begin{array}{cccc}
\frac{1}{1} & \frac{1}{2} & \frac{1}{3} & \cdots \\
\frac{2}{1} & \frac{2}{2} & \frac{2}{3} & \cdots \\
\frac{3}{1} & \frac{3}{2} & \frac{3}{3} & \cdots \\
\vdots & \vdots & \vdots & \ddots
\end{array}
\right]
$$
- 具体排列方式不限，但可以知道Rational Number Set的Cardinality也同为\\(\aleph_0\\)

### Uncountable Set 不可数集

- 下面给出一个不可数集的例子，其实既然知道了有理数集是Infinite Countable Set，那Uncountable Set很明显就是Irrational Number或者的Subset了

#### ex. Interval \\([0,1)\\) is Uncountable Set
 
假设区间\\([0,1)\\)中的所有实数是可数的，那么我们可以将这些实数按序列排列如下：
$$x_1, x_2, x_3, \ldots$$
- 每一个Real Number \\(x_i\\)都可以表示为小数形式
$$\begin{align}
x_1 = 0.a_{11}a_{12}a_{13}a_{14} \cdots \\
x_2 = 0.a_{21}a_{22}a_{23}a_{24} \cdots \\
x_3 = 0.a_{31}a_{32}a_{33}a_{34} \cdots \\
\vdots
\end{align}
$$
- 假设前三个实数
$$
\begin{array}{c|cccc}
 & \text{第1位} & \text{第2位} & \text{第3位} & \text{第4位} \\
\hline
x_1 & 3 & 1 & 4 & 1 \\
x_2 & 5 & 9 & 2 & 6 \\
x_3 & 5 & 3 & 5 & 8 \\
\end{array}
$$
- 康托尔的对角线论证法要求我们构造一个新的实数y，其小数部分的每一位都与列表中第i个数\\(x_i\\)的第i位不同，通过这样的构造，y与列表中的每个数\\(x_i\\)至少在第i位上不同，也就是说前面的假设：我们可以将实数按序列排列成一个序列不成立，因为永远存在一个y不在列表中
- 这证明了\\([0,1)\\)的实数集合是不可数的
- 这种证明方法也叫做Cantor的Diagonal Process

### Real Number Set is Uncountable 实数集是不可数集

- 通过一个Bijective Relationship
$$f(x)=-cot(\pi x)$$
- 其Domain为\\((0,1)\\)，Range为\\(\mathbb R\\)，即f为\\((0,1)和\mathbb R\\)的一个Bijective Relationship
- 因此\\((0,1)\\) ~ \\(\mathbb R\\)
- 已知\\((0,1)\\)是一个Uncountable Set，即证\\(\mathbb R\\)也是Uncountable的

### Continuum 连续统

- 和Real Number Set等势的Set称为continuum 连续统
- Continuum的Cardinality为\\(\aleph_1\\)

### Continuum hypothesis 连续统假设

- 1874 年 Cantor 提出猜想 : 不存在基数介于\\(ℵ_0\\)和\\(ℵ_1\\)的集合 . 这就是著名的连续统假设




















