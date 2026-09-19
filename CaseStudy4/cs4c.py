import numpy as np
from math import pi
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


# --- Airfoil helper ---
def cosine_spacing(n: int) -> np.ndarray:
    k = np.arange(n)
    theta = pi * k / (n - 1)
    return (1.0 - np.cos(theta)) * 0.5


def naca4_coordinates(
    code: str,
    n: int = 201,
    chord: float = 1.0,
    cosine: bool = True,
    closed: bool = True,
) -> np.ndarray:
    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    t = int(code[2:]) / 100.0
    x = cosine_spacing(n) if cosine else np.linspace(0.0, 1.0, n)
    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(np.maximum(x, 1e-12))
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
    )
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    for i, xi in enumerate(x):
        if p > 1e-12:
            if xi < p:
                yc[i] = m / (p**2) * (2 * p * xi - xi**2)
                dyc_dx[i] = 2 * m / (p**2) * (p - xi)
            else:
                yc[i] = m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xi - xi**2)
                dyc_dx[i] = 2 * m / ((1 - p) ** 2) * (p - xi)
    theta = np.arctan(dyc_dx)
    x_u = x - yt * np.sin(theta)
    y_u = yc + yt * np.cos(theta)
    x_l = x + yt * np.sin(theta)
    y_l = yc - yt * np.cos(theta)

    upper = np.stack([x_u, y_u], axis=1)
    lower = np.stack([x_l, y_l], axis=1)
    pts = np.vstack([upper[::-1], lower[1:]]) * chord
    if closed:
        pts[-1] = pts[0]

    # Flip horizontally and center
    pts[:, 0] = -pts[:, 0]
    pts[:, 0] -= (pts[:, 0].max() + pts[:, 0].min()) / 2
    pts[:, 1] -= (pts[:, 1].max() + pts[:, 1].min()) / 2
    return pts


