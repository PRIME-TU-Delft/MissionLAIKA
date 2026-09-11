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

        grid = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 2  # thicker lines
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        self.add(grid)



        eq1 = MathTex(
            r"M \text{ positive-definite}",
            color=dark_blue, font_size=48)[0]
        eq1.shift(eq1[0].get_bottom()[1] * DOWN + 5 * UNIT * LEFT)

        eq2 = MathTex(
            r"K \text{ positive-definite}",
            color=dark_blue, font_size=48)[0]
        eq2.shift(eq2[0].get_bottom()[1] * DOWN + 5 * UNIT * RIGHT)

        self.play(GrowFromCenter(eq1), GrowFromCenter(eq2))
        self.wait()
        self.play(FadeOut(eq1), FadeOut(eq2))
