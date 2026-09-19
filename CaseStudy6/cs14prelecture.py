import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Lecture14Scene(PrimeScene, ThreeDScene):
    def construct(self):
        super().construct()
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")
        green = ManimColor("#009B77")
        UNIT = 3 / 4

        grid = NumberPlane(
            background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15,
            },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 2,  # thicker lines
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        eq0 = MathTex(
            r"C = \begin{bmatrix} 0 & 2 \\ 1 & 1 \end{bmatrix}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq0.shift(eq0[0].get_bottom()[1] * DOWN)

        eq1 = MathTex(
            r"\operatorname{det} C = 0 \cdot 1 - 1 \cdot 2 = -2",
            color=dark_blue,
            font_size=48,
        )[0]
        eq1.shift(eq1[0].get_bottom()[1] * DOWN + 3 * UNIT * RIGHT)

        eq2 = MathTex(
            r"\text{Area} = |\operatorname{det} C| = 2", color=dark_blue, font_size=48
        )[0]
        eq2.shift(eq2[0].get_bottom()[1] * DOWN + UNIT * UP + 3 * UNIT * RIGHT)

        small_grid = (
            NumberPlane(
                background_line_style={
                    "stroke_color": green,
                    "stroke_width": 2,
                    "stroke_opacity": 0.15,
                },
                axis_config={
                    "stroke_color": green,  # axes color
                    "stroke_width": 4,  # thicker lines
                    "include_tip": True,
                },
                x_range=(-2, 2, 1),
                y_range=(-1, 2, 1),
            )
            .scale(UNIT)
            .shift(1.5 * UNIT * DOWN)
        )

        square = Square(
            side_length=UNIT,
            color=red,
            fill_color=red,
            fill_opacity=0.5,
        )

        C = np.array([[0, 2], [1, 1]])

        square2 = square.copy()
        square.shift(1.5 * UNIT * DOWN + 0.5 * UNIT * LEFT)
        square2.apply_matrix(C)
        square2.shift(2 * UNIT * DOWN + 1 * UNIT * RIGHT)

        self.add(grid)
        self.wait()
        self.play(Write(eq0))
        self.wait()
        self.play(
            LaggedStart(eq0.animate.shift(5 * UNIT * LEFT), Write(eq1), lag_ratio=0.5)
        )
        self.wait()
        self.play(
            Write(small_grid),
            Write(square),
            eq0.animate.shift(2 * UNIT * UP),
            eq1.animate.shift(2 * UNIT * UP),
        )
        self.wait()
        self.play(ReplacementTransform(square, square2))
        self.wait()
        self.play(Write(eq2))
        self.wait()
