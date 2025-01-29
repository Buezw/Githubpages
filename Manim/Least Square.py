from manim import *
import numpy as np

class Least(Scene):
    def construct(self):
        # 创建一个坐标系
        axes = Axes(
            x_range=[-3, 3, 1], 
            y_range=[-3, 3, 1], 
            x_length=6,  # x轴的长度
            y_length=6,  # y轴的长度
            axis_config={"color": BLUE},  # 坐标轴的颜色
            tips=True # 是否显示坐标轴的箭头
        )
        # line = FunctionGraph(lambda y: 0,color=BLUE,y_range=[-2.5, 2.5])
        # line_text = Text('y=x',font_size=30)
        # line_text.set_color(BLUE)
        vec = Vector([1, 2], color=YELLOW)
        vec_text = Text('<1,2>',font_size=30)
        vec_text.set_color(YELLOW)
        vec_text.next_to(vec,RIGHT)
        # line_text.next_to(vec_text,UP,buff=1)
        self.play(Create(axes),Create(vec),Create(vec_text))
        #self.wait(2)

        vec_1 = Vector([0, 2], color=YELLOW).shift(1,0,0)
        #vec_1_text = Text('<0,2>',font_size=30)
        #vec_1_text.set_color(YELLOW)
        #vec_1_text.next_to(vec_1,RIGHT)

        self.play(Create(vec_1))
        self.wait(2)
