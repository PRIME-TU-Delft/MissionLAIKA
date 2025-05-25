from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF')

class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        dark_blue = ManimColor('#0C2340')  #VERSION 2    DEFAULT
        red = ManimColor('#E03C31')        #E03C31       E03C31
        yellow = ManimColor('#cc9316')     #6CC24A       cc9316
        blue = ManimColor('#0076C2')       #0076C2       0076C2

        # Wheel
        outer_circle = Circle(stroke_color=dark_blue, radius=1.7)
        inner_circle = Circle(stroke_color=dark_blue, radius=0.9)
        line1 = Line(color=dark_blue, start=[0.4, 1.65, 0], end=[0.4, 3.15, 0])
        line2 = Line(color=dark_blue, start=[-0.4, 1.65, 0], end=[-0.4, 3.07, 0])
        wheel_text = Tex("wheel", font_size=42, color=dark_blue)

        wheel = Group(outer_circle, inner_circle, line1, line2, wheel_text)
        wheel.to_edge(2 * DOWN)
        # Ground
        ground = Line(color=dark_blue, start=[-15, 0, 0], end=[15, 0, 0])
        ground.to_edge(2 * DOWN)

        # Plane
        plane = Circle(stroke_color=dark_blue, radius=3)
        plane.scale([5.1, 1, 1])
        plane.move_to(Point([-4.1, 4.7, 0]))
        plane_text = Tex("airplane", font_size=42, color=dark_blue)
        plane_text.shift(2.7*UP)

        self.add(outer_circle, inner_circle, plane, line1, line2, ground)

        #Draw the ground lines
        ground_line = Line(color=dark_blue,start=[-15,-4,0], end=[-14,-3,0])
        ground_lines = []
        for i in range(30):
            ground_line_c = ground_line.copy().shift(i * RIGHT)
            ground_lines.append(ground_line_c)

        self.add(*ground_lines)

        self.wait(1);
        grid = NumberPlane(background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15
            },
            x_range=(1, 50, 1),
            y_range=(1, 25, 1),
            x_length=30,
            y_length=15
        )

        self.play(Write(grid))

        #annotate plane and wheel
        self.play(Write(plane_text), Write(wheel_text))

        m1 = Square(2, color = red)
        m2 = m1.copy()
        m1.to_edge(4.5*DOWN)
        m2.to_edge(UP)

        m2_text = MathTex("m_2", font_size=60, color = red).move_to(Point([0, 2.5, 0]))
        m1_text = MathTex("m_1", font_size=60, color = red).move_to(Point([0, -0.8, 0]))

        self.wait(2)

        # transform into mass spring model
        # airplane
        self.play(LaggedStart(Transform(mobject=plane, target_mobject=m2, path_arc=0), ShrinkToCenter(line1), ShrinkToCenter(line2), lag_ratio=0.4, run_time=1.2))
        # wheel
        self.play(
            Transform(mobject=outer_circle, target_mobject=m1, path_arc=0),
                  Transform(mobject=plane, target_mobject=m2, path_arc=0), ShrinkToCenter(inner_circle),
                  wheel_text.animate.move_to(Point([0, -0.8, 0])),
                plane_text.animate.shift(0.2 * DOWN), run_time=1.2)

        # change the annotations
        self.wait(2)
        self.play(Transform(wheel_text, m1_text))
        self.wait(0.5)
        self.play(Transform(plane_text, m2_text))
        self.wait(2)

        #springs
        spring2 = SVGMobject("../assets/Spring.svg", stroke_color=blue, stroke_width=3).scale(0.63)

        spring = spring2.copy()
        spring2.shift(UP * 0.88)
        spring.shift(DOWN * 2.37)
        self.play(Write(spring), Write(spring2))
        self.wait(1)

        # show k
        k2_text = MathTex("k_2", font_size=60, color=blue).move_to(Point([1.5, 0.9, 0]))
        k1_text = MathTex("k_1", font_size=60, color=blue).move_to(Point([1.5, -2.3, 0]))

        self.play(GrowFromPoint(k1_text, Point([0, -2.3, 0])))
        self.wait(1)
        self.play(GrowFromPoint(k2_text, Point([0, 0.9, 0])))
        self.wait(1)

        damping = SVGMobject("../assets/damping.svg", stroke_color=dark_blue, stroke_width=3).scale(0.63)
        damping.shift(0.88 * UP + 0.5 * LEFT)
        self.play(LaggedStart(spring2.animate.shift(RIGHT * 0.5), Write(damping), LaggedStart=0.9))
        self.wait(1)
        gamma = MathTex("\gamma", font_size=60, color=dark_blue).move_to(damping.get_left() + LEFT)
        self.play(GrowFromPoint(gamma, damping.get_center()))
        self.wait(1)

        x2_text = MathTex("x_2", font_size=60, color=yellow).move_to(Point(m2.get_left() + [-2, 0, 0]))
        x1_text = MathTex("x_1", font_size=60, color=yellow).move_to(Point(m1.get_left() + [-2, 0, 0]))
        # self.play(Write(x1_text))
        # self.wait(0.5)
        # self.play(Write(x2_text))
        self.wait(1)

        # move arrows to the side with dashed lines
        dashed_1 = DashedLine(m1.get_left(), m1.get_left()+1.5*LEFT, dashed_ratio=0.6, dash_length=0.2, color=yellow)
        dashed_2 = DashedLine(m2.get_left(), m2.get_left() + 1.5*LEFT, dashed_ratio=0.6, dash_length=0.2, color=yellow)
        xs = Group(x1_text, x2_text)
        self.play(Write(dashed_1), Write(dashed_2))

        x_axis = Arrow(start=4*LEFT + 3.25* DOWN, end=4*LEFT + 4*UP, color=dark_blue, stroke_width=4)
        x_axis_label = MathTex("x", font_size=60, color=dark_blue).move_to(x_axis.get_top() + 0.5 *LEFT + 0.5 *DOWN)
        self.play(GrowArrow(x_axis))
        self.play(Write(x_axis_label))
        self.wait(1)

        point = m2.get_left()+1.5*LEFT
        point2 = m1.get_left()+1.5*LEFT
        arrow1 = Line( point2, point2+0.1*DOWN, color=yellow)
        arrow2 = Line( start=point, end=point + 0.1* DOWN, color=yellow)

        #push the m2 mass down
        m2group = Group(dashed_2, plane, plane_text)
        self.wait()
        self.play(Write(x2_text))
        self.add(arrow2)
        self.play(gamma.animate.shift(0.4*DOWN), k2_text.animate.shift(0.4*DOWN),x2_text.animate.shift(0.4*DOWN),m2group.animate.shift(0.8*DOWN), arrow2.animate.stretch(8, 1, about_edge=UP), spring2.animate.stretch(0.34, dim=1, about_edge=DOWN), damping.animate.stretch(0.34, dim=1, about_edge=DOWN))

        #push the m2 and m1 masses down
        m2m1group = Group(dashed_2, plane, plane_text, outer_circle, dashed_1, spring2, damping, wheel_text)
        self.wait()
        self.play(Write(x1_text))
        self.add(arrow1)
        self.play(gamma.animate.shift(0.8*DOWN),k2_text.animate.shift(0.8*DOWN), k1_text.animate.shift(0.2*DOWN),x2_text.animate.shift(0.4*DOWN), x1_text.animate.shift(0.4*DOWN), m2m1group.animate.shift(0.8*DOWN),arrow2.animate.stretch(2, 1, about_edge=UP), arrow1.animate.stretch(8, 1, about_edge=UP), spring.animate.stretch(0.34, dim=1, about_edge=DOWN))

        #extend m2 mass
        self.play(gamma.animate.shift(0.4 * UP),k2_text.animate.shift(0.4 * UP), x2_text.animate.shift(0.4 * UP),
                  m2group.animate.shift(0.8 * UP), arrow2.animate.stretch(0.5, 1, about_edge=UP),
                  spring2.animate.stretch(1/0.34, dim=1, about_edge=DOWN),
                  damping.animate.stretch(1/0.34, dim=1, about_edge=DOWN))

        #extend both masses
        self.play(k2_text.animate.shift(0.8 * UP), gamma.animate.shift(0.8 * UP), k1_text.animate.shift(0.2 * UP),
                  x2_text.animate.shift(0.4 * UP), x1_text.animate.shift(0.4 * UP),
                  m2m1group.animate.shift(0.8 * UP), arrow2.animate.stretch(0.01, 1, about_edge=UP),
                  arrow1.animate.stretch(0.01, 1, about_edge=UP), spring.animate.stretch(1/0.34, dim=1, about_edge=DOWN))


        #MOVE CAMERA
        center = Point([3.5, 0, 0])
        self.play(self.camera.frame.animate.move_to(center))
        self.wait()

        #write the spring force and write newtons second law
        eq0 = MathTex("F_{\\text{spring}} = -kx", color = dark_blue)[0].shift(8*RIGHT +3*UP)
        eq02 = MathTex("F_{\\text{gravity}}=-mg", color = dark_blue)[0].shift(8*RIGHT +2* UP)
        eq0[9].set_color(blue)
        eq0[10].set_color(yellow)
        eq02[10].set_color(red)

        eq1p = MathTex("F_{\\text{total}} = ma = mx'' ", color = dark_blue)[0].shift(8*RIGHT)
        eq1p[7].set_color(red)
        eq1p[10].set_color(red)
        eq1p[11].set_color(yellow)

        eq1p2 = MathTex("F_{\\text{total}} = mx'' ", color=dark_blue)[0].shift(8.1 * RIGHT)
        eq1p2[7].set_color(red)
        eq1p2[8].set_color(yellow)

        eq1p3p = MathTex("F_{\\text{damping}} = - \\gamma x' = 0", color=dark_blue)[0]
        eq1p3p[:len(eq1p3p)-2].shift(8.35 * RIGHT + UP)
        eq1p3p[len(eq1p3p)-2:].shift(8.15 * RIGHT + UP)
        eq1p3p[11].set_color(yellow)
        eq1p3 = MathTex("F_{\\text{damping}} = 0", color=dark_blue)[0].shift(7.45 * RIGHT + UP)

        eq1 = MathTex("mx'' = F_{\\text{total}}", color = dark_blue)[0].shift(8.2*RIGHT)
        eq1[0].set_color(red)
        eq1[1].set_color(yellow)
        eq1c = eq1.copy()
        eq1c2 = eq1.copy()
        eq2 = MathTex("m_1x_1'' = F_{\\text{total}_1}", color = dark_blue)[0].shift(4.35*RIGHT +1.15*DOWN)
        eq3 = MathTex("m_2x_2'' = F_{\\text{total}_2}", color = dark_blue)[0].shift(4.35 * RIGHT + 1.85*DOWN)
        eq2[0:2].set_color(red)
        eq2[2].set_color(yellow)
        eq2[5].set_color(yellow)
        eq3[0:2].set_color(red)
        eq3[2].set_color(yellow)
        eq3[5].set_color(yellow)

        self.play(Write(eq0))
        self.wait()
        self.play(Write(eq02))
        self.wait()
        self.play(Write(eq1p3p[:len(eq1p3p)-2]))
        self.wait()
        self.play(Wiggle(eq0[10], scale_value=1.5))
        self.wait()
        self.play(Wiggle(eq1p3p[11], scale_value=1.5))
        self.wait()
        self.play(Write(eq1p))
        self.wait()
        self.play(ReplacementTransform(eq1p[0:7], eq1p2[0:7]),
                  ReplacementTransform(eq1p[10:], eq1p2[7:]),
                  ShrinkToCenter(eq1p[7:10]))

        self.wait()
        self.play(ReplacementTransform(eq1p2[0:6], eq1[5:]),
                  ReplacementTransform(eq1p2[6], eq1[4]),
                  ReplacementTransform(eq1p2[7:], eq1[0:4]))
        self.add(eq1c)
        self.add(eq1c2)
        self.wait(1)
        self.play((ReplacementTransform(eq1c2[0], eq2[0:2]), ReplacementTransform(eq1c[0], eq3[0:2])),
                  (ReplacementTransform(eq1c2[1:4], eq2[2:6]), ReplacementTransform(eq1c[1:4], eq3[2:6])),
                (ReplacementTransform(eq1c2[4:11], eq2[6:14]), ReplacementTransform(eq1c[4:11], eq3[6:14])))
        self.remove(eq3, eq2, eq1c)
        self.wait(2)

        # totals to gravity and spring
        eq21 = MathTex("m_1x_1'' = F_{\\text{gravity}_1} + F_{\\text{spring}_1} - F_{\\text{damping}}", color=dark_blue)[0].shift(6.45 * RIGHT+1.13*DOWN)
        eq31 = MathTex("m_2x_2'' = F_{\\text{gravity}_2} + F_{\\text{spring}_2} + F_{\\text{damping}}", color=dark_blue)[0].shift(6.45 * RIGHT + 1.83*DOWN)
        eq21[0:2].set_color(red)
        eq21[2].set_color(yellow)
        eq21[5].set_color(yellow)
        eq31[0:2].set_color(red)
        eq31[2].set_color(yellow)
        eq31[5].set_color(yellow)

        self.play(ReplacementTransform(eq2[0:7], eq21[0:7]), ReplacementTransform(eq3[0:7], eq31[0:7]),
                  ReplacementTransform(eq2[7:], eq21[7:]), ReplacementTransform(eq3[7:], eq31[7:]))

        #damping = 0
        self.wait()
        self.play(eq1p3p[:len(eq1p3p) - 2].animate.shift(0.2 * LEFT))
        self.play(Write(eq1p3p[len(eq1p3p) - 2:]))
        self.wait()
        self.play(ShrinkToCenter(eq1p3p[9:14]), ReplacementTransform(eq1p3p[:9], eq1p3[:9]),
                  ReplacementTransform(eq1p3p[14:], eq1p3[9:]))
        self.wait()

        #total = 0
        eq5 = MathTex("mx'' = F_{total} = 0", color=dark_blue)[0].shift(8 * RIGHT)
        eq5[0].set_color(red)
        eq5[1].set_color(yellow)

        self.play(ReplacementTransform(eq1, eq5[:len(eq1)]), GrowFromCenter(eq5[len(eq1):]))

        eq22 = MathTex("0 = F_{\\text{gravity}_1} + F_{\\text{spring}_1} - 0", color=dark_blue)[0].shift(
            6 * RIGHT + 1.15 * DOWN)
        eq32 = \
        MathTex("0 = F_{\\text{gravity}_2} + F_{\\text{spring}_2} + 0", color=dark_blue)[
            0].shift(6 * RIGHT + 1.85 * DOWN)

        self.play(LaggedStart(ShrinkToCenter(eq21[0:6]), ReplacementTransform(eq5[12].copy(), eq22[0]),
                              ShrinkToCenter(eq31[0:6]), ReplacementTransform(eq5[12].copy(), eq32[0]),
                              ReplacementTransform(eq21[6:26], eq22[1:21]),
                              ReplacementTransform(eq31[6:26], eq32[1:21]),
                              ShrinkToCenter(eq21[26:]),
                              ReplacementTransform(eq1p3[9].copy(), eq22[21:]),
                              ShrinkToCenter(eq31[26:]),
                              ReplacementTransform(eq1p3[9].copy(), eq32[21:]),
                              lag_ratio=0.5))

        self.wait()
        self.play(ShrinkToCenter(eq22[20:]), ShrinkToCenter(eq32[20:]))

        self.wait(1)
        eq6 = MathTex(
            r"\begin{cases}"
            r"0 = -m_1 g- k_1x_1 + k_2(x_2-x_1) \\"
            r"0 = -m_2 g- k_2(x_2-x_1) "
            r"\end{cases}", color=dark_blue
        )[0].shift(6.5*RIGHT+ 1.5 * DOWN)

        eq6[4:6].set_color(red)
        eq6[8:10].set_color(blue)
        eq6[10:12].set_color(yellow)
        eq6[13:15].set_color(blue)
        eq6[16:18].set_color(yellow)
        eq6[19:21].set_color(yellow)

        eq6[25:27].set_color(red)
        eq6[29:31].set_color(blue)
        eq6[32:34].set_color(yellow)
        eq6[35:37].set_color(yellow)

        self.play(LaggedStart(GrowFromCenter(eq6[0]),
                              ReplacementTransform(eq22[0:2], eq6[1:3]),
                              ReplacementTransform(eq22[2:11], eq6[3:7]),
                              ReplacementTransform(eq22[11], eq6[7]),
                              ReplacementTransform(eq22[12:], eq6[8:22]),
                              ReplacementTransform(eq32[0:2], eq6[22:24]),
                              ReplacementTransform(eq32[2:11], eq6[24:28]),
                              ReplacementTransform(eq32[11], eq6[28]),
                              ReplacementTransform(eq32[12:20], eq6[29:]),
                              lag_ratio=0.5))

        eq7 = MathTex(
            r"\begin{cases}"
            r"m_1g = - k_1x_1 + k_2(x_2-x_1) \\"
            r"m_2g = - k_2(x_2-x_1) "
            r"\end{cases}", color = dark_blue
        )[0].shift(6.5*RIGHT+ 1.5 * DOWN)
        self.wait(1)
        eq7[1:3].set_color(red)
        eq7[6:8].set_color(blue)
        eq7[8:10].set_color(yellow)
        eq7[11:13].set_color(blue)
        eq7[14:16].set_color(yellow)
        eq7[17:19].set_color(yellow)

        eq7[20:22].set_color(red)
        eq7[25:27].set_color(blue)
        eq7[28:30].set_color(yellow)
        eq7[31:33].set_color(yellow)

        self.play(ShrinkToCenter(eq6[1]), ReplacementTransform(eq6[4:7], eq7[1:4]),
                    ShrinkToCenter(eq6[22]), ReplacementTransform(eq6[25:28], eq7[20:23]),
                    ReplacementTransform(eq6[0], eq7[0]), ReplacementTransform(eq6[2], eq7[4]),
                  ReplacementTransform(eq6[23], eq7[23]), ShrinkToCenter(eq6[3]), ShrinkToCenter(eq6[24]),
                  ReplacementTransform(eq6[7:22], eq7[4:20]), ReplacementTransform(eq6[28:], eq7[23:]))

        self.wait(1)

        eq8 = MathTex(
            r"\begin{cases}"
            r"m_1g = (-k_1 -k_2)x_1+k_2x_2 \\"
            r"m_2g = k_2x_1 - k_2x_2 "
            r"\end{cases}", color = dark_blue
        )[0].shift(6.5*RIGHT+ 1.5 * DOWN)

        eq8[1:3].set_color(red)
        eq8[7:9].set_color(blue)
        eq8[10:12].set_color(blue)
        eq8[13:15].set_color(yellow)
        eq8[16:18].set_color(blue)
        eq8[18:20].set_color(yellow)

        eq8[20:22].set_color(red)
        eq8[24:26].set_color(blue)
        eq8[26:28].set_color(yellow)
        eq8[29:31].set_color(blue)
        eq8[31:33].set_color(yellow)

        self.play(ReplacementTransform(eq7[11:13].copy(), eq8[16:18]), ShrinkToCenter(eq7[8:10]), GrowFromCenter(eq8[5]),
                  GrowFromCenter(eq8[12]), ReplacementTransform(eq7[5:8], eq8[6:9]), ReplacementTransform(eq7[17:19], eq8[13:15]),
                  ReplacementTransform(eq7[16], eq8[9]), ReplacementTransform(eq7[11:13], eq8[10:12]), ReplacementTransform(eq7[10], eq8[15]),
                  ReplacementTransform(eq7[14:16], eq8[18:20]), ShrinkToCenter(eq7[13]), ShrinkToCenter(eq7[19]),
                  ReplacementTransform(eq7[0:5], eq8[0:5]),
                  ReplacementTransform(eq7[20:24], eq8[20:24]))

        self.play(ShrinkToCenter(eq7[24]), ReplacementTransform(eq7[25:27].copy(), eq8[24:26]),
                  ReplacementTransform(eq7[25:27], eq8[29:31]), ShrinkToCenter(eq7[27]),
                  ShrinkToCenter(eq7[33]),
                  ReplacementTransform(eq7[31:33], eq8[26:28]), ReplacementTransform(eq7[28:30], eq8[31:33]), ReplacementTransform(eq7[30], eq8[28]))

        self.remove(eq7, eq6, eq2, eq3, eq21, eq31,eq8, eq1, eq1c, eq1c2)
        self.add(eq8)
        self.wait()
        everything = Group(gamma, damping, ground, *ground_lines, plane, outer_circle, spring, spring2, x1_text, x2_text, dashed_2, dashed_1, k2_text, k1_text, plane_text, wheel_text)
        self.play(LaggedStart(ShrinkToCenter(eq0),ShrinkToCenter(eq02), ShrinkToCenter(eq1p3), ShrinkToCenter(eq5),  lag_ratio=0.5))
        self.play(everything.animate.shift(6*DOWN + 6*LEFT))
        self.play(eq8.animate.shift(2.7*LEFT +1.5*UP))
        self.play(eq8.animate.scale(1.5))
