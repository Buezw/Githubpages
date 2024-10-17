from manim import *
import random
import time
import numpy as np

class CoordinateSystem(Scene):
    def construct(self):
        # 创建一个坐标系
        axes = Axes(
            x_range=[-5, 5, 1],  # x轴范围：从-5到5，步长为1
            y_range=[-3, 3, 1],  # y轴范围：从-3到3，步长为1
            x_length=7,  # x轴的长度
            y_length=5,  # y轴的长度
            axis_config={"color": BLUE},  # 坐标轴的颜色
            tips=False  # 是否显示坐标轴的箭头
        )

        # 为坐标系添加标签
        labels = axes.get_axis_labels(x_label="x", y_label="y")

        # 显示坐标系和标签
        self.play(Create(axes), Write(labels))
        self.wait(2)
