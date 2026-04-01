from manim import *


def pendulum_graph_no_fric(scene):
    self = scene
    UNIT = 3 / 4
    dark_blue = ManimColor("#0C2340")
    red = ManimColor("#E03C31")  # ManimColor('#FF5132')
    yellow = ManimColor("#cc9316")  # ManimColor('#FFCC12')
    blue = ManimColor("#0076C2")  # ManimColor('#46A6FF')
    green = ManimColor("#009B77")

    friction_text = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \text{No friction: } b = 0 """,
        color=dark_blue,
        font_size=50,
    ).shift(3 * UNIT * UP)
    friction_formula = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        \theta = C_1 \cos(st) + C_2 \sin(st) \\
        \theta' = - C_1 \sin(st) + C_2s \cos(st)
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    )

    friction_formula_s1 = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        s \theta = C_1 \cos(st) + C_2  \sin(st) \\
        \theta' = - C_1 \sin(st) + C_2s \cos(st)
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    )

    friction_formula_s2 = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        s \theta = C_1 s \cos(st) + C_2 \sin(st) \\
        \theta' = - C_1 \sin(st) + C_2s \cos(st)
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    )

    friction_formula_s3 = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        s \theta = C_1 s \cos(st) + C_2 s \sin(st) \\
        \theta' = - C_1 \sin(st) + C_2s \cos(st)
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
    )

    friction_formula_s1[0][1].set_color(red)

    # # DEBUG
    # self.add(friction_formula_s1)
    # indices = index_labels(friction_formula_s1[0])
    # self.add(indices)
    # self.wait(1)
    # self.remove(friction_formula_s1)
    # self.remove(indices)
    
    friction_formula_s2[0][1].set_color(red)
    friction_formula_s2[0][6].set_color(red)

    # self.add(friction_formula_s2)
    # indices = index_labels(friction_formula_s2[0])
    # self.add(indices)
    # self.wait(1)
    # self.remove(friction_formula_s2)
    # self.remove(indices)

    friction_formula_s3[0][1].set_color(red)
    friction_formula_s3[0][6].set_color(red)
    friction_formula_s3[0][17].set_color(red)

    # self.add(friction_formula_s3)
    # indices = index_labels(friction_formula_s3[0])
    # self.add(indices)
    # self.wait(1)
    # self.remove(friction_formula_s3)
    # self.remove(indices)

    friction_formula_squared = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        (s\theta)^2 = C_1^2 s^2 \cos^2(st) + C_2^2 s^2 \sin^2(st) + 2 C_1 C_2 s^2 \cos(st) \sin(st) \\
        (\theta')^2 = - C_1^2 s^2 \sin^2(st) + C_2^2 s^2 \cos^2(st) - 2C_1 C_2 s^2 \cos(st) \sin(st)
        \end{cases}
        """,
        color=dark_blue,
        font_size=40,
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
        (s \theta)^2 + (\theta ')^2 = s^2 (C_1^2 + C_2^2)
        """,
        color=dark_blue,
        font_size=40,
    )
    main_group = VGroup(
        friction_formula, friction_formula_squared, bar, friction_addition
    ).arrange(DOWN, buff=0.45)

    self.play(Write(friction_text.shift(5.5 * UNIT * LEFT + 1 * UNIT * UP)))
    self.play(Write(friction_formula))
    friction_formula_s1.move_to(friction_formula, aligned_edge=LEFT)
    friction_formula_s2.move_to(friction_formula, aligned_edge=LEFT)
    friction_formula_s3.move_to(friction_formula, aligned_edge=LEFT)

    self.play(ReplacementTransform(friction_formula[0][0], friction_formula_s1[0][0]),
              ReplacementTransform(friction_formula[0][1], friction_formula_s1[0][1:3]),
              ReplacementTransform(friction_formula[0][2:], friction_formula_s1[0][3:]))
    self.wait(0.5)

    self.play(
        ReplacementTransform(friction_formula_s1[0][:4], friction_formula_s2[0][:4]),
        ReplacementTransform(friction_formula_s1[0][4:6], friction_formula_s2[0][4:7]),
        ReplacementTransform(friction_formula_s1[0][6:], friction_formula_s2[0][7:])
    )
    self.wait(0.5)
    self.play(
        ReplacementTransform(friction_formula_s2[0][:15], friction_formula_s3[0][:15]),
        ReplacementTransform(friction_formula_s2[0][15:17], friction_formula_s3[0][15:18]),
        ReplacementTransform(friction_formula_s2[0][17:], friction_formula_s3[0][18:])
    )
    self.wait(0.5)
    self.play(
        Write(friction_formula_squared),
        Write(plus.shift(0.7 * UNIT * DOWN)),
        Write(bar.shift(0.3 * UNIT * UP)),
    )
    self.play(Write(friction_addition))

    # self.play(FadeOut(friction_formula), FadeOut(friction_formula_s[0][15:18]), FadeOut(friction_formula_s[0][4:7]), FadeOut(friction_formula_s[0][1:3]), FadeOut(plus), FadeOut(bar), FadeOut(friction_text), FadeOut(friction_formula_squared))
    self.play(
        FadeOut(
            VGroup(
                friction_text,
                # friction_formula,
                friction_formula_s3,
                friction_formula_squared,
                plus,
                bar,
            )
        )
    )
    # self.remove(friction_formula_s, friction_formula)
    self.play(friction_addition.animate.shift(1 * UNIT * DOWN + 2 * UNIT * RIGHT))
    # pendulum 2:
    time = ValueTracker(0)

    # maximum swing angle in radians
    theta_max = 45 / 180 * PI

    # length of pendulum
    l = 3

    # gravity
    g = 9.81

    # angular freq
    w = np.sqrt(g / l)

    # damping
    b = 0

    # time period
    T = 2 * PI / w

    # damped angular freq
    wd = np.sqrt(max(w**2 - (b / 2) ** 2, 0))

    def theta_func(t):
        return theta_max * np.exp(-b * t / 2) * np.sin(wd * t)

    def theta_dot_func(t):
        return (
            theta_max
            * np.exp(-b * t / 2)
            * (wd * np.cos(wd * t) - (b / 2) * np.sin(wd * t))
        )

    # shift pendulum placement
    p_x = 3
    p_y = 1.5
    shift_req = p_x * RIGHT + p_y * UP

    wall = Line(
        start=ORIGIN + 1.5 * LEFT * UNIT + shift_req,
        end=1.5 * RIGHT * UNIT + shift_req,
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

    # background theta calculation
    theta = DecimalNumber().set_color(dark_blue).move_to(10 * RIGHT)
    theta.add_updater(lambda m: m.set_value(theta_func(time.get_value())))
    self.add(theta)

    phase_axes = (
        Axes(
            x_range=[-theta_max * 1.2, theta_max * 1.2, theta_max / 2],
            y_range=[
                -theta_max * wd * 1.2,
                theta_max * wd * 1.2,
                theta_max * wd / 2,
            ],
            x_length=4.5,
            y_length=4.5,
            axis_config={
                "color": dark_blue,
                "stroke_width": 3,
                "include_numbers": True,
            },
            tips=False,
        )
        .to_edge(LEFT)
        .shift(UP * 0.2)
    )

    # phase_labels = phase_axes.get_axis_labels(
    #     MathTex(r"\theta", color=dark_blue),
    #     MathTex(r"\theta'", color=dark_blue),
    # )

    theta_label = MathTex(r"\theta", color=dark_blue)
    theta_dot_label = MathTex(r"\theta'", color=dark_blue)

    phase_labels = VGroup(
        theta_label.next_to(phase_axes, RIGHT, buff=0.1).shift(1.5 * UNIT * LEFT),
        theta_dot_label.next_to(phase_axes, UP, buff=0.1),
    )

    phase_point = always_redraw(
        lambda: Dot(color=yellow).move_to(
            phase_axes.c2p(
                theta_func(time.get_value()), theta_dot_func(time.get_value())
            )
        )
    )

    phase_trace = TracedPath(
        phase_point.get_center,
        stroke_color=yellow,
        stroke_width=2,
    )

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
        lambda: get_line(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value()))
    )

    line_vertical = DashedLine(
        start=line.get_start(),
        end=line.get_start() + 3 * DOWN,
        color=dark_blue,
    )

    # mass at end of pendulum (BALL)
    def get_ball(x, y):
        dot = (
            Dot(fill_color=red, fill_opacity=1)
            .move_to(x * RIGHT + y * UP + shift_req)
            .scale(l)
        )
        return dot

    ball = always_redraw(
        lambda: get_ball(l * np.sin(theta.get_value()), -l * np.cos(theta.get_value()))
    )

    self.wait(1)

    # add pendulum
    self.play(
        LaggedStart(
            *(FadeIn(hatch_lines[i]) for i in range(8)), Create(wall), lag_ratio=0
        ),
        FadeIn(line_vertical),
        FadeIn(line),
        FadeIn(ball),
        Create(phase_axes, lag_ratio=0, run_time=1),
        FadeIn(phase_labels),
    )
    self.wait(1)

    no_friction_text = (
        MathTex(
            r"""{\renewcommand{\arraystretch}{1.45}
        \text{No friction: }
        """,
            color=dark_blue,
            font_size=40,
        )
        .move_to(phase_axes, DOWN)
        .shift(1 * DOWN * UNIT)
    )

    self.play(Write(no_friction_text))

    self.add(phase_trace, phase_point)
    self.play(time.animate.set_value(3 * T), rate_func=linear, run_time=3 * T)

    self.play(
        FadeOut(line_vertical),
        FadeOut(wall),
        *(FadeOut(hatch_lines[i]) for i in range(8)),
        FadeOut(line),
        FadeOut(ball),
        FadeOut(phase_axes),
        FadeOut(phase_labels),
        FadeOut(phase_point),
        FadeOut(phase_trace),
        FadeOut(friction_addition),
        FadeOut(no_friction_text),
    )
