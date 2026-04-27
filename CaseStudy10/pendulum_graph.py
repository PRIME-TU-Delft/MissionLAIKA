from manim import *


def pendulum_graph(scene):
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

    # def theta_func(t):
    #     return theta_max * np.exp(-b * t / 2) * np.sin(wd * t)

    # def theta_dot_func(t):
    #     return (
    #         theta_max
    #         * np.exp(-b * t / 2)
    #         * (wd * np.cos(wd * t) - (b / 2) * np.sin(wd * t))
    #     )

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
                theta_func(time.get_value()),
                theta_dot_func(time.get_value()) * v_scale,
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
        Write(line_vertical),
        Write(line),
        FadeIn(ball),
        Create(phase_axes, lag_ratio=0, run_time=1),
        Write(phase_labels),
    )
    self.wait(1)

    prep_theta = ValueTracker(0)

    theta.clear_updaters()
    theta.add_updater(lambda m: m.set_value(prep_theta.get_value()))

    self.play(
        prep_theta.animate.set_value(theta_max),
        run_time=1.2,
        rate_func=smooth,
    )

    time.set_value(0)
    theta.clear_updaters()
    theta.add_updater(lambda m: m.set_value(theta_func(time.get_value())))

    self.add(phase_trace, phase_point)
    self.play(time.animate.set_value(8 * T), rate_func=linear, run_time=8 * T)

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
    )