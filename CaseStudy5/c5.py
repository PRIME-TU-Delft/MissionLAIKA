from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF')
class Plane(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3/4
        dark_blue = ManimColor('#0C2340')

        self.wait()

        eq1 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{yaw}(\psi) = \begin{bmatrix}"
            r"\cos\psi & -\sin\psi & 0 \\"
            r"\sin\psi & \cos\psi & 0 \\"
            r"0 & 0 & 1"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=30
        )[0].to_corner(UR)

        self.play(Write(eq1))
        self.wait(1)
        self.play(Unwrite(eq1))
        self.wait(1)

        eq2 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{pitch}(\theta) = \begin{bmatrix}"
            r"\cos\theta & 0 & \sin\theta \\"
            r"0 & 1 & 0 \\"
            r"-\sin\theta & 0 & \cos\theta"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=30
        )[0].to_corner(UR)

        self.play(Write(eq2))
        self.wait(1)
        self.play(Unwrite(eq2))
        self.wait(1)

        eq3 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{roll}(\phi) = \begin{bmatrix}"
            r"1 & 0 & 0 \\"
            r"0 & \cos\phi & -\sin\phi \\"
            r"0 & \sin\phi & \cos\phi"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=30
        )[0].to_corner(UR)

        self.play(Write(eq3))
        self.wait(1)
        self.play(Unwrite(eq3))
        self.wait(1)

        grid = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(3 / 4)

        self.play(Write(grid))
        self.wait()

        eq12 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{yaw}(\psi) = \begin{bmatrix}"
            r"\cos\psi & -\sin\psi & 0 \\"
            r"\sin\psi & \cos\psi & 0 \\"
            r"0 & 0 & 1"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=24
        )[0]
        eq12.shift(3*UNIT*UP + 5*UNIT*LEFT - eq12[0].get_bottom()[1] * UP)

        eq22 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{pitch}(\theta) = \begin{bmatrix}"
            r"\cos\theta & 0 & \sin\theta \\"
            r"0 & 1 & 0 \\"
            r"-\sin\theta & 0 & \cos\theta"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=24
        )[0]
        eq22.shift(3*UNIT*UP - eq22[0].get_bottom()[1] * UP)

        eq32 = MathTex(
            r"{\renewcommand{\arraystretch}{1.5}"
            r"A_\text{roll}(\phi) = \begin{bmatrix}"
            r"1 & 0 & 0 \\"
            r"0 & \cos\phi & -\sin\phi \\"
            r"0 & \sin\phi & \cos\phi"
            r"\end{bmatrix}}",
            color=dark_blue,
            font_size=24
        )[0]
        eq32.shift(3*UNIT*UP + 5*UNIT*RIGHT - eq32[0].get_bottom()[1] * UP)

        self.play(FadeIn(eq12), FadeIn(eq22), FadeIn(eq32))

        initial = MathTex(r"(\mathbf{a},\mathbf{b},\mathbf{c})",color=dark_blue,font_size=32)
        first = MathTex(r"(\mathbf{a}_1,\mathbf{b}_1,\mathbf{c}_1)",color=dark_blue,font_size=32)
        second = MathTex(r"(\mathbf{a}_2,\mathbf{b}_2,\mathbf{c}_2)",color=dark_blue,font_size=32)
        third = MathTex(r"(\mathbf{a}_3,\mathbf{b}_3,\mathbf{c}_3)",color=dark_blue,font_size=32)
        initial.shift(6*UNIT*LEFT - initial[0].get_bottom()[1] * UP)
        first.shift(2 * UNIT * LEFT - first[0].get_bottom()[1] * UP)
        second.shift(2 * UNIT * RIGHT - second[0].get_bottom()[1] * UP)
        third.shift(6 * UNIT * RIGHT - third[0].get_bottom()[1] * UP)

        arrow1 = Line(start=initial.get_right(), end=first.get_left(), buff=0.4, color=dark_blue, stroke_width=2)
        arrow1.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        label1 = MathTex(r"A_\text{yaw}",color=dark_blue,font_size=32).next_to(arrow1, UP)

        arrow2 = Line(start=first.get_right(), end=second.get_left(), buff=0.4, color=dark_blue, stroke_width=2)
        arrow2.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        label2 = MathTex(r"A_\text{pitch}",color=dark_blue,font_size=32).next_to(arrow2, UP)

        arrow3 = Line(start=second.get_right(), end=third.get_left(), buff=0.4, color=dark_blue, stroke_width=2)
        arrow3.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        label3 = MathTex(r"A_\text{roll}",color=dark_blue,font_size=32).next_to(arrow3, UP)

        transition_group = Group(initial, first, second, third, arrow1, label1, arrow2, label2, label3, arrow3)

        self.play(Write(initial))
        self.wait()

        self.play(Write(arrow1), Write(label1), Write(first))
        self.wait()

        self.play(Write(arrow2), Write(label2), Write(second))
        self.wait()

        self.play(Write(arrow3), Write(label3), Write(third))
        self.wait()

        self.wait()
        self.play(FadeOut(eq12), FadeOut(eq22), FadeOut(eq32), FadeOut(transition_group))
        self.play(FadeOut(grid))
        self.wait()

        eq4 = MathTex(
            r"\mathbf{a} = \mathbf{a}",
            color=dark_blue,
            font_size=32
        )[0]
        eq4.shift(4*UNIT*UP + 5*UNIT*RIGHT)

        self.play(Write(eq4))
        self.wait()

        eq5 = MathTex(
            r"\mathbf{a}_1 = A_\text{yaw} \mathbf{a}",
            color=dark_blue,
            font_size=32
        )[0]
        eq5.shift(4*UNIT*UP + 5*UNIT*RIGHT)

        self.play(ReplacementTransform(eq4[0], eq5[0]), GrowFromPoint(eq5[1], eq4.get_center()),
                  ReplacementTransform(eq4[1], eq5[2]), GrowFromCenter(eq5[3:7]), ReplacementTransform(eq4[2], eq5[7]) )
        self.wait()

        eq6 = MathTex(
            r"\mathbf{a}_2 = A_\text{pitch} A_\text{yaw} \mathbf{a}",
            color=dark_blue,
            font_size=32
        )[0]
        eq6.shift(4*UNIT*UP + 5*UNIT*RIGHT)

        self.play(ReplacementTransform(eq5[0:3], eq6[0:3]), GrowFromCenter(eq6[3:9]),
                  ReplacementTransform(eq5[3:], eq6[9:]))
        self.wait()

        eq7 = MathTex(
            r"\mathbf{a}_3 = A_\text{roll} A_\text{pitch} A_\text{yaw} \mathbf{a}",
            color=dark_blue,
            font_size=32
        )[0]
        eq7.shift(4*UNIT*UP + 5*UNIT*RIGHT)

        self.play(ReplacementTransform(eq6[0:3], eq7[0:3]), GrowFromCenter(eq7[3:8]),
                  ReplacementTransform(eq6[3:], eq7[8:]))

        self.wait()

        eq8 = MathTex(
            r"\mathbf{a}_3 = A_\text{total} \mathbf{a}",
            color=dark_blue,
            font_size=32
        )[0]
        eq8.shift(4 * UNIT * UP + 5 * UNIT * RIGHT)

        self.play(ReplacementTransform(eq7[0:3], eq8[0:3]),
                  ReplacementTransform(eq7[3:len(eq7)-1], eq8[3: len(eq8)-1]),
                  ReplacementTransform(eq7[len(eq7)-1], eq8[len(eq8)-1]))

        self.wait()
