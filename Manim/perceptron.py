from manim import *
import numpy as np

class PerceptronAnimation(Scene):
    def construct(self):
        # 定义数据
        X = np.array([
            [0.5, 1.5],
            [1.0, 1.0],
            [1.5, 0.5],
            [2.0, 1.0],
            [2.5, 1.5],
            [3.0, 3.0],
            [3.5, 3.5],
            [4.0, 4.5],
            [4.5, 5.0],
            [5.0, 5.5]
        ])
        labels = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1])

        # 初始化权重和偏置
        W = np.array([0.0, 0.0])
        b = 0.0

        # 创建坐标轴
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 6, 1],
            x_length=6,
            y_length=6,
            tips=False,
            axis_config={"include_numbers": True}
        )
        axes_labels = axes.get_axis_labels(x_label="x1", y_label="x2")
        self.add(axes, axes_labels)

        # 绘制数据点
        positive_points = VGroup()
        negative_points = VGroup()
        for i in range(len(X)):
            point = Dot(axes.coords_to_point(X[i][0], X[i][1]))
            if labels[i] == 1:
                point.set_color(BLUE)
                positive_points.add(point)
            else:
                point.set_color(RED)
                negative_points.add(point)

        # 创建数据点的动画，减少 run_time
        self.play(Create(positive_points, run_time=0.5), Create(negative_points, run_time=0.5))
        self.wait(0.5)  # 减少等待时间

        # 初始化决策边界（初始时不可见）
        decision_boundary = always_redraw(lambda: self.get_decision_boundary(W, b, axes))
        self.add(decision_boundary)
        decision_boundary.set_opacity(0)

        # 训练模型
        n_epochs = 12  # 训练轮数
        for epoch in range(n_epochs):
            # 前向传播
            z = np.dot(X, W) + b
            output = np.array([1 if x > 0 else -1 for x in z])

            # 更新权重和偏置
            errors = 0
            for i in range(len(output)):
                if labels[i] * output[i] <= 0:
                    W = W + labels[i] * X[i]
                    b = b + labels[i]
                    errors += 1

            # 更新决策边界
            if W[0] != 0 or W[1] != 0:
                decision_boundary.set_opacity(1)
                self.play(
                    decision_boundary.animate.become(self.get_decision_boundary(W, b, axes)),
                    run_time=0.1 # 减少动画时间
                )
            else:
                decision_boundary.set_opacity(0)

            # 显示当前的 epoch 和错误数量
            epoch_text = Text(f"Epoch: {epoch + 1}, Errors: {errors}", font_size=24).to_corner(UP + RIGHT)
            self.play(Write(epoch_text, run_time=0.1))
            self.wait(0.5)  # 减少等待时间
            self.play(FadeOut(epoch_text, run_time=0.1))

        self.wait(0.5)  # 减少最终等待时间

    def get_decision_boundary(self, W, b, axes):
        if W[1] != 0:
            x_min, x_max = axes.x_range[0], axes.x_range[1]
            y_min = (-W[0] * x_min - b) / W[1]
            y_max = (-W[0] * x_max - b) / W[1]
            return Line(
                axes.coords_to_point(x_min, y_min),
                axes.coords_to_point(x_max, y_max),
                color=GREEN
            )
        elif W[0] != 0:
            x_boundary = -b / W[0]
            y_min, y_max = axes.y_range[0], axes.y_range[1]
            return Line(
                axes.coords_to_point(x_boundary, y_min),
                axes.coords_to_point(x_boundary, y_max),
                color=GREEN
            )
        return Line(ORIGIN, ORIGIN, color=WHITE).set_opacity(0)

