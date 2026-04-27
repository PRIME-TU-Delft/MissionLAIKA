from manim import *

def pendulum_init(scene):
    self = scene
    UNIT = 3 / 4
    dark_blue = ManimColor("#0C2340")
    red = ManimColor("#E03C31")  # ManimColor('#FF5132')
    yellow = ManimColor("#cc9316")  # ManimColor('#FFCC12')
    blue = ManimColor("#0076C2")  # ManimColor('#46A6FF')
    green = ManimColor("#009B77")
    
    pendulum_at_rest = MathTex(
            r"""{\renewcommand{\arraystretch}{1.15}
           \begin{cases}
            \theta = 0 \\
            \theta ' = 0 \\
            \end{cases}""",
            color=dark_blue,
            font_size=50,
        )

    time = ValueTracker(0)

    # maximum swing angle in radians
    theta_max = 30 / 180 * PI

    # length of pendulum
    l = 3

    # gravity
    g = 15

    # angular freq
    w = np.sqrt(g / l)

    # time period
    T = 2 * PI / w

    # shift pendulum placement
    p_x = 0
    p_y = 1.5
    shift_req = p_x * RIGHT + p_y * UP

    wall = Line(
        start=ORIGIN + 1.5 * LEFT * UNIT + p_y * UP,
        end=1.5 * RIGHT * UNIT + p_y * UP,
        stroke_color=dark_blue,
        stroke_width=4,
        fill_opacity=0.0,
    )

    hatch_lines = []
    for k in range(8):
        hatch_lines.append(
            Line(
                start=(wall.get_left() + UNIT * UP)
                + ((3 * UNIT / 8) * (k + 1)) * RIGHT,
                end=wall.get_left() + ((3 * UNIT / 8) * (k)) * RIGHT,
                color=dark_blue,
                stroke_width=3,
            )
        )

    self.play(
        LaggedStart(
            *(Create(hatch_lines[i]) for i in range(8)), Create(wall), lag_ratio=0.2
        )
    )

    # background theta calculation
    theta = DecimalNumber().set_color(dark_blue).move_to(10 * RIGHT)
    theta.add_updater(
        lambda m: m.set_value((theta_max) * np.sin(w * time.get_value()))
    )

    self.add(theta)

    def get_line(x, y):
        # pendulum
        line_here = Line(
            start=ORIGIN + shift_req,
            end=x * RIGHT + y * UP + shift_req,
            color=dark_blue,
        )

        # static (centerpoint)

        return line_here

    line = always_redraw(
        lambda: get_line(
            l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())
        )
    )

    line_vertical = DashedLine(
        start=line.get_start(),
        end=line.get_start() + 3 * DOWN,
        color=dark_blue,
    )

    # draw arc
    def angle_arc(theta):
        global angle
        global arc_text
        if theta == 0:
            angle = VectorizedPoint().move_to(10 * RIGHT)
            arc_text = VectorizedPoint().move_to(10 * RIGHT)
        else:
            if theta > 0:
                angle = Angle(
                    line,
                    line_vertical,
                    quadrant=(1, 1),
                    other_angle=True,
                    color=yellow,
                    fill_opacity=0,
                )

            elif theta < 0:
                angle = Angle(
                    line,
                    line_vertical,
                    quadrant=(1, 1),
                    other_angle=False,
                    color=yellow,
                    fill_opacity=0,
                )
        return angle

    angle = always_redraw(lambda: angle_arc(theta.get_value()))
    # self.add(angle)
    arc_text = (
        MathTex(r"\theta", color=yellow, font_size=40)
        .next_to(wall, DOWN)
        .shift(RIGHT * UNIT * 0.7 + 0.2 * UP * UNIT)
    )

    # arc_text.add_updater(lambda m: m.next_to(angle, DOWN))

    ball_label = MathTex(
        r"m",
        color=dark_blue,
        font_size=50,
    )
    ball_label.add_updater(lambda m: m.next_to(ball, RIGHT * UNIT))

    # midpoint helper for length label
    def get_midpoint(x, y):
        dot = (
            Dot(fill_color=red, fill_opacity=0)
            .move_to(x * RIGHT + y * UP + shift_req)
            .scale(l)
        )
        return dot

    midpoint = always_redraw(
        lambda: get_midpoint(
            l / 2 * np.sin(theta.get_value()), -l / 2 * np.cos(theta.get_value())
        )
    )
    self.add(midpoint)

    # length of pendulum label
    length_label = MathTex(
        r"L",
        color=dark_blue,
        font_size=50,
    )
    length_label.add_updater(lambda m: m.next_to(midpoint, RIGHT * UNIT * 0.75))

    # mass at end of pendulum (BALL)
    def get_ball(x, y):
        dot = (
            Dot(fill_color=red, fill_opacity=1)
            .move_to(x * RIGHT + y * UP + shift_req)
            .scale(l)
        )
        return dot

    ball = always_redraw(
        lambda: get_ball(
            l * np.sin(theta.get_value()), -l * np.cos(theta.get_value())
        )
    )

    # add pendulum
    self.play(Write(line_vertical), Write(line), FadeIn(ball), FadeIn(angle))
    self.play(Write(ball_label), Write(length_label))
    self.wait(1)
    # add pendulum at rest
    self.play(Write(pendulum_at_rest.shift(5 * RIGHT * UNIT)))

    self.wait(2)

    self.play(FadeOut(pendulum_at_rest))

    self.play(time.animate.set_value(3.25 * T), rate_func=linear, run_time=3.25 * T)
    self.play(
        FadeIn(
            arc_text.move_to(angle, DOWN).shift(
                DOWN * 0.5 * UNIT + RIGHT * 0.1 * UNIT
            )
        )
    )
    self.wait(1)

    ball_angle_no_dash = Angle(
        line,
        line_vertical,
        radius=l,
        quadrant=(1, 1),
        other_angle=True,
        color=yellow,
        fill_opacity=0,
    )
    ball_angle = DashedVMobject(ball_angle_no_dash)
    ball_angle.set_z_index(0)
    ball.set_z_index(1)
    self.play(Write(ball_angle))
    # pendulum = VGroup(angle, ball, line_vertical, line, length_label, ball_label,midpoint,arc_text)
    # self.play(pendulum.animate.shift(2*UNIT*RIGHT))

    force_gravity = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        F_g = mg""",
        color=dark_blue,
        font_size=50,
    )

    force_tension = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        F_t = mg \sin(\theta)""",
        color=dark_blue,
        font_size=50,
    )

    forces_eqs = (
        VGroup(force_gravity, force_tension)
        .arrange(DOWN, aligned_edge=LEFT)
        .shift(5 * LEFT * UNIT)
    )

    force_gravity[0].shift(force_gravity[0][0].get_bottom()[1] * DOWN)
    force_tension[0].shift(force_tension[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)
    self.play(Write(forces_eqs))

    self.wait(1)

    # gravity arrow
    gravity_arrow_start = ball.get_bottom()
    gravity_arrow_end = ball.get_bottom() + 2 * DOWN * UNIT
    gravity_arrow = Line(
        start=gravity_arrow_start, end=gravity_arrow_end, color=red, buff=0
    )
    gravity_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

    gravity_arrow_label = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        F_g""",
        color=red,
        font_size=30,
    ).next_to(gravity_arrow, LEFT)

    self.add(gravity_arrow)

    self.play(
        GrowFromPoint(gravity_arrow, ball.get_bottom()), Write(gravity_arrow_label)
    )

    self.wait(1)

    # tension arrow
    tension_arrow_start = ball.get_center()
    tension_arrow_end = ball.get_center() + 0.5 * DOWN * UNIT + 1.4 * LEFT * UNIT
    tension_arrow = Line(
        start=tension_arrow_start, end=tension_arrow_end, color=red, buff=0
    )
    tension_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

    tension_arrow_label = (
        MathTex(
            r"""{\renewcommand{\arraystretch}{1.45}
        F_t""",
            color=red,
            font_size=30,
        )
        .next_to(tension_arrow, UP)
        .shift(0.2 * LEFT + 0.2 * DOWN)
    )

    self.add(tension_arrow)

    self.play(
        GrowFromPoint(tension_arrow, ball.get_center()), Write(tension_arrow_label)
    )

    self.wait(1)

    # write triangle
    theta_now = theta.get_value()

    A = ball.get_center()
    B = gravity_arrow_end
    H = np.linalg.norm(B - A)

    # corner chosen so the angle at A matches the pendulum angle theta_now
    C = A + H * np.cos(theta_now) * (
        np.sin(theta_now) * RIGHT - np.cos(theta_now) * UP
    )

    leg1 = Line(A, C, color=dark_blue, buff=0)
    leg2 = Line(C, B, color=dark_blue, buff=0)

    right_angle = RightAngle(
        leg1, leg2, length=0.18, quadrant=(-1, 1), color=dark_blue
    )

    theta_arc = Angle(gravity_arrow, leg1, radius=0.28, color=dark_blue)
    # theta_arc = DashedVMobject(theta_arc_nodash, num_dashes=30, color=dark_blue)
    theta_label = MathTex(r"\theta", color=dark_blue, font_size=28).next_to(
        theta_arc, DOWN, buff=0.05
    )

    self.play(
        Create(leg1),
        Create(leg2),
        FadeIn(right_angle),
        Create(theta_arc),
        Write(theta_label),
    )

    newton = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        -mg \sin(\theta) = mL\theta''""",
        color=dark_blue,
        font_size=40,
    )

    theta_accel = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \theta'' = - \frac{g}{L} \sin(\theta)""",
        color=dark_blue,
        font_size=40,
    )

    newton_eqs = (
        VGroup(newton, theta_accel)
        .arrange(DOWN, aligned_edge=LEFT)
        .shift(5 * LEFT * UNIT)
    )

    newton[0].shift(newton[0][0].get_bottom()[1] * DOWN + 0.1 * UP *UNIT)
    theta_accel[0].shift(theta_accel[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)

    self.play(ReplacementTransform(forces_eqs, newton))
    self.wait(1)

    self.play(
        FadeOut(leg1),
        FadeOut(leg2),
        FadeOut(right_angle),
        FadeOut(theta_arc),
        FadeOut(theta_label),
        FadeOut(tension_arrow),
        FadeOut(tension_arrow_label),
        FadeOut(gravity_arrow),
        FadeOut(gravity_arrow_label),
    )

    arc_length = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        s=L \theta
        """,
        color=dark_blue,
        font_size=40,
    ).next_to(ball_angle, DOWN)

    arc_accel = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        a = L \theta''""",
        color=dark_blue,
        font_size=40,
    ).next_to(arc_length, DOWN)

    arc_length[0].shift(arc_length[0][0].get_bottom()[1] * DOWN + 3 * DOWN * UNIT)
    arc_accel[0].shift(arc_accel[0][0].get_bottom()[1] * DOWN + 4 * DOWN * UNIT)

    self.play(Write(arc_length))

    self.wait(1)
    self.play(Write(arc_accel))


    self.wait(1)
    self.play(Write(theta_accel))

    self.play(
        Wiggle(theta_accel[0][4], scale_value=1.5),
        Wiggle(ball_angle, scale_value=1.5),
    )

    self.wait()

    self.play(FadeOut(newton))
    self.play(
        FadeOut(ball),
        FadeOut(line),
        FadeOut(line_vertical),
        FadeOut(angle),
        FadeOut(length_label),
        FadeOut(ball_label),
        FadeOut(ball_angle),
        FadeOut(arc_length),
        FadeOut(arc_accel),
        FadeOut(wall),
        *(FadeOut(hatch_lines[i]) for i in range(8)),
        FadeOut(arc_text),
    )

    # theta equations

    theta_accel2 = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \theta'' = - \frac{g}{L} \sin(\theta)""",
        color=dark_blue,
        font_size=40,
    )

    small_theta = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \text{small } \theta: \sin(\theta) \approx \theta 
        """,
        color=dark_blue,
        font_size=40,
    )

    theta_approx = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \theta '' \approx -\frac{g}{L} \theta 
        """,
        color=dark_blue,
        font_size=40,
    )

    theta_friction = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \text{with friction: } \theta '' = -\frac{g}{L} \theta - b \theta '
        """,
        color=dark_blue,
        font_size=40,
    )

    theta_eqs = VGroup(
        theta_accel2, small_theta, theta_approx, theta_friction
    ).arrange(DOWN)
    theta_accel2[0].shift(theta_accel2[0][0].get_bottom()[1] * DOWN + 3 * UP * UNIT)
    small_theta[0].shift(small_theta[0][0].get_bottom()[1] * DOWN + 1 * UP * UNIT)
    theta_approx[0].shift(theta_approx[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)
    theta_friction[0].shift(theta_friction[0][0].get_bottom()[1] * DOWN + 3 * DOWN * UNIT)


    self.play(theta_accel.animate.move_to(theta_accel2.get_center()))
    self.add(theta_accel2)
    self.remove(theta_accel)
    self.play(Write(small_theta))

    self.wait(1)

    self.play(Write(theta_approx))

    self.wait(1)

    self.play(Write(theta_friction))

    self.wait(1)

    theta_matrix_calc = MathTex(
        r"""
        \begin{bmatrix}
        \theta\\
        \theta'
        \end{bmatrix}'
        =
        \begin{bmatrix}
        0 & 1 \\
        -\frac{g}{L} & -b
        \end{bmatrix}
        \begin{bmatrix}
        \theta \\
        \theta'
        \end{bmatrix}
        """,
        color=dark_blue,
        font_size=40,
    ).shift(3 * UP * UNIT)

    theta_matrix_calc[0].shift(theta_matrix_calc[0][0].get_bottom()[1] * DOWN + 2 * UP * UNIT)


    underbrace = MathTex(
        r"\overbrace{\qquad\qquad}_{\text{}}",
        color=dark_blue,
        font_size=40,
    )

    underbrace.move_to(theta_matrix_calc[0][7], aligned_edge=LEFT).shift(
        UP * UNIT
    )

    a_label = MathTex(
        r"A",
        color=dark_blue,
        font_size=40,
    )
    
    a_label.move_to(underbrace,aligned_edge=UP).shift(0.5 * UP * UNIT)

    # self.play(ReplacementTransform(theta_eqs, theta_matrix_calc))
    self.play(FadeOut(theta_eqs))
    self.play(Write(theta_matrix_calc))
    self.wait(1)
    self.play(FadeIn(underbrace),FadeIn(a_label))
    self.wait(0.5)

    # DEBUG
    # indices = index_labels(theta_matrix_calc[0])
    # self.add(indices)
    # self.wait()

    self.wait(1)

    A_calc = (
        MathTex(
            r"""{\renewcommand{\arraystretch}{1.45}
        \text{Eigenvalues of A: } \lambda = -\frac{b}{2} 
        \pm i \sqrt{\frac{g}{L}-\frac{b^2}{4}}""",
            color=dark_blue,
            font_size=40,
        )
    ).shift(1 * UNIT * UP)

    A_calc[0].shift(A_calc[0][0].get_bottom()[1] * DOWN)


    A_calc2 = (
        MathTex(
            r"""{\renewcommand{\arraystretch}{1.45}
        = -\frac{b}{2}} \pm is""",
            color=dark_blue,
            font_size=40,
        )
        .move_to(A_calc[0][8], aligned_edge=LEFT)
        .shift(1.5 * UNIT * DOWN + 2.8 * RIGHT * UNIT)
    )

    self.play(Write(A_calc))

    self.wait(1)

    self.play(Write(A_calc2))
    self.wait(1)

    theta_formula = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \theta = e^{-\frac{b}{2}t} ( C_1 \cos(st)+ C_2 \sin(st))""",
        color=dark_blue,
        font_size=40,
    ).shift(2 * UNIT * DOWN)

    theta_formula[0].shift(theta_formula[0][0].get_bottom()[1] * DOWN + 3 * DOWN * UNIT)


    self.play(Write(theta_formula))

    theta_d_formula = MathTex(
        r"""{\renewcommand{\arraystretch}{1.45}
        \theta ' = e^{-\frac{b}{2}t} (- C_1 s \sin(st)+C_2 s \cos(st) - \frac{b}{2}C_1 \cos(st) - \frac{b}{2} C_2 \sin(st))""",
        color=dark_blue,
        font_size=40,
    ).shift(3.5 * UNIT * DOWN)

    theta_d_formula[0].shift(theta_d_formula[0][0].get_bottom()[1] * DOWN + 4 * DOWN * UNIT)


    self.wait(1)

    self.play(Write(theta_d_formula))

    self.wait(2)

    self.play(
        FadeOut(theta_d_formula),
        FadeOut(theta_formula),
        FadeOut(A_calc),
        FadeOut(A_calc2),
        FadeOut(underbrace),
        FadeOut(a_label),
        FadeOut(theta_matrix_calc),
    )