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
        CAM_RIGHT = np.array([-1, 1, 0])
        CAM_UP = 5 / 4 * np.array([0, 0, 1])

        axes_defaults = {"color": dark_blue, "include_numbers": True}

        ar = [-3, 3, 1]
        axes = ThreeDAxes(
            x_range=ar,
            y_range=ar,
            z_range=[-2, 2, 1],
            x_length=10.5,
            y_length=10.5,
            z_length=7.0,
            axis_config=axes_defaults,
        )

        unit_x_vec = axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)
        unit_length = np.linalg.norm(unit_x_vec)

        self.move_camera(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            focal_distance=10000000,
            run_time=1,
        )

        eq2 = MathTex(
            r"\mathbf{u}(\mathbf{x}_0+\Delta \mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0) + J \Delta \mathbf{x}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq2.rotate(90 * DEGREES, axis=RIGHT)
        eq2.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))

        eq2.shift(-2.5 * CAM_RIGHT + 2 * CAM_UP)
        eq3 = eq2.copy().scale(1.2)

        self.play(Write(eq2))
        self.wait(1)

        self.play(
            ReplacementTransform(eq2[9:14], eq3[9:14]),
            eq2[:9].animate.set_opacity(0.5),
            eq2[14:].animate.set_opacity(0.5),
        )
        self.wait(1)

        self.play(ReplacementTransform(eq2[14:], eq3[14:]))
        self.wait(1)

        self.play(ReplacementTransform(eq2[:9], eq3[:9]))
        self.wait(1)
        self.play(FadeOut(eq3))
        self.wait(1)
