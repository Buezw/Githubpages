---
title: "LA 8. Diagonalization and Eigenvalues"
lang: en
date: 2024-11-25
tags: ["Docs","LA"]
math: mathjax
showWordCount: true
---
> Last Edit: 11/25/24

## Eigenvectors and Eigenvalues

- 考虑Linear Transformation为一种Function，输入x而输出\\(Ax\\)
- Eigenvector即对于指定的Vector x，其Ax平行于x，有
$$Ax=\lambda x$$
- 其中x为A的Eigenvector，\\(\lambda\\)为A的Eigenvalue
- 特征向量的定义要求\\(x \neq 0\\)

### Zero Eigenvalue

- 如果0为Matrix的Eigenvalue，则有
$$Ax=0x=0$$
- Eigenvalue 0所对应的Vector Span出了Matrix的Null Space
- 如果矩阵A为不可逆矩阵，则0是其特征值之一

### ex. Projection Matrix

- 对于Projection Matrix P，其Column Space中的任意Vector都会是一个Eigenvector

![[LA8.DiagonalizationandEigenvalues.png]]

- 因为当其投影到Subspace的时候并没有改变
- 因此x为Eigenvector，并且Eigenvalue为1
- 同时对于Orthogonal于Subspace的Vector，有\\(Px=0\\)，则这个x也是Eigenvector，其Eigenvalue为0

### ex. Permutation Matrix
<div>
$$A = \begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}$$
</div>

- 对于置换矩阵存在Eigenvector \\(x=[1,1]^T\\)，Eigenvalue为1
- 另一个Eigenvalue为\\(x=[-1,1]^T\\)，对应Eigenvalue为-1，\\(Ax=-x\\)

### Trace 迹

- \\(n\times n\\) 的Matrix存在n个Eigenvalue
- 并且它们的和，即为Trace，等于矩阵对角线上的元素之和
- 对于二阶矩阵，在已知一个特征值的条件下， 可以据此得到另一个特征值

## Solve Ax = lambdax

- 对于\\(Ax=\lambda x\\)存在两个未知数，下面讨论求解的办法
- Rewrite等式为\\((A-\lambda I)x=0\\)
- 如果系数矩阵\\(A - \lambda I\\)是**非奇异矩阵**（行列式不为零），那么方程组只有Trivial Solution \\(x=0\\)
- 而如果系数矩阵\\(A - \lambda I\\)是**奇异矩阵**（行列式为零），那么方程组可能有**非零解\\(x \neq 0\\)**
- 于是可以推出\\(det(A-\lambda I)=0\\)
- 在这个没有x的“特征方程”中，可以解得n个特征值，但是有可能方程有Repeated Root，则会得到重复的Eigenvalue
- 得到特征值之后，用消元法解\\(A-\lambda I\\)，这一矩阵零空间中的向量为矩阵 A的特征向量

### ex. 

- 对于Matirx 

<div> 
$$A= \begin{bmatrix}3 & 1 \\1 & 3\end{bmatrix}$$
</div>

<div>
$$\det (A-\lambda I) = \begin{vmatrix} 3-\lambda & 1 \\ 1 & 3-\lambda \end{vmatrix} = (3-\lambda)^2 - 1 = \lambda^2 - 6\lambda + 8$$
</div>

- 在一元二次方程中，6为Trace，8为Determinant
- 于是可以总结对于**二阶矩阵的Eigenvalue为该方程的解**

<div>
$$\lambda^2 - \text{trace}(A) \lambda + \det A = 0$$
</div>

- 对于上面的Matrix则有Eigenvalue = 4 & 2
<div>
$$A-4I = \begin{bmatrix} -1 & 1 \\ 1 & -1 \end{bmatrix}, \quad (A-4I)x_1 = 0, \quad x_1 = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$$
$$A-2I = \begin{bmatrix} 1 & 1 \\ 1 & 1 \end{bmatrix}, \quad (A-2I)x_2 = 0, \quad x_2 = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$
</div>

