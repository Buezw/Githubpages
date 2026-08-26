---
title: "D2L 3.3 A concise implementation of linear regression"
date: 2024-04-15
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 4
math: mathjax
pageStyle : "normal"
---

本节将介绍如何通过使用深度学习框架来简洁地实现[[3.2_Object-OrientedDesignforImplementation]]中的线性回归模型

## 3.3.1 生成数据集
```
import numpy as np
import torch
from torch.utils import data
from d2l import torch as d2l

true_w = torch.tensor([2, -3.4])
true_b = 4.2
features, labels = d2l.synthetic_data(true_w, true_b, 1000)
```
- `d2l.synthetic_data(true_w, true_b, 1000)` 是 `d2l` 库中的一个函数调用。这个函数用于生成合成数据，其中包括特征数据和对应的标签数据。
-  具体地，这个函数接受三个参数：
- `true_w`：真实的权重，用于生成特征数据。
- `true_b`：真实的偏置，用于生成特征数据。
- `1000`：生成数据的数量，这里是指生成1000个样本。

## 3.3.2 读取数据集

```
def load_array(data_arrays, batch_size, is_train=True):  #@save
    """构造一个PyTorch数据迭代器"""
    dataset = data.TensorDataset(*data_arrays)
    return data.DataLoader(dataset, batch_size, shuffle=is_train)

batch_size = 10
data_iter = load_array((features, labels), batch_size)
```
## 3.3.3 定义模型

- 对于标准深度学习模型，我们可以使用框架的预定义好的层
```
## nn是神经网络的缩写
from torch import nn
net = nn.Sequential(nn.Linear(2, 1))
```
- `nn.Sequential`：这是 PyTorch 中用于构建顺序神经网络模型的类。它允许用户按顺序堆叠多个层或模块，构建神经网络模型。
- `nn.Linear(2, 1)`：这里创建了一个全连接层，其中 `nn.Linear` 是 PyTorch 中用于定义全连接层的类。构造函数 `nn.Linear(in_features, out_features)` 接受两个参数：
- `in_features`：输入特征的数量。在这个例子中，输入特征的数量为 2。
- `out_features`：输出特征的数量。在这个例子中，输出特征的数量为 1。
因此，`net` 这个模型包含一个具有 2 个输入特征和 1 个输出特征的全连接层。
这样的模型可以用于简单的二分类问题，其中输入特征有 2 个，输出特征有 1 个，代表着模型对样本的分类结果。

## 3.3.4 初始化模型参数

```
net[0].weight.data.normal_(0, 0.01)
net[0].bias.data.fill_(0)
```

- 在网络的第一层输入参数

## 3.3.5 定义损失函数

- 计算均方误差使用的是`MSELoss`类，也称为平方�2范数。 默认情况下，它返回所有样本损失的平均值。
```
loss = nn.MSELoss()
```

## 3.3.6 定义优化算法

```
 trainer = torch.optim.SGD(net.parameters(), lr=0.03)
```

- 当我们实例化一个`SGD`实例时，我们要指定优化的参数 （可通过`net.parameters()`从我们的模型中获得）以及优化算法所需的超参数字典。 小批量随机梯度下降只需要设置`lr`值，这里设置为0.03。

## 3.3.7 训练

通过深度学习框架的高级API来实现我们的模型只需要相对较少的代码。 我们不必单独分配参数、不必定义我们的损失函数，也不必手动实现小批量随机梯度下降。 当我们需要更复杂的模型时，高级API的优势将大大增加。 当我们有了所有的基本组件，训练过程代码与我们从零开始实现时所做的非常相似。

```
num_epochs = 3
for epoch in range(num_epochs):
    for X, y in data_iter:
        l = loss(net(X) ,y)
        trainer.zero_grad()
        l.backward()
        trainer.step()
    l = loss(net(features), labels)
    print(f'epoch {epoch + 1}, loss {l:f}')
```
- `num_epochs = 3`：定义了训练的轮数，这里设置为 3
- `for epoch in range(num_epochs):`：使用 `for` 循环迭代每个训练轮数
- `for X, y in data_iter:`：使用 `data_iter` 迭代器遍历训练数据集，其中 `X` 是特征，`y` 是对应的标签
- `l = loss(net(X) ,y)`：计算模型对当前批次数据的预测值，并计算与真实标签之间的损失
- `trainer.zero_grad()`：梯度清零，以避免梯度累积
- `l.backward()`：反向传播，计算损失函数相对于模型参数的梯度
- `trainer.step()`：更新模型参数，采用优化算法更新参数
- `l = loss(net(features), labels)`：计算当前训练轮数结束后整个训练集上的损失
- `print(f'epoch {epoch + 1}, loss {l:f}')`：打印当前训练轮数和对应的损失值


























