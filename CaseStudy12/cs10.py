import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Lecture10Scene(PrimeScene, ThreeDScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        CAM_RIGHT = np.array([-1, 1, 0])
        CAM_UP = 5 / 4 * np.array([0, 0, 1])
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

        axes_defaults = {"color": dark_blue, "include_numbers": True}

        cam_phi = 75 * DEGREES
        cam_theta = 45 * DEGREES

        self.set_camera_orientation(
            phi=cam_phi, theta=cam_theta, focal_distance=10000000
        )

        ar = [-2, 4, 1]
        axes = ThreeDAxes(
            x_range=ar, y_range=ar, z_range=ar, **{"axis_config": axes_defaults}
        ).move_to(ORIGIN)

        # Create unit vectors using the axes' coordinates
        e1 = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(1, 0, 0), color=blue)
        e2 = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 1, 0), color=blue)
        e3 = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 0, 1), color=blue)

        # Labels at the tip of each vector
        e1_label = (
            MathTex(r"\mathbf{e}_1", color=blue)
            .next_to(e1.get_end(), RIGHT)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(180 * DEGREES, axis=np.array([0, 0, 1]))[0]
        )
        e2_label = (
            MathTex(r"\mathbf{e}_2", color=blue)
            .next_to(e2.get_end(), UP)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(90 * DEGREES, axis=np.array([0, 0, 1]))[0]
        )
        e3_label = (
            MathTex(r"\mathbf{e}_3", color=blue)
            .next_to(e3.get_end(), OUT)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(135 * DEGREES, axis=np.array([0, 0, 1]))[0]
        )

        # Add everything to the scene
        self.add(axes)
        self.wait()
        self.play(
            LaggedStart(
                GrowFromCenter(e1),
                GrowFromCenter(e2),
                GrowFromCenter(e3),
                lag_ratio=0.5,
            )
        )
        self.play(
            LaggedStart(
                GrowFromCenter(e1_label),
                GrowFromCenter(e2_label),
                GrowFromCenter(e3_label),
                lag_ratio=0.5,
            )
        )

        eq0 = MathTex(
            r"\mathbf{e}_1 \cdot \mathbf{e}_2 = "
            r"\begin{bmatrix} 1\\ 0\\ 0 \end{bmatrix}"
            r" \cdot \begin{bmatrix} 0\\ 1\\ 0 "
            r"\end{bmatrix} = 0 ",
            color=dark_blue,
            font_size=30,
        )[0]
        eq0.rotate(90 * DEGREES, axis=RIGHT)
        eq0.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq0.shift(3.5 * CAM_RIGHT + 2.5 * CAM_UP)
        eq0[0:2].set_color(blue)
        eq0[3:5].set_color(blue)

        eq1 = MathTex(
            r"\mathbf{e}_2 \cdot \mathbf{e}_3 = "
            r"\begin{bmatrix} 0\\ 1\\ 0 \end{bmatrix} "
            r"\cdot \begin{bmatrix} 0\\ 0\\ 1 "
            r"\end{bmatrix} = 0 ",
            color=dark_blue,
            font_size=30,
        )[0]
        eq1.rotate(90 * DEGREES, axis=RIGHT)
        eq1.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq1.shift(3.5 * CAM_RIGHT + 1.5 * CAM_UP)
        eq1[0:2].set_color(blue)
        eq1[3:5].set_color(blue)

        eq2 = MathTex(
            r"\mathbf{e}_3 \cdot \mathbf{e}_1 = "
            r"\begin{bmatrix} 0\\ 0\\ 1 \end{bmatrix} "
            r"\cdot \begin{bmatrix} 1\\ 0\\ 0 "
            r"\end{bmatrix} = 0 ",
            color=dark_blue,
            font_size=30,
        )[0]
        eq2.rotate(90 * DEGREES, axis=RIGHT)
        eq2.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq2.shift(3.5 * CAM_RIGHT + 0.5 * CAM_UP)
        eq2[0:2].set_color(blue)
        eq2[3:5].set_color(blue)

        self.wait()

        self.play(
            LaggedStart(
                ReplacementTransform(e1_label.copy(), eq0[0:2]),
                GrowFromCenter(eq0[2]),
                ReplacementTransform(e2_label.copy(), eq0[3:5]),
                Write(eq0[5:]),
                lag_ratio=0.5,
            )
        )
        self.play(
            LaggedStart(
                ReplacementTransform(e2_label.copy(), eq1[0:2]),
                GrowFromCenter(eq1[2]),
                ReplacementTransform(e3_label.copy(), eq1[3:5]),
                Write(eq1[5:]),
                lag_ratio=0.5,
            )
        )
        self.play(
            LaggedStart(
                ReplacementTransform(e3_label.copy(), eq2[0:2]),
                GrowFromCenter(eq2[2]),
                ReplacementTransform(e1_label.copy(), eq2[3:5]),
                Write(eq2[5:]),
                lag_ratio=0.5,
            )
        )

        self.wait()

        self.play(
            e1.animate.set_opacity(0.2),
            e2.animate.set_opacity(0.2),
            e3.animate.set_opacity(0.2),
            e1_label.animate.set_opacity(0.2),
            e2_label.animate.set_opacity(0.2),
            e3_label.animate.set_opacity(0.2),
        )

        n1 = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 2, 0), color=red)
        n2 = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 0, 3), color=red)
        n1_label = (
            MathTex(r"\begin{bmatrix} 0\\ 2\\ 0 \end{bmatrix}", font_size=30, color=red)
            .next_to(n1.get_end(), UP)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(90 * DEGREES, axis=np.array([0, 0, 1]))[0]
        )
        n2_label = (
            MathTex(r"\begin{bmatrix} 0\\ 0\\ 3 \end{bmatrix}", font_size=30, color=red)
            .next_to(n2.get_end(), UP)
            .rotate(90 * DEGREES, axis=RIGHT)
            .rotate(135 * DEGREES, axis=np.array([0, 0, 1]))[0]
        )

        self.play(
            LaggedStart(
                GrowFromCenter(n1),
                GrowFromCenter(n2),
                GrowFromCenter(n1_label),
                GrowFromCenter(n2_label),
                lag_ratio=0.5,
            )
        )

        eq3 = MathTex(
            r"\begin{bmatrix} 0\\ 2\\ 0 \end{bmatrix} "
            r"\cdot "
            r"\begin{bmatrix} 0\\ 0\\ 3 \end{bmatrix}"
            r" = 0",
            color=dark_blue,
            font_size=40,
        )[0]
        eq3.rotate(90 * DEGREES, axis=RIGHT)
        eq3.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq3.shift(-3.5 * CAM_RIGHT + 1.5 * CAM_UP)
        eq3[0:7].set_color(red)
        eq3[8:15].set_color(red)

        self.play(
            LaggedStart(
                ReplacementTransform(n1_label.copy(), eq3[0:7]),
                GrowFromCenter(eq3[7]),
                ReplacementTransform(n2_label.copy(), eq3[8:15]),
                Write(eq3[15:]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        self.play(
            FadeOut(n1_label), FadeOut(n2_label), FadeOut(n1), FadeOut(n2), FadeOut(eq3)
        )
        self.wait()

        self.play(
            e1.animate.set_opacity(1),
            e2.animate.set_opacity(1),
            e3.animate.set_opacity(1),
            e1_label.animate.set_opacity(1),
            e2_label.animate.set_opacity(1),
            e3_label.animate.set_opacity(1),
        )
        self.wait()

        eq4 = MathTex(
            r"\mathbf{e}_1 \cdot \mathbf{e}_1 = "
            r"\begin{bmatrix} 1\\ 0\\ 0 \end{bmatrix}"
            r" \cdot \begin{bmatrix} 1\\ 0\\ 0 "
            r"\end{bmatrix} = 1 ",
            color=dark_blue,
            font_size=30,
        )[0]
        eq4.rotate(90 * DEGREES, axis=RIGHT)
        eq4.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq4.shift(-3.5 * CAM_RIGHT + 1.5 * CAM_UP)
        eq4[0:2].set_color(blue)
        eq4[3:5].set_color(blue)

        self.play(
            LaggedStart(
                ReplacementTransform(e1_label.copy(), eq4[0:2]),
                GrowFromCenter(eq4[2]),
                ReplacementTransform(e1_label.copy(), eq4[3:5]),
                Write(eq4[5:]),
                lag_ratio=0.5,
            )
        )
        self.wait()

        self.play(Unwrite(eq0), Unwrite(eq1), Unwrite(eq2), Unwrite(eq4))

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
            y_range=(0, 46, 1),
        ).scale(UNIT)

        self.play(
            LaggedStart(
                Write(grid),
                ShrinkToCenter(axes),
                ShrinkToCenter(e1),
                ShrinkToCenter(e2),
                ShrinkToCenter(e3),
                lag_ratio=0.5,
            )
        )

        eq5 = MathTex(
            r"\begin{bmatrix} \mathbf{e}_1 & \mathbf{e}_2 & \mathbf{e}_3 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq5.shift(eq5[1].get_bottom()[1] * DOWN)
        eq5[1:7].set_color(blue)

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            run_time=3,
            added_anims=[
                ReplacementTransform(e1_label, eq5[1:3]),
                ReplacementTransform(e2_label, eq5[3:5]),
                ReplacementTransform(e3_label, eq5[5:7]),
            ],
        )

        self.wait()
        self.play(LaggedStart(Write(eq5[0]), Write(eq5[7]), lag_ratio=0.5))
        self.wait()

        eq6 = MathTex(
            r"\begin{bmatrix} 1 & 0 & 0\\ 0 & 1 & 0\\ 0 & 0 & 1 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq6.shift(eq6[5].get_bottom()[1] * DOWN)

        self.play(
            LaggedStart(
                ReplacementTransform(eq5[0], eq6[0:2]),
                ReplacementTransform(eq5[1:3], VGroup(eq6[2], eq6[5], eq6[8])),
                ReplacementTransform(eq5[3:5], VGroup(eq6[3], eq6[6], eq6[9])),
                ReplacementTransform(eq5[5:7], VGroup(eq6[4], eq6[7], eq6[10])),
                ReplacementTransform(eq5[7], eq6[11:]),
                lag_ratio=0.5,
            )
        )
        self.wait()

        eq7 = MathTex(
            r"\begin{bmatrix} 0 & 0 & 1\\ 1 & 0 & 0\\ 0 & 1 & 0 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq7.shift(eq7[5].get_bottom()[1] * DOWN)

        self.play(
            ReplacementTransform(eq6[0:2], eq7[0:2]),
            ReplacementTransform(
                VGroup(eq6[3], eq6[6], eq6[9]), VGroup(eq7[2], eq7[5], eq7[8])
            ),
            ReplacementTransform(
                VGroup(eq6[4], eq6[7], eq6[10]), VGroup(eq7[3], eq7[6], eq7[9])
            ),
            ReplacementTransform(
                VGroup(eq6[2], eq6[5], eq6[8]), VGroup(eq7[4], eq7[7], eq7[10])
            ),
            ReplacementTransform(eq6[11:], eq7[11:]),
        )
        self.wait()

        eq8 = MathTex(r"A^TA = I", color=dark_blue, font_size=40)[0]
        eq8.shift(eq8[0].get_bottom()[1] * DOWN)
        eq7b = MathTex(r"A = ", color=dark_blue, font_size=40)[0]
        eq7b.shift(eq7b[0].get_bottom()[1] * DOWN + 3 * UNIT * UP + 2 * UNIT * LEFT)
        self.play(
            LaggedStart(eq7.animate.shift(3 * UNIT * UP), FadeIn(eq7b), lag_ratio=0.5)
        )
        self.wait()
        self.play(Write(eq8))
        self.wait()
        self.play(FadeOut(eq8))

        # eq9 = MathTex(
        #     r"\begin{bmatrix} 0 & 0 & 1\\ 1 & 0 & 0\\ 0 & 1 & 0 \end{bmatrix}^T \begin{bmatrix} 0 & 0 & 1\\ 1 & 0 & 0\\ 0 & 1 & 0 \end{bmatrix} = I",
        #     color=dark_blue, font_size=40)[0]
        # eq9.shift(eq9[len(eq9) -1].get_bottom()[1] * DOWN)
        # self.play(ShrinkToCenter(eq8[0]), ReplacementTransform(eq7.copy(), eq9[0:13]), ReplacementTransform(eq8[1], eq9[13]), ShrinkToCenter(eq8[2]), ReplacementTransform(eq7.copy(), eq9[14:27]), ReplacementTransform(eq8[3:], eq9[27:]))
        # self.wait()
        # self.play(Wiggle(eq9[13], scale_value=1.5))
        # self.wait()
        #
        # #transpose matrix
        # eq10 = MathTex(
        #     r"\begin{bmatrix} 0 & 1 & 0\\ 0 & 0 & 1\\ 1 & 0 & 0 \end{bmatrix} \begin{bmatrix} 0 & 0 & 1\\ 1 & 0 & 0\\ 0 & 1 & 0 \end{bmatrix} = I",
        #     color=dark_blue, font_size=40)[0]
        # eq10.shift(eq10[len(eq10) - 1].get_bottom()[1] * DOWN)
        #
        # self.play(ReplacementTransform(eq9[14:], eq10[13:]), ReplacementTransform(eq9[:2], eq10[:2]),
        #           ReplacementTransform(eq9[11:13], eq10[11:13]), ShrinkToCenter(eq9[13]),
        #           ReplacementTransform(eq9[2], eq10[2]), ReplacementTransform(eq9[6], eq10[6]), ReplacementTransform(eq9[10], eq10[10]),
        #           ReplacementTransform(eq9[3], eq10[5]), ReplacementTransform(eq9[4], eq10[8]), ReplacementTransform(eq9[5], eq10[3]),
        #           ReplacementTransform(eq9[7], eq10[9]), ReplacementTransform(eq9[8], eq10[4]), ReplacementTransform(eq9[9], eq10[7])
        #           )
        # self.wait()
        #
        # # is there a point in showing matrix multiplication?
        #
        # eq11 = MathTex(
        #     r"\begin{bmatrix} 1 & 0 & 0\\ 0 & 1 & 0\\ 0 & 0 & 1 \end{bmatrix} = I",
        #     color=dark_blue, font_size=40)[0]
        # eq11.shift(eq11[len(eq11) - 1].get_bottom()[1] * DOWN)
        #
        # self.play(ShrinkToCenter(eq10[11:15]), ReplacementTransform(eq10[0], eq11[0]), ReplacementTransform(VGroup(eq10[1:11].submobjects, eq10[15:23].submobjects), eq11[1:10]), ReplacementTransform(eq10[23:25], eq11[10:12]), ReplacementTransform(eq10[25:], eq11[12:]))
        # self.wait()
        #
        # self.play(FadeOut(eq11))
        # self.wait()

        eq12 = MathTex(
            r"\begin{bmatrix} \cos{\psi} & -\sin{\psi} & 0\\ \sin{\psi} & \cos{\psi} & 0\\ 0 & 0 & 1 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq12.shift(eq12[12].get_bottom()[1] * DOWN)
        self.play(Write(eq12))
        self.wait()

        eq13 = MathTex(
            r"\begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix}0\\1\\0\end{bmatrix} = \begin{bmatrix}-\sin\psi\\\cos\psi\\0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq13.shift(
            eq13[12].get_bottom()[1] * DOWN
            + eq13[0].get_left()[0] * LEFT
            + 3 * UNIT * UP
            + 4 * UNIT * LEFT
        )

        eq14 = MathTex(
            r"\begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix}0\\0\\1\end{bmatrix} = \begin{bmatrix}0\\0\\1\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq14.shift(
            eq14[12].get_bottom()[1] * DOWN
            + eq14[0].get_left()[0] * LEFT
            + 4 * UNIT * LEFT
        )

        eq15 = MathTex(
            r"\begin{bmatrix} \cos\psi & -\sin\psi & 0 \\ \sin\psi & \cos\psi & 0 \\ 0 & 0 & 1 \end{bmatrix} \begin{bmatrix}1\\0\\0\end{bmatrix} = \begin{bmatrix}\cos\psi\\\sin\psi\\0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq15.shift(
            eq15[12].get_bottom()[1] * DOWN
            + eq15[0].get_left()[0] * LEFT
            + 3 * UNIT * DOWN
            + 4 * UNIT * LEFT
        )

        self.play(eq12.animate.shift(3 * UNIT * LEFT))
        self.wait()

        self.play(
            LaggedStart(
                FadeOut(eq7b),
                FadeOut(VGroup(eq7[0:2], eq7[11:13])),
                ReplacementTransform(VGroup(eq7[2], eq7[5], eq7[8]), eq13[28:31]),
                FadeIn(VGroup(eq13[26:28], eq13[31:33])),
                ReplacementTransform(VGroup(eq7[3], eq7[6], eq7[9]), eq14[28:31]),
                FadeIn(VGroup(eq14[26:28], eq14[31:33])),
                ReplacementTransform(VGroup(eq7[4], eq7[7], eq7[10]), eq15[28:31]),
                FadeIn(VGroup(eq15[26:28], eq15[31:33])),
                lag_ratio=0.1,
            )
        )
        self.wait()

        self.play(
            LaggedStart(
                ReplacementTransform(eq12.copy(), eq13[:26]),
                Write(eq13[33:]),
                ReplacementTransform(eq12.copy(), eq15[:26]),
                Write(eq15[33:]),
                ReplacementTransform(eq12, eq14[:26]),
                Write(eq14[33:]),
                lag_ratio=0.5,
            )
        )

        self.wait()

        eq16 = MathTex(
            r"\begin{bmatrix}\cos{\psi} & -\sin{\psi} & 0\\\sin{\psi} & \cos{\psi} & 0\\0 & 0 & 1\end{bmatrix} \begin{bmatrix}0 & 0 & 1\\1 & 0 & 0\\0 & 1 & 0\end{bmatrix} =\begin{bmatrix}-\sin\psi & 0 & \cos\psi \\\cos\psi & 0 & \sin\psi \\0 & 1 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq16.shift(eq16[12].get_bottom()[1] * DOWN)

        # UNIFY ROT MATRIX
        self.play(
            *[
                ReplacementTransform(VGroup(eq13[i], eq14[i], eq15[i]), eq16[i])
                for i in range(26)
            ]
        )

        # MAKE A MATRIX OUT OF VECTORS
        self.play(
            ReplacementTransform(eq13[26:28], eq16[26:28]),
            FadeOut(
                VGroup(
                    eq13[31:33].submobjects,
                    eq14[26:28].submobjects,
                    eq14[31:33].submobjects,
                    eq15[26:28].submobjects,
                )
            ),
            ReplacementTransform(eq15[31:33], eq16[37:39]),
            ReplacementTransform(eq13[28:31], VGroup(eq16[28], eq16[31], eq16[34])),
            ReplacementTransform(eq14[28:31], VGroup(eq16[29], eq16[32], eq16[35])),
            ReplacementTransform(eq15[28:31], VGroup(eq16[30], eq16[33], eq16[36])),
        )

        # UNIFY EQUAL SIGNS
        self.play(
            ReplacementTransform(VGroup(eq13[33], eq14[33], eq15[33]), eq16[39]),
        )

        # MAKE THE RESULT MATRIX OUT OF VECTORS
        self.play(
            ReplacementTransform(eq13[34:36], eq16[40:42]),
            FadeOut(
                VGroup(
                    eq13[46:].submobjects,
                    eq14[34:36].submobjects,
                    eq14[39:].submobjects,
                    eq15[34:36].submobjects,
                )
            ),
            ReplacementTransform(eq15[45:], eq16[64:]),
            ReplacementTransform(
                eq13[36:46],
                VGroup(eq16[42:47].submobjects, eq16[52:56].submobjects, eq16[61]),
            ),
            ReplacementTransform(eq14[36:39], VGroup(eq16[47], eq16[56], eq16[62])),
            ReplacementTransform(
                eq15[36:45], VGroup(eq16[48:52], eq16[57:61], eq16[63])
            ),
        )
        self.wait()

        eq17 = MathTex(
            r"\begin{bmatrix}-\sin\psi & 0 & \cos\psi \\\cos\psi & 0 & \sin\psi \\0 & 1 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq17.shift(eq17[12].get_bottom()[1] * DOWN)

        self.play(
            LaggedStart(
                FadeOut(eq16[:40]), ReplacementTransform(eq16[40:], eq17), lag_ratio=0.5
            )
        )
        self.wait()
        self.play(eq17.animate.scale(1.3))
        self.wait()
