from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF') #ManimColor('#002213')
class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3/4
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31')
        yellow = ManimColor('#cc9316')
        blue = ManimColor('#0076C2')

        grid = NumberPlane(background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15
            },
            x_range=(0,72,1),
            y_range=(0, 36, 1),
        ).scale(3/4)

        self.play(Write(grid))

        self.wait(1)

        eq0 = MathTex(r"\textbf{x}'' = A \textbf{x}", color=dark_blue, font_size=60)[0]
        eq0.shift(0 - eq0.get_bottom())
        eq0[0].set_color(yellow)
        eq0[5].set_color(yellow)

        self.play(Write(eq0))
        self.wait(1)

        eq1 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A = \begin{bmatrix}"
            r"-\frac{k}{m_1} & \frac{k}{m_1} & 0\\"
            r"\frac{k}{m_2} & -\frac{2k}{m_2} & \frac{k}{m_2}\\"
            r"0 & \frac{k}{m_1} & -\frac{k}{m_1}"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=60
        )[0]
        eq1.shift(3*UNIT*RIGHT + eq1[0].get_bottom()[1] * DOWN)
        eq1[8].set_color(blue)
        eq1[10:12].set_color(red)
        eq1[12].set_color(blue)
        eq1[14:16].set_color(red)
        eq1[17].set_color(blue)
        eq1[19:21].set_color(red)
        eq1[23].set_color(blue)
        eq1[25:27].set_color(red)
        eq1[27].set_color(blue)
        eq1[29:31].set_color(red)
        eq1[32].set_color(blue)
        eq1[34:36].set_color(red)
        eq1[37].set_color(blue)
        eq1[39:41].set_color(red)

        self.play(eq0.animate.shift(5*UNIT*LEFT))
        self.play(Write(eq1))
        self.wait(1)

        cloud = SVGMobject("../assets/cloud.svg", stroke_color=dark_blue, stroke_width=3)
        cloud.scale(1.35).shift(3*UNIT*LEFT + 3*UNIT*UP)
        cloud_circle1 = Circle(stroke_color=dark_blue, stroke_width=3).scale(0.1*UNIT).stretch(1.2, 0).shift(6*UNIT*LEFT + 1.4*UNIT*UP)
        cloud_circle2 = Circle(stroke_color=dark_blue, stroke_width=3).scale(0.2 * UNIT).stretch(1.2, 0).shift(
            5.6 * UNIT * LEFT + 2 * UNIT * UP)


        eq2 = MathTex(r"A \textbf{x} = \lambda \textbf{x}", color=dark_blue, font_size=60)[0].shift(
            3 * UNIT * UP + 3 * UNIT * LEFT)
        self.play(LaggedStart(FadeIn(cloud_circle1), FadeIn(cloud_circle2), FadeIn(cloud), lag_ratio=0.5))
        self.play(FadeIn(eq2))
        self.play(Indicate(eq2))
        self.wait(1)
        self.play(FadeOut(eq2), FadeOut(cloud_circle1), FadeOut(cloud_circle2), FadeOut(cloud))
        self.wait(1)

        self.play(self.camera.frame.animate.move_to(2 * UNIT * DOWN))
        self.wait(1)

        eq3 = MathTex("y'' = a^2y", color=dark_blue, font_size=60)[0]
        eq3.shift(4*UNIT*LEFT + 5*UNIT*DOWN - eq3[4].get_bottom()[1]*UP)
        eq4 = MathTex("y = f(t)", color=dark_blue, font_size=60)[0]
        eq4.shift(4 * UNIT * RIGHT + 5 * UNIT * DOWN- eq4[4].get_bottom()[1]*UP)
        self.play(Write(eq3))
        self.wait(1)
        self.play(Write(eq4))
        self.wait(1)

        self.play(self.camera.frame.animate.move_to(18*UNIT*RIGHT + 2.5 * UNIT * DOWN))
        self.wait(1)

        question = MathTex(r"\text{Which function } y = f(t) \text{ becomes a multiple}",color=dark_blue, font_size=42)[0]
        question2 = MathTex(r"\text{of itself after differentiating twice?}",color=dark_blue, font_size=42)[0]
        question.shift(18*UNIT*RIGHT +  UNIT * UP + question[0].get_bottom() * DOWN)
        question2.shift(18 * UNIT * RIGHT + question2[0].get_bottom() * DOWN)
        self.play(Write(question))
        self.play(Write(question2))
        self.wait(3)

        eq5 = MathTex("y = e^{at}",color=dark_blue, font_size=72)[0]
        eq5.shift(18*UNIT*RIGHT + 3 * UNIT * DOWN + eq5[2].get_bottom() * DOWN)

        self.play(Write(eq5))
        self.wait(2)

        eq6 = MathTex("y' = ae^{at}",color=dark_blue, font_size=72)[0]
        eq6.shift(18 * UNIT * RIGHT + 3 * UNIT * DOWN + eq6[3].get_bottom() * DOWN)
        eq7 = MathTex("y'' = aae^{at}",color=dark_blue, font_size=72)[0]
        eq7.shift(18 * UNIT * RIGHT + 3 * UNIT * DOWN + eq7[4].get_bottom() * DOWN)
        eq8 = MathTex("y'' = a^{2}e^{at}",color=dark_blue, font_size=72)[0]
        eq8.shift(18 * UNIT * RIGHT + 3 * UNIT * DOWN + eq8[4].get_bottom() * DOWN)
        eq9 = MathTex("y'' = a^{2}e^{at} = a^{2}y",color=dark_blue, font_size=72)[0]
        eq9.shift(18 * UNIT * RIGHT + 3 * UNIT * DOWN + eq9[4].get_bottom() * DOWN)
        self.play(ReplacementTransform(eq5[0], eq6[0]),
                  GrowFromCenter(eq6[1]),
                  ReplacementTransform(eq5[1], eq6[2]),
                  ReplacementTransform(eq5[2:], eq6[4:]),
                  GrowFromCenter(eq6[3]))
        self.wait(0.2)
        self.play(ReplacementTransform(eq6[0:2], eq7[0:2]),
                  GrowFromCenter(eq7[2]),
                  ReplacementTransform(eq6[2], eq7[3]),
                  ReplacementTransform(eq6[3:], eq7[5:]),
                  GrowFromCenter(eq7[4]))
        self.wait(0.2)
        self.play(ReplacementTransform(eq7[0:5], eq8[0:5]),
                  ReplacementTransform(eq7[5], eq8[5]),
                  ReplacementTransform(eq7[6:], eq8[6:]))
        self.wait(0.2)
        self.play(ReplacementTransform(eq8, eq9[: len(eq8)]),
                  GrowFromCenter(eq9[len(eq8):]))
        self.wait(0.2)

        #REVERSE
        self.play(
            ReplacementTransform(eq9[:len(eq8)], eq8),
            ShrinkToCenter(eq9[len(eq8):])
        )
        self.play(
            ReplacementTransform(eq8[0:5], eq7[0:5]),
            ReplacementTransform(eq8[5], eq7[5]),
            ReplacementTransform(eq8[6:], eq7[6:])
        )
        self.wait(0.1)
        self.play(
            ReplacementTransform(eq7[0:2], eq6[0:2]),
            ShrinkToCenter(eq7[2]),
            ReplacementTransform(eq7[3], eq6[2]),
            ReplacementTransform(eq7[4], eq6[3]),
            ReplacementTransform(eq7[6:], eq6[4:]),
            ShrinkToCenter(eq7[5])
        )
        self.wait(0.1)
        eq5c = MathTex("y = e^{at}",color=dark_blue, font_size=72)[0]
        eq5c.shift(18 * UNIT * RIGHT + 3 * UNIT * DOWN + eq5c[2].get_bottom() * DOWN)
        self.play(
            ReplacementTransform(eq6[0], eq5c[0]),
            ShrinkToCenter(eq6[1]),
            ReplacementTransform(eq6[2], eq5c[1]),
            ReplacementTransform(eq6[4:], eq5c[2:]),
            ShrinkToCenter(eq6[3])
        )

        eq4c = MathTex("y = e^{at}", color=dark_blue, font_size=60)[0]
        eq4c.shift(4 * UNIT * RIGHT + 5 * UNIT * DOWN - eq4c[2].get_bottom()[1] * UP)
        self.wait(1)
        self.play( self.camera.frame.animate.move_to(2 * UNIT * DOWN), Unwrite(eq5c[0:2]), ReplacementTransform(eq5c[2:], eq4c[2:]), ReplacementTransform(eq4[0:2], eq4c[0:2]), ShrinkToCenter(eq4[2:]))
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(2 * UNIT * UP))
        self.wait(1)

        eq10= MathTex(r"\textbf{x} = \textbf{v}e^{i \omega t}", color=dark_blue, font_size=60)[0]
        eq10.shift(
            4 * UNIT * UP + 4 * UNIT * LEFT - eq10[0].get_bottom()[1] * UP)
        eq10[0].set_color(yellow)

        self.play(Write(eq10))
        self.wait(1)
        eq10a = MathTex("\Rightarrow", color=dark_blue, font_size=60)[0].shift(4.3 * UNIT * UP + UNIT * LEFT)

        eq11 = MathTex(r"\textbf{x}'' = - \omega^2 \textbf{v}e^{i \omega t}", color=dark_blue, font_size=60)[0]
        eq11.shift(4 * UNIT * UP + 3 * UNIT * RIGHT - eq11[0].get_bottom()[1] * UP)
        eq11[0].set_color(yellow)

        self.play(Write(eq10a))
        self.wait(1)
        self.play(Write(eq11))
        self.wait(1)
        self.play(Wiggle(eq10[2:]), Wiggle(eq11[7:]))
        self.wait(1)

        eq12 = MathTex(r"\textbf{x}'' = -\omega^2 \textbf{x}", color=dark_blue, font_size=60)[0]
        eq12.shift(4 * UNIT * UP + 2.33 * UNIT * RIGHT - eq12[0].get_bottom()[1] * UP)
        eq12[0].set_color(yellow)
        eq12[7].set_color(yellow)
        self.play(ShrinkToCenter(eq11[7:]), ReplacementTransform(eq11[:7], eq12[:7]), ReplacementTransform(eq10[0].copy(), eq12[7:]))
        self.wait(1)
        self.play(Wiggle(eq12[:3], scale_value=1.2), Wiggle(eq0[:3], scale_value=1.2))
        self.wait(1)

        eq13= MathTex(r"-\omega^2 \textbf{x} = A \textbf{x}", color=dark_blue, font_size=60)[0]
        eq13.shift(5.55 * UNIT * LEFT - eq13[1].get_bottom()[1] * UP)
        eq13[3].set_color(yellow)
        eq13[6].set_color(yellow)
        self.play(ReplacementTransform(eq12[4:].copy(), eq13[:4]), ReplacementTransform(eq0[3:], eq13[4:]), ShrinkToCenter(eq0[:3]))

        eq13r = MathTex(r"A \textbf{x} = -\omega^2 \textbf{x}", color=dark_blue, font_size=60)[0]
        eq13r.shift( 5.55 * UNIT * LEFT- eq13r[0].get_bottom()[1] * UP)
        eq13r[1].set_color(yellow)
        eq13r[6].set_color(yellow)

        self.wait(1)
        self.play(ReplacementTransform(eq13[:4], eq13r[3:]),ReplacementTransform(eq13[4], eq13r[2]), ReplacementTransform(eq13[5:], eq13r[:2]))

        self.wait(1)
        self.play(Unwrite(eq3), Unwrite(eq4c))
        self.play(self.camera.frame.animate.move_to(0), FadeOut(eq10), FadeOut(eq10a), FadeOut(eq12))
        self.wait(1)
        self.play(LaggedStart(FadeIn(cloud_circle1), FadeIn(cloud_circle2), FadeIn(cloud), lag_ratio=0.5))
        self.play(FadeIn(eq2))
        self.play(Indicate(eq2))
        self.wait(1)
        self.play(FadeOut(eq2), FadeOut(cloud_circle1), FadeOut(cloud_circle2), FadeOut(cloud))
        self.wait(1)

        eq14 = MathTex("\lambda = -\omega^2", color=dark_blue, font_size=60)[0]
        eq14.shift(2 * UNIT * DOWN + 5.8 * UNIT * LEFT - eq14[0].get_bottom()[1] * UP)
        self.play(Write(eq14))
        self.wait(1)