- 与前面的例子\\(A=\begin{bmatrix} 0 & 1 \\ 1 & 0 \end{bmatrix}\\)的特征值和特征向量相对比，可知两者为一组平移矩阵
 - 在对角元素上分别加3，改变了特征值但是没有改变特征向量
 <div>
 $$Ax = \lambda x, \quad \text{则有} (A+3I)x = \lambda x + 3x = (\lambda + 3)x$$
 </div>

- 所以当两个Matrix有相同的Eigenvectors的时候，他们是可以“相加”的
- 当然其中一个为Identity Matrix的情况除外

## Trace Equal to Eigenvalue Summation 矩阵的迹等于特征值之和

- 将\\(det(A-\lambda I)=0\\)展开会得到\\(\lambda\\)的n 阶多项式，多项式的解就是矩阵 A 的特征值
- 根据多项式根与系数的关系，解之和即特征值之和等于\\(\lambda^{n-1}\\)的系数
- 而行列式展开式中只有对角线的积这一项包含的\\(\lambda^{n-1}\\)（其它项最高是n-2次方），而其系数为矩阵A对角线元素之和即矩阵A的Trace，因此特征值之和与矩阵的迹相等

## Symmetry Matrix's Eigenvector Orthogonal 对称矩阵的特征向量正交

- \\(\lambda_1,\lambda_2\\)是对称矩阵的两个不同的特征值，对应的特征向量分别为x1和x2。

<div>
$$\text{则有 } A\mathbf{x}_1 = \lambda_1 \mathbf{x}_1, \text{ 左乘 } \mathbf{x}_2^\top \text{ 得 } \mathbf{x}_2^\top A\mathbf{x}_1 = \lambda_1 \mathbf{x}_2^\top \mathbf{x}_1$$
$$\mathbf{x}_2^\top A\mathbf{x}_1 = (\mathbf{A}^\top \mathbf{x}_2)^\top \mathbf{x}_1 = \lambda_2 \mathbf{x}_2^\top \mathbf{x}_1。\\
\text{因此有 } (\lambda_1 - \lambda_2) \mathbf{x}_2^\top \mathbf{x}_1 = 0$$
</div>

- 而两特征值不等，所以两特征向量正交

## Complex eigenvalues 复数特征值

<div>
$$Q = \begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} = \begin{bmatrix} \cos 90^\circ & -\sin 90^\circ \\ \sin 90^\circ & \cos 90^\circ \end{bmatrix}$$
</div>

- Q是一个是一个90度Rotation Matrix
- 从矩阵的Trace和Determinant的值可以得到\\(\lambda_1+\lambda_2=0,\lambda_1\lambda_2=1\\)
- 仅观察Matrix可以发现他的Eigenvector只能是Zero Vector，因为其他Vector乘以Rotation Matrix，其方向将会改变而，不可逆平行于原向量，通过原来的计算可得
<div>
$$\det (Q - \lambda I) = \begin{vmatrix} -\lambda & -1 \\ 1 & -\lambda \end{vmatrix} = \lambda^2 + 1 = 0$$
</div>

- 可以解得\\(\lambda_1=i,\lambda_2=-i\\)
- 如果一个矩阵具有复数特征值a+bi则，它的共轭复数a-bi也是矩阵的特征值
- **实数特征值让特征向量伸缩而虚数让其旋转**

####  Antisymmetric matrices 反对称矩阵

- 即满足\\(A^T=-A\\)的矩阵
- 对称矩阵永远具有实数的特征值，而，具有纯虚数的特征值

## Triangular matrices and repeated eigenvalues 三角阵和重特征值

- 对于一个Uppertriangular Matrix 
<div>
$$A = \begin{bmatrix}3 & 1 \\0 & 3\end{bmatrix}$$
</div>


<div>
$$\det (A - \lambda I) = \begin{vmatrix} 3-\lambda & 1 \\ 0 & 3-\lambda \end{vmatrix} = (3-\lambda)(3-\lambda) = 0
$$
</div>

