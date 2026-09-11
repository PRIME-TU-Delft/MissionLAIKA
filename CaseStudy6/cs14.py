import numpy as np
from manim import *
from primescene import *

config.background_color = ManimColor('#FFFFFF')

class Lecture14Scene(PrimeScene, ThreeDScene):
    def construct(self):
        super().construct()
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31')
        yellow = ManimColor('#cc9316')
        blue = ManimColor('#0076C2')
        green = ManimColor('#009B77')
        CAM_RIGHT = np.array([-1, 1, 0])
        CAM_UP = 5 / 4 * np.array([0, 0, 1])

        axes_defaults = {
            "color": dark_blue,
            "include_numbers": False
        }

        ar = [-3, 3, 1]
        axes = ThreeDAxes(
            x_range=ar,
            y_range=ar,
            z_range=[-2, 2, 1],
            x_length=10.5,
            y_length=10.5,
            z_length=7.0,
            axis_config=axes_defaults
        )

        unit_x_vec = axes.c2p(1, 0, 0) - axes.c2p(0, 0, 0)
        unit_length = np.linalg.norm(unit_x_vec)

        cube = Cube(
            side_length= unit_length,
            fill_color=red,
            fill_opacity=0.5,
            stroke_color=dark_blue,
            stroke_width=0
        ).move_to(np.array([unit_length/2.0, unit_length/2.0, unit_length/2.0]))

        grid2 = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,
                "stroke_width": 0
            },
            x_range=(-3, 3, 1),
            y_range=(-3, 3, 1),
            shade_in_3d=True,
        ).scale(unit_length)

        grid = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,
                "stroke_width": 2
            },
            x_range=(-5, 5, 1),
            y_range=(-3, 3, 1),
            shade_in_3d=True,
        ).scale(unit_length)

        self.add(grid)

        square = Square(color=red, fill_color=red, fill_opacity=0.5, side_length=unit_length, shade_in_3d=True).shift(unit_length/2 * (UP + RIGHT))
        self.add(square)

        x0 = Sphere(axes.c2p(0, 0, 0), radius=0.05)
        x0.set_color(dark_blue)
        x0_label2d = MathTex(r"\mathbf{x}_0", color=dark_blue).next_to(x0.get_center(), DOWN)[0]
        x0_label3d = \
        MathTex(r"\mathbf{x}_0", color=dark_blue, shade_in_3d=True).next_to(x0.get_center(), IN, buff=0.38).rotate(90 * DEGREES,
                                                                                                        axis=RIGHT).rotate(
            135 * DEGREES, axis=np.array([0, 0, 1]))[0]

        self.add(x0, x0_label2d)
        self.wait(1)

        self.move_camera(
            phi=70 * DEGREES,
            theta=45 * DEGREES,
            focal_distance=10000000,
            run_time=3,
            added_anims=[Write(cube), Write(axes), FadeOut(grid), FadeIn(grid2), FadeOut(square), ReplacementTransform(x0_label2d, x0_label3d)]
        )
        self.wait(1)
        self.remove(square)

        def rotate_camera(time):
            self.play(theta.animate(run_time=time/2.0, rate_func=rate_functions.ease_in_sine).set_value(225 * DEGREES))
            self.play(theta.animate(run_time=time/2.0, rate_func=rate_functions.ease_out_sine).set_value(405 * DEGREES))
            theta.set_value(45 * DEGREES)

        phi, theta, focal_distance, gamma, distance_to_origin = self.camera.get_value_trackers()

        a = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 0, 1), color=green)
        b = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(0, 1, 0), color=blue)
        c = Arrow3D(start=axes.c2p(0, 0, 0), end=axes.c2p(1, 0, 0), color=yellow)

        a_label = \
        MathTex(r"\mathbf{a}", color=blue, shade_in_3d=True).next_to(b.get_center(), OUT,).rotate(90 * DEGREES, axis=RIGHT).rotate(
            -45 * DEGREES, axis=np.array([0, 0, 1]))[0]
        b_label = \
        MathTex(r"\mathbf{b}", color=green, shade_in_3d=True).next_to(a.get_center(), OUT).rotate(90 * DEGREES, axis=RIGHT).rotate(
            -45 * DEGREES, axis=np.array([0, 0, 1]))[0]
        c_label = \
        MathTex(r"\mathbf{c}", color=ManimColor('#fcc13f'), shade_in_3d=True).next_to(c.get_center(), OUT,).rotate(90 * DEGREES, axis=RIGHT).rotate(
            -45 * DEGREES, axis=np.array([0, 0, 1]))[0]

        self.play(theta.animate(run_time=1.5).set_value(225 * DEGREES), x0_label3d.animate.rotate(180 * DEGREES, axis=np.array([0, 0, 1])))
        self.wait(1)

        self.play(GrowFromCenter(a), GrowFromCenter(b), GrowFromCenter(c))
        self.wait(1)

        self.play(Write(a_label), Write(b_label), Write(c_label))
        self.wait(1)

        self.play(theta.animate(run_time=1.5).set_value(405 * DEGREES),
                  *[
                      label.animate.rotate(180 * DEGREES, axis=np.array([0, 0, 1]))
                      for label in [a_label, b_label, c_label, x0_label3d]
                  ])
        theta.set_value(45 * DEGREES)
        self.wait(1)

        eq1 = MathTex(r"V_{\text{cube}} = |\mathbf{a}\cdot (\mathbf{b}\times \mathbf{c})| = |\operatorname{det}([\mathbf{a} \ \mathbf{b} \ \mathbf{c}])|",
                      color=dark_blue, font_size=40)[0]
        eq1.rotate(90 * DEGREES, axis=RIGHT)
        eq1.rotate(135 * DEGREES, axis=np.array([0, 0, 1]))
        eq1.rotate(
            angle=phi.get_value() *DEGREES,
            axis=normalize(np.array([-1, 1, 0])),
        )
        eq1.shift(2.5 * CAM_RIGHT + 2 * CAM_UP)
        eq1[7].set_color(blue)
        eq1[10].set_color(green)
        eq1[12].set_color(yellow)
        eq1[22].set_color(blue)
        eq1[23].set_color(green)
        eq1[24].set_color(yellow)

        self.play(LaggedStart(
            Write(eq1[:7]),
            ReplacementTransform(a_label.copy(), eq1[7]),
            Write(eq1[8:10]),
            ReplacementTransform(b_label.copy(), eq1[10]),
            Write(eq1[11]),
            ReplacementTransform(c_label.copy(), eq1[12]),
            Write(eq1[13:15]),
            lag_ratio=0.5
        ))
        self.wait(1)
        self.play(LaggedStart(Write(eq1[15:22]),
            ReplacementTransform(a_label.copy(), eq1[22]),
            ReplacementTransform(b_label.copy(), eq1[23]),
            ReplacementTransform(c_label.copy(), eq1[24]),
            Write(eq1[24:]),
            lag_ratio=0.5))
        self.wait(1)
        self.play(FadeOut(eq1))

        S = np.array([
            [1, 0, 0],
            [0, 1, 1],
            [0, 0, 1],
        ])

        cube_translated = cube.copy()
        cube_translated.shift(0.5*(UP + 4*LEFT + OUT))
        cube_deformed = cube.copy()
        cube_deformed.apply_matrix(S)
        cube_deformed.shift(0.5*(UP + 4*LEFT + OUT))
        a_deformed = a.copy()
        b_deformed = b.copy()
        c_deformed = c.copy()
        Group(a_deformed, b_deformed, c_deformed).apply_matrix(S)
        Group(a_deformed, b_deformed, c_deformed).shift(0.5*(UP + 4*LEFT + OUT))

        self.wait(1)

        ux0 = Arrow3D(start=axes.c2p(0, 0, 0), end=0.5 * (UP + 4 * LEFT + OUT), color=dark_blue)
        ux0_label = \
            MathTex(r"\mathbf{u}(\mathbf{x}_0)", color=dark_blue, shade_in_3d=True, font_size=36).next_to(
                ux0.get_center(),
                IN, buff=0.5).rotate(90 * DEGREES,
                                     axis=RIGHT).rotate(
                -45 * DEGREES, axis=np.array([0, 0, 1]))[0]

        self.play(theta.animate(run_time=1.5).set_value(225 * DEGREES),
                  *[
                      label.animate.rotate(180 * DEGREES, axis=np.array([0, 0, 1]))
                      for label in [a_label, b_label, c_label, x0_label3d]
                  ]
                  )
        self.wait(1)

        self.play(ReplacementTransform(cube, cube_translated),
                  Group(a_label, b_label, c_label, a, b, c).animate.shift(0.5 * (UP + 4 * LEFT + OUT)),
                  axes.x_axis.animate.set_stroke(opacity=0.2),
                  axes.y_axis.animate.set_stroke(opacity=0.2),
                  axes.z_axis.animate.set_stroke(opacity=0.2),
                  )
        self.wait(1)

        self.play(GrowFromCenter(ux0),Write(ux0_label))
        self.wait(1)
        self.play(ux0_label.animate.set_opacity(0.4))
        self.wait(1)

        self.play(theta.animate(run_time=1.5).set_value(405 * DEGREES),
                  *[
                      label.animate.rotate(180 * DEGREES, axis=np.array([0, 0, 1]))
                      for label in [a_label, b_label, c_label, x0_label3d, ux0_label]
                  ]
                  )
        theta.set_value(45 * DEGREES)
        self.wait(1)

        Ja_label = \
            MathTex(r"J\mathbf{a}", color=blue, shade_in_3d=True)[0].move_to(a_label.get_center()).rotate(90 * DEGREES,
                                                                                                     axis=RIGHT).rotate(
                135 * DEGREES, axis=np.array([0, 0, 1]))
        Ja_label[0].set_color(dark_blue)
        Ja_label.shift(0.5*UP*unit_length)
        Jb_label = \
            MathTex(r"J\mathbf{b}", color=green, shade_in_3d=True)[0].move_to(b_label.get_center()).rotate(90 * DEGREES,
                                                                                                        axis=RIGHT).rotate(
                135 * DEGREES, axis=np.array([0, 0, 1]))
        Jb_label[0].set_color(dark_blue)
        Jb_label.shift(UP * unit_length)
        Jc_label = \
            MathTex(r"J\mathbf{c}", color=ManimColor('#fcc13f'), shade_in_3d=True)[0].move_to(c_label.get_center()).rotate(
                90 * DEGREES, axis=RIGHT).rotate(
                135 * DEGREES, axis=np.array([0, 0, 1]))
        Jc_label[0].set_color(dark_blue)

        self.wait(1)

        self.play(ReplacementTransform(cube_translated, cube_deformed),
                  ReplacementTransform(a, a_deformed),
                  ReplacementTransform(b, b_deformed),
                  ReplacementTransform(c, c_deformed),
                  ReplacementTransform(a_label, Ja_label[1]),
                  ReplacementTransform(b_label, Jb_label[1]),
                  ReplacementTransform(c_label, Jc_label[1]),
                  GrowFromCenter(Ja_label[0]),
                  GrowFromCenter(Jb_label[0]),
                  GrowFromCenter(Jc_label[0]),)
        self.wait(1)
        rotate_camera(3)
        self.wait(1)

        UNIT = 3 / 4
        Ja_label_2d = \
            MathTex(r"J\mathbf{a}", color=blue, font_size=48)[0].shift(UNIT*LEFT)
        Ja_label_2d[0].set_color(dark_blue)
        Ja_label_2d.shift(Ja_label_2d[1].get_bottom()[1] * DOWN)
        Jb_label_2d = \
            MathTex(r"J\mathbf{b}", color=green, font_size=48)[0]
        Jb_label_2d[0].set_color(dark_blue)
        Jb_label_2d.shift(Jb_label_2d[1].get_bottom()[1] * DOWN)
        Jc_label_2d = \
            MathTex(r"J\mathbf{c}", color=yellow, font_size=48)[0].shift(UNIT*RIGHT)
        Jc_label_2d[0].set_color(dark_blue)
        Jc_label_2d.shift(Jc_label_2d[1].get_bottom()[1] * DOWN)

        grid3 = NumberPlane(background_line_style={
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
        self.wait(1)

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES,
            run_time=3,
            added_anims=[grid2.animate.scale(UNIT/unit_length), FadeOut(axes), ReplacementTransform(Ja_label, Ja_label_2d),
                         ReplacementTransform(Jb_label, Jb_label_2d),
                         ReplacementTransform(Jc_label, Jc_label_2d), FadeOut(Group(cube_deformed, a_deformed, b_deformed, c_deformed, x0, ux0, ux0_label))]
        )
        self.play(FadeOut(grid2), FadeIn(grid3))
        self.wait(1)

        eq4 = MathTex(
            r"V_{\text{new}} = |J\mathbf{a}\cdot (J\mathbf{b}\times J\mathbf{c})|",
            color=dark_blue, font_size=48)[0]
        eq4.shift(eq4[0].get_bottom()[1] * DOWN)
        eq4[7].set_color(blue)
        eq4[11].set_color(green)
        eq4[14].set_color(yellow)

        eq5 = MathTex(
            r"V_{\text{new}} = |J\mathbf{a}\cdot (J\mathbf{b}\times J\mathbf{c})|=|\operatorname{det}([J\mathbf{a} \ J\mathbf{b} \ J\mathbf{c}])|",
            color=dark_blue, font_size=48)[0]
        eq5.shift(eq5[0].get_bottom()[1] * DOWN)
        eq5[7].set_color(blue)
        eq5[11].set_color(green)
        eq5[14].set_color(yellow)
        eq5[25].set_color(blue)
        eq5[27].set_color(green)
        eq5[29].set_color(yellow)

        self.play(ReplacementTransform(Ja_label_2d, eq4[6:8]),
                  ReplacementTransform(Jb_label_2d, eq4[10:12]),
                  ReplacementTransform(Jc_label_2d, eq4[13:15]),
                  GrowFromCenter(eq4[5]), GrowFromCenter(eq4[8:10]), GrowFromCenter(eq4[12]), GrowFromCenter(eq4[15:]), Write(eq4[:5]),)
        self.wait(1)

        self.play(LaggedStart(ReplacementTransform(eq4, eq5[:len(eq4)]), Write(eq5[len(eq4):]), lag_ratio=0.6))
        self.wait(1)

        eq6 = MathTex(
            r"=|\operatorname{det}(J[\mathbf{a} \ \mathbf{b} \ \mathbf{c}])|",
            color=dark_blue, font_size=48)[0]
        eq6.shift(eq6[2].get_bottom()[1] * DOWN + UNIT*UP)
        eq6.align_to(eq5[17], LEFT)
        eq6[8].set_color(blue)
        eq6[9].set_color(green)
        eq6[10].set_color(yellow)
        
        eq7 = MathTex(
            r"= |\operatorname{det}(J)\operatorname{det}([\mathbf{a} \ \mathbf{b} \ \mathbf{c}])|",
            color=dark_blue, font_size=48)[0]
        eq7.shift(eq7[2].get_bottom()[1] * DOWN)
        eq7.align_to(eq5[17], LEFT)
        eq7[13].set_color(blue)
        eq7[14].set_color(green)
        eq7[15].set_color(yellow)
        
        eq8 = MathTex(
            r"=|\operatorname{det}(J)|\,|\operatorname{det}([\mathbf{a} \ \mathbf{b} \ \mathbf{c}])|",
            color=dark_blue, font_size=48)[0]
        eq8.shift(eq8[2].get_bottom()[1] * DOWN + UNIT * DOWN)
        eq8.align_to(eq5[17], LEFT)
        eq8[15].set_color(blue)
        eq8[16].set_color(green)
        eq8[17].set_color(yellow)
        
        eq9 = MathTex(
            r"=|\operatorname{det}(J)|\,V_{\text{cube}}",
            color=dark_blue, font_size=48)[0]
        eq9.shift(eq9[2].get_bottom()[1] * DOWN + 2* UNIT * DOWN)
        eq9.align_to(eq5[17], LEFT)

        self.play( LaggedStart(eq5.animate.shift(2*UNIT*UP), Write(eq6), Write(eq7), Write(eq8),Write(eq9), lag_ratio=0.8))
        self.wait(1)

