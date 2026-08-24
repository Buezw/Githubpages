---
title: "D2L Weierstrass Approximation Theorem"
date: 2024-12-19
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 10
math: mathjax
pageStyle : "normal"
---
> Last Edit: 12/19/24

## Weierstrass Approximation Theorem

- 每一个定义在闭区间\\([a,b]\\)上的实值连续函数都可以被多项式序列在整个区间上一致逼近。
- 换句话说，给定任意的连续函数\\(f: [a, b] \to \mathbb{R}\\)和任意小的正数\\(\epsilon\\)，都存在一个多项式\\(P(x)\\)，使得对所有\\(x \in [a, b]\\)都有\\(|f(x) - P(x)| < \epsilon\\)

## Bernstein's Proof 1912

- 采用离散的Convolution
$$f(x)\approx\sum^n_{i=0}f(x_i)w(x_i)$$
- 其满足\\(\sum_i(x_i)=1\\)，离\\(x\\)越近的地方\\(w(x_i)\\)越大

### Binomial Distribution 二项分布

- 一种离散概率分布，用于模型在固定次数的独立试验中每次试验成功的次数
- 其质量概率函数为
$$P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$$
- p：单次独立事件的成功概率
- k：实验中事件成功的次数
- n：实验的总事件的数量

### Interpretation

- 这样理解，先不管\\(\binom{n}{k}\\)，假设一个成功率为\\(60\%\\)的事件，其总共实验次数为5次，也就是\\(p=0.6,n=5\\)
- 现在当\\(k=5\\)的时候，Binomial Distribution表示的概率为\\(0.6^5\\)，也就是说对于一个概率为0.6的事件，其独立测试五次后都成功的概率为\\(0.6^5\\)，这就是最简单的概率
- 当\\(k=3\\)时，概率质量函数为
$$\binom{5}{3} 0.6^3 (1-0.6)^{5-3}$$
- 也就是说，5次实验，每一个5次实验中3次成功的概率为\\(0.6^3 (1-0.6)^{5-3}\\)
- 而在5次实验中这些成功的和失败的实验都可能出现在不同的位置，而这些中的成功的事件的位置可以是
$$123,124,125,134,135,145,234,235,245,345$$
- 这10种情况，也就是出现5次中3次的会有10中情况，所以乘以10

## Bernstein Polynomial 伯恩斯坦多项式
$$B_n(x) = \sum_{i=0}^n f\left(\frac{i}{n}\right) \binom{n}{i} x^i (1-x)^{n-i}$$
- 用加权平均的方式（基于二项分布）生成新的多项式\\(B_n(x)\\)，作为\\(f(x)\\)的近似，实际上就是一个离散的Convolution

### Similarity to Convolution 
$$(f * g)(x) = \sum_{k} f(k) g(x-k)$$
- 可以发现两者的区别就在于Bernstein Poly的Weight是基于Binomial Distribution的
- 并且采样点不再是连续的输入而是离散且固定的值

### Expectation
$$B_n(x) = \mathbb{E}\left[f\left(\frac{X}{n}\right)\right]$$
- 最终可以得到Bernstein Polynomial的期望值在\\(n\rightarrow \infty\\)的情况下是就是\\(f(x)\\)
- 也就是说可以通过一致收敛性，说明\\(B_n(f, x)\\)在区间\\([0, 1]\\)上以任意精度逼近\\(f(x)\\)

