- 即\\(\lambda_1=\lambda_2=3\\)
<div>
$$(A-\lambda I)x = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}x = 0, \quad \text{得到} \quad x_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$
</div>

 - 其并没有没有线性无关的x2，说明A是一个退化矩阵，对应相同的特征值，而特征向量短缺


## Diagonalization 对角化

- 如果矩阵A具有n个线性无关的特征向量，将它们作为列向量可以组成一个可逆方阵S，并且有
<div>
$$AS = A \begin{bmatrix} \mathbf{x}_1 & \mathbf{x}_2 & \cdots & \mathbf{x}_n \end{bmatrix} 
= \begin{bmatrix} \lambda_1 \mathbf{x}_1 & \lambda_2 \mathbf{x}_2 & \cdots & \lambda_n \mathbf{x}_n \end{bmatrix} 
= S \begin{bmatrix} 
\lambda_1 & 0 & \cdots & 0 \\ 
0 & \lambda_2 & \cdots & 0 \\ 
\vdots & \vdots & \ddots & \vdots \\ 
0 & 0 & \cdots & \lambda_n 
\end{bmatrix} = S D$$
</div>

- 根据上式可写出\\(AS=SD\Rightarrow S^{-1}AS=D\\)，这就叫Diagonalization
- 同理也有\\(A=SDS^{-1}\\)

### Power of A  矩阵的幂

- 特征值给矩阵的幂计算提供了方法。
<div>
$$\text{如果 } A\mathbf{x} = \lambda \mathbf{x}, \text{ 则有 } A^2\mathbf{x} = \lambda A\mathbf{x} = \lambda^2 \mathbf{x}。$$
</div>

- 这说明了Matrix \\(A\\)与\\(A^2\\)拥有相同的Eigenvector
<div>
$$A^2 = S D S^{-1} S D S^{-1} = S D^2 S^{-1}$$
</div>

- 同理可以推广到k-th power的情况，有\\(A^k = S D^k S^{-1}\\)
- 这说明\\(A^k\\)有着和A一样的特征向量，而特征值为\\(\lambda^k\\)
- 如果矩阵A具有n个线性无关的特征向量，并且特征值均满足\\(|\lambda_i|<1\\)，则k→∞时，Ak→0

### Repeated eigenvalues 重特征值

- **如果矩阵A没有重特征值，则其一定具有n个线性无关的特征向量**
- **如果矩阵A有重特征值，它有可能具有n个线性无关的特征向量，也可能没有**
#### Identity Matrix

- 比如单位阵的特征值为重特征值1，但是其具有n个线性无关的特征向量

#### UpperTriangular Matrix

- 参考上面的例子
- 对于一个Uppertriangular Matrix 
<div>
$$A = \begin{bmatrix}3 & 1 \\0 & 3\end{bmatrix}$$
</div>

<div>
$$\det (A - \lambda I) = \begin{vmatrix} 3-\lambda & 1 \\ 0 & 3-\lambda \end{vmatrix} = (3-\lambda)(3-\lambda) = 0$$
</div>

- 即\\(\lambda_1=\lambda_2=3\\)
<div>
$$(A-\lambda I)x = \begin{bmatrix} 0 & 1 \\ 0 & 0 \end{bmatrix}x = 0, \quad \text{得到} \quad x_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix}$$
</div>

- 其存在Repeated Eigenvalue所以可能没有n个Linearly Independent的Eigenvector

 # Difference equations 差分方程
 
