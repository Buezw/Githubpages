---
title: "Calculus A1. Polynomial Interpolation"
lang: en
date: 2025-01-13
tags: ["Docs","Cal"]
math: mathjax
showWordCount: true
---
> Last Edit: 1/13/25

# Polynomial Interpolation

- 如果想要找一个Polynomial，其穿过两个Point，很简单的做法就是建立$P(x)=ax+b$的多项式
- 但是如果问题变成了三个点甚至更多，问题的复杂度就会上升很多，于是需要考虑另一种做法
- 对于点$(-1,-1),(1,3),(2,-2)$我们需要找到一个Polynomial穿过这三个点，可以先写出三个Quadratic Polynomial
$$L_1(x) := \begin{cases} 
1, & \text{if } x = -1 \\
0, & \text{if } x = 1 \\
0, & \text{if } x = 2,
\end{cases}

L_2(x) := \begin{cases} 
0, & \text{if } x = -1 \\
1, & \text{if } x = 1 \\
0, & \text{if } x = 2,
\end{cases}

L_3(x) := \begin{cases} 
0, & \text{if } x = -1 \\
0, & \text{if } x = 1 \\
1, & \text{if } x = 2.
\end{cases}
$$
- 之后再令$P_2(x)=−1L_1(x) + 3L_2(x) − 2L_3(x)$
- 分别查看三个点的值可以发现
$$P_2(-1) = -1L_1(-1) + 3L_2(-1) - 2L_3(-1) \\
= -1(1) + 3(0) - 2(0) \\
= -1$$
$$P_2(1) = -1L_1(1) + 3L_2(1) - 2L_3(1) \\
= -1(0) + 3(1) - 2(0) \\
= 3$$
$$
P_2(2) = -1L_1(2) + 3L_2(2) - 2L_3(2) \\
= -1(0) + 3(0) - 2(1) \\
= -2$$
- 可以发现这样构建的Polynomial是符合要求的，那么问题就变成了如何构建这三个Quadratic Polynomial
- 已知$L_1(x)$有两个Roots，分别为$x=1$和$x=2$，并且因为$L_1(-1)=1$所以有 
$$L_1(-1)=C(-1-1)(-1-2)=1\Rightarrow C=\frac{1}{(-1-1)(-1-2)}$$
- 同理对于$L_2$和$L_3$来说有
$$P_2(x) = -1 \frac{(x - 1)(x - 2)}{(-1 - 1)(-1 - 2)} + 3 \frac{(x + 1)(x - 2)}{(1 + 1)(1 - 2)} - 2 \frac{(x + 1)(x - 1)}{(2 + 1)(2 - 1)}
$$
- 这就是Lagrange Interpolation 拉格朗日插值法

## ex. 

- 将Lagrange Interpolation推广到四个点上，有
$$L_1(x) := \begin{cases} 
1, & \text{if } x = x_1 \\
0, & \text{if } x = x_2 \\
0, & \text{if } x = x_3 \\
0, & \text{if } x = x_4,
\end{cases}

L_2(x) := \begin{cases} 
0, & \text{if } x = x_1 \\
1, & \text{if } x = x_2 \\
0, & \text{if } x = x_3 \\
0, & \text{if } x = x_4,
\end{cases}

L_3(x) := \begin{cases} 
0, & \text{if } x = x_1 \\
0, & \text{if } x = x_2 \\
1, & \text{if } x = x_3 \\
0, & \text{if } x = x_4,
\end{cases}

L_4(x) := \begin{cases} 
0, & \text{if } x = x_1 \\
0, & \text{if } x = x_2 \\
0, & \text{if } x = x_3 \\
1, & \text{if } x = x_4.
\end{cases}$$
- 其最终的Polynomial将会长这样
$$P_3(x) = y_1 \frac{(x-x_2)(x-x_3)(x-x_4)}{(x_1-x_2)(x_1-x_3)(x_1-x_4)} + y_2 \frac{(x-x_1)(x-x_3)(x-x_4)}{(x_2-x_1)(x_2-x_3)(x_2-x_4)} + y_3 \frac{(x-x_1)(x-x_2)(x-x_4)}{(x_3-x_1)(x_3-x_2)(x_3-x_4)} + y_4 \frac{(x-x_1)(x-x_2)(x-x_3)}{(x_4-x_1)(x_4-x_2)(x_4-x_3)}$$


