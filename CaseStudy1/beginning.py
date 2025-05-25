from manim import *

config.background_color = ManimColor('#00FF00')
class Plane(MovingCameraScene):
    def construct(self):
        dark_blue = ManimColor('#FFFFFF')

        # Wheel
        outer_circle = Circle(stroke_color=dark_blue, radius=1.7)
        inner_circle = Circle(stroke_color=dark_blue, radius=0.9)
        line1 = Line(color=dark_blue, start=[0.4, 1.65, 0], end=[0.4,3.15,0])
        line2 = Line(color=dark_blue, start=[-0.4, 1.65, 0], end=[-0.4,3.07,0])
        wheel_text = Tex("wheel", font_size=60, color = dark_blue)

        wheel = Group(outer_circle, inner_circle, line1, line2,wheel_text)
        wheel.to_edge(2*DOWN)

        #Ground
        ground = Line(color=dark_blue,start=[-15,0,0], end=[15,0,0])
        ground.to_edge(2*DOWN)

        # Plane
        plane = Circle(stroke_color=dark_blue, radius=3)
        plane.scale([5.1,1,1])
        plane.move_to(Point([-4.1,4.7,0]))
        plane_text = Tex("airplane", font_size=70, color = dark_blue)
        plane_text.to_edge(UP)

        #Draw the initial scene
        self.play(Create(outer_circle), Create(inner_circle), Create(plane),Create(line1), Create(line2), Create(ground))

        #Draw the ground lines
        ground_line = Line(color=dark_blue,start=[-15,-4,0], end=[-14,-3,0])
        ground_lines = []
        for i in range(30):
            ground_line_c = ground_line.copy().shift(i * RIGHT)
            ground_lines.append(Create(ground_line_c))

        self.play(LaggedStart(*ground_lines), lag_ratio=0.5)