- **差分方程**描述了**离散变量**之间的递推关系
- 简单来说，差分方程是用来研究一系列离散点上的函数值之间的关系
- 从给定的一个向量\\(u_0\\)出发，我们可以通过对前一项乘以矩阵A得到下一项的方式，得到一个向量序列：\\(u_{k+1}=Au_k\\)
- 这里的\\(u_k+1=Au_k\\)可以是一个一阶差分方程，而\\(u_k=A^ku_0\\)就是方程的解
- 其可以写出Eigenvector的Linear Combination
<div>
$$\mathbf{u}_0 = c_1 \mathbf{x}_1 + c_2 \mathbf{x}_2 + \cdots + c_n \mathbf{x}_n = S\mathbf{c}$$
$$A\mathbf{u}_0 = c_1 \lambda_1 \mathbf{x}_1 + c_2 \lambda_2 \mathbf{x}_2 + \cdots + c_n \lambda_n \mathbf{x}_n$$
$$\mathbf{u}_k = A^k \mathbf{u}_0 = c_1 \lambda_1^k \mathbf{x}_1 + c_2 \lambda_2^k \mathbf{x}_2 + \cdots + c_n \lambda_n^k \mathbf{x}_n = D^k S\mathbf{c}$$
</div>

### Fibonacci sequence 斐波那契数列

- 斐波那契数列为0,1,1,2,3,4,8,13……其通项公式为\\(F_{k+2}=F_{k+1}+F_k\\)
- 令
<div>
$$\mathbf{u}_k = \begin{bmatrix} F_{k+2} \\ F_{k+1} \end{bmatrix}$$
</div>

<div>
$$F_{k+2} = F_{k+1} + F_k, \quad F_{k+1} = F_{k+1} \\ 
\text{写成矩阵形式为 } \mathbf{u}_{k+1} = \begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix} \mathbf{u}_k$$
</div>

- 所以现在A就是\\(\begin{bmatrix} 1 & 1 \\ 1 & 0 \end{bmatrix}\\)，求解其Eigenvalues有
<div>
$$\det(A - \lambda I) = \begin{vmatrix} 1-\lambda & 1 \\ 1 & -\lambda \end{vmatrix} = \lambda^2 - \lambda - 1 = 0$$
</div>

- \\(\text{解得 } \lambda_1 = \frac{1 + \sqrt{5}}{2}, \quad \lambda_2 = \frac{1 - \sqrt{5}}{2}\\)，且\\(\mathbf{u}_k = A^k \mathbf{u}_0 = c_1 \lambda_1^k \mathbf{x}_1 + c_2 \lambda_2^k \mathbf{x}_2\\)
- 由于\\(\lambda_1\\)大于零，\\(\lambda_2\\)小于零，则在k趋于无线的时候，\\(\lambda_2^k\\)趋于零
- 从特征值可以求得对应的特征向量\\(\mathbf{x}_1 = \begin{bmatrix} \lambda_1 \\ 1 \end{bmatrix} \text{ 的和 } \mathbf{x}_2 = \begin{bmatrix} \lambda_2 \\ 1 \end{bmatrix}\\)
> 在因为是二阶方程，而且矩阵\\(A - \lambda I\\)是奇异矩阵，所以只要符合其中一个方程即可，立刻可以看出\\(\begin{bmatrix} \lambda_1 \\ 1 \end{bmatrix}\\)是解

<div>
$$\text{从 } \mathbf{u}_0 = \begin{bmatrix} F_1 \\ F_0 \end{bmatrix} = c_1 \mathbf{x}_1 + c_2 \mathbf{x}_2, \text{ 可以求得 } c_1 = -c_2 = \frac{1}{\sqrt{5}}$$$$
\begin{bmatrix} F_{100} \\ F_{99} \end{bmatrix} = A^{99} \begin{bmatrix} F_1 \\ F_0 \end{bmatrix} = 
\begin{bmatrix} \lambda_1 & \lambda_2 \\ 1 & 1 \end{bmatrix} 
\begin{bmatrix} \lambda_1^{99} & 0 \\ 0 & \lambda_2^{99} \end{bmatrix} 
\begin{bmatrix} c_1 \\ c_2 \end{bmatrix} =
\begin{bmatrix} c_1 \lambda_1^{100} + c_2 \lambda_2^{100} \\ c_1 \lambda_1^{99} + c_2 \lambda_2^{99} \end{bmatrix}. \\
\text{可知 } F_{100} \approx c_1 \lambda_1^{100}.
$$

</div>





