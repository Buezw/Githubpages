---
draft: true
title: "Demo 2. Code & Math"
date: 2026-09-10
tags: ["Docs","Sample"]
math: mathjax
showWordCount: true
---
> Last Edit: 9/10/26

## Inline & Block Math

Black-Scholes 定价公式，用来检查行内公式 \\(C = S_0 N(d_1) - K e^{-rT} N(d_2)\\) 和块级公式的渲染：

$$d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}$$

## Code Blocks

Python:

```python
import numpy as np

def monte_carlo_price(s0, k, r, sigma, t, n_paths=100_000):
    z = np.random.standard_normal(n_paths)
    st = s0 * np.exp((r - 0.5 * sigma**2) * t + sigma * np.sqrt(t) * z)
    payoff = np.maximum(st - k, 0)
    return np.exp(-r * t) * payoff.mean()
```

C++:

```cpp
struct Order {
    uint64_t id;
    double price;
    int qty;
    bool is_buy;
};

double mid_price(const Order& bid, const Order& ask) {
    return (bid.price + ask.price) / 2.0;
}
```

一行内代码测试：`std::vector<Order>` 和变量 `sigma` 混排在文字中间。
