from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")  # ManimColor('#FF5132')
        yellow = ManimColor("#cc9316")  # ManimColor('#FFCC12')
        blue = ManimColor("#0076C2")  # ManimColor('#46A6FF')
        green = ManimColor("#009B77")

        grid = NumberPlane(
            background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15,
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        self.play(Write(grid))
        self.wait(1)

        ##########################################################################
        ##############################3 Mass System###############################
        ##########################################################################

        # Create Mass spring system (3 masses, 2 springs)
        # Masses
        left_square = Square(color=red, side_length=2 * UNIT).shift(LEFT * UNIT * 5)
        center_square = Square(color=red, side_length=4 * UNIT)
        right_square = Square(color=red, side_length=2 * UNIT).shift(RIGHT * UNIT * 5)

        # Springs
        spring_left = (
            SVGMobject("../assets/Spring.svg", stroke_color=dark_blue, stroke_width=3)
            .scale_to_fit_height(2 * UNIT)
            .rotate(PI / 2)
        )
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

        system = Group(
            spring_left, spring_right, left_square, right_square, center_square
        )
        system.scale(0.9)

        # mass labels
        m1_text = MathTex("m_1", font_size=60, color=red).move_to(
            Point([-3.75, 1.5, 0])
        )
        m2_text = MathTex("m_2", font_size=60, color=red).move_to(Point([0, 1.5, 0]))
        m3_text = MathTex("m_3", font_size=60, color=red).move_to(Point([3.75, 1.5, 0]))

        # spring labels
        k2_text = MathTex("k_2", font_size=60, color=blue).move_to(
            Point([2.25, 2.45, 0])
        )
        k1_text = MathTex("k_1", font_size=60, color=blue).move_to(
            Point([-2.25, 2.45, 0])
        )

        # nul A
        matrix_a_2 = MathTex(
            r"""{\renewcommand{\arraystretch}{1.45}
            \text{Computing } \operatorname{Nul} A:  \left[\begin{array}{ccc|c}
            -1 & 1 & 0 & 0\\
            1 & -2 & 1 & 0\\
            0 & 1 & -1 & 0
            \end{array}\right]}
            \sim 
            {\renewcommand{\arraystretch}{1.45}
            \left[\begin{array}{ccc|c}
            -1 & 1 & 0 & 0\\
            0 & -1 & 1 & 0\\
            0 & 0 & 0 & 0
            \end{array}\right]}""",
            color=dark_blue,
            font_size=40,
        )

        x_eq1 = MathTex(
            r"""{\renewcommand{\arraystretch}{1.15}
           \begin{cases}
            x_1 = x_2 \\
            x_2 = x_3 \\
            x_3 = x_3 \\
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
            font_size=50,
        )

        x_eq2 = MathTex(
            r"""{\renewcommand{\arraystretch}{1.15}
           \textbf{x} = x_3 \begin{bmatrix}
            1\\
            1\\
            1
            \end{bmatrix} """,
            color=dark_blue,
            font_size=50,
        )

        # add masses and springs
        self.play(
            LaggedStart(
                Write(left_square),
                Write(center_square),
                Write(right_square),
                lag_ratio=0.3,
            )
        )
        self.play(Write(spring_left), Write(spring_right))
        self.wait(1)
        self.play(system.animate.shift(2.5 * UP * UNIT))

        # add nul A
        self.play(Write(matrix_a_2.shift(2.05 * DOWN), run_time=3))
        self.wait(1)

        # shift nul A and add x equations
        self.add(x_eq1.shift(20 * RIGHT * UNIT + 2.05 * DOWN))
        self.play(
            matrix_a_2.animate.shift(20 * LEFT * UNIT),
            x_eq1.animate.shift(20 * LEFT * UNIT),
        )
        self.wait(1)
        self.play(x_eq1[0][37:40].animate.set_color(yellow))
        self.wait(1)

        # DEBUG
        # indices = index_labels(x_eq1[0])
        # self.add(indices)

        # create x labels and dashed lines
        x1_text = MathTex("x_1", font_size=60, color=yellow).move_to(
            left_square.get_center() + [0, -2.95 * UNIT, 0]
        )
        x2_text = MathTex("x_2", font_size=60, color=yellow).move_to(
            center_square.get_center() + [0, -2.95 * UNIT, 0]
        )
        x3_text = MathTex("x_3", font_size=60, color=yellow).move_to(
            right_square.get_center() + [0, -2.95 * UNIT, 0]
        )

        self.wait(1)

        # add arrows and move system
        point1 = center_square.get_center() + 2.5 * DOWN * UNIT
        point2 = left_square.get_center() + 2.5 * DOWN * UNIT
        point3 = right_square.get_center() + 2.5 * DOWN * UNIT

        arrow1 = Line(start=point2, end=point2 + 0.9 * RIGHT, color=yellow, buff=0)
        arrow1.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        arrow2 = Line(start=point1, end=point1 + 0.9 * RIGHT, color=yellow, buff=0)
        arrow2.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        arrow3 = Line(start=point3, end=point3 + 0.9 * RIGHT, color=yellow, buff=0)
        arrow3.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        self.add(arrow1, arrow2, arrow3)

        self.play(
            system.animate.shift(0.9 * RIGHT * UNIT),
            GrowFromPoint(arrow1, point2),
            GrowFromPoint(arrow2, point1),
            GrowFromPoint(arrow3, point3),
        )

        self.wait(2)

        self.play(
            system.animate.shift(0.9 * LEFT * UNIT),
            arrow1.animate.put_start_and_end_on(point2, point2),
            arrow2.animate.put_start_and_end_on(point1, point1),
            arrow3.animate.put_start_and_end_on(point3, point3),
            run_time=2,
        )
        self.wait(1)

        self.play(
            FadeOut(x_eq1),
            FadeOut(system)
        )
        self.wait(2)

        # Spans
        col_text = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
            \operatorname{Col} A = \operatorname{span} \left( {{\begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}}},
            {{\begin{bmatrix}
             1 \\ -2 \\ 1 \end{bmatrix}}} \right)
             """,
            font_size=40,
            color=dark_blue,
        )
        col_text = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
             \operatorname{Col} A = \operatorname{span} \left( """
            + r"""{{\begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}}}"""
            + r""",
            {{\begin{bmatrix}
             1 \\ -2 \\ 1 \end{bmatrix}}}"""
            + r""" \right)
             """,
            font_size=40,
            color=dark_blue,
        )
        variables = (
            VGroup(
                MathTex(r"""\begin{bmatrix} -1 \\ 1 \\ 0 \end{bmatrix}"""),
                MathTex(r"""\begin{bmatrix} 1 \\ -2 \\ 1 \end{bmatrix}"""),
            )
            .arrange_submobjects()
            .shift(UP)
        )
        col_text2 = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
            = \operatorname{span} \left( \begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}
            \begin{bmatrix}
             0 \\ -1 \\ 1 \end{bmatrix} \right)
             """,
            font_size=40,
            color=dark_blue,
        )

        col_text3 = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
            = \operatorname{span} \left( \begin{bmatrix}
             -1 \\ 1 \\ 0 \end{bmatrix}
            \begin{bmatrix}
             -1 \\ 0 \\ 1 \end{bmatrix} \right)
             """,
            font_size=40,
            color=dark_blue,
        )

        # Matrices
        a_matrix = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
            A = \begin{bmatrix}
             -1 & 1 \\ 1 & -1 \end{bmatrix} \sim
            \begin{bmatrix}
             -1 & 1 \\ 0 & 0 \end{bmatrix}
             """,
            font_size=50,
            color=dark_blue,
        )

        # A to col A
        col_calc = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
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
            font_size=40,
            color=dark_blue,
        )

        # span A
        col_textA = MathTex(
            r"""
            {\renewcommand{\arraystretch}{1.45}
            \operatorname{Col} A = \operatorname{span} \left( \begin{bmatrix}
             -1 \\ 1 \end{bmatrix}
            \right)
             """,
            font_size=50,
            color=dark_blue,
        )

        # DEBUG
        # indices = index_labels(col_calc[0])
        # self.add(col_calc, indices)

        self.play(Write(col_calc))

        self.wait(1)

        # self.play(FadeOut(col_calc))

        col_text[0][:].set_color(dark_blue)
        col_text.shift(20 * RIGHT * UNIT)

        self.play(
            col_calc.animate.shift(20 * LEFT * UNIT),
            col_text.animate.shift(20 * LEFT * UNIT),
        )

        # # DEBUG
        # # indices = index_labels(col_text[0])
        # # self.add(col_text, indices)

        self.wait(2)

        self.play(FadeOut(col_text), FadeOut(col_calc))


        com = Dot(system.get_center(), radius=0.08, color=dark_blue)
       

        ##########################################################################
        ##############################2 Mass System###############################
        ##########################################################################

        # Create Mass spring system (2 masses, 1 spring)
        left_square2 = Square(color=red, side_length=4 * 0.9 * UNIT).shift(
            LEFT * UNIT * 3
        )
        right_square2 = Square(color=red, side_length=4 * 0.9 * UNIT).shift(
            RIGHT * UNIT * 3
        )

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

        m1_text = MathTex("m", font_size=60, color=red).move_to(
            left_square2.get_center()
        )
        m2_text = MathTex("m", font_size=60, color=red).move_to(
            right_square2.get_center()
        )

        k_text = MathTex("k", font_size=60, color=blue).move_to(
            spring_center.get_top() + [0, 0.5, 0]
        )

        system2 = Group(
            spring_center, left_square2, right_square2, m1_text, m2_text, k_text
        )

        self.play(
            LaggedStart(FadeIn(left_square2), FadeIn(right_square2), lag_ratio=0.3)
        )

        self.play(Write(spring_center))

        self.play(Write(m1_text), Write(m2_text))
        self.play(Write(k_text))

        self.wait(1)

        self.play(system2.animate.shift(2.5 * UP * UNIT))

        # a_matrix.move_to(system2.get_bottom() +  2.5*DOWN)
        self.play(Write(a_matrix.shift(2.05 * DOWN)))
        self.wait(1)

        self.add(col_textA.shift(20 * RIGHT * UNIT + 2.05 * DOWN))
        self.play(
            a_matrix.animate.shift(20 * LEFT * UNIT),
            col_textA.animate.shift(20 * LEFT * UNIT),
        )
        self.wait(1)

        # DEBUG
        # indices = index_labels(col_textA[0])
        # indices.move_to(col_textA.get_center())
        # self.add(indices)
        # self.wait(2)

        self.play(col_textA[0][13:15].animate.set_color(yellow),col_textA[0][15:16].animate.set_color(green))

        point4 = left_square2.get_bottom() + 1.8 * UNIT * LEFT
        point5 = right_square2.get_bottom() + 1.8 * UNIT * RIGHT

        left_arrow_6 = Line(
            start=point4 + 0.5 * DOWN + 2.5 * RIGHT * UNIT,
            end=point4 + 0.5 * DOWN + 0.5 * LEFT * UNIT,
            color=yellow,
            buff=0,
        )
        left_arrow_6.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        right_arrow_6 = Line(
            start=point5 + 0.5 * DOWN + 2.5 * LEFT * UNIT,
            end=point5 + 0.5 * DOWN + 0.5 * RIGHT * UNIT,
            color=green,
            buff=0,
        )
        right_arrow_6.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        self.play(
            left_square2.animate.shift(1 * UNIT * LEFT),
            m1_text.animate.shift(1 * UNIT * LEFT),
            right_square2.animate.shift(1 * UNIT * RIGHT),
            m2_text.animate.shift(1 * UNIT * RIGHT),
            GrowFromPoint(left_arrow_6, point4 + 0.5 * DOWN + 2.5 * RIGHT * UNIT),
            GrowFromPoint(right_arrow_6, point5 + 0.5 * DOWN + 2.5 * LEFT * UNIT),
            run_time=1,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * RIGHT),
            m1_text.animate.shift(0.7 * UNIT * RIGHT),
            right_square2.animate.shift(0.7 * UNIT * LEFT),
            m2_text.animate.shift(0.7 * UNIT * LEFT),
            run_time=0.5,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * LEFT),
            m1_text.animate.shift(0.7 * UNIT * LEFT),
            right_square2.animate.shift(0.7 * UNIT * RIGHT),
            m2_text.animate.shift(0.7 * UNIT * RIGHT),
            run_time=0.3,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * RIGHT),
            m1_text.animate.shift(0.7 * UNIT * RIGHT),
            right_square2.animate.shift(0.7 * UNIT * LEFT),
            m2_text.animate.shift(0.7 * UNIT * LEFT),
            run_time=0.2,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * LEFT),
            m1_text.animate.shift(0.7 * UNIT * LEFT),
            right_square2.animate.shift(0.7 * UNIT * RIGHT),
            m2_text.animate.shift(0.7 * UNIT * RIGHT),
            run_time=0.2,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * RIGHT),
            m1_text.animate.shift(0.7 * UNIT * RIGHT),
            right_square2.animate.shift(0.7 * UNIT * LEFT),
            m2_text.animate.shift(0.7 * UNIT * LEFT),
            run_time=0.2,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * LEFT),
            m1_text.animate.shift(0.7 * UNIT * LEFT),
            right_square2.animate.shift(0.7 * UNIT * RIGHT),
            m2_text.animate.shift(0.7 * UNIT * RIGHT),
            run_time=0.2,
        )
        self.play(
            left_square2.animate.shift(0.7 * UNIT * RIGHT),
            m1_text.animate.shift(0.7 * UNIT * RIGHT),
            right_square2.animate.shift(0.7 * UNIT * LEFT),
            m2_text.animate.shift(0.7 * UNIT * LEFT),
            run_time=0.3,
        )

        self.play(
            left_square2.animate.shift(0.7 * UNIT * LEFT),
            m1_text.animate.shift(0.7 * UNIT * LEFT),
            right_square2.animate.shift(0.7 * UNIT * RIGHT),
            m2_text.animate.shift(0.7 * UNIT * RIGHT),
            run_time=0.5,
        )

        self.play(
            left_square2.animate.shift(1 * UNIT * RIGHT),
            m1_text.animate.shift(1 * UNIT * RIGHT),
            right_square2.animate.shift(1 * UNIT * LEFT),
            m2_text.animate.shift(1 * UNIT * LEFT),
            right_arrow_6.animate.put_start_and_end_on(point5 + 0.5 * DOWN + 2.5 * LEFT * UNIT,point5 + 0.5 * DOWN + 2.5 * LEFT * UNIT),
            left_arrow_6.animate.put_start_and_end_on(point4 + 0.5 * DOWN + 2.5 * RIGHT * UNIT,point4 + 0.5 * DOWN + 2.5 * RIGHT * UNIT),
            run_time=1,
        )
        self.wait(2)

        self.play(
            FadeOut(
                left_square2,
                right_square2,
                m1_text,
                m2_text,
                left_arrow_6,
                right_arrow_6,
                spring_center,
                k_text,
                col_textA,
            )
        )

        ##########################################################################
        ##############################3 Mass System###############################
        ##########################################################################
        point1 = center_square.get_center() + 2.5 * DOWN * UNIT
        point2 = left_square.get_center() + 2.5 * DOWN * UNIT
        point3 = right_square.get_center() + 2.5 * DOWN * UNIT

        # DEBUG
        # indices = index_labels(col_text[0])
        # indices.move_to(col_text.get_center())
        # self.add(indices)

        col_text.move_to(col_textA[0].get_center())
        self.play(FadeIn(system), FadeIn(com), FadeIn(col_text))

        left_arrow_3 = Line(start=point1, end=point1 + LEFT, color=green, buff=0)
        left_arrow_3.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        left_arrow_4 = Line(
            start=point1 + 1.1 * LEFT, end=point1 + 2.1 * LEFT, color=green, buff=0
        )
        left_arrow_4.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        right_arrow_3 = Line(start=point3, end=point3 + RIGHT, color=yellow, buff=0)
        right_arrow_3.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        right_arrow_4 = Line(start=point2, end=point2 + 1 * RIGHT, color=yellow, buff=0)
        right_arrow_4.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        self.play(
            col_text[0][34].animate.set_color(yellow),
        )


        

        self.play(
            GrowFromPoint(right_arrow_4, point2),
            left_square.animate.shift(0.5 * UNIT * RIGHT),
        )

        self.play(
            left_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.5
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.3
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.2
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.2
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.2
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.2
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.3
        )
        self.play(
            left_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.5
        )

        self.play(                
            left_square.animate.shift(0.5 * UNIT * LEFT),
            right_arrow_4.animate.put_start_and_end_on(point2, point2),
        )

        self.play(LaggedStart(
            col_text[0][34].animate.set_color(dark_blue),
            col_text[0][35:37].animate.set_color(green),lag_ratio=0.3)
        )

        self.play(
            center_square.animate.shift(1 * UNIT * LEFT),
            GrowFromPoint(left_arrow_3, point1),
            GrowFromPoint(left_arrow_4, point1 + 1.1 * LEFT),
        )

        self.play(
            center_square.animate.shift(0.5*UNIT * RIGHT),
            run_time=0.5
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * LEFT),
            run_time=0.3
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * RIGHT),
            run_time=0.2
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * LEFT),
            run_time=0.2
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * RIGHT),
            run_time=0.2
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * LEFT),
            run_time=0.2
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * RIGHT),
            run_time=0.3
        )
        self.play(
            center_square.animate.shift(0.5*UNIT * LEFT),
            run_time=0.5
        )

        self.play(
            left_arrow_3.animate.put_start_and_end_on(point1, point1),
            left_arrow_4.animate.put_start_and_end_on(point1 + 1.1 * LEFT, point1 + 1.1 * LEFT),
            center_square.animate.shift(1 * UNIT * RIGHT),
        )


        self.play(LaggedStart(
            col_text[0][35:37].animate.set_color(dark_blue),
            col_text[0][37].animate.set_color(yellow),lag_ratio=0.3)
        )

        self.play(
            right_square.animate.shift(0.5 * UNIT * RIGHT),
            GrowFromPoint(right_arrow_3, point3),
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.5,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.3,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.2,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.2,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.2,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.2,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * LEFT),
            run_time=0.3,
        )
        self.play(
            right_square.animate.shift(0.5 * UNIT * RIGHT),
            run_time=0.5,
        )


        self.play(
            right_arrow_3.animate.put_start_and_end_on(point3, point3),
            right_square.animate.shift(0.5 * UNIT * LEFT),
        )

