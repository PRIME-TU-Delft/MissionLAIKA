import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor('#FFFFFF')


class Lecture10Scene(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 8
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31')
        yellow = ManimColor('#cc9316')
        blue = ManimColor('#0076C2')
        green = ManimColor('#009B77')

        grid = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1.5,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 1  # thicker lines
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)
        self.add(grid)

        sky1 = ImageMobject("../assets/sky_layer1.png")
        sky2 = ImageMobject("../assets/sky_layer2.png")
        sky3 = ImageMobject("../assets/sky_layer3.png")
        skies = [sky1, sky2, sky3]

        for sky in skies:
            sky.set_width(config.frame_width)
            sky.to_edge(DOWN, buff=0)

        self.add(*skies)

        speeds = [3 / 8, 5 / 8, 7 / 8]
        for sky, v in zip(skies, speeds):
            sky.add_updater(lambda m, dt, v=v: m.shift(DOWN * v * dt))

        airplane_image = ImageMobject("../assets/AirplaneTop.png").scale(0.4)
        airplane_inside = ImageMobject("../assets/AirplaneTopInside.png").scale(0.4)
        self.add(airplane_image)
        self.wait(14)
        self.play(FadeIn(airplane_inside), FadeOut(airplane_image))
        self.wait(1)
        self.play(self.camera.frame.animate.scale(0.3).shift(0.9*UP))
        self.wait(1)

        a = (1.29*UP+ 0.07*RIGHT)
        b = (1.22*UP)
        f = (1.32*UP)
        c = 0.96*UP + 0.015*LEFT
        d = (0.9*UP+ 0.097*RIGHT)
        e = (1.07*UP+ 0.045*RIGHT)

        def arrow_tip_svg( color, scale=0.1):
            tip = SVGMobject("../assets/ArrowTip.svg", fill_color=color, stroke_width=0)
            tip.set_fill(color, opacity=1)
            tip.set_stroke(width=0)
            tip.scale(scale)
            return tip

        def attach_svg_tip_to_line(line: Line, color, line_end, scale=0.1):
            tip = arrow_tip_svg(color=color, scale=scale)

            # Your SVG points UP by default, so its direction is UP.
            # We rotate it to match the line direction.
            direction = line.get_unit_vector()  # from start -> end
            angle = angle_between_vectors(UP, direction)  # rotation needed

            tip_top = tip.get_critical_point(UP)
            tip.rotate(-angle, about_point=tip_top)
            tip.shift(line_end - tip_top)

            return tip

        a = (1.29 * UP + 0.07 * RIGHT)
        b = (1.22 * UP)
        f = (1.32 * UP)
        c = 0.96 * UP + 0.015 * LEFT
        d = (0.9 * UP + 0.097 * RIGHT)
        e = (1.07 * UP + 0.045 * RIGHT)

        c1 = Line(start=c, end=e-0.03*(e-c), color=red, stroke_width=1.5)
        c2 = Line(start=c, end=d-0.03*(d-c), color=blue, stroke_width=1.5)
        d1 = Line(start=b, end=f-0.03*(f-b), color=yellow, stroke_width=1.5)
        d2 = Line(start=b, end=a-0.03*(a-b), color=green, stroke_width=1.5)

        tip_c1 = attach_svg_tip_to_line(c1, red, line_end=e, scale=0.015)
        tip_c2 = attach_svg_tip_to_line(c2, blue, line_end=d, scale=0.015)
        tip_d1 = attach_svg_tip_to_line(d1, yellow, line_end=f, scale=0.015)
        tip_d2 = attach_svg_tip_to_line(d2, green, line_end=a, scale=0.015)
        c1.z_index = 1
        c2.z_index = 1
        d1.z_index = 1
        d2.z_index = 1
        tip_c1.z_index = 1
        tip_c2.z_index = 1
        tip_d1.z_index = 1
        tip_d2.z_index = 1

        self.play(Write(c1), Write(tip_c1), Write(c2), Write(tip_c2))
        self.wait(4)
        self.play(Write(d1), Write(tip_d1), Write(d2), Write(tip_d2))
        self.wait(3)

        airplane = SVGMobject("../assets/AirplaneTop.svg", stroke_color=dark_blue, stroke_width=6.3).scale(1.93)
        airplane.z_index = -1

        self.play(*[sky.animate.set_opacity(0) for sky in skies], FadeIn(airplane), FadeOut(airplane_inside), run_time=2)
        for sky in skies:
            sky.clear_updaters()
        self.remove(*skies)

        self.wait()

        a = 3*UNIT*UP + (np.sqrt(2)/2)*UNIT*(UP+RIGHT)
        b = 3*UNIT*UP
        f = 4*UNIT*UP
        c = 1*UNIT*UP
        d = 2*UNIT*RIGHT
        e = 3*UNIT*UP+ 1*UNIT*RIGHT

        c1_big = Line(start=c, end=e-0.05*(e-c), color=red, stroke_width=3)
        c2_big = Line(start=c, end=d-0.05*(d-c), color=blue, stroke_width=3)
        d1_big = Line(start=b, end=f-0.05*(f-b), color=yellow, stroke_width=3)
        d2_big = Line(start=b, end=a-0.05*(a-b), color=green, stroke_width=3)

        tip_c1_big = attach_svg_tip_to_line(c1_big, red, line_end=e, scale=0.03, )
        tip_c2_big = attach_svg_tip_to_line(c2_big, blue, line_end=d, scale=0.03)
        tip_d1_big = attach_svg_tip_to_line(d1_big, yellow, line_end=f, scale=0.03)
        tip_d2_big = attach_svg_tip_to_line(d2_big, green, line_end=a, scale=0.03)
        c1_big.z_index = 1
        c2_big.z_index = 1
        d1_big.z_index = 1
        d2_big.z_index = 1
        tip_c1_big.z_index = 1
        tip_c2_big.z_index = 1
        tip_d1_big.z_index = 1
        tip_d2_big.z_index = 1

        self.play(ReplacementTransform(tip_d1, tip_d1_big),
                  ReplacementTransform(tip_d2, tip_d2_big),
                  ReplacementTransform(d1, d1_big),
                  ReplacementTransform(d2, d2_big),)
        self.wait()

        self.play(ReplacementTransform(tip_c1, tip_c1_big),
                  ReplacementTransform(tip_c2, tip_c2_big),
                  ReplacementTransform(c1, c1_big),
                  ReplacementTransform(c2, c2_big), )
        self.wait()

        self.play(self.camera.frame.animate.shift(0.9 * DOWN).scale(0.5/0.3))
        self.wait(1)


        group = Group(airplane, c1_big, c2_big, d1_big, d2_big, tip_c1_big, tip_c2_big, tip_d1_big, tip_d2_big)
        group.save_state()
        self.play(group.animate.rotate(30 * DEGREES, about_point=ORIGIN))
        self.wait()
        self.play(FadeOut(airplane))
        self.wait()
        self.play(FadeIn(airplane)) #restore
        self.play(group.animate.rotate(-30 * DEGREES, about_point=ORIGIN)) #restore
        self.wait()

        group = Group(grid, airplane, c1_big, c2_big, d1_big, d2_big, tip_c1_big, tip_c2_big, tip_d1_big, tip_d2_big)
        group.save_state()
        self.play(group.animate.rotate(30 * DEGREES, about_point=ORIGIN))
        self.wait()
        self.play(FadeOut(airplane))
        self.wait()
        self.play(Group(grid, c1_big, c2_big, d1_big, d2_big, tip_c1_big, tip_c2_big, tip_d1_big, tip_d2_big).animate.rotate(-30 * DEGREES, about_point=ORIGIN))
        self.wait()

        vec0 = MathTex(
            r"\begin{bmatrix}1\\2 \\0\end{bmatrix}",
            color=red, font_size=20)[0]
        vec0.shift(vec0[3].get_bottom()[1] * DOWN + 3* UNIT*LEFT)
        vec1 = MathTex(
            r"\begin{bmatrix}2\\-1 \\0\end{bmatrix}",
            color=blue, font_size=20)[0]
        vec1.shift(vec1[4].get_bottom()[1] * DOWN + 1*UNIT*LEFT)
        vec2 = MathTex(
            r"\begin{bmatrix}1\\0 \\0\end{bmatrix}",
            color=yellow, font_size=20)[0]
        vec2.shift(vec2[3].get_bottom()[1] * DOWN + 1*UNIT * RIGHT)
        vec3 = MathTex(
            r"\begin{bmatrix}\frac{\sqrt{2}}{2}\\[4pt] \frac{\sqrt{2}}{2}\\[4pt] 0\end{bmatrix}",
            color=green, font_size=20)[0]
        vec3.shift(vec3[11].get_bottom()[1] * DOWN + 3 * UNIT * RIGHT)

        self.play(
            grid.background_lines.animate.set_stroke(width=0.5)
        )
        self.wait()
        self.play(LaggedStart(ReplacementTransform(Group(c1_big, tip_c1_big), vec0),
                              ReplacementTransform(Group(c2_big, tip_c2_big), vec1),
                              ReplacementTransform(Group(d1_big, tip_d1_big), vec2),
                              ReplacementTransform(Group(d2_big, tip_d2_big), vec3),
                              lag_ratio=0.5))

        # ENDING AT "Let’s now take a look at these 2, 3 by 2 matrices."

        eq0 = MathTex(
            r"C = \begin{bmatrix}1 & 2\\[4pt]2 & -1\\[4pt]0 & 0\end{bmatrix}, \quad D = \begin{bmatrix}1 & \frac{\sqrt{2}}{2}\\[4pt]0 & \frac{\sqrt{2}}{2}\\[4pt]0 & 0\end{bmatrix}",
            color=dark_blue, font_size=20)[0]
        eq0.shift(eq0[0].get_bottom()[1] * DOWN)

        self.play(LaggedStart(FadeOut(vec0[:2]), FadeOut(vec0[5:]), FadeOut(vec1[:2]), FadeOut(vec1[6:]),
                  ReplacementTransform(vec0[2:5], VGroup(eq0[5], eq0[7], eq0[10])),
                  ReplacementTransform(vec1[2:6], VGroup(eq0[6], *eq0[8:10], eq0[11])),
                  GrowFromCenter(eq0[2:5]), GrowFromCenter(eq0[12:15]), lag_ratio=0.5
                  ))
        self.wait(1)

        self.play(
            LaggedStart(FadeOut(vec2[:2]), FadeOut(vec2[5:]), FadeOut(vec3[:4]), FadeOut(vec3[15:]),
                ReplacementTransform(vec2[2:5], VGroup(eq0[22], eq0[28], eq0[34])),
                ReplacementTransform(vec3[4:15], VGroup(*eq0[23:28], *eq0[29:34], eq0[35])),
                GrowFromCenter(eq0[18:22]), GrowFromCenter(eq0[36:]), lag_ratio=0
            )
        )
        self.wait(1)
        self.play(Write(eq0[0:2]), Write(eq0[15:18]))
        self.wait(1)
