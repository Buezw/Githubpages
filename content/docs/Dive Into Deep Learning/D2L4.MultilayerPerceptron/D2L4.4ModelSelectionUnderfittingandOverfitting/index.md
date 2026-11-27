---
title: "D2L 4.4 Model Selection, Underfitting, and Overfitting"
lang: en
date: 2024-04-15
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 10
math: mathjax
pageStyle : "normal"
---
深度学习的目的是发现Pattern，即做到模型的Generalization 泛化

- Overfitting Problem

> 原因很简单：当我们将来部署该模型时，模型需要判断从未见过的患者。 只有当模型真正发现了一种泛化模式时，才会作出有效的预测

困难在于，当我们训练模型时，我们只能访问数据中的小部分样本。 
最大的公开图像数据集包含大约一百万张图像。 而在大部分时候，我们只能从数千或数万个数据样本中学习。 
在大型医院系统中，我们可能会访问数十万份医疗记录。 当我们使用有限的样本时，可能会遇到这样的问题： 当收集到更多的数据时，会发现之前找到的明显关系并不成立。

# Overfitting 过拟合

- 模型在训练数据上拟合的比在潜在分布中更接近的现象称为过拟合

![](/docs/D2L_Static/4.4_ModelSelectionUnderfittingandOverfitting/4.4_ModelSelectionUnderfittingandOverfitting-1.png)

- 左： Underfitting 欠拟合
- 中：拟合
- 右：Overfitting 过拟合

![](/docs/D2L_Static/4.4_ModelSelectionUnderfittingandOverfitting/4.4_ModelSelectionUnderfittingandOverfitting-2.png)

# Regularization 正则化

- 对抗过拟合的技术称为正则化
- Regularization 正则化


# 4.4.1 训练误差和泛化误差


## Training Error 训练误差

- 模型在训练数据集上计算得到的误差

## Generalization Error 泛化误差

- 同样分布样本的无限多个数据的模型误差期望
-  但问题是对于无限多个数据，我们不可能准确的计算出Genrelization Errorz


## 4.4.1.1 统计学习理论

- 我们假设训练数据和测试数据都是从相同的分布中独立提取的。 这通常被称为_独立同分布假设_（i.i.d. assumption）

## 4.4.1.2 模型复杂性

- 一个模型的复杂性取决于很多因素
- 如模型参数，取值范围

### Early Stopping 早停

- **早停（Early Stopping）**：这是一种防止过拟合的技术，其中训练过程在验证集上的性能开始恶化时停止。这意味着，如果模型在验证集上的误差开始增加，表明模型可能开始过拟合训练数据，此时停止进一步训练可以避免这种情况。

# 4.4.2 模型选择

- 在一个训练中，我们会选择几个候选模型对他们进行评估

## 4.4.2.1 验证集

