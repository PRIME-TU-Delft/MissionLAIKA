from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        dark_blue = ManimColor("#0C2340")  # VERSION 2    DEFAULT
        red = ManimColor("#E03C31")  # E03C31       E03C31
        yellow = ManimColor("#cc9316")  # 6CC24A       cc9316
        blue = ManimColor("#0076C2")  # 0076C2       0076C2

        UNIT = 3 / 4

        # Wheel
        outer_circle = Circle(stroke_color=dark_blue, radius=1.7)
        inner_circle = Circle(stroke_color=dark_blue, radius=0.9)
        line1 = Line(color=dark_blue, start=[0.4, 1.65, 0], end=[0.4, 3.15, 0])
        line2 = Line(color=dark_blue, start=[-0.4, 1.65, 0], end=[-0.4, 3.07, 0])
        wheel_text = Tex("wheel", font_size=42, color=dark_blue)

        wheel = Group(outer_circle, inner_circle, line1, line2, wheel_text)
        wheel.to_edge(2 * DOWN)
        # Ground
        ground = Line(color=dark_blue, start=[-15, 0, 0], end=[15, 0, 0])
        ground.to_edge(2 * DOWN)

        # Plane
        plane = Circle(stroke_color=dark_blue, radius=3)
        plane.scale([5.1, 1, 1])
        plane.move_to(Point([-4.1, 4.7, 0]))
        plane_text = Tex("airplane", font_size=42, color=dark_blue)
        plane_text.shift(2.7 * UP)

        self.add(outer_circle, inner_circle, plane, line1, line2, ground)

        # Draw the ground lines
        ground_line = Line(color=dark_blue, start=[-15, -4, 0], end=[-14, -3, 0])
        ground_lines = []
        for i in range(30):
            ground_line_c = ground_line.copy().shift(i * RIGHT)
            ground_lines.append(ground_line_c)

        self.add(*ground_lines)

        self.wait(1)
        # grid = NumberPlane(
        #     background_line_style={
        #         "stroke_color": dark_blue,
        #         "stroke_width": 1,
        #         "stroke_opacity": 0.15,
        #     },
        #     x_range=(0, 72, 1),
        #     y_range=(0, 36, 1),
        # ).scale(UNIT)

        # self.play(Write(grid))

        # annotate plane and wheel
        self.play(Write(plane_text), Write(wheel_text))

        m1 = Square(2, color=red)
        m2 = m1.copy()
        m1.to_edge(4.5 * DOWN)
        m2.to_edge(UP)

        m2_text = MathTex("m_2", font_size=60, color=red).move_to(Point([0, 2.5, 0]))
        m1_text = MathTex("m_1", font_size=60, color=red).move_to(Point([0, -0.8, 0]))

        self.wait(2)

        # transform into mass spring model
        # airplane
        # self.play(
        #     LaggedStart(
        #         Transform(mobject=plane, target_mobject=m2, path_arc=0),
        #         ShrinkToCenter(line1),
        #         ShrinkToCenter(line2),
        #         lag_ratio=0.4,
        #         run_time=1.2,
        #     )
        # )
        # # wheel
        # self.play(
        #     Transform(mobject=outer_circle, target_mobject=m1, path_arc=0),
        #     Transform(mobject=plane, target_mobject=m2, path_arc=0),
        #     ShrinkToCenter(inner_circle),
        #     wheel_text.animate.move_to(Point([0, -0.8, 0])),
        #     plane_text.animate.shift(0.2 * DOWN),
        #     run_time=1.2,
        # )

        # # change the annotations
        # self.wait(2)
        # self.play(Transform(wheel_text, m1_text))
        # self.wait(0.5)
        # self.play(Transform(plane_text, m2_text))
        # self.wait(2)

        # # springs
        # spring2 = SVGMobject(
        #     "../assets/Spring.svg", stroke_color=blue, stroke_width=3
        # ).scale(0.63)

        # spring = spring2.copy()
        # spring2.shift(UP * 0.88)
        # spring.shift(DOWN * 2.37)
        # self.play(Write(spring), Write(spring2))
        # self.wait(1)

        # # show k
        # k2_text = MathTex("k_2", font_size=60, color=blue).move_to(Point([1.5, 0.9, 0]))
        # k1_text = MathTex("k_1", font_size=60, color=blue).move_to(
        #     Point([1.5, -2.3, 0])
        # )

        # self.play(GrowFromPoint(k1_text, Point([0, -2.3, 0])))
        # self.wait(1)
        # self.play(GrowFromPoint(k2_text, Point([0, 0.9, 0])))
        # self.wait(1)

        # m2group_1 = Group(plane, plane_text)
        # self.wait()
        # self.play(
        #     k2_text.animate.shift(0.2 * DOWN),
        #     m2group_1.animate.shift(0.3 * DOWN),
        #     spring2.animate.stretch(0.75, dim=1, about_edge=DOWN),
        # )
        # self.play(
        #     k2_text.animate.shift(0.6 * UP),
        #     m2group_1.animate.shift(0.88 * UP),
        #     spring2.animate.stretch(23 / 12, dim=1, about_edge=DOWN),
        # )
        # self.play(
        #     k2_text.animate.shift(0.4 * DOWN),
        #     m2group_1.animate.shift(0.58 * DOWN),
        #     spring2.animate.stretch(16 / 23, dim=1, about_edge=DOWN),
        # )

        # self.wait()

        # damping = SVGMobject(
        #     "../assets/damping.svg", stroke_color=dark_blue, stroke_width=3
        # ).scale(0.63)
        # damping.shift(0.88 * UP + 0.5 * LEFT)
        # self.play(
        #     LaggedStart(
        #         spring2.animate.shift(RIGHT * 0.5), Write(damping), lag_ratio=0.9
        #     )
        # )
        # self.wait(1)
        # gamma = MathTex("\gamma", font_size=60, color=dark_blue).move_to(
        #     damping.get_left() + LEFT
        # )
        # self.play(GrowFromPoint(gamma, damping.get_center()))
        # self.wait(1)

        # x2_text = MathTex("x_2", font_size=60, color=yellow).move_to(
        #     Point(m2.get_left() + [-2, 0, 0])
        # )
        # x1_text = MathTex("x_1", font_size=60, color=yellow).move_to(
        #     Point(m1.get_left() + [-2, 0, 0])
        # )
        # # self.play(Write(x1_text))
        # # self.wait(0.5)
        # # self.play(Write(x2_text))
        # self.wait(1)

        # # move arrows to the side with dashed lines
        # dashed_1 = DashedLine(
        #     m1.get_left(),
        #     m1.get_left() + 1.5 * LEFT,
        #     dashed_ratio=0.6,
        #     dash_length=0.2,
        #     color=yellow,
        # )
        # dashed_2 = DashedLine(
        #     m2.get_left(),
        #     m2.get_left() + 1.5 * LEFT,
        #     dashed_ratio=0.6,
        #     dash_length=0.2,
        #     color=yellow,
        # )
        # xs = Group(x1_text, x2_text)
        # self.play(Write(dashed_1), Write(dashed_2))

        # x_axis = Arrow(
        #     start=5 * LEFT * UNIT + 3.25 * DOWN,
        #     end=5 * LEFT * UNIT + 4 * UP,
        #     color=dark_blue,
        #     stroke_width=4,
        # )
        # x_axis_label = MathTex("x", font_size=60, color=dark_blue).move_to(
        #     x_axis.get_top() + 0.5 * LEFT + 0.5 * DOWN
        # )
        # self.play(GrowArrow(x_axis))
        # self.play(Write(x_axis_label))
        # self.wait(1)

        # point = m2.get_left() + 1.5 * LEFT
        # point2 = m1.get_left() + 1.5 * LEFT
        # arrow1 = Line(point2, point2 + 0.1 * DOWN, color=yellow)
        # arrow2 = Line(start=point, end=point + 0.1 * DOWN, color=yellow)

        # # push the m2 mass down
        # m2group = Group(dashed_2, plane, plane_text)
        # self.wait()
        # self.play(Write(x2_text))
        # self.add(arrow2)
        # self.play(
        #     gamma.animate.shift(0.4 * DOWN),
        #     k2_text.animate.shift(0.4 * DOWN),
        #     x2_text.animate.shift(0.4 * DOWN),
        #     m2group.animate.shift(0.8 * DOWN),
        #     arrow2.animate.stretch(8, 1, about_edge=UP),
        #     spring2.animate.stretch(0.34, dim=1, about_edge=DOWN),
        #     damping.animate.stretch(0.34, dim=1, about_edge=DOWN),
        # )

        # # push the m2 and m1 masses down
        # m2m1group = Group(
        #     dashed_2,
        #     plane,
        #     plane_text,
        #     outer_circle,
        #     dashed_1,
        #     spring2,
        #     damping,
        #     wheel_text,
        # )
        # self.wait()
        # self.play(Write(x1_text))
        # self.add(arrow1)
        # self.play(
        #     gamma.animate.shift(0.8 * DOWN),
        #     k2_text.animate.shift(0.8 * DOWN),
        #     k1_text.animate.shift(0.2 * DOWN),
        #     x2_text.animate.shift(0.4 * DOWN),
        #     x1_text.animate.shift(0.4 * DOWN),
        #     m2m1group.animate.shift(0.8 * DOWN),
        #     arrow2.animate.stretch(2, 1, about_edge=UP),
        #     arrow1.animate.stretch(8, 1, about_edge=UP),
        #     spring.animate.stretch(0.34, dim=1, about_edge=DOWN),
        # )

        # # extend m2 mass
        # self.play(
        #     gamma.animate.shift(0.4 * UP),
        #     k2_text.animate.shift(0.4 * UP),
        #     x2_text.animate.shift(0.4 * UP),
        #     m2group.animate.shift(0.8 * UP),
        #     arrow2.animate.stretch(0.5, 1, about_edge=UP),
        #     spring2.animate.stretch(1 / 0.34, dim=1, about_edge=DOWN),
        #     damping.animate.stretch(1 / 0.34, dim=1, about_edge=DOWN),
        # )

        # # extend both masses
        # self.play(
        #     k2_text.animate.shift(0.8 * UP),
        #     gamma.animate.shift(0.8 * UP),
        #     k1_text.animate.shift(0.2 * UP),
        #     x2_text.animate.shift(0.4 * UP),
        #     x1_text.animate.shift(0.4 * UP),
        #     m2m1group.animate.shift(0.8 * UP),
        #     arrow2.animate.stretch(0.01, 1, about_edge=UP),
        #     arrow1.animate.stretch(0.01, 1, about_edge=UP),
        #     spring.animate.stretch(1 / 0.34, dim=1, about_edge=DOWN),
        # )
