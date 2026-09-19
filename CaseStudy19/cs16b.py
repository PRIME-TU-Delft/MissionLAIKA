from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")
        green = ManimColor("#009B77")

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

        eq6 = MathTex(
            r"\mathbf{\ddot u} + A\mathbf{u}= \mathbf{0}", color=dark_blue, font_size=48
        )[0]
        eq6.shift(eq6[1].get_bottom()[1] * DOWN + 4 * UNIT * UP + 7 * UNIT * RIGHT)
        eq6[1].set_color(yellow)
        eq6[4].set_color(yellow)

        eq7 = MathTex(
            r"A\mathbf{v}_i = \lambda_i\mathbf{v}_i", color=dark_blue, font_size=48
        )[0]
        eq7.shift(eq7[1].get_bottom()[1] * DOWN + 2 * UNIT * LEFT + UNIT * UP)

        eq8 = MathTex(r"\lambda_i = \omega_i^2", color=dark_blue, font_size=48)[0]
        eq8.shift(eq8[0].get_bottom()[1] * DOWN + 2 * UNIT * RIGHT + UNIT * UP)

        eq9 = MathTex(
            r"P = \begin{bmatrix} \mathbf{v_1} & \mathbf{v_2} & \dots & \mathbf{v_n} \end{bmatrix}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq9.shift(eq9[0].get_bottom()[1] * DOWN + 4 * UNIT * LEFT + UNIT * DOWN)

        eq10 = MathTex(
            r"D= \begin{bmatrix} \omega_1^2 & 0 & 0 \\ 0 & \ddots & 0 \\0 & 0 & \omega_n^2   \end{bmatrix}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq10.shift(eq10[0].get_bottom()[1] * DOWN + 5 * UNIT * RIGHT + UNIT * DOWN)

        eq11 = MathTex(r"A = PDP^{-1}", color=dark_blue, font_size=48)[0]
        eq11.shift(eq11[0].get_bottom()[1] * DOWN + 3 * UNIT * DOWN)

        self.add(grid, eq6, eq7, eq8, eq9, eq10, eq11)

        self.play(self.camera.frame.animate.shift(19 * UNIT * RIGHT))
        self.wait()

        eq20 = MathTex(
            r"\text{for every } \mathbf{x}\neq{\mathbf{0}},  \mathbf{x}^TM\mathbf{x} > 0",
            color=dark_blue,
            font_size=48,
        )[0]
        eq20.shift(eq20[0].get_bottom()[1] * DOWN + 14 * UNIT * RIGHT)

        eq21 = MathTex(
            r"\text{for every } \mathbf{x}\neq{\mathbf{0}},  \mathbf{x}^TK\mathbf{x} > 0",
            color=dark_blue,
            font_size=48,
        )[0]
        eq21.shift(eq21[0].get_bottom()[1] * DOWN + 24 * UNIT * RIGHT)

        eq20a = MathTex(r"M=M^T", color=dark_blue, font_size=48)[0]
        eq20a.shift(eq20a[0].get_bottom()[1] * DOWN + 14 * UNIT * RIGHT)

        eq21a = MathTex(r"K=K^T", color=dark_blue, font_size=48)[0]
        eq21a.shift(eq21a[0].get_bottom()[1] * DOWN + 24 * UNIT * RIGHT)

        eq22 = MathTex(
            r"\text{for every } \mathbf{x}\neq{\mathbf{0}},  \mathbf{x}^TM^{-1}\mathbf{x} > 0",
            color=dark_blue,
            font_size=48,
        )[0]
        eq22.shift(eq22[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(GrowFromCenter(eq20), GrowFromCenter(eq21))
        self.wait()
        self.play(
            GrowFromCenter(eq20a),
            GrowFromCenter(eq21a),
            Group(eq20, eq21).animate.shift(UNIT * UP),
        )
        self.wait()
        self.play(Write(eq22), Group(eq20, eq20a, eq21, eq21a).animate.shift(UNIT * UP))
        self.wait()

        eq27a = MathTex(r"\mathbf{x}^TM^{-1}\mathbf{x}", color=dark_blue, font_size=48)[
            0
        ]
        eq27a.shift(eq27a[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27b = MathTex(
            r"\mathbf{x}^TM^{-1}MM^{-1}\mathbf{x}", color=dark_blue, font_size=48
        )[0]
        eq27b.shift(eq27b[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27c = MathTex(
            r"\mathbf{x}^T\left(M^{-1}\right)^TMM^{-1}\mathbf{x}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq27c.shift(eq27c[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27d = MathTex(
            r"\left(M^{-1}\mathbf{x}\right)^TM\left(M^{-1}\mathbf{x}\right)",
            color=dark_blue,
            font_size=48,
        )[0]
        eq27d.shift(eq27d[1].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27e = MathTex(r"\mathbf{y}^TM\mathbf{y}", color=dark_blue, font_size=48)[0]
        eq27e.shift(eq27e[2].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27f = MathTex(r"\mathbf{y}^TM\mathbf{y}>0", color=dark_blue, font_size=48)[0]
        eq27f.shift(eq27f[2].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(
            ReplacementTransform(eq22[13:19].copy(), eq27a),
            Group(eq20, eq20a, eq21, eq21a, eq22).animate.shift(2 * UNIT * UP),
        )
        self.wait()

        self.play(
            ReplacementTransform(eq27a[:5], eq27b[:5]),
            ReplacementTransform(eq27a[5], eq27b[9]),
            GrowFromCenter(eq27b[5:9]),
        )
        self.wait()

        self.play(
            ReplacementTransform(eq27b[:2], eq27c[:2]),
            ReplacementTransform(eq27b[2:5], eq27c[3:6]),
            ReplacementTransform(eq27b[5:], eq27c[8:]),
            GrowFromCenter(eq27c[2]),
            GrowFromCenter(eq27c[6]),
            GrowFromCenter(eq27c[7]),
        )
        self.wait()

        self.play(
            ReplacementTransform(Group(eq27c[1], eq27c[7]), eq27d[6]),
            ReplacementTransform(eq27c[0], eq27d[4]),
            ReplacementTransform(eq27c[3:6], eq27d[1:4]),
            ReplacementTransform(eq27c[2], eq27d[0]),
            ReplacementTransform(eq27c[6], eq27d[5]),
            ReplacementTransform(eq27c[8], eq27d[7]),
            ReplacementTransform(eq27c[9:13], eq27d[9:13]),
            GrowFromCenter(eq27d[8]),
            GrowFromCenter(eq27d[13]),
        )
        self.wait()

        self.play(
            ReplacementTransform(eq27d[:6], eq27e[0]),
            ReplacementTransform(eq27d[6], eq27e[1]),
            ReplacementTransform(eq27d[7], eq27e[2]),
            ReplacementTransform(eq27d[8:], eq27e[3]),
        )
        self.wait()

        self.play(
            ReplacementTransform(eq27e[:4], eq27f[:4]),
            GrowFromCenter(eq27f[4:]),
        )
        self.wait()

        self.play(FadeOut(eq27f))
        self.wait()

        eq28 = MathTex(
            r"M^{-1}K\mathbf{v}_i = \lambda_i\mathbf{v}_i \Rightarrow \lambda_i > 0",
            color=dark_blue,
            font_size=48,
        )[0]
        eq28.shift(eq28[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(Write(eq28))
        self.wait()

        self.play(self.camera.frame.animate.shift(19 * UNIT * LEFT))
        self.wait()

        self.play(Indicate(eq8, color=green, scale_factor=1.2))
        self.wait()
