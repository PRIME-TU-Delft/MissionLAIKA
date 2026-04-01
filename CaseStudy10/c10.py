from manim import *
import pendulum_graph_no_fric
import pendulum_graph
import pendulum_init
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

        # pendulum_init.pendulum_init(self)
        # pendulum_graph.pendulum_graph(self)
        pendulum_graph_no_fric.pendulum_graph_no_fric(self)
