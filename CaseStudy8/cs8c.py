from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF')

class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3/4
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31') #ManimColor('#FF5132')
        yellow = ManimColor('#cc9316') #ManimColor('#FFCC12')
        blue = ManimColor('#0076C2') #ManimColor('#46A6FF')

        grid = NumberPlane(background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15
            },
            x_range=(0,72,1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        self.play(Write(grid))
        self.wait(1)


        # Create Mass spring system (3 masses, 2 springs)
        #Masses
        left_square = Square(color=red, side_length=2*UNIT).shift(LEFT * UNIT * 5 + 20 * RIGHT * UNIT)
        center_square = Square(color=red, side_length=4*UNIT). shift(20 * RIGHT * UNIT)
        right_square = Square(color=red, side_length=2*UNIT).shift(RIGHT * UNIT * 5+ 20 * RIGHT * UNIT)

        #Springs
        spring_left = SVGMobject("../assets/Spring.svg", stroke_color=dark_blue, stroke_width=3).scale_to_fit_height(2*UNIT).rotate(PI/2)
        spring_right = spring_left.copy()

        spring_left.shift(3 * LEFT * UNIT+ 20 * RIGHT * UNIT)
        spring_right.shift(3 * RIGHT * UNIT+ 20 * RIGHT * UNIT)

        spring_color = blue

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

        system = Group(spring_left, spring_right, left_square, right_square, center_square)
        system.shift(20*LEFT*UNIT + 2.5*UP*UNIT).scale(0.9)

        # mass labels
        m1_text = MathTex("m_1", font_size=60, color = red).move_to(Point([-3.75, 1.5, 0]))
        m2_text = MathTex("m_2", font_size=60, color = red).move_to(Point([0, 1.5, 0]))
        m3_text = MathTex("m_3", font_size=60, color = red).move_to(Point([3.75, 1.5, 0]))


        # spring labels
        k2_text = MathTex("k_2", font_size=60, color=blue).move_to(Point([2.25, 2.45, 0]))
        k1_text = MathTex("k_1", font_size=60, color=blue).move_to(Point([-2.25, 2.45, 0]))

        # nul A
        matrix_a_2 = MathTex(
            r"""{\renewcommand{\arraystretch}{1.5}
            \textbf{Nul A} = \left[\begin{array}{ccc|c}
            -1 & 1 & 0 & 0\\
            1 & -2 & 1 & 0\\
            0 & 1 & -1 & 0
            \end{array}\right]}
            \sim 
            \left[\begin{array}{ccc|c}
            -1 & 1 & 0 & 0\\
            0 & -1 & 1 & 0\\
            0 & 0 & 0 & 0
            \end{array}\right]}""",
            color=dark_blue,
            font_size=40
        )

        x_eq1 = MathTex(
           r"""\begin{cases}
            x_1 = x_2 \\
            x_2 = x_3 \\
            x_1 = x_3 \\
            \end{cases} \rightarrow
            \begin{bmatrix}
            x_1\\
            x_2\\
            x_3
            \end{bmatrix} = \begin{bmatrix}
            1\\
            1\\
            1
            \end{bmatrix} x_3""",
            color=dark_blue,
            font_size=50
        )

        # add masses and springs
        self.play(
            LaggedStart(
                FadeIn(left_square),
                FadeIn(center_square),
                FadeIn(right_square),
                lag_ratio=0.3
            )
        )
        self.play(Write(spring_left), Write(spring_right))
        self.wait(1)

        # add nul A
        self.play(Write(matrix_a_2.shift(2.5*DOWN), run_time=3))
        self.wait(1)

        # shift nul A and add x equations
        self.add(x_eq1.shift(20*RIGHT*UNIT + 2.5*DOWN))
        self.play(matrix_a_2.animate.shift(20*LEFT*UNIT),
                  x_eq1.animate.shift(20*LEFT*UNIT))
        self.wait(1)

        # create x labels and dashed lines
        x1_text = MathTex("x_1", font_size=60, color=yellow).move_to(left_square.get_bottom() + [0, -1.75, 0])
        x2_text = MathTex("x_2", font_size=60, color=yellow).move_to(center_square.get_bottom() + [0, -1, 0])
        x3_text = MathTex("x_3", font_size=60, color=yellow).move_to(right_square.get_bottom() + [0, -1.75, 0])
        dashed_1 = DashedLine(left_square.get_bottom(), left_square.get_bottom()+1.25*DOWN, dashed_ratio=0.6, dash_length=0.2, color=yellow)
        dashed_2 = DashedLine(center_square.get_bottom(), center_square.get_bottom()+0.5*DOWN, dashed_ratio=0.6, dash_length=0.2, color=yellow)
        dashed_3 = DashedLine(right_square.get_bottom(), right_square.get_bottom()+1.25*DOWN, dashed_ratio=0.6, dash_length=0.2, color=yellow)

        self.play(Write(dashed_1), Write(dashed_2), Write(dashed_3))
        self.play(Write(x1_text), Write(x2_text), Write(x3_text))

        self.wait(1)

        # add arrows and move system
        point1 = center_square.get_bottom() + 0.5*DOWN
        point2 = left_square.get_bottom() + 1.25*DOWN  
        point3 = right_square.get_bottom() + 1.25*DOWN

        arrow1 = Arrow(start=point2, end=point2 + 0.1*RIGHT, color=yellow, buff=0)
        arrow2 = Arrow(start=point1, end=point1 + 0.1*RIGHT, color=yellow, buff=0)
        arrow3 = Arrow(start=point3, end=point3 + 0.1*RIGHT, color=yellow, buff=0)

        self.add(arrow1, arrow2, arrow3)

        self.play(
            system.animate.shift(0.75 * RIGHT * UNIT),
            arrow1.animate.put_start_and_end_on(point2, point2 + 0.75*RIGHT),
            arrow2.animate.put_start_and_end_on(point1, point1 + 0.75*RIGHT),
            arrow3.animate.put_start_and_end_on(point3, point3 + 0.75*RIGHT),
            x1_text.animate.shift(0.5*RIGHT),
            x2_text.animate.shift(0.5*RIGHT),
            x3_text.animate.shift(0.5*RIGHT),
        )
        
        # replace x's with 1
        text1 = MathTex(r"1", font_size=60, color=yellow)
        text2 = MathTex(r"1", font_size=60, color=yellow)
        text3 = MathTex(r"1", font_size=60, color=yellow)

        self.play(ReplacementTransform(x1_text, text1.move_to(x1_text)), ReplacementTransform(x2_text, text2.move_to(x2_text)), ReplacementTransform(x3_text, text3.move_to(x3_text)))
        self.wait(2)

        # shift system back to starting position
        self.play(
            system.animate.shift(0.75 * LEFT * UNIT),
            arrow1.animate.put_start_and_end_on(point2, point2),
            arrow2.animate.put_start_and_end_on(point1, point1),
            arrow3.animate.put_start_and_end_on(point3, point3),
            text1.animate.shift(0.5*LEFT),
            text2.animate.shift(0.5*LEFT),
            text3.animate.shift(0.5*LEFT),
        )
        self.wait(1)

        # Move camera and reset scene
        center = Point([12, 0, 0])
        self.play(self.camera.frame.animate.move_to(center),duration=2)
        self.remove(system, arrow1, arrow2, arrow3, text1, text2, text3, dashed_1, dashed_2, dashed_3,x_eq1, matrix_a_2)
        self.camera.frame.move_to(Point([0, 0, 0]))
        self.wait(1)

        # Spans
        col_text = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            Col A = span \left( {{\begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}}}
            {{\begin{bmatrix}
             1 \\ -2 \\ 1 \end{bmatrix}}} \right)
             """, 
            font_size=60, color=dark_blue)
        col_text = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            Col A = span \left( """+ r"""{{\begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}}}"""+ r"""
            {{\begin{bmatrix}
             1 \\ -2 \\ 1 \end{bmatrix}}}""" +r""" \right)
             """, 
            font_size=60, color=dark_blue)
        variables = VGroup(MathTex(r"""\begin{bmatrix} -1 \\ 1 \\ 0 \end{bmatrix}"""), MathTex(r"""\begin{bmatrix} 1 \\ -2 \\ 1 \end{bmatrix}""")).arrange_submobjects().shift(UP)
        col_text2 = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            = span \left( \begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}
            \begin{bmatrix}
             0 \\ -1 \\ 1 \end{bmatrix} \right)
             """,
            font_size=60, color=dark_blue
        )

        col_text3 = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            = span \left( \begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}
            \begin{bmatrix}
             -1 \\ 0 \\ 1 \end{bmatrix} \right)
             """,
            font_size=60, color=dark_blue
        )

        # Matrices
        a_matrix = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            A = \begin{bmatrix}
             -1 & 1 \\ 1 & -1 \end{bmatrix} \sim
            \begin{bmatrix}
             -1 & 1 \\ 0 & 0 \end{bmatrix}
             """,
            font_size=40, color=dark_blue
        )

        # A to col A
        col_calc = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            A = {{\begin{bmatrix}
            -1 & 1 & 0\\
            1 & -2 & 1\\
            0 & 1 & -1
            \end{bmatrix}}}
            \sim 
            {{\begin{bmatrix}
            -1 & 1 & 0\\
            0 & -1 & 1\\
            0 & 0 & 0 
            \end{bmatrix}}}}""",
            font_size=40, color=dark_blue)


        # span A
        col_textA = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.5}
            Col A = span \left( \begin{bmatrix}
             -1 \\ 1 \end{bmatrix}
            \right)
             """, 
            font_size=40, color=dark_blue)


        # Create Mass spring system (3 masses, 2 springs)
        # Masses
        left_square = Square(color=red, side_length=2*UNIT).shift(LEFT * UNIT * 5 + 1 * UNIT * DOWN)
        center_square = Square(color=red, side_length=4*UNIT).shift(1 * UNIT * DOWN)
        right_square = Square(color=red, side_length=2*UNIT).shift(RIGHT * UNIT * 5 + 1 * UNIT * DOWN)

        # Springs
        spring_left = SVGMobject("../assets/Spring.svg", stroke_color=dark_blue, stroke_width=3).scale_to_fit_height(2*UNIT).rotate(PI/2)
        spring_right = spring_left.copy()

        spring_left.shift(3 * LEFT * UNIT)
        spring_right.shift(3 * RIGHT * UNIT)

        spring_color = blue
        # Add springs
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

        system = Group(spring_left, spring_right, left_square, right_square, center_square)

        # Create Mass spring system (2 masses, 1 spring)
        left_square2 = Square(color=red, side_length=2*UNIT).shift(LEFT * UNIT * 2 + 1 * UNIT * DOWN)
        right_square2 = Square(color=red, side_length=2*UNIT).shift(RIGHT * UNIT * 2 + 1 * UNIT * DOWN)

        # Springs
        spring_center = spring_left.copy()

        spring_color = blue
        # Add springs
        def get_spring3():
            start = left_square2.get_right()
            end = right_square2.get_left()

            def spring_func(t):
                interp = start + t * (end - start)
                offset = np.array([0, 0.2 * np.sin(30 * t), 0])
                return interp + offset

            return ParametricFunction(spring_func, t_range=[0, 1], color=spring_color)


        spring_center = always_redraw(get_spring3)

        system2 = Group(spring_center, left_square2, right_square2)
        system2.shift(6.5*DOWN+3*RIGHT)

        m1_text = MathTex("m", font_size=60, color = red).move_to(left_square2.get_center())
        m2_text = MathTex("m", font_size=60, color = red).move_to(right_square2.get_center())

        k_text = MathTex("k", font_size=60, color=blue).move_to(spring_center.get_top() + [0, 0.5, 0])



        # DEBUG
        # indices = index_labels(col_calc[0])
        # self.add(col_calc, indices)
        self.play(Write(col_calc))
        # self.wait(1)
        # self.play(LaggedStart(col_calc[0][30:32].animate.set_color(red), col_calc[0][35:37].animate.set_color(blue), lag_ratio=1))
        # self.play(LaggedStart(
        #     AnimationGroup(col_calc[0][7:9].animate.set_color(red),col_calc[0][11].animate.set_color(red),col_calc[0][15].animate.set_color(red)), 
        #     AnimationGroup(col_calc[0][9].animate.set_color(blue),col_calc[0][12:14].animate.set_color(blue),col_calc[0][16].animate.set_color(blue)), lag_ratio=1))
        
        # self.wait(1)
        col_text[0][:].set_color(dark_blue)
        col_text.shift(20 * RIGHT * UNIT)
        # self.play(FadeOut(col_calc[0][24:]))
        # col_text[0][19:23].set_color(red)
        # col_text[0][33:37].set_color(blue)
        self.wait(1)
        # self.play(ReplacementTransform(col_calc[0][:2],col_text[0][:5]), FadeTransform(col_calc[0][2:24],col_text[0][5:]))
        self.play(col_calc.animate.shift(20*LEFT*UNIT),col_text.animate.shift(20 * LEFT * UNIT))

        # DEBUG
        # indices = index_labels(col_text[0])
        # self.add(col_text, indices)

        self.wait(1)
        # self.play(col_text[0][:].animate.set_color(dark_blue))


        self.play(col_text.animate.scale(0.70))
        self.play(col_text.animate.shift(2.3 * UP))

        col_text2.set_opacity(0)
        col_text2.scale(0.70)
        col_text2.move_to(col_text.get_center())
        self.add(col_text2) 

        combined = VGroup(col_text.copy(), col_text2.copy()).arrange(RIGHT, buff=0.1)
        combined.shift(-combined.get_center())
        combined.shift(2.3*UP)

        system_col = Group(left_square, center_square, right_square, spring_left, spring_right)

        system_col.shift(20* RIGHT * UNIT)
        self.add(system_col)
        com = Dot(system_col.get_center(), radius=0.08, color=dark_blue)
        self.add(com)
        system_col = Group(system_col, com)
        self.play(system_col.animate.shift(20*LEFT*UNIT))
        self.wait(1)



        self.play(
            col_text.animate.move_to(combined[0].get_center()),
            col_text2.animate.set_opacity(1).move_to(combined[1].get_center())
        )

        # DEBUG
        #indices = index_labels(col_text2[0])
        #self.add(indices)


        self.wait(1)
        self.play(col_text2[0][15:18].animate.set_color(yellow), col_text2[0][30:33].animate.set_color(yellow))

        point1 = left_square.get_left()
        point2 = center_square.get_bottom()
        point3 = right_square.get_right()

        left_arrow_1 = Arrow(start=point1, end=point1 + 1 * LEFT, color=yellow, buff=0)
        left_arrow_2 = Arrow(start=point2+0.5*DOWN + 0.1*LEFT, end=point2+0.5*DOWN + 1.1 * LEFT, color=yellow, buff=0)
        right_arrow_1 = Arrow(start=point3, end=point3 + 1 * RIGHT, color=yellow, buff=0)
        right_arrow_2 = Arrow(start=point2+0.5*DOWN + 0.1*RIGHT, end=point2+0.5*DOWN + 1.1 * RIGHT, color=yellow, buff=0)

        
        def out_and_back(t):
            return 2 * t if t <= 0.5 else 2 * (1 - t)

        start_pos = center_square.get_center()
        def update_center(mob):
            alpha = tracker.get_value()
            if alpha <= 0.25:
                progress = alpha / 0.25
                offset = -0.25 * progress
            elif alpha <= 0.75:
                progress = (alpha - 0.25) / 0.5
                offset = -0.25 + 0.5 * progress
            else:
                progress = (alpha - 0.75) / 0.25
                offset = 0.25 - 0.25 * progress
            
            mob.move_to(start_pos + offset * RIGHT)

        tracker = ValueTracker(0)
        center_square.add_updater(update_center)

        self.play(
            AnimationGroup(left_square.animate.shift(0.5 * LEFT),
            right_square.animate.shift(0.5 * RIGHT),
            rate_func=out_and_back,
            lag_ratio=0),
            tracker.animate.set_value(1),

            run_time=2
        )
        center_square.remove_updater(update_center)
        right_square.shift(0.5 * LEFT)
        left_square.shift(0.5 * RIGHT)


        self.play(GrowArrow(left_arrow_1), GrowArrow(right_arrow_1),GrowArrow(left_arrow_2),GrowArrow(right_arrow_2),duration=3)

        self.wait(2)

        self.play(
            left_arrow_1.animate.scale(0.01).set_opacity(0).set_stroke(width=0).set_fill(opacity=0),
            left_arrow_2.animate.scale(0.01).set_opacity(0).set_stroke(width=0).set_fill(opacity=0),
            right_arrow_1.animate.scale(0.01).set_opacity(0).set_stroke(width=0).set_fill(opacity=0),
            right_arrow_2.animate.scale(0.01).set_opacity(0).set_stroke(width=0).set_fill(opacity=0),
            run_time=1
        )
        self.wait(1)

        col_text3.move_to(combined[1].get_center()).scale(0.70)

        self.play(ReplacementTransform(col_text2, col_text3))

        self.play(col_text3[0][15:18].animate.set_color(yellow), col_text3[0][29:31].animate.set_color(yellow),col_text3[0][32].animate.set_color(yellow))

        left_arrow_3 = Arrow(start=point1, end=point1 +  LEFT, color=yellow, buff=0)
        left_arrow_4 = Arrow(start=point1 + 1.1*LEFT, end=point1 + 2.1 * LEFT, color=yellow, buff=0)
        right_arrow_3 = Arrow(start=point3, end=point3 +  RIGHT, color=yellow, buff=0)
        right_arrow_4 = Arrow(start=point2+0.5*DOWN, end=point2+0.5*DOWN + 1 * RIGHT, color=yellow, buff=0)

        self.play(AnimationGroup(left_square.animate.shift(1 * UNIT * LEFT),right_square.animate.shift(0.5 * UNIT * RIGHT), center_square.animate.shift(0.5 * UNIT * RIGHT), run_time=0.7),)
        self.play(AnimationGroup(left_square.animate.shift(1 * UNIT * RIGHT), right_square.animate.shift(0.5 * UNIT * LEFT), center_square.animate.shift(0.5 * UNIT * LEFT), run_time=0.7),)
        self.play(GrowArrow(left_arrow_3), GrowArrow(left_arrow_4), GrowArrow(right_arrow_3), GrowArrow(right_arrow_4),duration=3)
        self.wait(1)
        
        # Move camera down
        center = Point([0, -7.5, 0])
        self.play(self.camera.frame.animate.move_to(center),duration=2)
        self.wait()


        
        self.play(
            LaggedStart(
                FadeIn(left_square2),
                FadeIn(right_square2),
                lag_ratio=0.3
            )
        )

        self.play(Write(spring_center))
        
        self.play(Write(m1_text), Write(m2_text))
        self.play(Write(k_text))

        a_matrix.move_to(system2.get_left() + 4*LEFT + 1.25*UP)
        self.play(Write(a_matrix))
        self.wait(1)

        col_textA.next_to(a_matrix, DOWN, aligned_edge=LEFT, buff=1.2)
        self.play(Write(col_textA))

        # DEBUG
        # indices = index_labels(col_textA[0])
        # indices.move_to(col_textA.get_center())
        # self.add(indices)
        # self.wait(2)

        self.play(col_textA[0][13:16].animate.set_color(yellow))

        point4 = left_square2.get_bottom() + 1*UNIT*LEFT
        point5 = right_square2.get_bottom() + 1*UNIT*RIGHT

        self.play(
            left_square2.animate.shift(0.5 * UNIT * LEFT),
            m1_text.animate.shift(0.5 * UNIT * LEFT),
            right_square2.animate.shift(0.5 * UNIT * RIGHT),
            m2_text.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.7
        )
        self.play(
            left_square2.animate.shift(0.5 * UNIT * RIGHT),
            m1_text.animate.shift(0.5 * UNIT * RIGHT),
            right_square2.animate.shift(0.5 * UNIT * LEFT),
            m2_text.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.7
        )
        self.wait(1)

        left_arrow_6 = Arrow(start=point4+0.5*DOWN + 2 * RIGHT, end=point4+0.5*DOWN, color=yellow, buff=0)
        right_arrow_6 = Arrow(start=point5+0.5*DOWN + 2 * LEFT, end=point5+0.5*DOWN, color=yellow, buff=0)

        self.play(GrowArrow(left_arrow_6), GrowArrow(right_arrow_6),duration=3)
        self.wait(1)
