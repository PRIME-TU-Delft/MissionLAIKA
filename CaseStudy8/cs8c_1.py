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


        ##########################################################################
        ##############################3 Mass System###############################
        ##########################################################################


        # Create Mass spring system (3 masses, 2 springs)
        #Masses
        left_square = Square(color=red, side_length=2*UNIT).shift(LEFT * UNIT * 5)
        center_square = Square(color=red, side_length=4*UNIT)
        right_square = Square(color=red, side_length=2*UNIT).shift(RIGHT * UNIT * 5)

        #Springs
        spring_left = SVGMobject("../assets/Spring.svg", stroke_color=dark_blue, stroke_width=3).scale_to_fit_height(2*UNIT).rotate(PI/2)
        spring_right = spring_left.copy()

        spring_left.shift(3 * LEFT * UNIT)
        spring_right.shift(3 * RIGHT * UNIT)

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

        # mass labels
        m1_text = MathTex("m_1", font_size=60, color = red).move_to(Point([-3.75, 0, 0]))
        m2_text = MathTex("m_2", font_size=60, color = red).move_to(Point([0, 0, 0]))
        m3_text = MathTex("m_3", font_size=60, color = red).move_to(Point([3.75, 0, 0]))


        # spring labels
        k2_text = MathTex("k", font_size=60, color=blue).move_to(Point([2.25, 0.95, 0]))
        k1_text = MathTex("k", font_size=60, color=blue).move_to(Point([-2.25, 0.95, 0]))

        # m1 = m2
        m1m2 = MathTex("m_1 = m_3",font_size=60, color=dark_blue).move_to(Point([0,2.4,0]))
        m1m2[0][:2].set_color(red)
        m1m2[0][3:].set_color(red)

        plane_svg = SVGMobject("../assets/AirplaneFront.svg", stroke_color=dark_blue, stroke_width=4).scale_to_fit_height(4*UNIT)
        list = plane_svg.submobjects
        # labels = index_labels(plane_svg)
        # self.add(labels)

        self.play(Write(plane_svg))
        self.wait(2)
        self.remove(plane_svg)
        self.add(*list)  # add submobjects directly to the scene instead

        self.play(LaggedStart(
            ReplacementTransform(list[7], left_square),
            ReplacementTransform(VGroup(*list[:6]), center_square),
            ReplacementTransform(list[6], right_square),
            lag_ratio=0.3
        ))

        # self.play(LaggedStart(Write(left_square), Write(center_square),Write(right_square),lag_ratio=0.3))
        self.wait(1)

        self.play(Write(spring_left),Write(spring_right))
        self.wait(1)


        self.play(Write(m2_text))
        self.wait(1)
        self.play(Write(m1_text))
        self.wait(1)
        self.play(Write(m3_text))

        # self.play(LaggedStart(Write(m1_text), Write(m2_text),Write(m3_text),lag_ratio=0.3))
        self.wait(1)

        self.play(Write(m1m2))
        self.wait(1)
        self.play(m1m2.animate.scale(1.2), duration=3)
        self.wait(1)

        self.play(m1m2.animate.scale(1/1.2), duration=3)
        self.wait(1)
    
        self.play(Unwrite(m1m2))
        self.wait(1)

        self.play(Write(k1_text), Write(k2_text))
        self.wait(1)



        self.wait(2)
        
        self.play(FadeOut(system),FadeOut(m1_text),FadeOut(m2_text),FadeOut(m3_text),FadeOut(k1_text),FadeOut(k2_text),FadeOut(m1m2))

        self.wait(1)

        ###################################################################
        #############################Equations#############################
        ###################################################################

        # eq7 = MathTex(
        #     r"\begin{cases}"
        #     r"m_1x_1'' = k(x_2-x_1)\\"
        #     r"m_2x_2'' = - k(x_2-x_1) +k(x_3-x_2) \\"
        #     r"m_3x_3''=-k(x_3-x_2)"
        #     r"\end{cases}", font_size=65, color = dark_blue
        # )

        # eq7[0][5:7].set_color(red)
        # eq7[0][20:22].set_color(red)
        # eq7[0][45:47].set_color(red)

        # eq7[0][7].set_color(yellow)
        # eq7[0][10].set_color(yellow)
        # eq7[0][22].set_color(yellow)
        # eq7[0][25].set_color(yellow)
        # eq7[0][47].set_color(yellow)
        # eq7[0][50].set_color(yellow)
        # eq7[0][14:16].set_color(yellow)
        # eq7[0][17:19].set_color(yellow)
        # eq7[0][30:32].set_color(yellow)
        # eq7[0][33:35].set_color(yellow)
        # eq7[0][39:41].set_color(yellow)

        # eq7[0][42:44].set_color(yellow)
        # eq7[0][55:57].set_color(yellow)
        # eq7[0][58:60].set_color(yellow)

        # eq7[0][12].set_color(blue)
        # eq7[0][28].set_color(blue)
        # eq7[0][37].set_color(blue)
        # eq7[0][53].set_color(blue)

        eq7 = MathTex(
            r"\begin{aligned}"
            r"m_1x_1'' &= k(x_2-x_1)\\[0pt]"
            r"m_2x_2'' &= - k(x_2-x_1) +k(x_3-x_2) = kx_1 - 2kx_2 +kx_3 \\[0pt]"
            r"m_3x_3''&=-k(x_3-x_2) \end{aligned}", font_size=50, color = dark_blue
        ).shift(UP * 0.27 * UNIT)

        
        # # DEBUG
        # indices = index_labels(eq7[0])
        # indices.move_to(eq7.get_center())
        # self.add(indices)
        # self.wait(2)


        eq7[0][:2].set_color(red)
        eq7[0][15:17].set_color(red)
        eq7[0][53:55].set_color(red)

        eq7[0][2].set_color(yellow)
        eq7[0][5].set_color(yellow)
        eq7[0][17].set_color(yellow)
        eq7[0][20].set_color(yellow)
        eq7[0][55].set_color(yellow)
        eq7[0][58].set_color(yellow)
        eq7[0][9:11].set_color(yellow)
        eq7[0][12:14].set_color(yellow)
        eq7[0][25:27].set_color(yellow)
        eq7[0][28:30].set_color(yellow)
        eq7[0][34:36].set_color(yellow)
        eq7[0][37:39].set_color(yellow)
        eq7[0][42:44].set_color(yellow)
        eq7[0][47:49].set_color(yellow)
        eq7[0][51:53].set_color(yellow)
        eq7[0][63:65].set_color(yellow)
        eq7[0][66:68].set_color(yellow)

        eq7[0][7].set_color(blue)
        eq7[0][23].set_color(blue)
        eq7[0][32].set_color(blue)
        eq7[0][41].set_color(blue)
        eq7[0][46].set_color(blue)
        eq7[0][50].set_color(blue)
        eq7[0][61].set_color(blue)

        self.play(Write(eq7))

        self.play(
            ApplyWave(eq7[0][    2], amplitude=0.05),
            ApplyWave(eq7[0][    5], amplitude=0.05),
            ApplyWave(eq7[0][   17], amplitude=0.05),
            ApplyWave(eq7[0][   20], amplitude=0.05),
            ApplyWave(eq7[0][   55], amplitude=0.05),
            ApplyWave(eq7[0][   58], amplitude=0.05),
            ApplyWave(eq7[0][ 9:11], amplitude=0.05),
            ApplyWave(eq7[0][12:14], amplitude=0.05),
            ApplyWave(eq7[0][25:27], amplitude=0.05),
            ApplyWave(eq7[0][28:30], amplitude=0.05),
            ApplyWave(eq7[0][34:36], amplitude=0.05),
            ApplyWave(eq7[0][37:39], amplitude=0.05),
            ApplyWave(eq7[0][42:44], amplitude=0.05),
            ApplyWave(eq7[0][47:49], amplitude=0.05),
            ApplyWave(eq7[0][51:53], amplitude=0.05),
            ApplyWave(eq7[0][63:65], amplitude=0.05),
            ApplyWave(eq7[0][66:68], amplitude=0.05),
            run_time=2
        )

        # self.play(
        #     eq7[0][    2].animate.shift(UP*0.1*UNIT),
        #     eq7[0][    5].animate.shift(UP*0.1*UNIT),
        #     eq7[0][   17].animate.shift(UP*0.1*UNIT),
        #     eq7[0][   20].animate.shift(UP*0.1*UNIT),
        #     eq7[0][   55].animate.shift(UP*0.1*UNIT),
        #     eq7[0][   58].animate.shift(UP*0.1*UNIT),
        #     eq7[0][ 9:11].animate.shift(UP*0.1*UNIT),
        #     eq7[0][12:14].animate.shift(UP*0.1*UNIT),
        #     eq7[0][25:27].animate.shift(UP*0.1*UNIT),
        #     eq7[0][28:30].animate.shift(UP*0.1*UNIT),
        #     eq7[0][34:36].animate.shift(UP*0.1*UNIT),
        #     eq7[0][37:39].animate.shift(UP*0.1*UNIT),
        #     eq7[0][42:44].animate.shift(UP*0.1*UNIT),
        #     eq7[0][47:49].animate.shift(UP*0.1*UNIT),
        #     eq7[0][51:53].animate.shift(UP*0.1*UNIT),
        #     eq7[0][63:65].animate.shift(UP*0.1*UNIT),
        #     eq7[0][66:68].animate.shift(UP*0.1*UNIT),
        #     run_time=0.5
        # )

        # self.play(
        #     eq7[0][2].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][5].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][17].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][20].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][55].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][58].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][9:11].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][12:14].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][25:27].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][28:30].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][34:36].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][37:39].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][42:44].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][47:49].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][51:53].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][63:65].animate.shift(DOWN*0.1*UNIT),
        #     eq7[0][66:68].animate.shift(DOWN*0.1*UNIT),
        #     run_time=0.5
        # )

        # self.play(eq7.animate.scale(1.2), duration=3)

        # self.play(eq7.animate.scale(1/1.2), duration=3)

        # DEBUG
        # indices = index_labels(eq7[0])
        # self.add(eq7, indices)

        self.wait(3)




