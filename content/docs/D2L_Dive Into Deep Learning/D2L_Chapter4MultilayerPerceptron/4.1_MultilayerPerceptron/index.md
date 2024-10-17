---
title: "D2L 4.3 Simple Implementation of Multilayer Perceptron"
date: 2024-04-15
tags: ["D2L","Computer Science","Docs"]
series: ["D2L"]
series_order: 10
math: mathjax
pageStyle : "normal"
---
通过更高级的API进一步简洁训练过程

# 4.3.1 模型

```
net = nn.Sequential(nn.Flatten(),
                    nn.Linear(784, 256),
                    nn.ReLU(),
                    nn.Linear(256, 10))

def init_weights(m):
    if type(m) == nn.Linear:
        nn.init.normal_(m.weight, std=0.01)

net.apply(init_weights);
```

- 初始化神经网络

```
batch_size, lr, num_epochs = 256, 0.1, 10
loss = nn.CrossEntropyLoss(reduction='none')
trainer = torch.optim.SGD(net.parameters(), lr=lr)

train_iter, test_iter = d2l.load_data_fashion_mnist(batch_size)
d2l.train_ch3(net, train_iter, test_iter, loss, num_epochs, trainer)
```



















