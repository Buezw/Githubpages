from manim import *
import numpy as np

class RandomDots(Scene):
    def construct(self):
        # 生成10000个随机点
        points = [Dot(point=[np.random.uniform(-6, 6), np.random.uniform(-3.5, 3.5), 0], radius=0.05, color=WHITE) for _ in range(10000)]
        
        # 将所有点的动画组合成按顺序出现的动画
        animations = [Create(dot) for dot in points]
        
        # 使用Succession让这些动画按顺序播放
        self.play(Succession(*animations, lag_ratio=0.001))  # 控制动画间隔时间
        self.wait()

