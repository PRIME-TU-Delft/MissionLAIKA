from manim import *
import numpy as np

class OrbitTypes(Scene):
    def construct(self):
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31') #ManimColor('#FF5132')
        yellow = ManimColor('#cc9316') #ManimColor('#FFCC12')
        blue = ManimColor('#0076C2') #ManimColor('#46A6FF')

        body = Circle(radius=0.22)
        body.set_fill(blue, opacity=1)
        body.set_stroke(blue, width=2)
        body.move_to(ORIGIN)

        # Small glow around body
        glow = Circle(radius=0.34)
        glow.set_fill(blue, opacity=0.15)
        glow.set_stroke(opacity=0)
        glow.move_to(ORIGIN)

        a, b = 1.55, 1.05
        c = np.sqrt(a**2 - b**2)

        ellipse = ParametricFunction(
            lambda t: np.array([a * np.cos(t), b * np.sin(t) + c, 0]),
            t_range=[0, TAU],
            color=BLACK,
            stroke_width=5,
        )
        ellipse.move_to(ORIGIN)

        ellipse_label = Text("Ellipse:", font_size=28, color=BLACK)
        ellipse_label.next_to(ellipse, UP, buff=0.15).shift(RIGHT * 0.4)

        ellipse_formula = MathTex(
            r"\frac{(x-h)^2}{a^2}+\frac{(y-k)^2}{b^2}=1",
            font_size=28,
            color=BLACK
        )
        ellipse_formula.next_to(ellipse_label, RIGHT, buff=0.15)

        p = 0.75
        parabola = ParametricFunction(
            lambda t: np.array([t, t**2 / (4 * p) - p, 0]),
            t_range=[-2.3, 2.3],
            color=BLACK,
            stroke_width=5,
        )
        parabola.move_to(ORIGIN).shift(1 * DOWN)

        parabola_label = Text("Parabola:", font_size=28, color=BLACK)
        parabola_label.next_to(parabola, RIGHT, buff=0.2).shift(UP * 0.4)

        parabola_formula = MathTex(
            r"y=\frac{x^2}{4p}-p",
            font_size=28,
            color=BLACK
        )
        parabola_formula.next_to(parabola_label, RIGHT, buff=0.15)

        a2, b2 = 0.75, 1.2
        c2 = np.sqrt(a2**2 + b2**2)
        hyperbola = ParametricFunction(
            lambda t: np.array([b2 * np.sinh(t), a2 * np.cosh(t) - c2, 0]),
            t_range=[-1.3, 1.3],
            color=BLACK,
            stroke_width=5,
        ).shift(2 * DOWN)

        hyperbola_label = Text("Hyperbola:", font_size=28, color=BLACK)
        hyperbola_label.next_to(hyperbola, RIGHT, buff=0.2).shift(UP * 0.2)

        hyperbola_formula = MathTex(
            r"\frac{(y-k)^2}{a^2}-\frac{(x-h)^2}{b^2}=1",
            font_size=28,
            color=BLACK
        )
        hyperbola_formula.next_to(hyperbola_label, RIGHT, buff=0.15)

        group = VGroup(
            glow, body,
            ellipse, parabola, hyperbola,
            ellipse_label, parabola_label, hyperbola_label,
            ellipse_formula, parabola_formula, hyperbola_formula
        )
        group.scale(1.15).shift(2*LEFT)

        self.add(
            glow, body, ellipse, parabola, hyperbola,
            ellipse_label, parabola_label, hyperbola_label,
            ellipse_formula, parabola_formula, hyperbola_formula
        )