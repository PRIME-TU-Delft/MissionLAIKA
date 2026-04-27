from manim import *


def pendulum_graph_no_fric(scene):
    self = scene
    UNIT = 3 / 4
    dark_blue = ManimColor("#0C2340")
    red = ManimColor("#E03C31")
    yellow = ManimColor("#cc9316")
    blue = ManimColor("#0076C2")
    green = ManimColor("#009B77")

    friction_text = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \text{No friction: } b = 0 """,
        color=dark_blue,
        font_size=50,
    ).shift(3 * UNIT * UP)



    # Split the formula into separate objects so only the first line transforms.
    old_theta_line = MathTex(
        r"\theta = C_1 \cos(st) + C_2 \sin(st)",
        color=dark_blue,
        font_size=40,
    )

    theta_dot_line = MathTex(
        r"\theta' = - C_1s \sin(st) + C_2s \cos(st)",
        color=dark_blue,
        font_size=40,
    )

    formula_lines = VGroup(old_theta_line, theta_dot_line).arrange(
        DOWN, aligned_edge=LEFT, buff=0.25
    )

    # brace = MathTex(r"\left\{", color=dark_blue, font_size=70).next_to(
    #     formula_lines, LEFT, buff=0.2
    # )
    brace = MathTex(r"\bigg\{", color=dark_blue, font_size=40)
    brace.match_height(formula_lines)
    brace.next_to(formula_lines, LEFT, buff=0.12)    
    # brace = Brace(formula_lines, LEFT, buff=0.15, color=dark_blue)

    friction_formula = VGroup(brace, formula_lines)
    brace[0].shift(brace[0][0].get_bottom()[1] * DOWN)
    formula_lines[0].shift(formula_lines[0][0].get_bottom()[1] * DOWN + 1 * UP * UNIT)

    old_theta_line[0].shift(old_theta_line[0][0].get_bottom()[1] * DOWN + 1 * UP * UNIT)
    theta_dot_line[0].shift(theta_dot_line[0][0].get_bottom()[1] * DOWN)


    # This is the target for the replacement transform.
    new_theta_line = MathTex(
        r"s\theta = C_1 s \cos(st) + C_2 s \sin(st)",
        color=dark_blue,
        font_size=40,
    ).move_to(old_theta_line, aligned_edge=LEFT)

    friction_formula_squared = MathTex(
        r"""{\renewcommand{\arraystretch}{1.15}
        \begin{cases}
        (s\theta)^2 = C_1^2 s^2 \cos^2(st) + C_2^2 s^2 \sin^2(st) + 2 C_1 C_2 s^2 \cos(st) \sin(st) \\
        (\theta')^2 = C_1^2 s^2 \sin^2(st) + C_2^2 s^2 \cos^2(st) - 2C_1 C_2 s^2 \cos(st) \sin(st)
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

    # 0 5 16

    new_theta_line[0][0].set_color(red)
    new_theta_line[0][5].set_color(red)
    new_theta_line[0][16].set_color(red)

    main_group = VGroup(
        friction_formula, friction_formula_squared, bar, friction_addition
    ).arrange(DOWN, buff=0.45)

    friction_text[0].shift(friction_text[0][0].get_bottom()[1] * DOWN + 5.5 * UNIT * LEFT + 4 * UP * UNIT)


    self.play(Write(friction_text))
    self.play(Write(friction_formula))

    # Only replace the first line; the theta' line stays still.
    new_theta_line.move_to(old_theta_line, aligned_edge=LEFT)
    self.play(ReplacementTransform(old_theta_line, new_theta_line))

    # indices = index_labels(new_theta_line[0])
    # self.add(indices)

    self.wait(0.5)

    self.wait(0.5)
    friction_formula_squared[0].shift(friction_formula_squared[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)
    plus[0].shift(plus[0][0].get_bottom()[1] * DOWN)
    bar[0].shift(bar[0][0].get_bottom()[1] * DOWN + 1 * DOWN * UNIT)

    self.play(
        Write(friction_formula_squared),
        Write(plus.shift(0.5 * DOWN * UNIT)),
        Write(bar),
    )

    friction_addition[0].shift(friction_addition[0][0].get_bottom()[1] * DOWN + 2 * DOWN * UNIT + 4 * LEFT * UNIT)

    
    self.play(Write(friction_addition))

    self.play(
        FadeOut(
            VGroup(
                friction_text,
                brace,
                new_theta_line,
                theta_dot_line,
                friction_formula_squared,
                plus,
                bar,
            )
        )
    )

    self.play(friction_addition.animate.shift(2 * UNIT * DOWN + 4 * UNIT * RIGHT))

    # pendulum 2:
    time = ValueTracker(0)

    # maximum swing angle in radians
    theta_ref = 45 / 180 * PI
    theta_max_tracker = ValueTracker(15 * PI / 180)

    theta_max = 15 / 180 * PI
    scale = theta_max / theta_ref

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
    alpha = b / 2
    wd = np.sqrt(max(w**2 - alpha**2, 0))

    def theta_func(t):
        return theta_max_tracker.get_value() * np.exp(-alpha * t) * (
            np.cos(wd * t) + (alpha / wd) * np.sin(wd * t)
        )

    def theta_dot_func(t):
        return -theta_max_tracker.get_value() * (w**2 / wd) * np.exp(-alpha * t) * np.sin(wd * t)

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
    theta.set_value(0)
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
        # .shift(UP * 0.2)
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

    v_scale = 0.6  # smaller = wider-looking ellipse

    phase_point = always_redraw(
        lambda: Dot(color=yellow).move_to(
            phase_axes.c2p(
                scale * theta_func(time.get_value()),
                scale * theta_dot_func(time.get_value()) * v_scale,
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

    prep_theta = ValueTracker(0)

    theta.clear_updaters()
    theta.add_updater(lambda m: m.set_value(prep_theta.get_value()))

    self.play(
        prep_theta.animate.set_value(theta_max_tracker.get_value()),
        run_time=1.2,
        rate_func=smooth,
    )

    theta.clear_updaters()
    theta.add_updater(lambda m: m.set_value(theta_func(time.get_value())))

    self.add(phase_trace, phase_point)
    self.play(time.animate.set_value(3 * T), rate_func=linear, run_time=3 * T)
    phase_trace.suspend_updating()
    phase_trace_frozen = phase_trace.copy()
    phase_trace_frozen.clear_updaters()
    self.add(phase_trace_frozen)
    frozen_ellipse = ParametricFunction(
        lambda u: phase_axes.c2p(
            scale * theta_max * np.cos(u),
            -scale * theta_max * w * np.sin(u) * v_scale,
        ),
        t_range=[0, TAU],
        color=yellow,
        stroke_width=2,
    )
    self.add(frozen_ellipse)
    self.remove(phase_point)
    self.wait(1)

    end_theta = theta_max_tracker.get_value()

    prep_theta = ValueTracker(end_theta)

    line.clear_updaters()
    ball.clear_updaters()

    line.add_updater(
        lambda m: m.become(
            Line(
                start=ORIGIN + shift_req,
                end=ORIGIN + shift_req
                + l * np.sin(prep_theta.get_value()) * RIGHT
                - l * np.cos(prep_theta.get_value()) * UP,
                color=dark_blue,
            )
        )
    )

    ball.add_updater(
        lambda m: m.become(
            Dot(fill_color=red, fill_opacity=1)
            .move_to(
                ORIGIN + shift_req
                + l * np.sin(prep_theta.get_value()) * RIGHT
                - l * np.cos(prep_theta.get_value()) * UP
            )
            .scale(l)
        )
    )

    self.play(
        prep_theta.animate.set_value(45 * PI / 180),
        run_time=1.2,
        rate_func=smooth,
    )

    self.wait(1)

    time2 = ValueTracker(0)
    theta.clear_updaters()
    theta.add_updater(lambda m: m.set_value(theta_func(time2.get_value())))

    line.clear_updaters()
    ball.clear_updaters()

    theta_max_tracker.set_value(45 * PI / 180)

    theta.add_updater(lambda m: m.set_value(theta_func_2(time2.get_value())))
    line.add_updater(
        lambda m: m.become(
            Line(
                start=ORIGIN + shift_req,
                end=ORIGIN + shift_req
                + l * np.sin(theta_func_2(time2.get_value())) * RIGHT
                - l * np.cos(theta_func_2(time2.get_value())) * UP,
                color=dark_blue,
            )
        )
    )
    ball.add_updater(
        lambda m: m.become(
            Dot(fill_color=red, fill_opacity=1)
            .move_to(
                ORIGIN + shift_req
                + l * np.sin(theta_func_2(time2.get_value())) * RIGHT
                - l * np.cos(theta_func_2(time2.get_value())) * UP
            )
            .scale(l)
        )
    )

    theta_max = 45 / 180 * PI

    l = 3
    g = 9.81
    w = np.sqrt(g / l)
    b = 0
    T = 2 * PI / w
    alpha = b / 2
    wd = np.sqrt(max(w**2 - alpha**2, 0))

    def theta_func_2(t):
        return theta_max * np.exp(-alpha * t) * (
            np.cos(wd * t) + (alpha / wd) * np.sin(wd * t)
        )

    def theta_dot_func_2(t):
        return -theta_max * (w**2 / wd) * np.exp(-alpha * t) * np.sin(wd * t)

    phase_point2 = always_redraw(
        lambda: Dot(color=yellow).move_to(
            phase_axes.c2p(
                0.33 * theta_func_2(time2.get_value()),
                0.33 * theta_dot_func_2(time2.get_value()) * v_scale,
            )
        )
    )

    phase_trace2 = TracedPath(
        phase_point2.get_center,
        stroke_color=yellow,
        stroke_width=2,
    )

    self.add(phase_trace2, phase_point2)
    self.play(time2.animate.set_value(3 * T), rate_func=linear, run_time=3 * T)

    frozen_ellipse2 = ParametricFunction(
        lambda u: phase_axes.c2p(
            0.33 * theta_max * np.cos(u),
            0.33 * -theta_max * w * np.sin(u) * v_scale,
        ),
        t_range=[0, TAU],
        color=yellow,
        stroke_width=2,
    )
    self.add(frozen_ellipse2)
    self.remove(phase_point2)

    line.clear_updaters()
    ball.clear_updaters()
    self.play(
        FadeOut(line_vertical),
        FadeOut(wall),
        *(FadeOut(hatch_lines[i]) for i in range(8)),
        FadeOut(line),
        FadeOut(ball),
        FadeOut(phase_axes),
        FadeOut(phase_labels),
        FadeOut(phase_trace),
        FadeOut(phase_point2),
        FadeOut(phase_trace2),
        FadeOut(friction_addition),
        FadeOut(frozen_ellipse),
        FadeOut(frozen_ellipse2),
        FadeOut(phase_trace_frozen)
    )