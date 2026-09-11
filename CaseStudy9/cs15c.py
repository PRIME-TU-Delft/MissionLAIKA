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
        self.add(system)

        self.play(system.animate.shift(20 * LEFT * UNIT))
        self.wait(1)
        #horizontal movement
        self.play(left_square.animate.shift(1 * UNIT * RIGHT), right_square.animate.shift(2 * UNIT * RIGHT), run_time=0.5)
        self.play(left_square.animate.shift(3 * UNIT * LEFT), right_square.animate.shift(3 * UNIT * LEFT), run_time=0.5)
        self.play(left_square.animate.shift(2 * UNIT * RIGHT), right_square.animate.shift(1 * UNIT * RIGHT), run_time=0.5)

        a=11
        b=21

        eq0 = MathTex(
            r"\begin{cases}"
            r"m_1 x_1'' = k(x_2-x_1) \\"
            r"m_2 x_2'' = -k(x_2-x_1) + k(x_3-x_2) \\"
            r"m_3 x_3'' = -k(x_3-x_2) \\"
            r"\end{cases}", color=dark_blue
        )[0]
        eq0.shift(20 * RIGHT * UNIT)
        eq0[5 + 3 + 4].set_color(blue)
        eq0[5 + 5 + 4:5 + 7 + 4].set_color(yellow)
        eq0[5 + 8 + 4:5 + 10 + 4].set_color(yellow)
        eq0[5 + a + 4 + 8].set_color(blue)
        eq0[5 + a + 6 + 8:5 + a + 8 + 8].set_color(yellow)
        eq0[5 + a + 9 + 8:5 + a + 11 + 8].set_color(yellow)
        eq0[5 + a + 13 + 8].set_color(blue)
        eq0[5 + a + 15 + 8:5 + a + 17 + 8].set_color(yellow)
        eq0[5 + a + 18 + 8:5 + a + 20 + 8].set_color(yellow)
        eq0[5 + a + b + 4 + 12].set_color(blue)
        eq0[5 + a + b + 6 + 12:5 + a + b + 8 + 12].set_color(yellow)
        eq0[5 + a + b + 9 + 12:5 + a + b + 11 + 12].set_color(yellow)
        eq0[5:7].set_color(red)
        eq0[5 + a + 4:5 + a + 4 + 2].set_color(red)
        eq0[5 + a + 4 + b + 4:5 + a + 4 + b + 4 + 2].set_color(red)
        eq0[5 + 2].set_color(yellow)
        eq0[5 + a + 4 + 2].set_color(yellow)
        eq0[5 + a + 4 + b + 4 + 2].set_color(yellow)
        eq0[5 + 2 + 3].set_color(yellow)
        eq0[5 + a + 4 + 2 + 3].set_color(yellow)
        eq0[5 + a + 4 + b + 4 + 2 + 3].set_color(yellow)

        self.play(system.animate.shift(20 * LEFT * UNIT), eq0.animate.shift(20 * LEFT * UNIT))
        self.remove(system)
        self.play(eq0.animate.scale(1.2))
        self.play(eq0.animate.scale(5.0/6))
        self.wait(1)
        self.play(eq0.animate.shift(20 * LEFT * UNIT))
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
        eq1.shift(20 * RIGHT * UNIT + eq1[0].get_bottom()[1] * DOWN)
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

        self.play(eq1.animate.shift(20 * LEFT * UNIT))
        self.play(eq1.animate.scale(1.2))
        self.play(eq1.animate.scale(5.0 / 6))
        self.wait(1)
        self.play(eq1.animate.shift(20 * LEFT * UNIT))
        self.wait(1)

        eq2 = MathTex(
            r"\begin{bmatrix}"
            r"\lambda_1 \\"
            r"\lambda_2 \\"
            r"\lambda_3"
            r"\end{bmatrix} ="
            r"\begin{bmatrix}"
            r"0 \\"
            r"-\frac{k}{m_1} \\"
            r"-\frac{k(2m_1 + m_2)}{m_1 m_2}"
            r"\end{bmatrix}",
            color=dark_blue,
            font_size=48
        )[0]
        eq2.shift(eq2[4].get_bottom()[1] * DOWN)
        eq2[15].set_color(blue)
        eq2[17:19].set_color(red)
        eq2[20].set_color(blue)
        eq2[23:25].set_color(red)
        eq2[26:28].set_color(red)
        eq2[30:34].set_color(red)

        self.play(Write(eq2))
        self.wait(1)

        eq3 = MathTex(
            r"\left[ \mathbf{v}_1 \quad \mathbf{v}_2 \quad \mathbf{v}_3 \right] ="
            r"\left[ \begin{array}{ccc}"
            r"1 & -1 & 1 \\"
            r"1 & 0 & -\frac{2m_1}{m_2} \\"
            r"1 & 1 & 1"
            r"\end{array} \right]",
            color=dark_blue,
            font_size=48
        )[0]
        eq3.shift(2 * UNIT * DOWN + eq3[1].get_bottom()[1] * DOWN)
        eq3[19:21].set_color(red)
        eq3[22:24].set_color(red)

        self.play(Write(eq3), eq2.animate.shift(2 * UP * UNIT))
        self.wait(1)

        eq4 = MathTex("\lambda = -\omega^2", color=dark_blue, font_size=48)[0]
        eq4.shift(2 * UNIT * UP + 4 * UNIT * RIGHT - eq4[0].get_bottom()[1] * UP)
        self.play(LaggedStart(eq2.animate.shift(3*UNIT*LEFT),Write(eq4), lag_ratio=0.4))

        eigen = Group(eq2, eq3, eq4)
        self.wait(1)
        self.play(FadeOut(eigen))
        self.wait(1)

        eq00 = MathTex(
            r"\textbf{x}(t) = C_1 \textbf{v}_1 e^{i \omega_1 t} + C_2 \textbf{v}_2 e^{i \omega_2 t} + \cdots + C_n \textbf{v}_n e^{i \omega_n t}",
            color=dark_blue
        )[0]
        eq00.shift(eq00[0].get_bottom()[1] * DOWN)
        self.play(Write(eq00))
        self.wait(1)

        eq5 = MathTex(
            r"\textbf{x}(t) = C_1 \textbf{v}_1 \cos(\omega_1 t) + C_2 \textbf{v}_2 \cos(\omega_2 t) + \cdots + C_n \textbf{v}_n \cos(\omega_n t)",
            color=dark_blue
        )[0]
        eq5.shift(eq5[0].get_bottom()[1] * DOWN)
        self.play(ReplacementTransform(eq00[:9], eq5[:9]), ReplacementTransform(eq00[9:14], eq5[9:17]), ReplacementTransform(eq00[14:19], eq5[17:22]), ReplacementTransform(eq00[19:24], eq5[22:30]), ReplacementTransform(eq00[24:33], eq5[30:39]), ReplacementTransform(eq00[33:], eq5[39:]),)


        self.wait(1)
        self.play(Indicate(eq5[13:15]), Indicate(eq5[26:28]), Indicate(eq5[43:45]))
        self.wait(1)
        self.play(Indicate(eq5[5:7]), Indicate(eq5[18:20]), Indicate(eq5[35:37]))
        self.wait(1)
        self.play(Indicate(eq5[7:9]), Indicate(eq5[20:22]), Indicate(eq5[37:39]))
        self.wait(1)
        self.add(system)
        system.move_to(19 * UNIT * RIGHT)
        self.play(self.camera.frame.animate.move_to(19 * UNIT * RIGHT))
        self.wait(1)
        self.play(Unwrite(eq5))

        eq7 = MathTex(
            r"\lambda_1 = 0",
            color=dark_blue,
            font_size=48
        )[0]
        eq7.shift(12 * UNIT * RIGHT + 3 * UNIT * UP + eq7[0].get_bottom()[1] * DOWN)
        self.play(Write(eq7))
        self.wait(1)

        eq8 = MathTex(
            r"\mathbf{v}_1 ="
            r"\begin{bmatrix}"
            r"1 \\"
            r"1 \\"
            r"1"
            r"\end{bmatrix}",
            color=dark_blue,
            font_size=48
        )[0]
        eq8.shift(15 * UNIT * RIGHT + 3 * UNIT * UP + eq8[0].get_bottom()[1] * DOWN)
        self.play(Write(eq8))
        self.wait(1)

        self.play(system.animate.shift(1*UNIT*RIGHT))
        self.wait(1)

        eq52 = MathTex(
            r"\textbf{x}(t) = C_2 \textbf{v}_2 \cos\left(\omega_2 t\right) + C_3 \textbf{v}_3 \cos\left(\omega_3 t\right)",
            color=dark_blue
        )[0]
        eq52.shift(eq52[0].get_bottom()[1] * DOWN)
        self.add(eq52)


        eq6 = MathTex(
            r"\textbf{x}(t) = C_2 "
            r"\begin{bmatrix}"
            r"-1 \\"
            r"0 \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_2} t\right) + C_3 "
            r"\begin{bmatrix}"
            r"1 \\"
            r"-\frac{2m_1}{m_2} \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_3} t\right)", color=dark_blue
        )[0]
        eq6[34:36].set_color(red)
        eq6[37:39].set_color(red)
        eq6.shift(eq6[0].get_bottom()[1] * DOWN)
        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.wait(1)

        self.play(ReplacementTransform(eq52[:7], eq6[:7]), ReplacementTransform(eq52[7:9], eq6[7:15]),
                  ReplacementTransform(eq52[9:13], eq6[15:19]), ReplacementTransform(eq52[13: 15], eq6[19:24]),
                  ReplacementTransform(eq52[15:20], eq6[24:29]), ReplacementTransform(eq52[20:22], eq6[29:42]),
                  ReplacementTransform(eq52[22:26], eq6[42:46]), ReplacementTransform(eq52[26:28], eq6[46:51]),
                  ReplacementTransform(eq52[28:], eq6[51:]))

        eq9 = MathTex(
            r"m_2 = 3 m_1",
            color=dark_blue,
            font_size=48
        )[0]
        eq9.shift(2*UNIT*UP + eq9[0].get_bottom()[1] * DOWN)
        eq9[:2].set_color(red)
        eq9[4:6].set_color(red)
        self.play(Write(eq9))
        self.wait(1)

        eq10 = MathTex(
            r"\textbf{x}(t) = C_2 "
            r"\begin{bmatrix}"
            r"-1 \\"
            r"0 \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_2} t\right) + C_3 "
            r"\begin{bmatrix}"
            r"1 \\"
            r"-\frac{2}{3} \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_3} t\right)", color=dark_blue
        )[0]
        eq10.shift(eq10[0].get_bottom()[1] * DOWN)
        self.play(ReplacementTransform(eq6[34:36], eq10[32]), ShrinkToCenter(eq6[31:33]), ReplacementTransform(eq6[33], eq10[31]), ReplacementTransform(eq6[:31], eq10[:31]), ReplacementTransform(eq6[36:], eq10[33:]))
        self.wait(1)

        self.play(FadeOut(eq9))
        self.play(system.animate.shift(1 * UNIT * LEFT), Unwrite(eq7), Unwrite(eq8))

        eq11 = MathTex(
            r"\textbf{x}(t) = C_2 "
            r"\begin{bmatrix}"
            r"-1 \\"
            r"0 \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_2} t\right)", color=dark_blue, font_size=28
        )[0]
        eq11.shift(19 * UNIT * RIGHT + 4 * UNIT * DOWN + eq11[0].get_bottom()[1] * DOWN)

        left_eq = left_square.get_center()
        center_eq = center_square.get_center()
        right_eq = right_square.get_center()

        # --- Oscillation Parameters ---
        # Mode V₂ = [-1, 0, 1] with eigenfrequency
        w1 = 1
        w2_eigen = np.sqrt(2)
        C1 = 0.5
        C2 = 0.5
        direction = UP

        # --- Time Tracker ---
        time_tracker = ValueTracker(0)
        dummy = Mobject()
        dummy.add_updater(lambda m, dt: time_tracker.increment_value(dt))
        self.add(dummy)

        # --- Phase 1 ---
        # Equation: x(t) = C₂ V₂ cos(w₂ t)
        # Left mass: xₗ(t) = - C₂ cos(√2 t)
        left_square.add_updater(
            lambda m: m.move_to(
                left_eq + direction * (
                        - C2 * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )
        # Center mass: x_c(t) = 0
        center_square.add_updater(
            lambda m: m.move_to(
                center_eq
            )
        )
        # Right mass: xᵣ(t) = C₂ cos(w₂ t)
        right_square.add_updater(
            lambda m: m.move_to(
                right_eq + direction * (
                        C2 * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )

        # Let Phase 1 run for 6 seconds.
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(19 * UNIT * RIGHT),
                  ReplacementTransform(eq10[:len(eq11)].copy(), eq11))
        self.wait(20)

        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.play(Unwrite(eq11))
        self.wait(1)
        # --- Transition to Phase 2 ---
        # Stop the Phase 1 updaters.
        left_square.clear_updaters()
        center_square.clear_updaters()
        right_square.clear_updaters()
        dummy.clear_updaters()

        # Reset the time tracker to start the new phase.
        time_tracker.set_value(0)

        eq12 = MathTex(
            r"\textbf{x}(t) = C_3 "
            r"\begin{bmatrix}"
            r"1 \\"
            r"-\frac{2}{3} \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_3} t\right)", color=dark_blue, font_size=28
        )[0]
        eq12.shift(19 * UNIT * RIGHT + 4 * UNIT * DOWN + eq12[0].get_bottom()[1] * DOWN)
        self.wait(1)


        # --- Phase 2 ---
        # Equation: x(t) = C3 V3 cos(w3 t)
        # Left mass: xₗ(t) = C3 cos(w3 t)
        left_square.add_updater(
            lambda m: m.move_to(
                left_eq + direction * (
                        C2 * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )
        # Center mass: x_c(t) = C3 cos(w3 t)
        center_square.add_updater(
            lambda m: m.move_to(
                center_eq + direction * (
                        -(2.0/3.0) * C2 * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )
        # Right mass: xᵣ(t) = -2/3 * C3 cos(w3 t)
        right_square.add_updater(
            lambda m: m.move_to(
                right_eq + direction * (
                        C2 * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )

        # Restart the dummy updater so that time_tracker keeps advancing.
        dummy.add_updater(lambda m, dt: time_tracker.increment_value(dt))
        self.add(dummy)

        # Let Phase 2 run.
        self.play(self.camera.frame.animate.move_to(19 * UNIT * RIGHT),
                  ReplacementTransform(eq10[0:5].copy(), eq12[0:5]), ReplacementTransform(eq10[27:].copy(), eq12[5:]))
        self.wait(20)

        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.play(Unwrite(eq12))
        # --- Transition to Phase 3 ---
        # Stop the Phase 2 updaters.
        left_square.clear_updaters()
        center_square.clear_updaters()
        right_square.clear_updaters()
        dummy.clear_updaters()

        # Reset the time tracker to start the new phase.
        time_tracker.set_value(0)

        eq13 = MathTex(
            r"\textbf{x}(t) = C_2 "
            r"\begin{bmatrix}"
            r"-1 \\"
            r"0 \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_2} t\right) + C_3 "
            r"\begin{bmatrix}"
            r"1 \\"
            r"-\frac{2}{3} \\"
            r"1"
            r"\end{bmatrix}"
            r"t \cos\left(- \sqrt{\lambda_3} t\right)", color=dark_blue
        )[0]
        eq13.shift(eq13[0].get_bottom()[1] * DOWN)
        self.wait(1)
        self.play(ReplacementTransform(eq10[:39], eq13[:39]), GrowFromCenter(eq13[39]), ReplacementTransform(eq10[39:], eq13[40:]))
        self.play(Indicate(eq13[39]))
        self.wait(1)

        eq14 = MathTex(
            r"\textbf{x}(t) = C_2 "
            r"\begin{bmatrix}"
            r"-1 \\"
            r"0 \\"
            r"1"
            r"\end{bmatrix}"
            r" \cos\left(- \sqrt{\lambda_2} t\right) + C_3 "
            r"\begin{bmatrix}"
            r"1 \\"
            r"-\frac{2}{3} \\"
            r"1"
            r"\end{bmatrix}"
            r"t \cos\left(- \sqrt{\lambda_3} t\right)", color=dark_blue, font_size=28
        )[0]
        eq14.shift(19 * UNIT * RIGHT + 4 * UNIT * DOWN + eq14[0].get_bottom()[1] * DOWN)


        # --- Phase 3 ---
        # Equation: x(t) = C2 V2 cos(w2 t) + C3 V3 t cos(w3 t)
        # Left mass: xₗ(t) = C3 cos(w3 t)
        left_square.add_updater(
            lambda m: m.move_to(
                left_eq + direction * (
                        - C2 * np.cos(w2_eigen * time_tracker.get_value()) +
                        C2 * time_tracker.get_value() * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )
        center_square.add_updater(
            lambda m: m.move_to(
                center_eq + direction * (
                        -(2.0 / 3.0) * C2 * time_tracker.get_value() * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )
        right_square.add_updater(
            lambda m: m.move_to(
                right_eq + direction * (
                        C2 * np.cos(w2_eigen * time_tracker.get_value()) +
                        C2 * time_tracker.get_value() * np.cos(w2_eigen * time_tracker.get_value())
                )
            )
        )

        dummy.add_updater(lambda m, dt: time_tracker.increment_value(dt))
        self.add(dummy)

        # Let Phase 3 run.
        self.wait(1)
        self.play(self.camera.frame.animate.move_to(19 * UNIT * RIGHT), ReplacementTransform(eq13.copy(), eq14), )
        self.wait(10)

        self.play(Unwrite(eq13))
        self.play(self.camera.frame.animate.move_to(ORIGIN))
        self.play(Unwrite(eq14))
        # --- Transition to Phase 3 ---
        # Stop the Phase 2 updaters.
        left_square.clear_updaters()
        center_square.clear_updaters()
        right_square.clear_updaters()
        dummy.clear_updaters()

        eq15 = MathTex("k", color=blue)[0]
        eq15.shift(2 * UNIT * LEFT + eq15[0].get_bottom()[1] * DOWN)
        eq16 = MathTex("m_1", color=red)[0]
        eq16.shift(eq16[0].get_bottom()[1] * DOWN)
        eq17 = MathTex("m_2", color=red)[0]
        eq17.shift(2 * UNIT * RIGHT + eq17[0].get_bottom()[1] * DOWN)

        self.play(LaggedStart(Write(eq15), Write(eq16), Write(eq17), lag_ratio=0.5))
        self.wait(2)