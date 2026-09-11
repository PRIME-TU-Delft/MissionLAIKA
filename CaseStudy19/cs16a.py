from manim import *
from primescene import *
config.background_color = ManimColor("#FFFFFF")


class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")
        green = ManimColor('#009B77')

        grid = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 2  # thicker lines
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        airplane_svg = SVGMobject("../assets/AirplaneFront.svg")
        airplane_svg.set_color(dark_blue).set_stroke(color=dark_blue, width=12).scale(2).shift(5.5*UNIT*LEFT + UP)
        self.add(airplane_svg)

        self.camera.frame.shift(5.5*UNIT*LEFT+0.05*UP).scale(1.5)
        self.wait()

        self.play(Write(grid))
        self.wait()

        self.play(self.camera.frame.animate.scale(1/1.5).shift(5.5*UNIT*RIGHT+0.05*DOWN))
        self.wait()

        airplane_half = SVGMobject("../assets/AirplaneFrontHalf.svg")
        airplane_half.set_color(dark_blue).set_stroke(color=dark_blue, width=12).scale(2).shift(UP).align_to(airplane_svg, RIGHT)
        self.play(FadeIn(airplane_half), FadeOut(airplane_svg))
        self.wait()

        beam_width = 11*UNIT
        beam_height = 0.5*UNIT

        beam = Rectangle(
            width=beam_width,
            height=beam_height,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_opacity=0.0,
        )

        wall = Line(
            start=ORIGIN,
            end=3*UNIT*UP,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_opacity=0.0,
        ).next_to(beam, LEFT, buff=0)

        hatch_lines = []
        for k in range(8):
            hatch_lines.append(
                Line(
                    start=(wall.get_right()+UNIT*LEFT) + (-1.5*UNIT + (3*UNIT/8) * k) * UP,
                    end=wall.get_right() + (-1.5*UNIT + (3*UNIT/8) * (k+1)) * UP,
                    color=dark_blue,
                    stroke_width=3,
                )
            )


        VGroup(wall, *hatch_lines, beam).move_to(ORIGIN)

        self.wait()

        list = airplane_half.submobjects

        self.play(LaggedStart(
            ReplacementTransform(list[4], beam),
            ReplacementTransform(list[0], wall),
            *(ShrinkToCenter(list[i]) for i in (1, 2, 3)),
            *(Create(hatch_lines[i]) for i in range(8)),
            lag_ratio=0.2)
        )

        eq0 = MathTex(
            r"M \mathbf{\ddot u} + K\mathbf{u}= \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq0.shift(eq0[0].get_bottom()[1] * DOWN + 3*UNIT*UP)
        self.play(Write(eq0))
        self.wait()

        eq1 = MathTex(
            r"mx'' + kx = 0",
            color=dark_blue, font_size=32)[0]
        eq1.shift(eq1[0].get_bottom()[1] * DOWN + 4 * UNIT * UP+6*UNIT*RIGHT)
        eq1[0].set_color(red)
        eq1[1].set_color(yellow)
        eq1[5].set_color(blue)
        eq1[6].set_color(yellow)

        cloud = SVGMobject("../assets/cloud.svg")
        cloud.set_color(dark_blue).set_stroke(color=dark_blue, width=3).shift(6*UNIT*RIGHT + 4*UNIT*UP)
        cloud_circle1 = Circle(stroke_color=dark_blue, stroke_width=3).scale(0.1 * UNIT).stretch(1.2, 0).shift(
            2.75 * UNIT * RIGHT + 3.25 * UNIT * UP)
        cloud_circle2 = Circle(stroke_color=dark_blue, stroke_width=3).scale(0.2 * UNIT).stretch(1.2, 0).shift(
            3.5 * UNIT * RIGHT + 3.5 * UNIT * UP)

        self.play(LaggedStart(FadeIn(cloud_circle1), FadeIn(cloud_circle2), FadeIn(cloud), FadeIn(eq1), lag_ratio=0.2))
        self.wait()
        self.play(LaggedStart( FadeOut(cloud_circle1), FadeOut(cloud_circle2), FadeOut(cloud), FadeOut(eq1), lag_ratio=0.2))
        self.wait()
        self.play(eq0.animate.shift(7*UNIT*RIGHT+UNIT*UP))
        self.wait()

        p1 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.5 * beam_width * RIGHT)
        p2 = Dot(color=blue, radius=0.085).move_to(beam.get_right())

        self.play(FadeIn(p1, scale=0.5), FadeIn(p2, scale=0.5))
        self.wait(1.2)

        def dof_glyphs(anchor: Mobject, idx: str) -> VGroup:
            base = anchor.get_center()

            ax = Arrow(base, base + 0.85 * RIGHT, color=yellow, stroke_width=4, buff=0.0)
            tx = MathTex(fr"u_{idx}", font_size=36, color=yellow).next_to(ax, RIGHT, buff=0.12)

            ay = Arrow(base, base + 0.85 * UP, color=yellow, stroke_width=4, buff=0.0)
            ty = MathTex(fr"v_{idx}", font_size=36, color=yellow).next_to(ay, UP, buff=0.12)

            arc = Arc(radius=0.45, start_angle=0, angle=182 * DEGREES, arc_center=base, color=yellow)
            arc_tip = Arrow(
                arc.point_from_proportion(0.85),
                arc.point_from_proportion(1.0),
                color=yellow,
                stroke_width=4,
                buff=0.0,
                max_tip_length_to_length_ratio=0.8,
            )
            ttheta = MathTex(fr"\theta_{idx}", font_size=36, color=yellow).next_to(arc, LEFT, buff=0.2).shift(0.2*UP)

            return VGroup(ax, tx, ay, ty, arc, arc_tip, ttheta)

        dofs1 = dof_glyphs(p1, "1")
        dofs2 = dof_glyphs(p2, "2")

        self.play(LaggedStart(GrowArrow(dofs1[0]), Write(dofs1[1]), GrowArrow(dofs2[0]), Write(dofs2[1]), lag_ratio=0.5))
        self.play(LaggedStart(GrowArrow(dofs1[2]), Write(dofs1[3]), GrowArrow(dofs2[2]), Write(dofs2[3]), lag_ratio=0.5))
        self.play(LaggedStart(Create(dofs1[4]), Create(dofs2[4]), GrowArrow(dofs1[5]),
                              GrowArrow(dofs2[5]), Write(dofs1[6]), Write(dofs2[6]), lag_ratio=0.35))
        self.wait()

        eq2 = MathTex(
            r"\mathbf{u} =\begin{bmatrix}u_1 & v_1 & \theta_1 & u_2 & v_2 & \theta_2\end{bmatrix}^{T}",
            color=yellow, font_size=48)[0]
        eq2.shift(eq2[0].get_bottom()[1] * DOWN + 3 * UNIT * UP)
        self.play(Write(eq2))
        self.wait()

        self.play(eq0[2].animate.set_color(yellow), eq0[5].animate.set_color(yellow))
        self.wait()

        self.play(LaggedStart(FadeOut(VGroup(wall, *hatch_lines, beam, eq2, dofs1, dofs2, p1, p2)), eq0.animate.shift(7*UNIT*LEFT + 4*UNIT*DOWN), lag_ratio=0.5))
        self.wait()

        eq3 = MathTex(
            r"M^{-1}M \mathbf{\ddot u} + M^{-1}K\mathbf{u}= M^{-1}\mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq3.shift(eq3[0].get_bottom()[1] * DOWN)
        eq3[5].set_color(yellow)
        eq3[11].set_color(yellow)
        self.play(ReplacementTransform(eq0[:4], eq3[3:7]),
                  ReplacementTransform(eq0[4:7], eq3[10:13]),
                  ReplacementTransform(eq0[7:], eq3[16:]),
                  GrowFromCenter(eq3[:3]), GrowFromCenter(eq3[7:10]), GrowFromCenter(eq3[13:16]))
        self.wait()

        eq4 = MathTex(
            r"\mathbf{\ddot u} + M^{-1}K\mathbf{u}= \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq4.shift(eq4[3].get_bottom()[1] * DOWN)
        eq4[1].set_color(yellow)
        eq4[7].set_color(yellow)
        self.play(ReplacementTransform(eq3[4:13], eq4[:9]),
                  ReplacementTransform(eq3[16:], eq4[9:]),
                  ShrinkToCenter(eq3[:4]),
                  ShrinkToCenter(eq3[13:16]))
        self.wait()

        eq5 = MathTex(
            r"A = M^{-1}K",
            color=dark_blue, font_size=48)[0]
        eq5.shift(eq5[0].get_bottom()[1] * DOWN + 2*UNIT*DOWN)

        eq6 = MathTex(
            r"\mathbf{\ddot u} + A\mathbf{u}= \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq6.shift(eq6[1].get_bottom()[1] * DOWN)
        eq6[1].set_color(yellow)
        eq6[4].set_color(yellow)

        self.play(Write(eq5[:2]))
        self.wait()

        self.play(ReplacementTransform(eq4[:3], eq6[:3]),
                  ReplacementTransform(eq4[3:7], eq5[2:]),
                  ReplacementTransform(eq4[7:], eq6[4:]),
                  ReplacementTransform(eq5[0].copy(), eq6[3]))
        self.wait()

        self.play(FadeOut(eq5), eq6.animate.shift(4*UNIT*UP+ 7*UNIT*RIGHT))
        self.wait()

        eq7 = MathTex(
            r"A\mathbf{v}_i = \lambda_i\mathbf{v}_i",
            color=dark_blue, font_size=48)[0]
        eq7.shift(eq7[1].get_bottom()[1] * DOWN)

        self.play(Write(eq7))
        self.wait()

        eq8 = MathTex(
            r"\lambda_i = \omega_i^2",
            color=dark_blue, font_size=48)[0]
        eq8.shift(eq8[0].get_bottom()[1] * DOWN + 2*UNIT*RIGHT)
        self.play(Write(eq8), eq7.animate.shift(2*UNIT*LEFT))
        self.wait()

        self.play(eq8.animate.shift(UNIT*UP), eq7.animate.shift(UNIT*UP))
        self.wait()

        #move that 1 up and write P D and A =PDP
        eq9 = MathTex(
            r"P = \begin{bmatrix} \mathbf{v_1} & \mathbf{v_2} & \dots & \mathbf{v_n} \end{bmatrix}",
            color=dark_blue, font_size=48)[0]
        eq9.shift(eq9[0].get_bottom()[1] * DOWN + 4 * UNIT * LEFT + UNIT * DOWN)

        eq10 = MathTex(
            r"D= \begin{bmatrix} \omega_1^2 & 0 & 0 \\ 0 & \ddots & 0 \\0 & 0 & \omega_n^2   \end{bmatrix}",
            color=dark_blue, font_size=48)[0]
        eq10.shift(eq10[0].get_bottom()[1] * DOWN + 5 * UNIT * RIGHT + UNIT * DOWN)

        eq11 = MathTex(
            r"A = PDP^{-1}",
            color=dark_blue, font_size=48)[0]
        eq11.shift(eq11[0].get_bottom()[1] * DOWN +3 * UNIT * DOWN)

        self.play(Write(eq9))
        self.wait()
        self.play(Write(eq10))
        self.wait()
        self.play(Write(eq11))
        self.wait()

        #======NEW PART
        self.play(self.camera.frame.animate.shift(19 * UNIT * RIGHT))
        self.wait()

        eq20 = MathTex(
            r"M",
            color=dark_blue, font_size=48)[0]
        eq20.shift(eq20[0].get_bottom()[1] * DOWN + 16 * UNIT * RIGHT)

        eq21 = MathTex(
            r"K",
            color=dark_blue, font_size=48)[0]
        eq21.shift(eq21[0].get_bottom()[1] * DOWN + 22 * UNIT * RIGHT)

        eq20a = MathTex(
            r"M=M^T",
            color=dark_blue, font_size=48)[0]
        eq20a.shift(eq20a[0].get_bottom()[1] * DOWN + 16 * UNIT * RIGHT)

        eq21a = MathTex(
            r"K=K^T",
            color=dark_blue, font_size=48)[0]
        eq21a.shift(eq21a[0].get_bottom()[1] * DOWN + 22 * UNIT * RIGHT)

        self.play(LaggedStart(GrowFromCenter(eq20), GrowFromCenter(eq21), lag_ratio=0.5))
        self.wait()

        self.play(LaggedStart(ReplacementTransform(eq20, eq20a[0]),
                              Write(eq20a[1:]),
                              ReplacementTransform(eq21, eq21a[0]),
                              Write(eq21a[1:]), lag_ratio=0.5))
        self.wait()

        eq22 = MathTex(
            r"\left(M^{-1}\right)^T=M^{-1}",
            color=dark_blue, font_size=48)[0]
        eq22.shift(eq22[1].get_bottom()[1] * DOWN + UNIT*UP + 16 * UNIT * RIGHT)

        self.play(GrowFromPoint(eq22, eq20a.get_center()))
        self.wait()

        eq23 = MathTex(
            r"(M^{-1}K)^T\neq M^{-1}K",
            color=dark_blue, font_size=48)[0]
        eq23.shift(eq23[1].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT + UNIT * DOWN)

        self.play(Write(eq23))
        self.wait()

        eq24 = MathTex(
            r"\text{for every } \mathbf{x}\neq{\mathbf{0}},  \mathbf{x}^TM\mathbf{x} > 0",
            color=dark_blue, font_size=48)[0]
        eq24.shift(eq24[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(FadeOut(Group(eq20a, eq21a, eq22, eq23)))
        self.wait()
        self.play(Write(eq24))
        self.wait()

        eq25 = MathTex(
            r"M=\begin{bmatrix} 3 & -1\\-1 & 2\end{bmatrix}",
            color=dark_blue, font_size=48)[0]
        eq25.shift(eq25[0].get_bottom()[1] * DOWN + 24 * UNIT * RIGHT)

        self.play(eq24.animate.shift(5 * UNIT * LEFT), Write(eq25))
        self.wait()

        eq26a = MathTex(
            r"\mathbf{x}^TM\mathbf{x}",
            color=dark_blue, font_size=48)[0]
        eq26a.shift(eq26a[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(Group(eq24, eq25).animate.shift(3 * UNIT * UP), ReplacementTransform(eq24[13:17].copy(), eq26a))
        self.wait()

        eq26b = MathTex(
            r"\begin{bmatrix} x_1 & x_2\end{bmatrix}\begin{bmatrix} 3 & -1\\-1 & 2\end{bmatrix}\begin{bmatrix} x_1 \\ x_2\end{bmatrix}",
            color=dark_blue, font_size=48)[0]
        eq26b.shift(eq26b[1].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(ReplacementTransform(eq26a[:2], eq26b[:6]))
        self.play(ShrinkToCenter(eq26a[2]), ReplacementTransform(eq25[2:].copy(), eq26b[6:6+len(eq25[2:])]), eq26a[3].animate.shift(2*UNIT*RIGHT))
        self.play(ReplacementTransform(eq26a[3], eq26b[6+len(eq25[2:]):]))
        self.wait()

        eq26c = MathTex(
            r"\begin{bmatrix} x_1 & x_2\end{bmatrix}\begin{bmatrix} 3 & -1\\-1 & 2\end{bmatrix}\begin{bmatrix} x_1 \\ x_2\end{bmatrix}=3x_1^2-2x_1x_2+2x_2^2",
            color=dark_blue, font_size=48)[0]
        eq26c.shift(eq26c[1].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(ReplacementTransform(eq26b, eq26c[:len(eq26b)]), Write(eq26c[len(eq26b):]))
        self.wait()

        self.play(FadeOut(Group(eq25, eq24, eq26c[:len(eq26b)+1])))
        self.wait()

        self.play(FadeOut(eq26c))
        self.wait()

        eq27a = MathTex(
            r"\mathbf{x}^TM^{-1}\mathbf{x}",
            color=dark_blue, font_size=48)[0]
        eq27a.shift(eq27a[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27b = MathTex(
            r"\mathbf{x}^TM^{-1}MM^{-1}\mathbf{x}",
            color=dark_blue, font_size=48)[0]
        eq27b.shift(eq27b[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27c = MathTex(
            r"\mathbf{x}^T\left(M^{-1}\right)^TMM^{-1}\mathbf{x}",
            color=dark_blue, font_size=48)[0]
        eq27c.shift(eq27c[0].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27d = MathTex(
            r"\left(M^{-1}\mathbf{x}\right)^TM\left(M^{-1}\mathbf{x}\right)",
            color=dark_blue, font_size=48)[0]
        eq27d.shift(eq27d[1].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27e = MathTex(
            r"\mathbf{y}^TM\mathbf{y}",
            color=dark_blue, font_size=48)[0]
        eq27e.shift(eq27e[2].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        eq27f = MathTex(
            r"\mathbf{y}^TM\mathbf{y}>0",
            color=dark_blue, font_size=48)[0]
        eq27f.shift(eq27f[2].get_bottom()[1] * DOWN + 19 * UNIT * RIGHT)

        self.play(Write(eq27a))
        self.wait()

        self.play(ReplacementTransform(eq27a[:5], eq27b[:5]),
                  ReplacementTransform(eq27a[5], eq27b[9]),
                  GrowFromCenter(eq27b[5:9]),)
        self.wait()

        self.play(ReplacementTransform(eq27b[:2], eq27c[:2]),
                  ReplacementTransform(eq27b[2:5], eq27c[3:6]),
                  ReplacementTransform(eq27b[5:], eq27c[8:]),
                  GrowFromCenter(eq27c[2]),
                  GrowFromCenter(eq27c[6]),
                  GrowFromCenter(eq27c[7]),
                  )
        self.wait()

        self.play(ReplacementTransform(Group(eq27c[1], eq27c[7]), eq27d[6]),
                  ReplacementTransform(eq27c[0], eq27d[4]),
                  ReplacementTransform(eq27c[3:6], eq27d[1:4]),
                  ReplacementTransform(eq27c[2], eq27d[0]),
                  ReplacementTransform(eq27c[6], eq27d[5]),
                  ReplacementTransform(eq27c[8], eq27d[7]),
                  ReplacementTransform(eq27c[9:13], eq27d[9:13]),
                  GrowFromCenter(eq27d[8]),
                  GrowFromCenter(eq27d[13]),
                  )
        self.wait()

        self.play(ReplacementTransform(eq27d[:6], eq27e[0]),
                  ReplacementTransform(eq27d[6], eq27e[1]),
                  ReplacementTransform(eq27d[7], eq27e[2]),
                  ReplacementTransform(eq27d[8:], eq27e[3]),
                  )
        self.wait()

        self.play(ReplacementTransform(eq27e[:4], eq27f[:4]),
                  GrowFromCenter(eq27f[4:]),)
        self.wait()

        self.play(FadeOut(eq27f))
        self.wait()

        self.play(self.camera.frame.animate.shift(19 * UNIT * LEFT))
        self.wait()
        #==============

        eq12 = MathTex(
            r"\mathbf{y} = P^{-1}\mathbf{u}",
            color=dark_blue, font_size=48)[0]
        eq12.shift(eq12[2].get_bottom()[1] * DOWN)
        eq12[5].set_color(yellow)

        self.play(LaggedStart(eq11.animate.shift(7*UNIT*UP+7*UNIT*LEFT), eq10.animate.shift(3*UNIT*DOWN + 1 *UNIT*RIGHT), FadeOut(VGroup(eq7, eq8)), Write(eq12[:2]), ReplacementTransform(eq9[0], eq12[2]), FadeOut(eq9[1:]),  Write(eq12[3:]), lag_ratio=0.5))
        self.wait()

        self.play(eq12.animate.shift(1*UNIT*UP), eq6.animate.shift(5*UNIT*DOWN + 7*UNIT*LEFT))
        self.wait()

        eq13 = MathTex(
            r"P^{-1}\mathbf{\ddot u} + P^{-1}A\mathbf{u} = P^{-1}\mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq13.shift(eq13[0].get_bottom()[1] * DOWN + UNIT*DOWN)
        eq13[10].set_color(yellow)
        eq13[4].set_color(yellow)

        self.play(ReplacementTransform(eq6[:3], eq13[3:6]),
                  ReplacementTransform(eq6[3:6], eq13[9:12]),
                  ReplacementTransform(eq6[6], eq13[15]),
                  GrowFromCenter(eq13[:3]),
                  GrowFromCenter(eq13[6:9]),
                  GrowFromCenter(eq13[12:15]),)
        self.wait()

        eq13b = MathTex(
            r"P^{-1}\mathbf{\ddot u} + P^{-1}A\mathbf{u} = \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq13b.shift(eq13b[0].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq13b[10].set_color(yellow)
        eq13b[4].set_color(yellow)

        self.play(ReplacementTransform(eq13[:12], eq13b[:12]),
                  ReplacementTransform(eq13[15], eq13b[12]),
                  ShrinkToCenter(eq13[12:15]), )
        self.wait()

        eq14 = MathTex(
            r"P^{-1}\mathbf{\ddot u} + P^{-1}PDP^{-1}\mathbf{u} = \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq14.shift(eq14[0].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq14[14].set_color(yellow)
        eq14[4].set_color(yellow)

        self.play(ReplacementTransform(eq13b[:9], eq14[:9]), ReplacementTransform(eq11[2:].copy(), eq14[9:14]),ShrinkToCenter(eq13b[9]), ReplacementTransform(eq13b[10:], eq14[14:]))
        self.wait()

        eq15 = MathTex(
            r"P^{-1}\mathbf{\ddot u} + DP^{-1}\mathbf{u} = \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq15.shift(eq15[0].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq15[10].set_color(yellow)
        eq15[4].set_color(yellow)

        self.play(ReplacementTransform(eq14[:6], eq15[:6]),ShrinkToCenter(eq14[6:10]), ReplacementTransform(eq14[10:], eq15[6:]))
        self.wait()

        self.play(Wiggle(VGroup(eq15[:3], eq15[4])), Wiggle(eq15[7:11]), Wiggle(eq12[2:]))
        self.wait()

        eq16 = MathTex(
            r"\mathbf{\ddot y} + D\mathbf{y} = \mathbf{0}",
            color=dark_blue, font_size=48)[0]
        eq16.shift(eq16[3].get_bottom()[1] * DOWN + UNIT * DOWN)

        self.play(ReplacementTransform(VGroup(*eq15[:3], eq15[4]), eq16[1]), ReplacementTransform(eq15[3], eq16[0]),
                  ReplacementTransform(eq15[5:7], eq16[2:4]), ReplacementTransform(eq15[7:11], eq16[4]), ReplacementTransform(eq15[11:], eq16[5:]) )
        self.wait()

        self.play(eq12.animate.shift(3*UNIT*UP + 7 * UNIT* RIGHT), eq16.animate.shift(1*UNIT*UP))
        self.wait()

        self.play(LaggedStart(Indicate(eq10[5:8], color= green, scale_factor=1.2),
                              Indicate(eq10[11], color= green, scale_factor=2),
                              Indicate(eq10[12], color= green, scale_factor=2),
                              Indicate(eq10[13], color= green, scale_factor=2),
                              Indicate(eq10[17:20], color= green, scale_factor=1.2), lag_ratio=0.25))
        self.wait()

        eq17 = MathTex(r"\ddot y_1 + \omega_1^2 y_1 = 0", color=dark_blue, font_size=48)[0]
        eq17.shift(eq17[4].get_bottom()[1] * DOWN+2*UNIT*UP)
        eq18 = MathTex(r"\ddot y_2 + \omega_2^2 y_2 = 0", color=dark_blue, font_size=48)[0]
        eq18.shift(eq18[4].get_bottom()[1] * DOWN + UNIT*UP)
        eq19 = MathTex(r"\ddot y_3 + \omega_3^2 y_3 = 0", color=dark_blue, font_size=48)[0]
        eq19.shift(eq19[4].get_bottom()[1] * DOWN)
        eq20 = MathTex(r"\ldots", color=dark_blue, font_size=48)[0]
        eq20.shift(eq20[0].get_bottom()[1] * DOWN + UNIT*DOWN)
        eq21 = MathTex(r"\ddot y_n + \omega_n^2 y_n = 0", color=dark_blue, font_size=48)[0]
        eq21.shift(eq21[4].get_bottom()[1] * DOWN + 2*UNIT *DOWN)

        self.play(LaggedStart(ReplacementTransform(eq16[0].copy(), eq17[0]), ReplacementTransform(eq16[1].copy(), eq17[1]),
                              ReplacementTransform(eq16[2].copy(), eq17[3]), ReplacementTransform(eq16[3].copy(), eq17[4]),
                              ReplacementTransform(eq16[4].copy(), eq17[6]), ReplacementTransform(eq16[5:].copy(), eq17[8:]),
                              Write(eq17[2]), Write(eq17[5]), Write(eq17[7]),

                              ReplacementTransform(eq16[0].copy(), eq18[0]),
                              ReplacementTransform(eq16[1].copy(), eq18[1]),
                              ReplacementTransform(eq16[2].copy(), eq18[3]),
                              ReplacementTransform(eq16[3].copy(), eq18[4]),
                              ReplacementTransform(eq16[4].copy(), eq18[6]),
                              ReplacementTransform(eq16[5:].copy(), eq18[8:]),
                              Write(eq18[2]), Write(eq18[5]), Write(eq18[7]),

                              ReplacementTransform(eq16[0].copy(), eq19[0]),
                              ReplacementTransform(eq16[1].copy(), eq19[1]),
                              ReplacementTransform(eq16[2].copy(), eq19[3]),
                              ReplacementTransform(eq16[3].copy(), eq19[4]),
                              ReplacementTransform(eq16[4].copy(), eq19[6]),
                              ReplacementTransform(eq16[5:].copy(), eq19[8:]),
                              Write(eq19[2]), Write(eq19[5]), Write(eq19[7]),

                              Write(eq20),

                              ReplacementTransform(eq16[0], eq21[0]),
                              ReplacementTransform(eq16[1], eq21[1]),
                              ReplacementTransform(eq16[2], eq21[3]),
                              ReplacementTransform(eq16[3], eq21[4]),
                              ReplacementTransform(eq16[4], eq21[6]),
                              ReplacementTransform(eq16[5:], eq21[8:]),
                              Write(eq21[2]), Write(eq21[5]), Write(eq21[7]),
                              ), run_time=2)
        self.wait()

        self.play(FadeOut(VGroup(eq17, eq18, eq19, eq20, eq21, eq11, eq12, eq10)))
        self.wait()

        self.play(LaggedStart(
            Create(beam),
            Create(wall),
            *(Create(hatch_lines[i]) for i in range(8)),
            lag_ratio=0.2)
        )

        p1 = Dot(color=blue, radius=0.085).move_to(beam.get_right())
        p2 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.1 * beam_width * RIGHT)
        p3 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.2 * beam_width * RIGHT)
        p4 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.3 * beam_width * RIGHT)
        p5 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.4 * beam_width * RIGHT)
        p6 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.5 * beam_width * RIGHT)
        p7 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.6 * beam_width * RIGHT)
        p8 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.7 * beam_width * RIGHT)
        p9 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.8 * beam_width * RIGHT)
        p10 = Dot(color=blue, radius=0.085).move_to(beam.get_left() + 0.9 * beam_width * RIGHT)


        self.play(LaggedStart(*[FadeIn(p) for p in [p2, p3, p4, p5, p6, p7, p8, p9, p10, p1]], lag_ratio = 0.2))
        self.wait()

        eq2 = MathTex(
            r"\mathbf{u} =\begin{bmatrix}u_1 & v_1 & \theta_1 & u_2 & v_2 & \theta_2 & u_3 & \ldots \end{bmatrix}^{T}",
            color=yellow, font_size=48)[0]
        eq2.shift(eq2[0].get_bottom()[1] * DOWN + 3 * UNIT * UP)
        self.play(Write(eq2))
        self.wait()

        self.play(FadeOut(VGroup(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, beam, wall, hatch_lines, eq2)))
        self.wait()

        # beam_width = 11 * UNIT
        # beam_height = 0.5 * UNIT
        #
        # beam2 = Rectangle(
        #     width=beam_width,
        #     height=beam_height,
        #     stroke_color=dark_blue,
        #     stroke_width=4,
        #     fill_opacity=0.0,
        # )
        #
        # wall2 = Line(
        #     start=ORIGIN,
        #     end=3 * UNIT*UP,
        #     stroke_color=dark_blue,
        #     stroke_width=4,
        #     fill_opacity=0.0,
        # ).next_to(beam2, LEFT, buff=0)
        #
        # hatch2 = VGroup()
        # for k in range(8):
        #     hatch2.add(
        #         Line(
        #             start=(wall2.get_left()+UNIT*LEFT) + (-1.5 * UNIT + (3 * UNIT / 8) * k) * UP,
        #             end=wall2.get_right() + (-1.5 * UNIT + (3 * UNIT / 8) * (k + 1)) * UP,
        #             color=dark_blue,
        #             stroke_width=3,
        #         )
        #     )
        #
        # VGroup(wall2, *hatch2, beam2).move_to(ORIGIN)
        #
        # L = beam_width
        # x_left = beam2.get_left()[0]
        # y0 = beam2.get_center()[1]
        #
        # # def mode1(s):
        # #     return (s ** 2) * (3 - 2 * s)
        #
        # def mode2(s):
        #     return (s ** 2) * (3 - 2 * s) * (1 - 2.2 * s)
        #
        # t = ValueTracker(0.0)
        #
        # def make_curve(shape_func, amp=0.9):
        #     curve = VMobject(color=dark_blue, stroke_width=40)
        #     pts = []
        #     for k in range(70):
        #         s = k / 69
        #         x = x_left + s * L
        #         y = y0 + 0.75 * np.sin(t.get_value()) * shape_func(s) * amp
        #         pts.append([x, y, 0])
        #     curve.set_points_smoothly(pts)
        #     return curve
        #
        # # curve1 = always_redraw(lambda: make_curve(mode1, amp=1.0))
        # curve2 = always_redraw(lambda: make_curve(mode2, amp=1.0))
        #
        # # Show mode 1
        # self.play(Create(wall2), Create(hatch2), Create(beam2))
        # self.wait(0.3)
        # self.play(FadeOut(beam2), FadeIn(curve2))
        # # self.play(t.animate.set_value(2 * PI), run_time=2.0, rate_func=linear)
        # # self.play(t.animate.set_value(4 * PI), run_time=2.0, rate_func=linear)
        #
        # # Switch to mode 2
        # # self.remove(curve1)
        # # self.add(curve2)
        # self.play(t.animate.set_value(2 * PI), run_time=2.0, rate_func=linear)
        # self.play(t.animate.set_value(4 * PI), run_time=2.0, rate_func=linear)
        # self.play(t.animate.set_value(6 * PI), run_time=2.0, rate_func=linear)
        # self.play(t.animate.set_value(8 * PI), run_time=2.0, rate_func=linear)
        # self.wait()
        #
        # self.play(FadeOut(VGroup(wall2, hatch2, curve2, )))
        # self.wait(0.5)