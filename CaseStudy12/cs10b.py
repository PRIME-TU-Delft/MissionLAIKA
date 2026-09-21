import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Lecture10Scene(PrimeScene):
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
        self.add(grid)
        self.wait(1)

        # STARTING AT "Let’s now take a look at these 2, 3 by 2 matrices."

        eq0 = MathTex(
            r"C = \begin{bmatrix}1 & 2\\[4pt]2 & -1\\[4pt]0 & 0\end{bmatrix}, \quad D = \begin{bmatrix}1 & \frac{\sqrt{2}}{2}\\[4pt]0 & \frac{\sqrt{2}}{2}\\[4pt]0 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq0.shift(eq0[0].get_bottom()[1] * DOWN)

        self.play(Write(eq0))
        self.wait(1)

        # column properties
        self.play(
            LaggedStart(
                Wiggle(VGroup(eq0[5], eq0[7], eq0[10])),
                Wiggle(VGroup(eq0[6], eq0[8:10], eq0[11])),
                lag_ratio=0.3,
            )
        )
        self.wait(1)
        self.play(
            LaggedStart(
                Wiggle(VGroup(eq0[22], eq0[28], eq0[34])),
                Wiggle(VGroup(eq0[23:28], eq0[29:34], eq0[35])),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        eq1 = MathTex(
            r"A_{\mathrm{yaw}}(\psi)C=\begin{bmatrix}\cos\psi &"
            r" -\sin\psi & 0\\[4pt]\sin\psi & \cos\psi & 0\\[4pt]0 &"
            r" 0 & 1\end{bmatrix}\begin{bmatrix}1 & 2\\[4pt]2 & -1\\[4pt]0 & 0\end{bmatrix}=\begin{bmatrix}\cos\psi-2\sin\psi &"
            r" 2\cos\psi+\sin\psi\\[6pt]\sin\psi+2\cos\psi &"
            r" 2\sin\psi-\cos\psi\\[6pt]0 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=36,
        )[0]
        eq1.shift(eq1[0].get_bottom()[1] * DOWN)

        eq2 = MathTex(
            r"A_{\mathrm{yaw}}(\psi)D=\begin{bmatrix}\cos\psi &"
            r" -\sin\psi & 0\\[4pt]\sin\psi & \cos\psi & 0\\[4pt]0 & 0 &"
            r" 1\end{bmatrix}\begin{bmatrix}1 & \frac{\sqrt{2}}{2}\\[4pt]0 & \frac{\sqrt{2}}{2}\\[4pt]0 & 0\end{bmatrix} =\begin{bmatrix}\cos\psi &"
            r" \frac{\sqrt{2}}{2}\,(\cos\psi-\sin\psi)\\[8pt]\sin\psi &"
            r" \frac{\sqrt{2}}{2}\,(\sin\psi+\cos\psi)\\[8pt]0 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=36,
        )[0]
        eq2.shift(3 * UNIT * DOWN + eq2[0].get_bottom()[1] * DOWN)
        eq2.align_to(eq1, LEFT)

        self.play(eq0.animate.shift(3 * UNIT * UP))
        self.wait(1)
        self.play(Write(eq1[:9]), Write(eq2[:9]))
        self.wait(1)
        self.play(Write(eq1[9:37]), Write(eq2[9:37]))
        self.play(
            LaggedStart(
                ReplacementTransform(eq0[2:15].copy(), eq1[37:50]),
                ReplacementTransform(eq0[18:].copy(), eq2[37:59]),
                lag_ratio=0.5,
            )
        )
        self.play(Write(eq1[50]), Write(eq2[59]))
        self.play(LaggedStart(Write(eq1[51:]), Write(eq2[60:])))
        self.wait(1)

        eq3 = MathTex(
            r"A_{\text{yaw}}(\psi)C = \begin{bmatrix}\cos\psi-2\sin\psi & 2\cos\psi+\sin\psi\\[6pt]\sin\psi+2\cos\psi & 2\sin\psi-\cos\psi\\[6pt]0 & 0\end{bmatrix},"
            r" \quad A_{\text{yaw}}(\psi)D = \begin{bmatrix}\cos\psi & \frac{\sqrt{2}}{2}\,(\cos\psi-\sin\psi)\\[8pt]\sin\psi & \frac{\sqrt{2}}{2}\,(\sin\psi+\cos\psi)\\[8pt]0 & 0\end{bmatrix}",
            color=dark_blue,
            font_size=32,
        )[0]
        eq3.shift(3 * UNIT * UP + eq3[0].get_bottom()[1] * DOWN)

        self.play(
            LaggedStart(
                ShrinkToCenter(eq1[9:51]),
                ShrinkToCenter(eq2[9:60]),
                eq0.animate.shift(4 * UNIT * UP),
                ReplacementTransform(eq1[:9], eq3[:9]),
                ReplacementTransform(eq1[51:], eq3[9 : 9 + len(eq1[51:])]),
                GrowFromCenter(eq3[9 + len(eq1[51:])]),
                ReplacementTransform(
                    eq2[:9], eq3[9 + len(eq1[51:]) + 1 : 9 + len(eq1[51:]) + 10]
                ),
                ReplacementTransform(eq2[60:], eq3[9 + len(eq1[51:]) + 10 :]),
                lag_ratio=0.3,
            )
        )
        self.wait(1)

        eq4 = MathTex(
            r"\begin{bmatrix}\cos\psi-2\sin\psi\\[6pt]\sin\psi+2\cos\psi\\[6pt]0\end{bmatrix}\centerdot\begin{bmatrix}2\cos\psi+\sin\psi\\[6pt]2\sin\psi-\cos\psi\\[6pt]0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq4.shift(eq4[14].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq4[4:25].set_color(blue)
        eq4[34:55].set_color(red)

        self.play(
            eq3[13:23].animate.set_color(blue),
            eq3[33:43].animate.set_color(blue),
            eq3[53].animate.set_color(blue),
        )
        self.wait(1)

        self.play(
            LaggedStart(
                ReplacementTransform(
                    Group(*eq3[13:23].copy(), *eq3[33:43].copy(), *eq3[53].copy()),
                    eq4[4:25],
                ),
                GrowFromCenter(eq4[:4]),
                GrowFromCenter(eq4[25:29]),
                GrowFromCenter(eq4[29]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        self.play(
            eq3[23:33].animate.set_color(red),
            eq3[43:53].animate.set_color(red),
            eq3[54].animate.set_color(red),
        )
        self.wait(1)

        self.play(
            LaggedStart(
                ReplacementTransform(
                    Group(*eq3[23:33].copy(), *eq3[43:53].copy(), *eq3[54].copy()),
                    eq4[34:55],
                ),
                GrowFromCenter(eq4[30:34]),
                GrowFromCenter(eq4[55:59]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        eq5 = MathTex(
            r"\begin{bmatrix}\cos\psi-2\sin\psi\\[6pt]\sin\psi+2\cos\psi\\[6pt]0\end{bmatrix}\centerdot\begin{bmatrix}\sin\psi + 2\cos\psi\\[6pt]-(\cos\psi- 2\sin\psi)\\[6pt]0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq5.shift(eq5[14].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq5[4:25].set_color(blue)
        eq5[34:58].set_color(red)

        self.play(
            ReplacementTransform(eq4[:34], eq5[:34]),
            ReplacementTransform(eq4[54:], eq5[57:]),
        )
        self.play(
            ReplacementTransform(eq4[34:39], eq5[39:44]),
            ReplacementTransform(eq4[39], eq5[38]),
            ReplacementTransform(eq4[40:44], eq5[34:38]),
        )
        self.play(
            ReplacementTransform(eq4[44:49], eq5[51:56]),
            ReplacementTransform(eq4[49], eq5[50]),
            ReplacementTransform(eq4[50:54], eq5[46:50]),
            GrowFromCenter(eq5[44]),
            GrowFromCenter(eq5[45]),
            GrowFromCenter(eq5[56]),
        )
        self.wait(1)

        eq6 = MathTex(
            r"\begin{bmatrix}a\\[6pt]b\\[6pt]0\end{bmatrix}\centerdot\begin{bmatrix}b\\[6pt]-a\\[6pt]0\end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq6.shift(eq6[5].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq6[4].set_color(green)
        eq6[5].set_color(yellow)
        eq6[16].set_color(yellow)
        eq6[18].set_color(green)

        self.play(
            ReplacementTransform(eq5[4:14], eq6[4]),
            ReplacementTransform(eq5[14:24], eq6[5]),
            ReplacementTransform(eq5[24:34], eq6[6:16]),
            ReplacementTransform(eq5[:4], eq6[:4]),
        )
        self.play(
            ReplacementTransform(eq5[34:44], eq6[16]),
            ReplacementTransform(eq5[45:57], eq6[18]),
            ReplacementTransform(eq5[44], eq6[17]),
            ReplacementTransform(eq5[57:], eq6[19:]),
        )
        self.wait(1)

        eq7 = MathTex(
            r"\begin{bmatrix}a\\[6pt]b\\[6pt]0\end{bmatrix}\centerdot\begin{bmatrix}b\\[6pt]-a\\[6pt]0\end{bmatrix}=ab -ab",
            color=dark_blue,
            font_size=40,
        )[0]
        eq7.shift(eq7[5].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq7[4].set_color(green)
        eq7[5].set_color(yellow)
        eq7[16].set_color(yellow)
        eq7[18].set_color(green)
        eq7[26].set_color(yellow)
        eq7[25].set_color(green)
        eq7[28].set_color(green)
        eq7[29].set_color(yellow)

        self.play(
            ReplacementTransform(eq6, eq7[: len(eq6)]), GrowFromCenter(eq7[len(eq6) :])
        )
        self.wait(1)

        eq8 = MathTex(
            r"\begin{bmatrix}a\\[6pt]b\\[6pt]0\end{bmatrix}\centerdot\begin{bmatrix}b\\[6pt]-a\\[6pt]0\end{bmatrix}=0",
            color=dark_blue,
            font_size=40,
        )[0]
        eq8.shift(eq8[5].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq8[4].set_color(green)
        eq8[5].set_color(yellow)
        eq8[16].set_color(yellow)
        eq8[18].set_color(green)

        self.play(
            ReplacementTransform(eq7[: len(eq6) + 1], eq8[: len(eq6) + 1]),
            ReplacementTransform(eq7[len(eq6) + 1 :], eq8[len(eq6) + 1 :]),
        )
        self.wait(1)

        self.play(
            FadeOut(eq8),
            eq3[13:23].animate.set_color(dark_blue),
            eq3[33:43].animate.set_color(dark_blue),
            eq3[53].animate.set_color(dark_blue),
            eq3[23:33].animate.set_color(dark_blue),
            eq3[43:53].animate.set_color(dark_blue),
            eq3[54].animate.set_color(dark_blue),
        )
        self.wait(1)

        self.play(Group(*eq3[74:78], *eq3[94:98], eq3[114]).animate.set_color(blue))
        self.wait(1)

        eq9 = MathTex(r"\cos^2\psi + \sin^2\psi", color=dark_blue, font_size=40)[0]
        eq9.shift(eq9[0].get_bottom()[1] * DOWN + UNIT * UP + 4.2 * UNIT * RIGHT)
        eq9b = MathTex(r"1", color=dark_blue, font_size=40)[0]
        eq9b.shift(eq9b[0].get_bottom()[1] * DOWN + UNIT * UP + 4.2 * UNIT * RIGHT)

        self.play(Write(eq9))
        self.wait(1)
        self.play(ReplacementTransform(eq9, eq9b))
        self.wait(1)
        self.play(FadeOut(eq9b))
        self.wait(1)
        self.play(
            Group(*eq3[74:78], *eq3[94:98], eq3[114]).animate.set_color(dark_blue)
        )
        self.wait(1)

        eq10 = MathTex(
            r"\begin{bmatrix}\dfrac{\sqrt{2}}{2}\,(\cos\psi-\sin\psi)\\[8pt]\dfrac{\sqrt{2}}{2}\,"
            r"(\sin\psi+\cos\psi)\\[8pt]0\end{bmatrix}\centerdot \begin{bmatrix}\dfrac{\sqrt{2}}{2}\,"
            r"(\cos\psi-\sin\psi)\\[8pt]\dfrac{\sqrt{2}}{2}\,(\sin\psi+\cos\psi)\\[8pt]0\end{bmatrix}="
            r" \left(\tfrac{\sqrt{2}}{2}(\cos\psi-\sin\psi)\right)^2+"
            r" \left(\tfrac{\sqrt{2}}{2}(\sin\psi+\cos\psi)\right)^2",
            color=dark_blue,
            font_size=30,
        )[0]
        eq10.shift(eq10[len(eq10) - 5].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq10[7:40].set_color(blue)
        eq10[55:88].set_color(blue)

        self.play(Group(*eq3[78:94], *eq3[98:114], eq3[115]).animate.set_color(blue))
        self.wait(1)

        self.play(
            LaggedStart(
                ReplacementTransform(
                    Group(*eq3[78:94].copy(), *eq3[98:114].copy(), eq3[115].copy()),
                    eq10[7:40],
                ),
                GrowFromCenter(eq10[:7]),
                GrowFromCenter(eq10[40:47]),
                GrowFromCenter(eq10[47]),
                ReplacementTransform(
                    Group(*eq3[78:94].copy(), *eq3[98:114].copy(), eq3[115].copy()),
                    eq10[55:88],
                ),
                GrowFromCenter(eq10[48:55]),
                GrowFromCenter(eq10[88:95]),
                Write(eq10[95:]),
                lag_ratio=0.8,
            )
        )
        self.wait(1)

        eq11 = MathTex(
            r" \left(\tfrac{\sqrt{2}}{2}(\cos\psi-\sin\psi)\right)^2+"
            r" \left(\tfrac{\sqrt{2}}{2}(\sin\psi+\cos\psi)\right)^2",
            color=dark_blue,
            font_size=40,
        )[0]
        eq11.shift(eq11[7].get_bottom()[1] * DOWN)
        self.play(ReplacementTransform(eq10[96:], eq11), FadeOut(eq10[:96]))
        self.wait(1)

        eq11b = MathTex(
            r"\tfrac{1}{2}\bigl[ (\cos\psi-\sin\psi)^2+"
            r" (\sin\psi+\cos\psi)^2\bigr]",
            color=dark_blue,
            font_size=40,
        )[0]
        eq11b.shift(eq11b[6].get_bottom()[1] * DOWN)
        self.play(
            LaggedStart(
                ShrinkToCenter(eq11[0]),
                ReplacementTransform(Group(*eq11[1:6], *eq11[21:26]), eq11b[:3]),
                GrowFromCenter(eq11b[3]),
                ReplacementTransform(eq11[6:17], eq11b[4:15]),
                ShrinkToCenter(eq11[17]),
                ReplacementTransform(eq11[18], eq11b[15]),
                ReplacementTransform(eq11[19], eq11b[16]),
                ShrinkToCenter(eq11[20]),
                ReplacementTransform(eq11[26:37], eq11b[17:28]),
                ShrinkToCenter(eq11[37]),
                ReplacementTransform(eq11[38], eq11b[28]),
                GrowFromCenter(eq11b[29]),
                lag_ratio=0.0,
            )
        )
        self.wait(1)

        eq12 = MathTex(r"(a-b)^2+(a+b)^2", color=dark_blue, font_size=40)[0]
        eq12.shift(eq12[1].get_bottom()[1] * DOWN + 2 * UNIT * DOWN)
        eq12[1].set_color(green)
        eq12[3].set_color(yellow)
        eq12[8].set_color(green)
        eq12[10].set_color(yellow)
        self.play(Write(eq12))
        self.wait(1)

        eq13 = MathTex(r"(a-b)^2+(a+b)^2=2(a^2+b^2)", color=dark_blue, font_size=40)[0]
        eq13.shift(eq13[1].get_bottom()[1] * DOWN + 2 * UNIT * DOWN)
        eq13[1].set_color(green)
        eq13[3].set_color(yellow)
        eq13[8].set_color(green)
        eq13[10].set_color(yellow)
        eq13[16].set_color(green)
        eq13[19].set_color(yellow)

        eq14 = MathTex(r"a = \cos\psi, b = \sin\psi", color=dark_blue, font_size=40)[0]
        eq14.shift(eq14[0].get_bottom()[1] * DOWN + 3 * UNIT * DOWN)
        eq14[0].set_color(green)
        eq14[7].set_color(yellow)

        self.play(Write(eq14))
        self.wait(1)

        self.play(
            LaggedStart(
                ReplacementTransform(eq12, eq13[: len(eq12)]),
                Write(eq13[len(eq12) :]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)

        eq15 = MathTex(
            r"\tfrac{1}{2}\cdot 2(\cos^2\psi+ \sin^2\psi)",
            color=dark_blue,
            font_size=40,
        )[0]
        eq15.shift(eq15[6].get_bottom()[1] * DOWN)
        self.play(
            ReplacementTransform(eq11b[:3], eq15[:3]),
            ReplacementTransform(eq11b[3:], eq15[3:]),
        )
        self.wait(1)

        self.play(Unwrite(eq14), Unwrite(eq13))
        self.wait(1)

        eq16 = MathTex(r"\tfrac{1}{2}\cdot 2(1)", color=dark_blue, font_size=40)[0]
        eq16.shift(eq16[6].get_bottom()[1] * DOWN)
        self.play(
            ReplacementTransform(eq15[:6], eq16[:6]),
            ReplacementTransform(eq15[6:17], eq16[6]),
            ReplacementTransform(eq15[17], eq16[7]),
        )
        self.wait(1)

        eq17 = MathTex(r"1", color=dark_blue, font_size=40)[0]
        eq17.shift(eq17[0].get_bottom()[1] * DOWN)
        self.play(ReplacementTransform(eq16, eq17))
        self.wait(1)

        self.play(FadeOut(eq17))
        self.wait(1)

        self.play(
            Group(*eq3[78:94], *eq3[98:114], eq3[115]).animate.set_color(dark_blue)
        )

        self.play(eq3.animate.shift(3 * UNIT * DOWN))
        self.wait(1)

        self.play(
            LaggedStart(
                Wiggle(Group(*eq3[13:23], *eq3[33:43], *eq3[53])),
                Wiggle(Group(*eq3[23:33], *eq3[43:53], *eq3[54])),
                lag_ratio=0.3,
            )
        )
        self.wait(1)

        self.play(
            LaggedStart(
                Wiggle(Group(*eq3[74:78], *eq3[94:98], eq3[114])),
                Wiggle(Group(*eq3[78:94], *eq3[98:114], eq3[115])),
                lag_ratio=0.6,
            )
        )
        self.wait()
