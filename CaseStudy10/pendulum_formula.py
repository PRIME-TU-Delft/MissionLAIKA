from manim import *


def pendulum_formula(scene):
    self = scene
    UNIT = 3 / 4
    dark_blue = ManimColor("#0C2340")
    red = ManimColor("#E03C31")  # ManimColor('#FF5132')
    yellow = ManimColor("#cc9316")  # ManimColor('#FFCC12')
    blue = ManimColor("#0076C2")  # ManimColor('#46A6FF')
    green = ManimColor("#009B77")
    
    theta_label = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \text{With friction: }
        """,
        color=dark_blue,
        font_size=40,
    )
    theta_formula = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \begin{cases}
        \theta = e^{-\frac{b}{2}t} ( C_1 \cos(st)+ C_2 \sin(st)) \\
        \theta ' = e^{-\frac{b}{2}t} (- C_1 s \sin(st)+C_2 s \cos(st) - \frac{b}{2}C_1 \cos(st) - \frac{b}{2} C_2 \sin(st))
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    ).shift(2 * UNIT * DOWN)

    main_group = VGroup(
        theta_label, theta_formula
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)

    theta_label[0].shift(theta_label[0][0].get_bottom()[1] * DOWN + 1 * UP * UNIT)
    theta_formula[0].shift(theta_formula[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)


    self.play(Write(theta_label))
    self.play(Write(theta_formula))

    self.wait(1)

    self.play(theta_formula[0][63:75].animate.set_color(yellow),theta_formula[0][76:88].animate.set_color(yellow))
    self.wait(0.5)

    # DEBUG
    # indices = index_labels(theta_formula[0])
    # self.add(indices)
    # self.wait(1)
    # # self.remove(theta_formula)
    # self.remove(indices)

    theta_formula2 = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \begin{cases}
        \theta = e^{-\frac{b}{2}t} ( C_1 \cos(st)+ C_2 \sin(st)) \\
        \theta ' + \frac{b}{2}\theta = e^{-\frac{b}{2}t} (- C_1 \sin(st)+C_2 s \cos(st))
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    )

    theta_formula2.move_to(theta_formula, aligned_edge=LEFT)

    # self.remove(theta_formula)

    # DEBUG
    # indices = index_labels(theta_formula2[0])
    # self.add(theta_formula2)
    # self.add(indices)
    # self.wait(1)
    # # self.remove(theta_formula)
    # self.remove(indices)

    self.play(ReplacementTransform(theta_formula[0][:30], theta_formula2[0][:30]),
        ReplacementTransform(theta_formula[0][30:32], theta_formula2[0][30:37]),
        ReplacementTransform(theta_formula[0][32:], theta_formula2[0][37:]))
    

    self.wait(1)

    self.play(theta_label.animate.shift(2*UNIT*UP),
              theta_formula2.animate.shift(2*UNIT*UP))


    friction_formula_squared = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        (s\theta)^2 = e^{-bt}(C_1^2s^2 \cos(st)^2+C_2^2s^2\sin(st)^2+2C_1C_2s^2\cos(st)\sin(st)) \\
        (\theta' + \frac{b}{2}\theta)^2 = e^{-bt}(C_1^2s^2\sin(st)^2+C_2^2s^2\cos(st)^2-2C_1C_2s^2\cos(st)\sin(st))
        \end{cases}
        """,
        color=dark_blue,
        font_size=35,
    )

    plus = MathTex("+", color=dark_blue, font_size=40)
    plus.next_to(friction_formula_squared, LEFT, buff=0.2)

    bar = Line(
        friction_formula_squared.get_left() + LEFT * 0.4,
        friction_formula_squared.get_right() + RIGHT * 0.2,
        color=dark_blue,
        stroke_width=3,
    )

    friction_addition = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        (s \theta)^2 + (\theta ' + \frac{b}{2}\theta)^2 = e^{-bt}s^2 (C_1^2 + C_2^2)
        """,
        color=dark_blue,
        font_size=40,
    ).shift(2*UNIT*LEFT)
    main_group = VGroup(
        friction_formula_squared, bar, friction_addition
    ).arrange(DOWN, buff=0.45).shift(1.5*UNIT*DOWN)


    self.wait(0.5)

    bar[0].shift(bar[0][0].get_bottom()[1] * DOWN + 2 * DOWN * UNIT)
    friction_formula_squared[0].shift(friction_formula_squared[0][0].get_bottom()[1] * DOWN + 2 * DOWN * UNIT)
    plus[0].shift(plus[0][0].get_bottom()[1] * DOWN )




    self.wait(0.5)
    self.play(
        Write(friction_formula_squared),
        Write(plus.shift(1.6 * UNIT * DOWN)),
        Write(bar),
    )

    friction_addition[0].shift(friction_addition[0][0].get_bottom()[1] * DOWN )

    self.play(Write(friction_addition.shift(3.42*UNIT*LEFT + 3 * DOWN * UNIT)))

    self.wait(1)

    self.play(FadeOut(plus),FadeOut(bar),FadeOut(friction_addition),FadeOut(friction_addition),
             FadeOut(theta_formula2), FadeOut(theta_label), FadeOut(friction_formula_squared))

