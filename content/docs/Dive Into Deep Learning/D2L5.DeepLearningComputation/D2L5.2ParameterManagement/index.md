---
title: "D2L 5.2 Parameter Management"
date: 2025-01-17
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
math: mathjax
pageStyle : "normal"
---
> Last Edit: 1/17/25

在训练的过程中，目标是找到使得Cost Function最小化的Parameters，而有些时候需要提取其中一层的参数检查或者移动到其他环境下，这就需要访问参数

# 5.2.1 Access parameters 访问参数

- 现在先用一个简单的MLP

``` python
import torch
from torch import nn

net = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 1))
X = torch.rand(size=(2, 4))
net(X)
```

- 当采用pytorch的Sequential定义模型的时候，可以通过Index访问层

``` python
print(net[2].state_dict())
-> OrderedDict([('weight', tensor([[-0.0861,  0.1627,  0.2363,  0.2068,  0.0122, -0.1120, -0.3021, -0.2810]])), ('bias', tensor([0.0187]))])
```

- 查看Output，其包含了'weight' 和 'bias' 两个参数
- 需要知道的是每一层的参数的名称都对应唯一的值，如访问所有模型参数时

``` python
print(net.state_dict())
-> OrderedDict([('0.weight', tensor([[ 0.2787,  0.1086,  0.2637,  0.1725],
        [ 0.0952,  0.4238,  0.0774, -0.1717],
        [-0.2244,  0.0670, -0.4168,  0.1995],
        [ 0.1364, -0.1932,  0.0650,  0.3378],
        [-0.1094,  0.2522, -0.2162, -0.2466],
        [ 0.1079,  0.0859, -0.4721, -0.1010],
        [-0.2436,  0.2096, -0.3895,  0.4636],
        [ 0.2348,  0.1281, -0.1079,  0.4432]])), ('0.bias', tensor([-0.0356,  0.3268,  0.3199, -0.4558, -0.2564, -0.3566, -0.1493,  0.0168])), ('2.weight', tensor([[-0.0861,  0.1627,  0.2363,  0.2068,  0.0122, -0.1120, -0.3021, -0.2810]])), ('2.bias', tensor([0.0187]))])
```

## 5.2.1.1 Target Parameter 目标参数

- 既然能访问层下参数，当然也能访问到具体参数

``` python
print(type(net[2].bias))
print(net[2].bias)
print(net[2].bias.data)
-> <class 'torch.nn.parameter.Parameter'>
	Parameter containing:
	tensor([0.0187], requires_grad=True)
	tensor([0.0187])
```

- 单个参数是一个复合对象，即不止包含值

## 5.2.1.3 Collect Parameter from blocks

``` python
def block1():
    return nn.Sequential(nn.Linear(4, 8), nn.ReLU(),
                         nn.Linear(8, 4), nn.ReLU())

def block2():
    net = nn.Sequential()
    for i in range(4):
        # 在这里嵌套
        net.add_module(f'block {i}', block1())
    return net

rgnet = nn.Sequential(block2(), nn.Linear(4, 1))
rgnet(X)
```

- 这里构建了一个挺复杂的网络，具体来说block2定义了一个大块，其中input要经过4个block1之后通过一个Linear Layer，完整结构如下

``` python
->  rgnet: Sequential(
	    (0): block2: Sequential(
	        (block 0): block1
	        (block 1): block1
	        (block 2): block1
	        (block 3): block1
	    )
	    (1): Linear(4, 1)
	)
```

- 就像多层的List一样，需要通过维度依次访问，最外层为一个Block 2和一个Linear，而Block2 内部依然是一个“二维列表”，通过`rgnet[0][1][0].bias.data`就可以访问到(block 1): block1的Linear层的bias的值

# 5.2.2 Parameter Initialization 参数初始化

- 前面讨论过了一个系统的初始化的重要性，可以简单的通过框架做默认初始化也可以自定义

## 5.2.2.1 Built-in initialization 内置初始化

``` python
def init_normal(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, mean=0, std=0.01)
        nn.init.zeros_(m.bias)
net.apply(init_normal)
net[0].weight.data[0], net[0].bias.data[0]
```

- 上面的`nn.init.normal_`和`nn.init.zeros_`分别对应了Gaussian Distribution和零值
- `nn.init.constant_(m.weight,1)`则可以将weight全设置为固定值1

## 5.2.2.2 Custom Initialization 自定义初始化

# 5.2.3 Combined Parameter 参数绑定

- 通过在定义模型之间定义层，后将层作为元素直接放入模型中，这样就可以做到模型中的两个层不止在数值上是相等的，其调用的Memory都是同一个（即改一个则全变）

> 当参数绑定时，梯度会发生什么情况？ 答案是由于模型参数包含梯度，因此在反向传播期间第二个隐藏层 （即第三个神经网络层）和第三个隐藏层（即第五个神经网络层）的梯度会加在一起。
> -> 将补充原理

















