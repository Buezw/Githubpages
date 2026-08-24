---
title: "D2L 5.4 Custom Layer"
date: 2025-01-19
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
math: mathjax
pageStyle : "normal"
---
> Last Edit: 1/19/25

在整体网络中，存在一些不同的层，他们都是专门用来处理不同事件的，这也令自定义层变得有必要

# 5.4.1 Layer without parameter

``` python
import torch
import torch.nn.functional as F
from torch import nn

class CenteredLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, X):
        return X - X.mean()
```

- 将比之前的层，这个forward过程中仅包含了一个减去平均值的操作，这相当于在模型中以一个层的方式包装了一个函数

# 5.4.2 Layer with parameter

``` python
class MyLinear(nn.Module):
    def __init__(self, in_units, units):
        super().__init__()
        self.weight = nn.Parameter(torch.randn(in_units, units))
        self.bias = nn.Parameter(torch.randn(units,))
    def forward(self, X):
        linear = torch.matmul(X, self.weight.data) + self.bias.data
        return F.relu(linear)
```

- 本质上就是重构了一下pytorch的`nn.Linear`模块

``` python
self.weight = nn.Parameter(torch.randn(in_units, units))
        self.bias = nn.Parameter(torch.randn(units,))
```

- 权重矩阵W决定了输入X如何被映射到输出空间。
- 每个输入特征（列）需要与输出特征（列）有连接。
- 因此，权重矩阵需要有：
- 行数：输入特征的数量（`in_units`）
- 列数：输出特征的数量（`units`）
- 转换到pytorch中就相当于

``` python
import torch
import torch.nn as nn
import torch.nn.functional as F

class MyLinearWithBuiltin(nn.Module):
    def __init__(self, in_units, units):
        super().__init__()
        self.linear = nn.Linear(in_units, units)  # 内置线性层
    
    def forward(self, X):
        linear = self.linear(X)  # 使用内置线性层
        return F.relu(linear)    # ReLU 激活函数
```
