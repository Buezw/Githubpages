---
title: "D2L 3.2 Object-Oriented Design for Implementation"
lang: en
date: 2024-04-15
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 3
math: mathjax
pageStyle : "normal"
---
从零开始实现整个方法， 包括数据流水线、模型、损失函数和小批量随机梯度下降优化器。 虽然现代的深度学习框架几乎可以自动化地进行所有这些工作，但从零开始实现可以确保我们真正知道自己在做什么。

## 3.2.1  生成数据集

- 为了简单起见，我们将根据带有噪声的线性模型构造一个人造数据集
- 使用线性模型参数\\(w=[2,-3.4]^T,b=4.2\\)和噪声项\\(\epsilon\\)生成数据集及其标签
$$y=Xw+b+\epsilon$$
-  \\(\epsilon\\)可以视为模型预测和标签时的潜在观测误差

## 3.2.2 读取数据集

## 3.2.3 初始化模型参数

- 通过从均值为0、标准差为0.01的正态分布中采样随机数来初始化权重， 并将偏置初始化为0。
```
w = torch.normal(0, 0.01, size=(2,1), requires_grad=True)
b = torch.zeros(1, requires_grad=True)
```
- 在初始化参数之后，我们的任务是更新这些参数，直到这些参数足够拟合我们的数据
- 并运用2.5 自动微分来计算梯度

## 3.2.4 定义模型

- 这里我们用的还是线性模型，即$$\hat y=w^Tx+b$$
```
def linreg(X, w, b):  #@save
    """线性回归模型"""
    return torch.matmul(X, w) + b
```

## 3.2.5 定义损失函数

- 模型建立后，开始使用对原函数的损失函数进行梯度下降
- 这里我们使用3.1_LinearRegression

## 3.2.6 定义优化算法

- 使用3.1_LinearRegression

## 3.2.7 训练

- 本质为执行一下循环
- 初始化参数
- 更新梯度，更新参数




















