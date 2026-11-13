from manim import *
# import pendulum_graph_no_fric
# import pendulum_graph
# import pendulum_init
# import pendulum_formula
# import pendulum_double_pane
import ex_animation_pendulum
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


        ex_animation_pendulum.pendulum_graph(self)
  
