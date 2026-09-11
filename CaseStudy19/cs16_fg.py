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
        green = ManimColor('#009B77')


        eq26c = MathTex(
            r"\begin{bmatrix} x_1 & x_2\end{bmatrix}\begin{bmatrix} 3 & -1\\-1 & 2\end{bmatrix}\begin{bmatrix} x_1 \\ x_2\end{bmatrix}=3x_1^2-2x_1x_2+2x_2^2",
            color=dark_blue, font_size=48)[0]
        eq26c.shift(eq26c[1].get_bottom()[1] * DOWN)

        eq26d = MathTex(
            r"f(x_1, x_2)=3x_1^2-2x_1x_2+2x_2^2",
            color=dark_blue, font_size=48)[0]
        eq26d.shift(eq26d[0].get_bottom()[1] * DOWN +4*UNIT*DOWN)

        self.add(eq26c[21:])
        self.play(ReplacementTransform(eq26c[21:], eq26d[9:]), Write(eq26d[:9]))
        self.wait(1)
        self.play(FadeOut(eq26d))
