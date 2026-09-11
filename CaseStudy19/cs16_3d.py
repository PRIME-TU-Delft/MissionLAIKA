import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor('#FFFFFF')


class Lecture14Scene(PrimeScene, ThreeDScene):
    def construct(self):
        super().construct()
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31')
        yellow = ManimColor('#cc9316')
        blue = ManimColor('#0076C2')
        green = ManimColor('#009B77')
        CAM_RIGHT = np.array([-1, 1, 0])
        CAM_UP = 5 / 4 * np.array([0, 0, 1])
        UNIT = 3/4

        axes_defaults = {
            "color": dark_blue,
            "include_numbers": False
        }

        ar = [-3, 3, 1]
        axes = ThreeDAxes(
            x_range=ar,
            y_range=ar,
            z_range=[-2, 2, 1],
            x_length=10.5,
            y_length=10.5,
            z_length=7.0,
            axis_config=axes_defaults
        )

        unit_x_vec = axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)
        unit_length = np.linalg.norm(unit_x_vec)

        grid2 = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,
                "stroke_width": 0
            },
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            shade_in_3d=True,
        ).scale(UNIT)

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
        self.wait(1)
        self.play(FadeOut(grid), FadeIn(grid2))

        self.move_camera(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            focal_distance=10000000,
            run_time=3,
            added_anims=[LaggedStart(grid2.animate.scale(unit_length/UNIT), Write(axes), lag_ratio=0.5)]
        )
        self.wait(1)

        surface = Surface(
            lambda u, v: axes.c2p(
                u,
                v,
                3 * u ** 2 - 2 * u * v + 2 * v ** 2
            ),
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(40, 40),
        )

        surface.set_style(
            fill_opacity=0.5,
            stroke_color=red,
            stroke_width=0.5,
            fill_color=red
        )
        self.play(Create(surface), run_time=3)

        def rotate_camera(time):
            self.play(
                theta.animate(run_time=time / 2.0, rate_func=rate_functions.ease_in_sine).set_value(225 * DEGREES))
            self.play(
                theta.animate(run_time=time / 2.0, rate_func=rate_functions.ease_out_sine).set_value(405 * DEGREES))
            theta.set_value(45 * DEGREES)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        rotate_camera(4)
        self.wait(1)
        self.play(FadeOut(surface))
        self.wait(1)


        grid3 = NumberPlane(background_line_style={
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
        self.wait(1)

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            run_time=3,
            added_anims=[grid2.animate.scale(UNIT / unit_length), FadeOut(axes)]
        )
        self.play(FadeOut(grid2), FadeIn(grid3))
        self.wait(1)


