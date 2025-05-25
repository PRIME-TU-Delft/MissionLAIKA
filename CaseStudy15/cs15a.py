from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF') #ManimColor('#002213')
class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3/4
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31') #ManimColor('#FF5132')
        yellow = ManimColor('#cc9316') #ManimColor('#FFCC12')
        blue = ManimColor('#0076C2') #ManimColor('#46A6FF')

        #Airplane is drawn in a different animation on green screen

        airplane_svg = SVGMobject("../assets/AirplaneFront.svg")
        airplane_svg.set_color(dark_blue).scale(1.35).shift(UP * 0.3)
        self.add(airplane_svg)
        self.wait(3)

        grid = NumberPlane(background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15
            },
            x_range=(0,72,1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        self.play(Write(grid))

        self.wait(3)

        list = airplane_svg.submobjects

        #Masses
        left_square = Square(color=dark_blue, side_length=2*UNIT).shift(LEFT * UNIT * 5)
        center_square = Square(color=dark_blue, side_length=4*UNIT)
        right_square = Square(color=dark_blue, side_length=2*UNIT).shift(RIGHT * UNIT * 5)

        #Springs
        spring_left = SVGMobject("../assets/Spring.svg", stroke_color=dark_blue, stroke_width=3).scale_to_fit_height(2*UNIT).rotate(PI/2)
        spring_right = spring_left.copy()

        spring_left.shift(3 * LEFT * UNIT)
        spring_right.shift(3 * RIGHT * UNIT)

        # INTRO 3 - Transform to mass-spring model - masses
        self.play(LaggedStart(
            ReplacementTransform(list[6], right_square),
            ReplacementTransform(list[7], left_square),
            ReplacementTransform(list[0], center_square),
            *(ShrinkToCenter(list[i]) for i in (1,2,3,4,5)),
            lag_ratio=0.2)
        )

        self.wait(2)

        spring_color = dark_blue
        #Add springs
        def get_spring():
            start = left_square.get_right()
            end = center_square.get_left()

            def spring_func(t):
                interp = start + t * (end - start)
                offset = np.array([0, 0.2 * np.sin(30 * t), 0])
                return interp + offset

            return ParametricFunction(spring_func, t_range=[0, 1], color=spring_color)

        def get_spring2():
            start = center_square.get_right()
            end = right_square.get_left()

            def spring_func(t):
                interp = start + t * (end - start)
                offset = np.array([0, 0.2 * np.sin(30 * t), 0])
                return interp + offset

            return ParametricFunction(spring_func, t_range=[0, 1], color=spring_color)

        spring_left = always_redraw(get_spring)
        spring_right = always_redraw(get_spring2)
        self.play(Write(spring_left), Write(spring_right))

        #SCENE 1.0

        #vertical movement
        self.play(left_square.animate.shift(2*UNIT*UP), right_square.animate.shift(2*UNIT*DOWN), run_time=0.5)
        self.play(left_square.animate.shift(4 * UNIT * DOWN), right_square.animate.shift(4 * UNIT * UP), run_time=0.5)
        self.play(left_square.animate.shift(2 * UNIT * UP), right_square.animate.shift(2 * UNIT * DOWN), run_time=0.5)

        self.wait()
        #horizontal movement
        self.play(left_square.animate.shift(1 * UNIT * RIGHT), right_square.animate.shift(2 * UNIT * RIGHT), run_time=0.5)
        self.play(left_square.animate.shift(3 * UNIT * LEFT), right_square.animate.shift(3 * UNIT * LEFT), run_time=0.5)
        self.play(left_square.animate.shift(2 * UNIT * RIGHT), right_square.animate.shift(1 * UNIT * RIGHT), run_time=0.5)


        self.wait(2)

        # SCENE 1.1

        m2 = MathTex("m_2", font_size=60, color=red)
        m1_left = MathTex("m_1", font_size=60, color=red).shift(LEFT * UNIT * 5)
        m1_right = MathTex("m_3", font_size=60, color=red).shift(RIGHT * UNIT * 5)

        self.play(LaggedStart(Write(m1_left), left_square.animate.set_color(red), Write(m1_right), right_square.animate.set_color(red), lag_ratio=0.2))
        self.wait(1)
        self.play(Write(m2), center_square.animate.set_color(red))
        self.wait(1)

        k_left = MathTex("k", font_size=60, color=blue)
        k_right = k_left.copy()
        k_left.shift(3 * LEFT * UNIT + 1.25 * UP * UNIT)
        k_right.shift(3 * RIGHT * UNIT + 1.25 * UP * UNIT)

        spring_left.clear_updaters()
        spring_right.clear_updaters()
        self.play(LaggedStart(GrowFromPoint(k_left, 3 * LEFT * UNIT),
                              spring_left.animate.set_color(blue),
                              GrowFromPoint(k_right, 3 * RIGHT * UNIT),
                              spring_right.animate.set_color(blue),
                              lag_ratio=0.2))
        spring_color = blue
        self.remove(spring_left, spring_right)
        spring_left = always_redraw(get_spring)
        spring_right = always_redraw(get_spring2)
        self.add(spring_left, spring_right)

        self.wait(1)
        self.play(self.camera.frame.animate.move_to(UNIT * DOWN))

        x_axis = Line(start=10*UNIT*LEFT + 5*UNIT*DOWN, end=8*UNIT*RIGHT + 5*UNIT*DOWN, color=dark_blue, stroke_width=4)
        x_axis.add_tip()
        x_axis_label = MathTex("x", font_size=60, color=dark_blue).move_to(x_axis.get_right() + 0.5 *UNIT* DOWN)
        self.play(Write(x_axis))
        self.play(Write(x_axis_label))
        self.wait(1)

        x1_line = DashedLine(left_square.get_bottom(), left_square.get_bottom() + 2* DOWN * UNIT, color=yellow, dash_length=0.2*UNIT, dashed_ratio=0.6 )
        x2_line = DashedLine(center_square.get_bottom(), center_square.get_bottom() + DOWN * UNIT, color=yellow,
                              dash_length=0.2 * UNIT, dashed_ratio=0.6)
        x3_line = DashedLine(right_square.get_bottom(), right_square.get_bottom() + 2 * DOWN * UNIT, color=yellow,
                              dash_length=0.2 * UNIT, dashed_ratio=0.6)

        self.play(LaggedStart(Write(x1_line), Write(x2_line), Write(x3_line), lag_ratio=0.2))

        x1_equil = x1_line.get_bottom()
        x2_equil = x2_line.get_bottom()
        x3_equil = x3_line.get_bottom()

        x1_dist = always_redraw(lambda : Line(x1_equil, x1_line.get_bottom(), color=yellow))
        x2_dist = always_redraw(lambda: Line(x2_equil, x2_line.get_bottom(), color=yellow))
        x3_dist = always_redraw(lambda: Line(x3_equil, x3_line.get_bottom(), color=yellow))
        self.play(Write(x1_dist), Write(x2_dist), Write(x3_dist))

        x1 = MathTex("x_1", font_size=60, color=yellow).move_to(x1_dist.get_center() + 0.5 * UNIT * DOWN)
        x2 = MathTex("x_2", font_size=60, color=yellow).move_to(x2_dist.get_center() + 0.5 * UNIT * DOWN)
        x3 = MathTex("x_3", font_size=60, color=yellow).move_to(x3_dist.get_center() + 0.5 * UNIT * DOWN)

        self.play(LaggedStart(Write(x1), Write(x2), Write(x3), lag_ratio=0.2))
        x1.add_updater(lambda m: m.move_to(x1_dist.get_center() + 0.5 * UNIT * DOWN))
        x2.add_updater(lambda m: m.move_to(x2_dist.get_center() + 0.5 * UNIT * DOWN))
        x3.add_updater(lambda m: m.move_to(x3_dist.get_center() + 0.5 * UNIT * DOWN))

        #MOVING STUFF WITH TRACKERS
        x1_tracker = ValueTracker(0)
        x2_tracker = ValueTracker(0)
        x3_tracker = ValueTracker(0)

        #left
        left_square.add_updater(lambda m: m.move_to(RIGHT * UNIT * (x1_tracker.get_value()) + LEFT * UNIT * 5))
        m1_left.add_updater(lambda m : m.move_to(left_square.get_center()))
        x1_line.add_updater(lambda m: m.move_to(left_square.get_center()+ 2 * DOWN * UNIT))
        value_x1 = always_redraw(
            lambda: DecimalNumber(
                x1_tracker.get_value(), num_decimal_places=2, color = yellow
            ).move_to(x1_dist.get_center()+0.5*UNIT*DOWN)
        )
        self.play(ReplacementTransform(x1, value_x1))

        #center
        center_square.add_updater(lambda m: m.move_to(RIGHT * UNIT * (x2_tracker.get_value())))
        m2.add_updater(lambda m: m.move_to(center_square.get_center()))
        x2_line.add_updater(lambda m: m.move_to(center_square.get_center() + 2.5 * DOWN * UNIT))
        value_x2 = always_redraw(
            lambda: DecimalNumber(
                x2_tracker.get_value(), num_decimal_places=2, color=yellow
            ).move_to(x2_dist.get_center()+0.5*UNIT*DOWN)
        )
        self.play(ReplacementTransform(x2, value_x2))

        # right
        right_square.add_updater(lambda m: m.move_to(RIGHT * UNIT * (x3_tracker.get_value()) + RIGHT * UNIT * 5))
        m1_right.add_updater(lambda m: m.move_to(right_square.get_center()))
        x3_line.add_updater(lambda m: m.move_to(right_square.get_center() + 2 * DOWN * UNIT))
        value_x3 = always_redraw(
            lambda: DecimalNumber(
                x3_tracker.get_value(), num_decimal_places=2, color=yellow
            ).move_to(x3_dist.get_center()+0.5*UNIT*DOWN)
        )
        self.play(ReplacementTransform(x3, value_x3))

        k_left.add_updater(lambda m : m.move_to(spring_left.get_center() + 1.25 * UP * UNIT))
        k_right.add_updater(lambda m : m.move_to(spring_right.get_center() + 1.25 * UP * UNIT))

        self.play(x1_tracker.animate.set_value(2), x2_tracker.animate.set_value(1), run_time=2)
        self.play(x1_tracker.animate.set_value(0), x2_tracker.animate.set_value(0), run_time=2)
        self.play(x3_tracker.animate.set_value(-2), x2_tracker.animate.set_value(-1), run_time=2)
        self.play(x3_tracker.animate.set_value(0), x2_tracker.animate.set_value(0), run_time=2)
        self.play(x1_tracker.animate.set_value(-3), x2_tracker.animate.set_value(-2), x3_tracker.animate.set_value(-1), run_time=2)
        self.play(x1_tracker.animate.set_value(0), x2_tracker.animate.set_value(0), x3_tracker.animate.set_value(0),
                  run_time=2)
        self.wait(2)

        self.play(Unwrite(value_x1), Unwrite(value_x2), Unwrite(value_x3))
        self.play(Unwrite(x1_dist), Unwrite(x2_dist), Unwrite(x3_dist))
        self.play( Unwrite(x1_line), Unwrite(x2_line), Unwrite(x3_line))

        self.play(Unwrite(x_axis), Unwrite(x_axis_label))

        self.wait(1)
        self.play(self.camera.frame.animate.move_to(center_square))

        self.wait(1)

        # SHOW FORCES FOR CENTER MASS
        groupm2 = Group(center_square, m2)
        self.play(Indicate(groupm2))
        self.wait(1)

        self.play(x1_tracker.animate.set_value(-2), run_time=1)
        self.play(x1_tracker.animate.set_value(0), run_time=1)

        eq01 = MathTex("x_2-x_1", color=dark_blue, font_size=60)[0].shift(2.75 * UNIT * DOWN + 3 * UNIT * LEFT)
        eq01[:2].set_color(yellow)
        eq01[3:].set_color(yellow)
        eq02 = MathTex("-k(x_2-x_1)", color=dark_blue, font_size=60)[0].shift(2.75 * UNIT * DOWN + 3 * UNIT * LEFT)
        eq02[1].set_color(blue)
        eq02[3:5].set_color(yellow)
        eq02[6:8].set_color(yellow)
        eq03 = MathTex("k(x_3-x_2)", color=dark_blue, font_size=60)[0].shift(2.75 * UNIT * DOWN + 3 * UNIT * RIGHT)
        eq03[0].set_color(blue)
        eq03[2:4].set_color(yellow)
        eq03[5:7].set_color(yellow)
        eq0 = (MathTex("F_2 = -k(x_2-x_1) + k(x_3-x_2)", color=dark_blue, font_size=60)[0]
               .shift(2.75 * UNIT * DOWN + 0.5 * UNIT * LEFT))
        eq0[4].set_color(blue)
        eq0[6:8].set_color(yellow)
        eq0[9:11].set_color(yellow)
        eq0[13].set_color(blue)
        eq0[15:17].set_color(yellow)
        eq0[18:20].set_color(yellow)

        self.play(Write(eq01))
        self.wait(1)
        self.play(ReplacementTransform(eq01, eq02[3:8]), Write(eq02[:3]), Write(eq02[8]))
        self.wait(1)
        self.play(x3_tracker.animate.set_value(2), run_time=1)
        self.play(x3_tracker.animate.set_value(0), run_time=1)
        self.wait(1)
        self.play(Write(eq03))
        self.wait(1)
        self.play(ReplacementTransform(eq02, eq0[3:3+len(eq02)]), ReplacementTransform(eq03, eq0[13:]), Write(eq0[:3]), Write(eq0[12]))
        self.wait(1)
        self.play(eq0.animate.scale(0.8))
        self.play(eq0.animate.shift(9 * UNIT * LEFT + 4 * UNIT * DOWN - eq0[0].get_corner(DL)))
        self.wait(1)

        # SHOW FORCES FOR LEFT MASS
        groupm1 = Group(left_square, m1_left)
        self.play(Indicate(groupm1))
        self.wait(1)

        eq21 = MathTex("--k(x_2-x_1)", color=dark_blue, font_size=60)[0].shift(2.75 * UNIT * DOWN + 3 * UNIT * LEFT)
        eq21[2].set_color(blue)
        eq21[4:6].set_color(yellow)
        eq21[7:9].set_color(yellow)
        eq2 = (MathTex("F_1 = k(x_2-x_1)", color=dark_blue, font_size=60)[0]
               .shift(2.75 * UNIT * DOWN + 3.5 * UNIT * LEFT))
        eq2[3].set_color(blue)
        eq2[5:7].set_color(yellow)
        eq2[8:10].set_color(yellow)
        self.play(ReplacementTransform(eq0[3:12].copy(), eq21[1:]))
        self.wait(1)
        self.play(Write(eq21[0]))
        self.wait(1)
        self.play(Unwrite(eq21[:2]))
        self.wait(1)
        self.play(ReplacementTransform(eq21[2:], eq2[3:]), Write(eq2[:3]))

        self.play(eq2.animate.scale(0.8))
        self.play(eq2.animate.shift(9 * UNIT * LEFT + 3 * UNIT * DOWN - eq2[0].get_corner(DL)))
        self.wait(1)

        # SHOW FORCES FOR RIGHT MASS
        groupm3 = Group(right_square, m1_right)
        self.play(Indicate(groupm3))
        self.wait(1)

        eq31 = MathTex("-k(x_3-x_2)", color=dark_blue, font_size=60)[0].shift(2.5 * UNIT * RIGHT, 2.75 * UNIT * DOWN)
        eq31[1].set_color(blue)
        eq31[3:5].set_color(yellow)
        eq31[6:8].set_color(yellow)
        eq3 = (MathTex("F_3 = -k(x_3-x_2)", color=dark_blue, font_size=60)[0]
               .shift(2.5 * UNIT * RIGHT, 2.75 * UNIT * DOWN))
        eq3[4].set_color(blue)
        eq3[6:8].set_color(yellow)
        eq3[9:11].set_color(yellow)
        self.play(ReplacementTransform(eq0[13:].copy(), eq31[1:]))
        self.wait(1)
        self.play(Write(eq31[0]))
        self.wait(1)
        self.play(ReplacementTransform(eq31, eq3[3:]), Write(eq3[:3]))
        self.wait(1)

        self.play(eq3.animate.scale(0.8))
        self.play(eq3.animate.shift(9*UNIT*LEFT + 5* UNIT * DOWN - eq3[0].get_corner(DL)))
        self.wait(1)

        group1 = Group(m1_right, right_square,center_square, m2, spring_left, k_left, m1_left, left_square, spring_right, k_right, m1_left)
        for mob in group1:
            mob.clear_updaters()
        self.add(group1)

        #SCENE1 -> SCENE2: model scaled down
        group4 = Group(m1_right, right_square,center_square, m2, spring_left, k_left, m1_left, left_square, spring_right, k_right, m1_left)
        self.play(group4.animate.scale(0.5))
        self.play(group4.animate.shift(4*UNIT*UP + 6*UNIT*LEFT))
        self.wait(1)

        #F1, F2, F3 scaled and moved
        group5 = Group(eq0, eq2, eq3)
        self.play(group5.animate.scale(0.8, about_point=eq2.get_left()))
        self.play(group5.animate.shift(5 * UNIT * UP))
        self.wait(1)

        self.play(self.camera.frame.animate.move_to(8 * UNIT * RIGHT))

        eq4 = MathTex(r"\textbf{F} = m \textbf{a}", color=dark_blue, font_size=60)[0]
        eq4.shift(8 * UNIT * RIGHT - eq4.get_bottom())

        eq4[2].set_color(red)
        self.play(Write(eq4))
        self.wait(1)

        eq5 = MathTex(r"\textbf{a} = \textbf{x}''", color=dark_blue, font_size=60)[0]
        eq5.shift(11 * UNIT * RIGHT - eq5.get_bottom())
        eq5[2].set_color(yellow)
        self.play(LaggedStart(eq4.animate.shift(3*UNIT*LEFT), Write(eq5), lag_ratio=0.4))
        self.wait(1)

        eq6 = MathTex(r"\textbf{F} = m \textbf{x}''", color=dark_blue, font_size=60)[0]
        eq6.shift(8 * UNIT * RIGHT - eq6.get_bottom())
        eq6[2].set_color(red)
        eq6[3].set_color(yellow)

        self.play(ShrinkToCenter(eq4[3]), ShrinkToCenter(eq5[:2]), ReplacementTransform(eq4[:3], eq6[:3]), ReplacementTransform(eq5[2:], eq6[3:]))

        self.play(eq6.animate.scale(0.6))
        self.play(eq6.animate.shift(3*UNIT*UP + 8* RIGHT *UNIT - eq6.get_bottom()))


        eq7 = MathTex(r"\textbf{x} ="
            r"\begin{bmatrix}"
            r"x_1\\"
            r"x_2\\"
            r"x_3"
            r"\end{bmatrix}", color=dark_blue, font_size=60)[0]
        eq7.shift(8 * UNIT * RIGHT - eq7[0].get_bottom()[1] - eq7.get_center()[0])
        eq7[0].set_color(yellow)
        eq7[4:6].set_color(yellow)
        eq7[6:8].set_color(yellow)
        eq7[8:10].set_color(yellow)

        self.play(Write(eq7))
        self.wait(1)

        eq8 = MathTex(r"\textbf{x}' ="
                      r"\begin{bmatrix}"
                      r"x_1'\\"
                      r"x_2'\\"
                      r"x_3'"
                      r"\end{bmatrix}", color=dark_blue, font_size=60)[0]
        eq8.shift(8 * UNIT * RIGHT - eq8[0].get_bottom()[1] - eq8.get_center()[0])
        eq8[0].set_color(yellow)
        eq8[5:14].set_color(yellow)
        eq8[6].set_color(dark_blue)
        eq8[9].set_color(dark_blue)
        eq8[12].set_color(dark_blue)
        self.play(ReplacementTransform(eq7[0], eq8[0]), GrowFromCenter(eq8[1]))
        self.play(GrowFromCenter(eq8[6]), GrowFromCenter(eq8[9]), GrowFromCenter(eq8[12]),
                  ReplacementTransform(eq7[1:5], eq8[2:6]),
                  ReplacementTransform(eq7[5:7], eq8[7:9]),
                  ReplacementTransform(eq7[7:9], eq8[10:12]),
                  ReplacementTransform(eq7[9:], eq8[13:]),)
        self.wait(1)

        eq9 = MathTex(r"\textbf{x}'' ="
                      r"\begin{bmatrix}"
                      r"x_1''\\"
                      r"x_2''\\"
                      r"x_3''"
                      r"\end{bmatrix}", color=dark_blue, font_size=60)[0]
        eq9.shift(8 * UNIT * RIGHT - eq9[0].get_bottom()[1] - eq9.get_center()[0])
        eq9[0].set_color(yellow)
        eq9[6:18].set_color(yellow)
        eq9[7:9].set_color(dark_blue)
        eq9[11:13].set_color(dark_blue)
        eq9[15:17].set_color(dark_blue)
        self.play(GrowFromCenter(eq9[2]), GrowFromCenter(eq9[8]), GrowFromCenter(eq9[12]), GrowFromCenter(eq9[16]),
                  ReplacementTransform(eq8[0:2], eq9[0:2]),
                  ReplacementTransform(eq8[2:7], eq9[3:8]),
                  ReplacementTransform(eq8[7:10], eq9[9:12]),
                  ReplacementTransform(eq8[10:13], eq9[13:16]),
                  ReplacementTransform(eq8[13:], eq9[17:]))

        self.play(eq9.animate.scale(0.6))
        self.wait(1)
        self.play(LaggedStart(eq6.animate.shift(4 * UNIT * UP - eq6.get_bottom()), eq9.animate.shift(5 * UNIT * RIGHT + 4 * UNIT * UP - eq9[0].get_bottom()[1] * UP - eq9.get_center()[0] * RIGHT), self.camera.frame.animate.move_to(ORIGIN),   lag_ratio=0.4))
        self.wait(1)

        eq10 = MathTex(
            r"\begin{cases}"
            r"F_1 = k(x_2-x_1) \\"
            r"F_2 = -k(x_2-x_1) + k(x_3-x_2) \\"
            r"F_3 = -k(x_3-x_2) \\"
            r"\end{cases}", color=dark_blue
        )[0]
        eq10[5 + 3].set_color(blue)
        eq10[5 + 5:5 + 7].set_color(yellow)
        eq10[5 + 8:5 + 10].set_color(yellow)
        eq10[5 + len(eq2) + 4].set_color(blue)
        eq10[5 + len(eq2) + 6:5 + len(eq2) + 8].set_color(yellow)
        eq10[5 + len(eq2) + 9:5 + len(eq2) + 11].set_color(yellow)
        eq10[5 + len(eq2) + 13].set_color(blue)
        eq10[5 + len(eq2) + 15:5 + len(eq2) + 17].set_color(yellow)
        eq10[5 + len(eq2) + 18:5 + len(eq2) + 20].set_color(yellow)
        eq10[5 + len(eq2) + len(eq0) + 4].set_color(blue)
        eq10[5 + len(eq2) + len(eq0) + 6:5 + len(eq2) + len(eq0) + 8].set_color(yellow)
        eq10[5 + len(eq2) + len(eq0) + 9:5 + len(eq2) + len(eq0) + 11].set_color(yellow)


        self.play(ReplacementTransform(eq2, eq10[5:5+len(eq2)]))
        self.play(ReplacementTransform(eq0, eq10[5 + len(eq2):5 + len(eq2) + len(eq0)]))
        self.play(ReplacementTransform(eq3, eq10[5 + len(eq2) + len(eq0):5 + len(eq2) + len(eq0) +len(eq3)]))
        self.play(Write(eq10[:5]))

        eq11 = MathTex(
            r"\begin{cases}"
            r"m_1 x_1'' = k(x_2-x_1) \\"
            r"m_2 x_2'' = -k(x_2-x_1) + k(x_3-x_2) \\"
            r"m_3 x_3'' = -k(x_3-x_2) \\"
            r"\end{cases}", color=dark_blue
        )[0]
        eq11[5 + 3+4].set_color(blue)
        eq11[5 + 5+4:5 + 7+4].set_color(yellow)
        eq11[5 + 8+4:5 + 10+4].set_color(yellow)
        eq11[5 + len(eq2) + 4+8].set_color(blue)
        eq11[5 + len(eq2) + 6+8:5 + len(eq2) + 8+8].set_color(yellow)
        eq11[5 + len(eq2) + 9+8:5 + len(eq2) + 11+8].set_color(yellow)
        eq11[5 + len(eq2) + 13+8].set_color(blue)
        eq11[5 + len(eq2) + 15+8:5 + len(eq2) + 17+8].set_color(yellow)
        eq11[5 + len(eq2) + 18+8:5 + len(eq2) + 20+8].set_color(yellow)
        eq11[5 + len(eq2) + len(eq0) + 4+12].set_color(blue)
        eq11[5 + len(eq2) + len(eq0) + 6+12:5 + len(eq2) + len(eq0) + 8+12].set_color(yellow)
        eq11[5 + len(eq2) + len(eq0) + 9+12:5 + len(eq2) + len(eq0) + 11+12].set_color(yellow)
        eq11[5:7].set_color(red)
        eq11[5+len(eq2)+4:5+len(eq2)+4+2].set_color(red)
        eq11[5+len(eq2)+4+len(eq0)+4:5+len(eq2)+4+len(eq0)+4+2].set_color(red)
        eq11[5 + 2].set_color(yellow)
        eq11[5 + len(eq2) + 4 + 2].set_color(yellow)
        eq11[5 + len(eq2) + 4 + len(eq0) + 4 + 2].set_color(yellow)
        eq11[5 + 2+3].set_color(yellow)
        eq11[5 + len(eq2) + 4 + 2+3].set_color(yellow)
        eq11[5 + len(eq2) + 4 + len(eq0) + 4 + 2+3].set_color(yellow)

        self.play(ReplacementTransform(eq10[:5], eq11[:5]),
                  ReplacementTransform(eq10[7:7+len(eq2)-2], eq11[11:11+len(eq2)-2]),
                  ReplacementTransform(eq10[7+len(eq2):7+len(eq2) + len(eq0) - 2], eq11[11+len(eq2)+4:11+len(eq2)+len(eq0)+2]),
                  ReplacementTransform(eq10[7+len(eq2) + len(eq0):7+len(eq2) + len(eq0) +len(eq3) - 2], eq11[11+len(eq2)+len(eq0)+8:11+len(eq2)+len(eq0)+len(eq3)+6]),)
        self.play(ReplacementTransform(eq6[2].copy(), eq11[5]),
                  ReplacementTransform(eq6[2].copy(), eq11[5+len(eq2)+4]),
                  ReplacementTransform(eq6[2].copy(), eq11[5+len(eq2)+4+len(eq0)+4]),
                  ShrinkToCenter(eq10[5]),
                  ShrinkToCenter(eq10[5 + len(eq2)]),
                  ShrinkToCenter(eq10[5 + len(eq2) + len(eq0)]),
                  ReplacementTransform(eq6[3:].copy(), eq11[5+2:5+2+3]),
                  ReplacementTransform(eq6[3:].copy(), eq11[5+len(eq2)+4+2:5+len(eq2)+4+2+3]),
                  ReplacementTransform(eq6[3:].copy(), eq11[5+len(eq2)+4+len(eq0)+4+2:5+len(eq2)+4+len(eq0)+4+2+3]),
                  ReplacementTransform(eq10[5+1].copy(), eq11[5+1]),
                  ReplacementTransform(eq10[5 + len(eq2)+1].copy(), eq11[5+len(eq2)+4+1]),
                  ReplacementTransform(eq10[5 + len(eq2) + len(eq0)+1].copy(), eq11[5+len(eq2)+4+len(eq0)+4+1]),
                  ReplacementTransform(eq10[5 + 1], eq11[5+2+3]),
                  ReplacementTransform(eq10[5 + len(eq2) + 1], eq11[5+len(eq2)+4+2+3]),
                  ReplacementTransform(eq10[5 + len(eq2) + len(eq0) + 1], eq11[5+len(eq2)+4+len(eq0)+4+2+3]),
                  )

        self.wait(1)

