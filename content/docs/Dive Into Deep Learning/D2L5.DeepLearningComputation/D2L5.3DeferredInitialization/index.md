---
title: "D2L 5.3 Deferred Initialization"
date: 2025-01-18
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
math: mathjax
pageStyle : "normal"
---
> Last Edit: 1/18/25

Deferred Initialization是指模型的某些参数在模型创建时并不会立即被初始化，而是会在第一次接收到输入数据时，根据输入数据的实际形状动态地完成初始化
需要知道的是延后初始化的**核心目标** 就是为了解决 **输入维度未知** 的问题，而模型内部层之间的维度通常是事先定义好的

# 5.3.1 Create Network 实例化网络

``` python
class MyNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(0, 0),  
            nn.ReLU(),
            nn.Linear(0, 0) 
        )
```

- 先定义模型框架，将两个Linear Layer留空，这样就可以在之后更改

``` python
def forward(self, x):
    if isinstance(self.layers[0], nn.Linear) and self.layers[0].in_features == 0:
        self.layers[0] = nn.Linear(x.size(1), 256)  # 动态初始化第一层
    if isinstance(self.layers[2], nn.Linear) and self.layers[2].in_features == 0:
        self.layers[2] = nn.Linear(256, 10)  # 动态初始化第二层
    return self.layers(x)
```

- 定义前向传播的过程，并在过程中加入初始化的部分，由于不知道具体的输入维度，将`self.layers[0] = nn.Linear(x.size(1), 256)`这一层的input Feature设置为输入的维度，也就是`x.size(1)`，而层与层之间的维度都是可以自行调整的，这里就可以设置这一层的output维度为256
- 分别检查定义模型时的层和运行后的，有

``` 
Before input:
Layer 0 weights: None
Layer 2 weights: None

After input:
Layer 0 weights: torch.Size([256, 20])
Layer 2 weights: torch.Size([10, 256])
```


