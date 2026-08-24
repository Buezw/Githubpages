---
title: "D2L 3.6 Implementation of softmax regression from scratch"
date: 2024-04-15
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 7
math: mathjax
pageStyle : "normal"
---
## 3.6.1 初始化模型参数

- 和之前线性回归的例子一样，这里的每个样本都将用固定长度的向量表示。 原始数据集中的每个样本都是28×28的图像。 本节将展平每个图像，把它们看作长度为784的向量
- 在3.5中，我们选择了一个拥有10个类别的数据集，所以softmax网络的输出维度为10

### 初始化权重w

- 与线性回归一样，我们使用正态分布初始化权重w，偏置初始化为0

```
num_inputs = 784
num_outputs = 10

W = torch.normal(0, 0.01, size=(num_inputs, num_outputs), requires_grad=True)
b = torch.zeros(num_outputs, requires_grad=True)
```

## 3.6.2 定义softmax操作

- 实现softmax操作由三个步骤组成
- 对每个项求幂
- 对每一行求和，得到其规范化常数
- 每一行除以其规范化常数，保持结果的和为1
$$softmax(X)_{ij}=\frac{exp(X_{ij})}{\sum_kexp(X_{ik})}$$
- 分母或规范化常数，有时也称为_配分函数_（其对数称为对数-配分函数）。 该名称来自[统计物理学](https://en.wikipedia.org/wiki/Partition_function_(statistical_mechanics))中一个模拟粒子群分布的方程

```
def softmax(X):
    X_exp = torch.exp(X)
    partition = X_exp.sum(1, keepdim=True)
    return X_exp / partition  # 这里应用了广播机制
```

- keepdim=True: 在进行张量操作时，保持原始张量的维度


- `torch.normal(0, 1, (2, 5))` 是用 PyTorch 生成一个服从均值为 0，标准差为 1 的正态分布的张量。
- 其中的 (2, 5) 是指生成的张量的形状为 2 行 5 列的矩阵

## 3.6.3 定义模型

- 定义softmax操作后，我们可以实现softmax回归模型

```
def net(X):
    return softmax(torch.matmul(X.reshape((-1, W.shape[0])), W) + b)
```

## 3.6.4 定义损失函数

- 引入[[Cross-Entropy 交叉熵]]损失函数
- 深度学习中，交叉熵函数最为常见，因为分类问题的数量远远超过了回归问题

```
y = torch.tensor([0, 2])
y_hat = torch.tensor([[0.1, 0.3, 0.6], [0.3, 0.2, 0.5]])
y_hat[[0, 1], y]
```

- y_hat： 包含2个样本在3个类别的预测概率
- y：真实类，0代表第一类，1代表第二类，2代表第三类
- `[[0,1],y]`：一种tensor的高级引索功能，其选择了y_hat中的第一行和第二行
- 而y给予了列的位置，所以输出分别为第一行第0位和第二行第2位


## 3.6.5 分类精度

- 给定预测概率分布\\(\hat y\\)，当我们必须输出Hard Prediciton 硬预测时，我们通常选择概率最高的类
- 当预测和标签分类y一致时，即是正确的
- 分类精度指的就是正确预测数量与总预测数量之比

```
def accuracy(y_hat, y):  #@save
	"""计算预测正确的数量"""
    if len(y_hat.shape) > 1 and y_hat.shape[1] > 1:
        y_hat = y_hat.argmax(axis=1)
    cmp = y_hat.type(y.dtype) == y
    return float(cmp.type(y.dtype).sum())
```


### 扩展到任意数据迭代器data_iter可访问的数据集

```
def evaluate_accuracy(net, data_iter):  #@save
    """计算在指定数据集上模型的精度"""
    if isinstance(net, torch.nn.Module):
        net.eval()  # 将模型设置为评估模式
    metric = Accumulator(2)  # 正确预测数、预测总数, Accmulator在下面定义
    with torch.no_grad():
        for X, y in data_iter:
            metric.add(accuracy(net(X), y), y.numel())
    return metric[0] / metric[1]
```

- 首先，如果 `net` 是 `torch.nn.Module` 的子类，就将模型设置为评估模式，即调用 `net.eval()`。在评估模式下，模型的行为可能会略有不同，比如 `Dropout` 层在评估模式下会关闭，以避免随机丢弃部分节点
- 创建了一个名为 `metric` 的累加器（Accumulator）。这个累加器用于记录正确预测数和总预测数，初始化为两个元素的列表 `[0, 0]`
- `Accumulator`：这个类在下面定义
- 使用 `torch.no_grad()` 上下文管理器，禁用梯度计算
- 最后就是将评估结果添加至metric中

### Accumulator类

- 这里定义一个实用程序类`Accumulator`，用于对多个变量进行累加。 在上面的`evaluate_accuracy`函数中， 我们在`Accumulator`实例中创建了2个变量， 分别用于存储正确预测的数量和预测的总数量。 当我们遍历数据集时，两者都将随着时间的推移而累加。

```
class Accumulator:  #@save
    """在n个变量上累加"""
    def __init__(self, n):
        self.data = [0.0] * n

    def add(self, *args):
        self.data = [a + float(b) for a, b in zip(self.data, args)]

    def reset(self):
        self.data = [0.0] * len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
```

- `__init__(self, n)`: 这是类的构造函数，用于初始化累加器。它接受一个参数 `n`，表示要累加的变量的数量。在初始化时，创建了一个包含 n 个元素的列表，每个元素初始化为 0.0
- `add(self, *args)`: 这个方法用于将参数 `args` 中的值与累加器中的值相加。参数 `args` 是一个可变参数，可以接受任意数量的参数。通过 `zip` 函数，将 `args` 中的值逐个与累加器中对应位置的值相加，并更新累加器中的值
- `reset(self)`: 这个方法用于重置累加器的值
- `__getitem__(self, idx)`: 这个方法允许通过索引访问累加器中的值。给定一个索引 `idx`，它返回累加器中对应位置的值

## 3.6.6 训练

- 首先，我们定义一个函数来训练一个迭代周期
- `updater`是更新模型参数的常用函数，它接受批量大小作为参数

```
def train_epoch_ch3(net, train_iter, loss, updater):  #@save
    """训练模型一个迭代周期（定义见第3章）"""
    # 将模型设置为训练模式
    if isinstance(net, torch.nn.Module):
        net.train()
    # 训练损失总和、训练准确度总和、样本数
    metric = Accumulator(3)
    for X, y in train_iter:
        # 计算梯度并更新参数
        y_hat = net(X)
        l = loss(y_hat, y)
        if isinstance(updater, torch.optim.Optimizer):
            # 使用PyTorch内置的优化器和损失函数
            updater.zero_grad()
            l.mean().backward()
            updater.step()
        else:
            # 使用定制的优化器和损失函数
            l.sum().backward()
            updater(X.shape[0])
        metric.add(float(l.sum()), accuracy(y_hat, y), y.numel())
    # 返回训练损失和训练精度
    return metric[0] / metric[2], metric[1] / metric[2]
```

- `if isinstance(net, torch.nn.Module):`：检查变量 `net` 是否是 `torch.nn.Module` 类的实例
- `net.train()`: 这一行将模型（`net`）设置为训练模式
- `metric = Accumulator(3)`: 创建一个长度为3的累加器
- 在计算梯度后，根据数据类型，如pytorch类或者自定义类累加处理结果

### 训练函数

```
def train_ch3(net, train_iter, test_iter, loss, num_epochs, updater):  #@save
    """训练模型（定义见第3章）"""
    animator = Animator(xlabel='epoch', xlim=[1, num_epochs], ylim=[0.3, 0.9],
                        legend=['train loss', 'train acc', 'test acc'])
    for epoch in range(num_epochs):
        train_metrics = train_epoch_ch3(net, train_iter, loss, updater)
        test_acc = evaluate_accuracy(net, test_iter)
        animator.add(epoch + 1, train_metrics + (test_acc,))
    train_loss, train_acc = train_metrics
    assert train_loss < 0.5, train_loss
    assert train_acc <= 1 and train_acc > 0.7, train_acc
    assert test_acc <= 1 and test_acc > 0.7, test_acc
```





























