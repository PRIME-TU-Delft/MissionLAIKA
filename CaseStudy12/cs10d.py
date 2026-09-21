import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Lecture10Scene(PrimeScene, ThreeDScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

        axes_defaults = {"color": dark_blue, "include_numbers": True}

        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        ar = [-3, 3, 1]
        axes = ThreeDAxes(x_range=ar, y_range=ar, z_range=ar, axis_config=axes_defaults)
        self.add(axes)

        cube = Cube(
            side_length=2 * UNIT,
            fill_color=blue,
            fill_opacity=0.5,
            stroke_color=dark_blue,
            stroke_width=0,
        ).move_to(ORIGIN)

        cube.save_state()
        self.play(FadeIn(cube))
        self.wait(1)

        angle = np.pi / 4

        Rz = np.array(
            [
                [np.cos(angle), -np.sin(angle), 0],
                [np.sin(angle), np.cos(angle), 0],
                [0, 0, 1],
            ]
        )

        S = np.array(
            [
                [1, 1, 0],
                [0, 1, 0],
                [0, 0, 1],
            ]
        )

        D = np.array(
            [
                [2, 0, 0],
                [0, 0.5, 0],
                [0, 0, 3],
            ]
        )

        T = D @ S @ Rz

        Rz_tex = MathTex(
            r"R_z = \begin{bmatrix}"
            r"\cos\left(\frac{\pi}{4}\right) & -\sin\left(\frac{\pi}{4}\right) & 0 \\"
            r"\sin\left(\frac{\pi}{4}\right) & \cos\left(\frac{\pi}{4}\right) & 0 \\"
            r"0 & 0 & 1"
            r"\end{bmatrix}",
            color=dark_blue,
            font_size=32,
        ).to_corner(UR)

        S_tex = MathTex(
            r"S = \begin{bmatrix}"
            r"1 & 1 & 0 \\"
            r"0 & 1 & 0 \\"
            r"0 & 0 & 1"
            r"\end{bmatrix}",
            color=dark_blue,
            font_size=32,
        ).to_corner(UR)

        D_tex = MathTex(
            r"D = \begin{bmatrix}"
            r"2 & 0 & 0 \\"
            r"0 & 0.5 & 0 \\"
            r"0 & 0 & 3"
            r"\end{bmatrix}",
            color=dark_blue,
            font_size=32,
        ).to_corner(UR)

        T_tex = MathTex(r"T = D S R_z", color=dark_blue, font_size=32).to_corner(UR)

        def rotate_camera(time):
            self.play(
                theta.animate(
                    run_time=time / 2.0, rate_func=rate_functions.ease_in_sine
                ).set_value(225 * DEGREES)
            )
            self.play(
                theta.animate(
                    run_time=time / 2.0, rate_func=rate_functions.ease_out_sine
                ).set_value(405 * DEGREES)
            )
            theta.set_value(45 * DEGREES)

        def show_matrix_transform(matrix, tex, run_time=2):
            self.add_fixed_in_frame_mobjects(tex)
            self.play(FadeIn(tex))
            self.play(ApplyMatrix(matrix, cube), run_time=run_time)

            rotate_camera(time=6)

            self.play(FadeOut(tex))
            self.play(Restore(cube), run_time=run_time)

        phi, theta, focal_distance, gamma, distance_to_origin = (
            self.camera.get_value_trackers()
        )

        rotate_camera(time=4)

        show_matrix_transform(Rz, Rz_tex)
        show_matrix_transform(S, S_tex)
        show_matrix_transform(D, D_tex)
        show_matrix_transform(T, T_tex)

        self.wait(2)
