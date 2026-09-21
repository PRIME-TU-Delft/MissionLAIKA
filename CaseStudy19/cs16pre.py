from manim import *
from primescene import *


class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4

        airplane_svg = SVGMobject("../assets/AirplaneFront.svg")
        airplane_svg.set_color(WHITE).set_stroke(color=WHITE, width=12).scale(2).shift(
            5.5 * UNIT * LEFT + UP
        )

        self.camera.frame.shift(5.5 * UNIT * LEFT + 0.05 * UP).scale(1.5)
        self.wait()
        self.play(Write(airplane_svg))
        self.wait()
