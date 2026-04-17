from manim import *


def pendulum_double_pane(scene):
    self = scene
    UNIT = 3 / 4
    dark_blue = ManimColor("#0C2340")
    red = ManimColor("#E03C31")  # ManimColor('#FF5132')
    yellow = ManimColor("#cc9316")  # ManimColor('#FFCC12')
    blue = ManimColor("#0076C2")  # ManimColor('#46A6FF')
    green = ManimColor("#009B77")
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
    b = 0.1

    # time period
    T = 2 * PI / w

    # damped angular freq

    alpha = b / 2
    wd = np.sqrt(max(w**2 - alpha**2, 0))

    def theta_func(t):
        return theta_max * np.exp(-alpha * t) * (
            np.cos(wd * t) + (alpha / wd) * np.sin(wd * t)
        )

    def theta_dot_func(t):
        return -theta_max * (w**2 / wd) * np.exp(-alpha * t) * np.sin(wd * t)

    # shift pendulum placement
    p_x = 15
    p_y = 15
    shift_req = p_x * RIGHT + p_y * UP

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
        .shift(UP * 0.2+0.3*LEFT*UNIT)
    )


    # --- time graph on the right ---------------------------------
    theta1_color = blue 
    theta_color = red

    def theta1_func(t):
        # Replace this with your actual theta1(t)
        # For now, this is just an example:
        return 0.6 * theta_dot_func(t)

    max_time = 8 * T
    max_y = 1.2 * theta_max

    time_axes = Axes(
        x_range=[0, max_time, T],
        # y_range=[-max_y, max_y, theta_max / 2],
        y_range=[
                -theta_max * wd * 1.2,
                theta_max * wd * 1.2,
                theta_max * wd / 2,
            ],
        x_length=4.2,
        y_length=4.5,
        axis_config={
            "color": dark_blue,
            "stroke_width": 3,
            "include_numbers": True,
        },
        tips=False,
    ).next_to(phase_axes, RIGHT).shift(LEFT * 5.5 * UNIT)

    time_labels = time_axes.get_axis_labels(
        MathTex(r"t", color=dark_blue),
        MathTex(r"", color=yellow),
    ).shift(1*LEFT*UNIT+0.5*DOWN*UNIT)

    theta_time_dot = always_redraw(
        lambda: Dot(color=theta_color).move_to(
            time_axes.c2p(time.get_value(), theta_func(time.get_value()))
        )
    )

    theta1_time_dot = always_redraw(
        lambda: Dot(color=theta1_color).move_to(
            time_axes.c2p(time.get_value(), theta1_func(time.get_value()))
        )
    )

    theta_time_trace = TracedPath(
        theta_time_dot.get_center,
        stroke_color=theta_color,
        stroke_width=2,
    )

    theta1_time_trace = TracedPath(
        theta1_time_dot.get_center,
        stroke_color=theta1_color,
        stroke_width=2,
    )


    # Legend for the time graph
    legend_theta = VGroup(
        Line(LEFT * 0.3, RIGHT * 0.3, color=theta_color, stroke_width=6),
        MathTex(r"\theta", color=theta_color),
    ).arrange(RIGHT, buff=0.2)

    legend_theta1 = VGroup(
        Line(LEFT * 0.3, RIGHT * 0.3, color=theta1_color, stroke_width=6),
        MathTex(r"\theta'", color=theta1_color),
    ).arrange(RIGHT, buff=0.2)

    legend = VGroup(legend_theta, legend_theta1).arrange(
        DOWN, aligned_edge=LEFT, buff=0.15
    ).next_to(time_axes, UP, buff=0.2)

    legend_group = VGroup(legend)
    legend_group.next_to(time_axes, DOWN).shift(1.5*UNIT*UP + 3.75 *UNIT*RIGHT)
# -------------------------------------------------------------


    theta_label = MathTex(r"\theta", color=dark_blue)
    theta_dot_label = MathTex(r"\theta'", color=dark_blue)

    phase_labels = VGroup(
        theta_label.next_to(phase_axes, RIGHT, buff=0.1).shift(1.5 * UNIT * LEFT),
        theta_dot_label.next_to(phase_axes, UP, buff=0.1),
    )


    v_scale = 0.6  # smaller = wider-looking ellipse

    phase_point = always_redraw(
        lambda: Dot(color=yellow).move_to(
            phase_axes.c2p(theta_func(time.get_value()),
                        theta_dot_func(time.get_value()) * v_scale)
        )
    )

    phase_trace = TracedPath(
        phase_point.get_center,
        stroke_color=yellow,
        stroke_width=2,
    )







    self.wait(1)
    # add pendulum
    self.play(
        Create(phase_axes, lag_ratio=0, run_time=1),
        Write(phase_labels),
        Create(time_axes, lag_ratio=0, run_time=1),
        Write(time_labels),
        FadeIn(legend_group),
    )

    self.wait(1)

    self.add(
        phase_trace,
        phase_point,
        theta_time_trace,
        theta1_time_trace,
        theta_time_dot,
        theta1_time_dot,
    )
    self.play(time.animate.set_value(5 * T), rate_func=linear, run_time=5 * T)
    # self.remove(phase_point, phase_trace, theta_time_trace, theta1_time_trace, theta_time_dot, theta1_time_dot)
    self.play(
        FadeOut(phase_axes),
        FadeOut(phase_labels),
        FadeOut(phase_point),
        FadeOut(phase_trace),
        FadeOut(theta_time_trace),
        FadeOut(theta1_time_trace),
        FadeOut(theta_time_dot),
        FadeOut(theta1_time_dot),
        FadeOut(time_axes),
        FadeOut(time_labels),
        FadeOut(legend_group)
    )