> [训练集，验证集，测试集分别是什么_训练集 验证集 测试集-CSDN博客](https://blog.csdn.net/qq_24884193/article/details/104071664)
- 总的来说，对于Superivised Training，一般讲整体划为3个区块

![](/docs/D2L_Static/4.4_ModelSelectionUnderfittingandOverfitting/4.4_ModelSelectionUnderfittingandOverfitting-3.png)

### Training Set 训练集

- 训练集用来训练模型，即确定模型的权重和偏置这些参数，通常我们称这些参数为学习参数
- 训练集中的参数**直接参与到梯度下降中**

### Validation Set 验证集
z
- 而验证集用于模型的选择，更具体地来说，验证集并不参与学习参数的确定，也就是验证集并**没有参与梯度下降**的过程
- 验证集只是为了选择**超参数**，比如网络层数、网络节点数、迭代次数、学习率这些都叫超参数

### Test Set 测试集

- 测试集只使用一次，即在训练完成后评价最终的模型时使用。它既不参与学习参数过程，也不参数超参数选择过程，而仅仅使用于模型的评价

## 4.4.2.2 K-Fold Cross-Validation K折交叉验证

- 训练数据稀缺时，我们甚至可能无法提供足够的数据来构成一个合适的验证集

### 过程描述

- **数据分组**：首先，整个数据集被随机分成K个大小大致相同的子集。
- **迭代训练与验证**：每次迭代中，选择其中一个子集作为验证集，而其余的K-1个子集合并作为训练集。
- **性能评估**：模型在训练集上训练，并在验证集上进行评估。这个过程重复K次，每次选择不同的子集作为验证集。
- **平均性能**：最终模型的性能是所有K次迭代中验证性能的平均值。这样可以更全面地评估模型的性能。


# 4.4.3 欠拟合还是过拟合？

- Generlization Error高的模型叫做Underfitting
- Train Error远低于Validation Error的模型叫做Overfitting
## 4.4.3.1 模型复杂性

![[Pasted image 20240615153938.png]]

- 简单来说，从左到右模型经历了从欠拟合到过拟合的一个过程，也是从高损失到高方差的过程
- 其是因为模型从没学习过参数到对于微小参数（甚至是随机噪声）严重敏感的一个过程
### Lost 损失

- **定义**：偏差是指模型在预测中的系统误差，即模型对学习数据的一般性质的理解程度。
- **高偏差**：通常表示模型过于简单（欠拟合），未能捕捉到数据的关键结构，通常会导致在训练集和测试集上都表现不佳。

 ### Variance 方差

- **定义**：方差是指模型对于训练数据的微小变化的敏感度。
- **高方差**：表示模型过于复杂（过拟合），对训练数据中的随机噪声也进行了学习，这可能使得模型在新的、未见过的数据上表现不佳。


## 4.4.3.2 数据集大小

- 训练数据集中的样本越少，我们就越有可能（且更严重地）过拟合
- 而样本更过通常会减小Gerneralization Error
- 一般来说，更多的数据不会有什么坏处

# 4.4.4 多项式回归

- 拟合一个多项式

- 4.4 Overfitting Normal & Underfitting - Pytorch
- 
## 4.4.4.1 生成数据集

![[Pasted image 20240616094316.png]]
- 噪声值位均值0到标准差0.1的正态分布
-  在优化的过程中，我们通常希望避免非常大的梯度值或损失值。 这就是我们将特征从$x^i$调整为$\frac{x^i}{i!}$的原因

```
max_degree = 20  # 多项式的最大阶数
n_train, n_test = 100, 100  # 训练和测试数据集大小
true_w = np.zeros(max_degree)  # 分配大量的空间
true_w[0:4] = np.array([5, 1.2, -3.4, 5.6])

features = np.random.normal(size=(n_train + n_test, 1))
np.random.shuffle(features)
poly_features = np.power(features, np.arange(max_degree).reshape(1, -1))
for i in range(max_degree):
    poly_features[:, i] /= math.gamma(i + 1)  # gamma(n)=(n-1)!
# labels的维度:(n_train+n_test,)
labels = np.dot(poly_features, true_w)
labels += np.random.normal(scale=0.1, size=labels.shape)
```

- `max_degree = 20` : 即使多项式仅为三阶，但我们需要用一个20纬的多项式去拟合它，这是复杂模型中的一种
- `features = np.random.normal(size=(n_train + n_test, 1))`: 分配200个一维的特征
- `np.random.shuffle(features)`: 随机打乱数据
- `poly_features = np.power(features, np.arange(max_degree).reshape(1, -1))`：分配每个特征的高阶数据
- 使用伽马正则化防止特征的迅速增大
- 最后点乘特征和真实权重得到Label，并将Label加上合适的噪声

```
# NumPy ndarray转换为tensor
true_w, features, poly_features, labels = [torch.tensor(x, dtype=
    torch.float32) for x in [true_w, features, poly_features, labels]]

features[:2], poly_features[:2, :], labels[:2]
```

- 转化为tensor

```
def evaluate_loss(net, data_iter, loss):  #@save
    """评估给定数据集上模型的损失"""
    metric = d2l.Accumulator(2)  # 损失的总和,样本数量
    for X, y in data_iter:
        out = net(X)
        y = y.reshape(out.shape)
        l = loss(out, y)
        metric.add(l.sum(), l.numel())
    return metric[0] / metric[1]
```

```
def train(train_features, test_features, train_labels, test_labels,
          num_epochs=400):
    loss = nn.MSELoss(reduction='none')
    input_shape = train_features.shape[-1]
    # 不设置偏置，因为我们已经在多项式中实现了它
    net = nn.Sequential(nn.Linear(input_shape, 1, bias=False))
    batch_size = min(10, train_labels.shape[0])
    train_iter = d2l.load_array((train_features, train_labels.reshape(-1,1)),
                                batch_size)
    test_iter = d2l.load_array((test_features, test_labels.reshape(-1,1)),
                               batch_size, is_train=False)
    trainer = torch.optim.SGD(net.parameters(), lr=0.01)
    animator = d2l.Animator(xlabel='epoch', ylabel='loss', yscale='log',
                            xlim=[1, num_epochs], ylim=[1e-3, 1e2],
                            legend=['train', 'test'])
    for epoch in range(num_epochs):
        d2l.train_epoch_ch3(net, train_iter, loss, trainer)
        if epoch == 0 or (epoch + 1) % 20 == 0:
            animator.add(epoch + 1, (evaluate_loss(net, train_iter, loss),
                                     evaluate_loss(net, test_iter, loss)))
    print('weight:', net[0].weight.data.numpy()
```


### 欠拟合

```
# 从多项式特征中选择前2个维度，即1和x
train(poly_features[:n_train, :2], poly_features[n_train:, :2],
      labels[:n_train], labels[n_train:])
```

- 只给予了前两个特征值
![[Pasted image 20240704160340.png]]

 ### 过拟合

```
# 从多项式特征中选取所有维度
train(poly_features[:n_train, :], poly_features[n_train:, :],
      labels[:n_train], labels[n_train:], num_epochs=1500)
```

- 将w中的20列全部给到了模型导致了过拟合
![[Pasted image 20240704160346.png]]

