import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Lecture10Scene(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

        grid = (
            NumberPlane(
                background_line_style={
                    "stroke_color": dark_blue,
                    "stroke_width": 1,
                    "stroke_opacity": 0.15,
                },
                axis_config={
                    "stroke_color": dark_blue,  # axes color
                    "stroke_width": 2,  # thicker lines
                },
                x_range=(-36, 36, 1),
                y_range=(-18, 18, 1),
            )
            .scale(UNIT)
            .set_z_index(-2)
        )
        self.play(FadeIn(grid))
        self.wait(1)

        rectangle = (
            Rectangle(
                color=ManimColor("#FFFFFF"),
                height=12.0,
                width=7 * UNIT,
                stroke_color=dark_blue,
                fill_color=ManimColor("#FFFFFF"),
                fill_opacity=1,
            )
            .shift((0.5 * config.frame_width + 1.5) * RIGHT)
            .set_z_index(-1)
        )
        dotted_rect = DashedVMobject(rectangle, num_dashes=100)
        rectangle.set_stroke_color(ManimColor("#FFFFFF"))

        # starting at "Let's go into 2d"
        square = (
            Square(side_length=2 * UNIT, color=red, stroke_color=red, fill_color=red)
            .move_to(grid.get_center(), DL)
            .set_z_index(-2)
        )
        self.play(
            DrawBorderThenFill(square),
            self.camera.frame.animate.shift(5 * UNIT * RIGHT + 2 * UNIT * UP),
            FadeIn(rectangle),
            FadeIn(dotted_rect),
        )
        self.wait(1)

        rect_left = rectangle.get_left()[0]
        rect_right = rectangle.get_right()[0]

        frame_left = self.camera.frame.get_left()[0]
        frame_right = self.camera.frame.get_right()[0]

        visible_left = max(rect_left, frame_left)
        visible_right = min(rect_right, frame_right)

        center_x = (visible_left + visible_right) / 2
        center_of_rectangle = center_x * RIGHT + 2 * UNIT * UP

        eq00 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq00.shift(center_of_rectangle)

        eq0 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} \cos\frac{\pi}{4} & -\sin\frac{\pi}{4} \\ \sin\frac{\pi}{4} & \cos\frac{\pi}{4} \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq0.shift(center_of_rectangle)

        grid0 = (
            NumberPlane(
                background_line_style={
                    "stroke_color": dark_blue,
                    "stroke_width": 1,
                    "stroke_opacity": 0.15,
                },
                axis_config={
                    "stroke_color": red,  # axes color
                    "stroke_width": 2,  # thicker lines
                },
                x_range=(-36, 36, 1),
                y_range=(-18, 18, 1),
            )
            .scale(UNIT)
            .set_z_index(-2)
        )
        self.play(Write(eq00))
        self.wait(1)

        self.play(
            ReplacementTransform(eq00[:5], eq0[:5]),
            ShrinkToCenter(eq00[5:-1]),
            GrowFromCenter(eq0[5:-1]),
            ReplacementTransform(eq00[-1], eq0[-1]),
            Rotate(square, 45 * DEGREES, about_point=grid.get_center()),
            Rotate(grid0, 45 * DEGREES, about_point=grid.get_center()),
        )
        self.wait(1)
        self.play(
            FadeOut(grid0),
        )
        self.wait(1)

        eq00 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq00.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq0[:5], eq00[:5]),
            ShrinkToCenter(eq0[5:-1]),
            GrowFromCenter(eq00[5:-1]),
            ReplacementTransform(eq0[-1], eq00[-1]),
            Rotate(square, -45 * DEGREES, about_point=grid.get_center()),
        )
        self.wait(1)

        eq1 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq1.shift(center_of_rectangle)
        grid1 = (
            NumberPlane(
                background_line_style={
                    "stroke_color": dark_blue,
                    "stroke_width": 1,
                    "stroke_opacity": 0.15,
                },
                axis_config={
                    "stroke_color": red,  # axes color
                    "stroke_width": 2,  # thicker lines
                },
                x_range=(-36, 36, 1),
                y_range=(-18, 18, 1),
            )
            .scale(UNIT)
            .set_z_index(-2)
        )

        square.save_state()
        grid1.save_state()

        self.play(
            ReplacementTransform(eq00[:5], eq1[:5]),
            ShrinkToCenter(eq00[5:-1]),
            GrowFromCenter(eq1[5:-1]),
            ReplacementTransform(eq00[-1], eq1[-1]),
            ApplyMatrix(np.array([[1, 2], [0, 1]]), square),
            ApplyMatrix(np.array([[1, 2], [0, 1]]), grid1),
        )
        self.wait(1)
        self.play(FadeOut(grid1))
        self.wait(1)

        eq00 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq00.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq1[:5], eq00[:5]),
            ShrinkToCenter(eq1[5:-1]),
            GrowFromCenter(eq00[5:-1]),
            ReplacementTransform(eq1[-1], eq00[-1]),
            square.animate.restore(),
        )
        self.wait(1)
        grid1.restore()

        vec0 = Line(start=square.get_corner(DL), end=square.get_corner(UL), color=blue)
        vec0.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec1 = Line(start=square.get_corner(UL), end=square.get_corner(UR), color=blue)
        vec1.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec2 = Line(start=square.get_corner(DR), end=square.get_corner(UR), color=blue)
        vec2.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec3 = Line(start=square.get_corner(DL), end=square.get_corner(DR), color=blue)
        vec3.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        self.play(
            LaggedStart(
                Write(vec0), Write(vec1), Write(vec2), Write(vec3), lag_ratio=0.5
            )
        )
        self.wait(1)

        vec4_label = MathTex(
            r"\begin{bmatrix} 0 \\ 2  \end{bmatrix}", color=blue, font_size=40
        )[0]
        vec4_label.move_to(vec0.get_center() + LEFT)
        vec5_label = MathTex(
            r"\begin{bmatrix} 2 \\ 0  \end{bmatrix}", color=blue, font_size=40
        )[0]
        vec5_label.move_to(vec3.get_center() + DOWN)

        self.play(LaggedStart(Write(vec4_label), Write(vec5_label), lag_ratio=0.5))
        self.wait(1)

        eq2 = MathTex(
            r"\begin{bmatrix} 0 & 2 \\ 2 & 0 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq2.shift(2 * UNIT * UP + 11.5 * UNIT * RIGHT)

        square.save_state()
        self.remove(eq1)

        # self.play(Write(eq3[:len(eq1)]), ReplacementTransform(eq2, eq3[len(eq1):]))

        eq1 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq1.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq00[:5], eq1[:5]),
            ShrinkToCenter(eq00[5:-1]),
            GrowFromCenter(eq1[5:-1]),
            ReplacementTransform(eq00[-1], eq1[-1]),
            ApplyMatrix(np.array([[1, 2], [0, 1]]), square),
            ApplyMatrix(np.array([[1, 2], [0, 1]]), grid1),
        )
        self.wait(1)

        eq3 = MathTex(
            r"\begin{bmatrix} 1 & 2 \\ 0 & 1 \end{bmatrix}"
            r"\begin{bmatrix} 0 & 2 \\ 2 & 0 \end{bmatrix}="
            r"\begin{bmatrix} 4 & 2 \\ 2 & 0 \end{bmatrix}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq3.shift(center_of_rectangle)
        eq3[7:11].set_color(blue)
        eq3[14:18].set_color(red)

        self.play(Write(eq3), eq1.animate.shift(3 * UP))
        self.wait(1)

        vec8 = Line(
            start=ORIGIN, end=2 * UNIT * UP + 4 * UNIT * RIGHT, color=red
        ).set_z_index(-2)
        vec8.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec9 = Line(
            start=2 * UNIT * UP + 4 * UNIT * RIGHT,
            end=2 * UNIT * UP + 6 * UNIT * RIGHT,
            color=red,
        ).set_z_index(-2)
        vec9.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec10 = Line(
            start=2 * UNIT * RIGHT, end=2 * UNIT * UP + 6 * UNIT * RIGHT, color=red
        ).set_z_index(-2)
        vec10.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        vec11 = Line(start=ORIGIN, end=2 * UNIT * RIGHT, color=red).set_z_index(-2)
        vec11.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)

        vec8_label = MathTex(
            r"\begin{bmatrix} 4 \\ 2  \end{bmatrix}", color=red, font_size=40
        )[0]
        vec8_label.move_to(vec8.get_center() + 0.5 * LEFT + UP)
        vec11_label = MathTex(
            r"\begin{bmatrix} 2 \\ 0  \end{bmatrix}", color=red, font_size=40
        )[0]
        vec11_label.move_to(vec11.get_center() + DOWN)

        self.play(
            ReplacementTransform(vec0.copy(), vec8),
            ReplacementTransform(vec1.copy(), vec9),
            ReplacementTransform(vec2.copy(), vec10),
            ReplacementTransform(vec3.copy(), vec11),
            ReplacementTransform(vec4_label.copy(), vec8_label),
            vec4_label.animate.set_opacity(0.3),
            vec0.animate.set_opacity(0.3),
            vec1.animate.set_opacity(0.3),
            vec2.animate.set_opacity(0.3),
            vec3.animate.set_opacity(0.3),
            ReplacementTransform(vec5_label, vec11_label),
        )
        self.wait(1)

        self.play(ShrinkToCenter(eq3))
        self.wait(1)

        self.play(Wiggle(vec8_label))
        self.wait()

        eq5 = MathTex(
            r"\|\mathbf{a}\|=\sqrt{\mathbf{a} \cdot \mathbf{a}}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq5.shift(center_of_rectangle)
        self.play(Write(eq5))
        self.wait(1)

        eq5b = MathTex(
            r"\left\|\begin{bmatrix} 4 \\ 2 \end{bmatrix}\right\|=\sqrt{\begin{bmatrix} 4 \\ 2 \end{bmatrix} \cdot \begin{bmatrix} 4 \\ 2 \end{bmatrix}}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq5b.shift(center_of_rectangle)

        self.play(
            LaggedStart(
                ReplacementTransform(eq5[0], eq5b[0:4]),
                ShrinkToCenter(eq5[1]),
                ReplacementTransform(vec8_label.copy(), eq5b[4:8]),
                ReplacementTransform(eq5[2], eq5b[8:12]),
                ReplacementTransform(eq5[3], eq5b[12]),
                ReplacementTransform(eq5[4:6], eq5b[13:15]),
                ReplacementTransform(eq5[6], eq5b[15:19]),
                ReplacementTransform(eq5[7], eq5b[19]),
                ReplacementTransform(eq5[8], eq5b[20:]),
                lag_ratio=0.25,
            )
        )
        self.wait(1)

        eq5c = MathTex(
            r"\left\|\begin{bmatrix} 4 \\ 2  \end{bmatrix}\right\|=\sqrt{20}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq5c.shift(center_of_rectangle)
        self.play(
            ReplacementTransform(eq5b[:13], eq5c[:13]),
            ReplacementTransform(eq5b[13:15], eq5c[13:15]),
            ReplacementTransform(eq5b[15:], eq5c[15:]),
        )
        self.wait(1)
        self.play(FadeOut(eq5c))
        self.wait()

        eq6 = MathTex(
            r"\mathbf{a} \cdot \mathbf{b} = \|\mathbf{a}\| \|\mathbf{b}\| \cos\theta",
            color=dark_blue,
            font_size=40,
        )[0]
        eq6.shift(center_of_rectangle)
        self.play(Write(eq6))
        self.wait(1)

        eq6b = MathTex(
            r"\begin{bmatrix} 4 \\ 2  \end{bmatrix} \cdot \begin{bmatrix} 2 \\ 0  \end{bmatrix} = 2 \sqrt{20}  \cos\theta",
            color=dark_blue,
            font_size=40,
        )[0]
        eq6b.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq6[0], eq6b[0:4]),
            ReplacementTransform(eq6[1], eq6b[4]),
            ReplacementTransform(eq6[2], eq6b[5:9]),
            ReplacementTransform(eq6[3], eq6b[9]),
            ReplacementTransform(eq6[4:7], eq6b[11:15]),
            ReplacementTransform(eq6[7:10], eq6b[10]),
            ReplacementTransform(eq6[10:], eq6b[15:]),
        )
        self.wait(1)

        eq6c = MathTex(
            r"\cos\theta = \frac{8}{2 \sqrt{20}}  ", color=dark_blue, font_size=40
        )[0]
        eq6c.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq6b[15:], eq6c[0:4]),
            ReplacementTransform(eq6b[9], eq6c[4]),
            ReplacementTransform(eq6b[10:15], eq6c[7:]),
            GrowFromCenter(eq6c[6]),
            ReplacementTransform(eq6b[:9], eq6c[5]),
        )
        self.wait(1)

        self.play(
            FadeOut(
                VGroup(
                    eq6c,
                    vec8_label,
                    vec11_label,
                    vec4_label,
                    vec0,
                    vec1,
                    vec2,
                    vec3,
                    vec8,
                    vec9,
                    vec10,
                    vec11,
                )
            ),
            eq1.animate.shift(3 * DOWN),
        )
        self.wait()

        tri1 = Polygon(
            [0, 0, 0],
            [2 * UNIT, 0, 0],
            [2 * UNIT, 1 * UNIT, 0],
            color=red,
            fill_opacity=0.3,
            stroke_width=0,
        )
        quad = Polygon(
            [2 * UNIT, 0, 0],
            [2 * UNIT, 1 * UNIT, 0],
            [4 * UNIT, 2 * UNIT, 0],
            [4 * UNIT, 1 * UNIT, 0],
            color=red,
            fill_opacity=0.3,
            stroke_width=0,
        )
        tri2 = Polygon(
            [4 * UNIT, 1 * UNIT, 0],
            [4 * UNIT, 2 * UNIT, 0],
            [6 * UNIT, 2 * UNIT, 0],
            color=red,
            fill_opacity=0.3,
            stroke_width=0,
        )

        self.play(FadeIn(tri1), FadeIn(quad), FadeIn(tri2))
        self.wait(1)
        self.play(
            LaggedStart(
                quad.animate.shift(2 * UNIT * LEFT),
                tri2.animate.shift(4 * UNIT * LEFT),
                lag_ratio=0.6,
            )
        )

        self.play(FadeOut(grid1))
        self.wait(1)

        eq00 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 1 & 0 \\ 0 & 1 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0].set_z_index(2)
        eq00.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq1[:5], eq00[:5]),
            ShrinkToCenter(eq1[5:-1]),
            GrowFromCenter(eq00[5:-1]),
            ReplacementTransform(eq1[-1], eq00[-1]),
            square.animate.restore(),
        )
        self.wait(1)

        grid1.restore()

        eq7 = MathTex(
            r"T(\mathbf{v}) = \begin{bmatrix} 2 & 1 \\ 0 & 2 \end{bmatrix} \mathbf{v}",
            color=dark_blue,
            font_size=40,
        )[0]
        eq7.shift(center_of_rectangle)

        self.play(
            ReplacementTransform(eq00[:5], eq7[:5]),
            ShrinkToCenter(eq00[5:-1]),
            GrowFromCenter(eq7[5:-1]),
            ReplacementTransform(eq00[-1], eq7[-1]),
            ApplyMatrix(np.array([[2, 1], [0, 2]]), square),
            ApplyMatrix(np.array([[2, 1], [0, 2]]), grid1),
        )
        self.wait(1)