class Lecture4Scene(PrimeScene):
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

        x = MathTex(
            r"\mathbf{x} ="
            r"\begin{bmatrix} x_1\\ x_2 \end{bmatrix}",
            color=dark_blue,
            font_size=60,
        )[0]
        x.shift(3 * UNIT * LEFT + 3 * UNIT * UP + x[0].get_bottom()[1] * DOWN)
        x[0].set_color(blue)
        x[3:7].set_color(blue)

        ux = MathTex(
            r"\mathbf{u} ="
            r"\begin{bmatrix} u_1(\mathbf{x})\\ u_2(\mathbf{x}) \end{bmatrix}",
            color=dark_blue,
            font_size=60,
        )[0]
        ux.shift(3 * UNIT * RIGHT + 3 * UNIT * UP + ux[0].get_bottom()[1] * DOWN)
        ux[0].set_color(yellow)
        ux[3:5].set_color(yellow)
        ux[6].set_color(blue)
        ux[8:10].set_color(yellow)
        ux[11].set_color(blue)

        eq1 = MathTex(
            r"u_1(\mathbf{x}) \approx u_1(\mathbf{x}_0) + \nabla u_1(\mathbf{x}_0) \cdot (\mathbf{x}-\mathbf{x}_0)",
            color=dark_blue,
            font_size=60,
        )[0]
        eq1.shift(1 * UNIT * UP + eq1[0].get_bottom()[1] * DOWN)
        eq1[0:2].set_color(yellow)
        eq1[3].set_color(blue)
        eq1[6:8].set_color(yellow)
        eq1[9:11].set_color(green)
        eq1[14:16].set_color(yellow)
        eq1[17:19].set_color(green)
        eq1[22].set_color(blue)
        eq1[24:26].set_color(green)

        eq2 = MathTex(
            r"u_2(\mathbf{x}) \approx u_2(\mathbf{x}_0) + \nabla u_2(\mathbf{x}_0) \cdot (\mathbf{x}-\mathbf{x}_0)",
            color=dark_blue,
            font_size=60,
        )[0]
        eq2.shift(1 * UNIT * DOWN + eq2[0].get_bottom()[1] * DOWN)
        eq2[0:2].set_color(yellow)
        eq2[3].set_color(blue)
        eq2[6:8].set_color(yellow)
        eq2[9:11].set_color(green)
        eq2[14:16].set_color(yellow)
        eq2[17:19].set_color(green)
        eq2[22].set_color(blue)
        eq2[24:26].set_color(green)

        nabla = MathTex(
            r"\nabla = \mathbf{i}\frac{\partial}{\partial x_1} + \mathbf{j}\frac{\partial}{\partial x_2}",
            color=dark_blue,
            font_size=48,
        )[0]
        nabla.shift(3 * UNIT * DOWN + nabla[0].get_bottom()[1] * DOWN)
        nabla[6:8].set_color(blue)
        nabla[13:15].set_color(blue)

        self.wait(1)
        self.play(Write(x))
        self.wait(1)
        self.play(Write(ux))
        self.wait(1)
        self.play(Write(eq1))
        self.wait(1)
        self.play(Write(eq2))
        self.wait(1)
        self.play(Write(nabla))
        self.wait(1)

        eq3 = MathTex(
            r"\begin{bmatrix}u_1 (\mathbf{x})\\u_2  (\mathbf{x})\end{bmatrix} \approx"
            r" \begin{bmatrix}u_1 (\mathbf{x}_0)\\u_2  (\mathbf{x}_0)\end{bmatrix}"
            r" +\begin{bmatrix}\frac{\partial u_1}{\partial x_1}(\mathbf{x}_0)"
            r" & \frac{\partial u_1}{\partial x_2}(\mathbf{x}_0)\\\frac{\partial u_2}{\partial x_1}(\mathbf{x}_0)"
            r" & \frac{\partial u_2}{\partial x_2}(\mathbf{x}_0)\end{bmatrix} (\mathbf{x}-\mathbf{x}_0)",
            color=dark_blue,
            font_size=60,
        )[0]
        eq3.shift(eq3[len(eq3) - 3].get_bottom()[1] * DOWN)
        eq3[1:3].set_color(yellow)
        eq3[6:8].set_color(yellow)
        eq3[4].set_color(blue)
        eq3[9].set_color(blue)
        eq3[14:16].set_color(yellow)
        eq3[20:22].set_color(yellow)
        eq3[17:19].set_color(green)
        eq3[23:25].set_color(green)
        eq3[30:32].set_color(yellow)
        eq3[34:36].set_color(blue)
        eq3[37:39].set_color(green)
        eq3[41:43].set_color(yellow)
        eq3[45:47].set_color(blue)
        eq3[48:50].set_color(green)
        eq3[52:54].set_color(yellow)
        eq3[56:58].set_color(blue)
        eq3[59:61].set_color(green)
        eq3[63:65].set_color(yellow)
        eq3[67:69].set_color(blue)
        eq3[70:72].set_color(green)
        eq3[75].set_color(blue)
        eq3[77:79].set_color(green)

        eq3xcopy = eq3[74:].copy()

        self.play(
            LaggedStart(
                ReplacementTransform(eq1[0:5], eq3[1:6]),
                ReplacementTransform(eq2[0:5], eq3[6:11]),
                Write(eq3[:1]),
                Write(eq3[11:12]),
                ReplacementTransform(Group(eq1[5], eq2[5]), eq3[12]),
                ReplacementTransform(eq1[6:12], eq3[14:20]),
                ReplacementTransform(eq2[6:12], eq3[20:26]),
                Write(eq3[13:14]),
                Write(eq3[26:27]),
                ReplacementTransform(Group(eq1[12], eq2[12]), eq3[27]),
                FadeOut(Group(eq1[20], eq2[20])),
                ReplacementTransform(eq1[21:], eq3xcopy),
                ReplacementTransform(eq2[21:], eq3[74:]),
                ReplacementTransform(eq1[13:20], eq3[29:51]),
                ReplacementTransform(eq2[13:20], eq3[51:73]),
                Write(eq3[28]),
                Write(eq3[73]),
                lag_ratio=0.5,
            )
        )

        self.remove(eq3xcopy)
        self.wait(1)

        eq4 = MathTex(
            r"\mathbf{u} (\mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0)+"
            r"\begin{bmatrix}\frac{\partial u_1}{\partial x_1}(\mathbf{x}_0) & "
            r"\frac{\partial u_1}{\partial x_2}(\mathbf{x}_0)\\\frac{\partial u_2}{\partial x_1}(\mathbf{x}_0)"
            r" & \frac{\partial u_2}{\partial x_2}(\mathbf{x}_0)\end{bmatrix} (\mathbf{x}-\mathbf{x}_0)",
            color=dark_blue,
            font_size=60,
        )[0]
        eq4.shift(eq4[len(eq4) - 3].get_bottom()[1] * DOWN)
        eq4[0].set_color(yellow)
        eq4[2].set_color(blue)
        eq4[5].set_color(yellow)
        eq4[7:9].set_color(green)
        eq4[13:15].set_color(yellow)
        eq4[17:19].set_color(blue)
        eq4[20:22].set_color(green)
        eq4[24:26].set_color(yellow)
        eq4[28:30].set_color(blue)
        eq4[31:33].set_color(green)
        eq4[35:37].set_color(yellow)
        eq4[39:41].set_color(blue)
        eq4[42:44].set_color(green)
        eq4[46:48].set_color(yellow)
        eq4[50:52].set_color(blue)
        eq4[53:55].set_color(green)
        eq4[58].set_color(blue)
        eq4[60:62].set_color(green)

        self.play(
            LaggedStart(
                ReplacementTransform(eq3[:12], eq4[:4]),
                ReplacementTransform(eq3[12], eq4[4]),
                ReplacementTransform(eq3[13:27], eq4[5:10]),
                ReplacementTransform(eq3[27:], eq4[10:]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)
        self.play(FadeOut(nabla))
        self.wait(1)

        eq4a = MathTex(
            r"J = \frac{\partial(u_1, u_2)}{\partial(x_1, x_2)} = \begin{bmatrix}\frac{\partial u_1}{\partial x_1}(\mathbf{x}_0) & "
            r"\frac{\partial u_1}{\partial x_2}(\mathbf{x}_0)\\\frac{\partial u_2}{\partial x_1}(\mathbf{x}_0)"
            r" & \frac{\partial u_2}{\partial x_2}(\mathbf{x}_0)\end{bmatrix}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq4a.shift(eq4a[0].get_bottom()[1] * DOWN + 3 * UNIT * DOWN)
        eq4a[4:6].set_color(yellow)
        eq4a[7:9].set_color(yellow)
        eq4a[13:15].set_color(blue)
        eq4a[16:18].set_color(blue)
        eq4a[22:24].set_color(yellow)
        eq4a[26:28].set_color(blue)
        eq4a[29:31].set_color(green)
        eq4a[33:35].set_color(yellow)
        eq4a[37:39].set_color(blue)
        eq4a[40:42].set_color(green)
        eq4a[44:46].set_color(yellow)
        eq4a[48:50].set_color(blue)
        eq4a[51:53].set_color(green)
        eq4a[55:57].set_color(yellow)
        eq4a[59:61].set_color(blue)
        eq4a[62:64].set_color(green)

        self.play(
            ReplacementTransform(eq4[11:57].copy(), eq4a[len(eq4a) - 46 :]),
            Write(eq4a[: len(eq4a) - 46]),
        )
        self.wait(1)

        eq5 = MathTex(
            r"\mathbf{u}(\mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0) + J (\mathbf{x}-\mathbf{x}_0)",
            color=dark_blue,
            font_size=60,
        )[0]
        eq5.shift(eq5[len(eq5) - 3].get_bottom()[1] * DOWN)
        eq5[0].set_color(yellow)
        eq5[2].set_color(blue)
        eq5[5].set_color(yellow)
        eq5[7:9].set_color(green)
        eq5[13].set_color(blue)
        eq5[15:17].set_color(green)

        self.play(
            LaggedStart(
                ReplacementTransform(eq4[11:57], eq5[11]),
                ReplacementTransform(eq4[:11], eq5[:11]),
                ReplacementTransform(eq4[57:], eq5[12:]),
                lag_ratio=0.5,
            )
        )
        self.wait(1)
        self.play(FadeOut(eq5), FadeOut(x), FadeOut(ux))

        eq6 = MathTex(r"\mathbf{x}_0", color=dark_blue, font_size=60)[0]
        eq6.shift(eq6[0].get_bottom()[1] * DOWN)
        eq6[:2].set_color(green)

        eq6b = MathTex(
            r"\mathbf{x}_0+\Delta \mathbf{x}", color=dark_blue, font_size=60
        )[0]
        eq6b.shift(eq6b[0].get_bottom()[1] * DOWN)
        eq6b[:2].set_color(green)
        eq6b[4].set_color(blue)

        eq7 = MathTex(
            r"\Delta \mathbf{x}=\begin{bmatrix} \Delta x_1 \\ \Delta x_2 \end{bmatrix}",
            color=dark_blue,
            font_size=60,
        )[0]
        eq7.shift(3 * UNIT * UP + eq7[0].get_bottom()[1] * DOWN)
        eq7[1].set_color(blue)
        eq7[5:7].set_color(blue)
        eq7[8:10].set_color(blue)

        eq8 = MathTex(
            r"\mathbf{u}(\mathbf{x}_0+\Delta \mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0) + J (\mathbf{x}_0+\Delta \mathbf{x}-\mathbf{x}_0)=\mathbf{u}(\mathbf{x}_0) + J \Delta \mathbf{x}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq8.shift(eq8[0].get_bottom()[1] * DOWN)
        eq8[0].set_color(yellow)
        eq8[2:4].set_color(green)
        eq8[6].set_color(blue)
        eq8[9].set_color(yellow)
        eq8[11:13].set_color(green)
        eq8[17:19].set_color(green)
        eq8[21].set_color(blue)
        eq8[23:25].set_color(green)
        eq8[27].set_color(yellow)
        eq8[29:31].set_color(green)
        eq8[35].set_color(blue)

        eq9 = MathTex(
            r"\mathbf{u}(\mathbf{x}_0+\Delta \mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0) + J \Delta \mathbf{x}",
            color=dark_blue,
            font_size=60,
        )[0]
        eq9.shift(eq9[0].get_bottom()[1] * DOWN)
        eq9[0].set_color(yellow)
        eq9[2:4].set_color(green)
        eq9[6].set_color(blue)
        eq9[9].set_color(yellow)
        eq9[11:13].set_color(green)
        eq9[17].set_color(blue)

        self.play(Write(eq6))
        self.wait(1)
        self.play(
            LaggedStart(
                ReplacementTransform(eq6, eq6b[:2]), Write(eq6b[2:]), lag_ratio=0.5
            )
        )
        self.wait(1)
        self.play(Write(eq7))
        self.wait(1)
        self.play(
            eq7.animate.shift(3 * UNIT * LEFT),
            eq6b.animate.shift(3 * UNIT * RIGHT + 3 * UNIT * UP),
        )
        self.wait(1)
        self.play(Write(eq8))
        self.wait(1)
        self.play(Wiggle(eq8[27:32]))
        self.wait(1)
        self.play(Wiggle(eq8[33:36]))
        self.play(
            LaggedStart(
                ShrinkToCenter(eq8[9:27]),
                ReplacementTransform(eq8[:9], eq9[:9]),
                ReplacementTransform(eq8[27:], eq9[9:]),
                lag_ratio=0.1,
            )
        )
        self.wait(1)
        self.play(Wiggle(eq9[9:14]))
        self.wait(1)
        self.play(Wiggle(eq9[15]))
        self.wait(1)
