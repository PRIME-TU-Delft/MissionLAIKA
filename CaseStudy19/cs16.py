from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


class Plane(MovingCameraScene, PrimeScene):
    """
    Sequential + centered version (no overlaps / nothing off-screen):
    - Each concept appears centered, then fades out.
    - You can later reposition groups however you like.
    """

    def construct(self):
        super().construct()

        # --- Colors (match your template) ---
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

        # --- Grid (match your template style) ---
        grid = NumberPlane(
            background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15,
            },
            x_range=(1, 50, 1),
            y_range=(1, 25, 1),
            x_length=30,
            y_length=15,
        )
        self.play(Write(grid))
        self.wait(0.5)

        # Helper: show centered, then clear
        def show_then_clear(mobj: Mobject, hold=1.0, in_anim=None, out_anim=None):
            in_anim = in_anim or FadeIn
            out_anim = out_anim or FadeOut
            self.play(in_anim(mobj))
            self.wait(hold)
            self.play(out_anim(mobj))

        # ==========================================================
        # 1) Title
        # ==========================================================
        title = Tex("Wing/Beam Vibrations \\& Eigenmodes", font_size=54, color=dark_blue)
        show_then_clear(title, hold=1.2, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 2) Physical model: cantilever beam
        # ==========================================================
        beam_width = 8.5
        beam_height = 0.35

        beam = Rectangle(
            width=beam_width,
            height=beam_height,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_color=ManimColor("#FFFFFF"),
            fill_opacity=1.0,
        )

        wall = Rectangle(
            width=0.5,
            height=1.8,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_color=ManimColor("#FFFFFF"),
            fill_opacity=1.0,
        ).next_to(beam, LEFT, buff=0)

        hatch_lines = VGroup()
        for k in range(9):
            hatch_lines.add(
                Line(
                    start=wall.get_left() + 0.05 * RIGHT + (-0.85 + 0.22 * k) * UP,
                    end=wall.get_left() + 0.45 * RIGHT + (-0.65 + 0.22 * k) * UP,
                    color=dark_blue,
                    stroke_width=3,
                )
            )

        clamp_label = Tex("fixed", font_size=34, color=dark_blue).next_to(wall, LEFT)

        model_text = Tex("Model the wing as a cantilever beam", font_size=40, color=dark_blue)
        model_text.next_to(beam, UP, buff=0.7)

        beam_model = VGroup(model_text, wall, hatch_lines, beam, clamp_label).move_to(ORIGIN)

        self.play(Create(wall), Create(hatch_lines), Create(beam), Write(model_text), Write(clamp_label))
        self.wait(1.2)

        # ==========================================================
        # 3) Discretization points
        # ==========================================================
        # Keep the beam on screen; add points + labels, then clear all.
        p1 = Dot(color=red, radius=0.085).move_to(beam.get_left() + 0.55 * beam_width * RIGHT)
        p2 = Dot(color=red, radius=0.085).move_to(beam.get_right())

        p1_label = MathTex("1", font_size=42, color=red).next_to(p1, DOWN, buff=0.15)
        p2_label = MathTex("2", font_size=42, color=red).next_to(p2, DOWN, buff=0.15)

        disc_text = Tex("Discretize: choose a few points", font_size=40, color=dark_blue).next_to(
            model_text, DOWN, buff=0.35
        )

        self.play(Write(disc_text))
        self.play(FadeIn(p1, scale=0.5), FadeIn(p2, scale=0.5), Write(p1_label), Write(p2_label))
        self.wait(1.2)

        # ==========================================================
        # 4) DOFs at each point (x, y, theta)
        # ==========================================================
        def dof_glyphs(anchor: Mobject, idx: str) -> VGroup:
            base = anchor.get_center()

            ax = Arrow(base, base + 0.85 * RIGHT, color=yellow, stroke_width=4, buff=0.0)
            tx = MathTex(fr"x_{idx}", font_size=36, color=yellow).next_to(ax, RIGHT, buff=0.12)

            ay = Arrow(base, base + 0.85 * UP, color=yellow, stroke_width=4, buff=0.0)
            ty = MathTex(fr"y_{idx}", font_size=36, color=yellow).next_to(ay, UP, buff=0.12)

            arc = Arc(radius=0.45, start_angle=25 * DEGREES, angle=300 * DEGREES, arc_center=base, color=yellow)
            arc_tip = Arrow(
                arc.point_from_proportion(0.92),
                arc.point_from_proportion(0.98),
                color=yellow,
                stroke_width=4,
                buff=0.0,
                max_tip_length_to_length_ratio=0.8,
            )
            ttheta = MathTex(fr"\theta_{idx}", font_size=36, color=yellow).next_to(arc, DOWN, buff=0.08)

            return VGroup(ax, tx, ay, ty, arc, arc_tip, ttheta)

        dofs1 = dof_glyphs(p1, "1").shift(0.25 * DOWN + 0.1 * LEFT)
        dofs2 = dof_glyphs(p2, "2").shift(0.25 * DOWN + 0.1 * LEFT)

        dof_text = Tex("At each point: translations and rotation", font_size=40, color=dark_blue).next_to(
            disc_text, DOWN, buff=0.35
        )

        self.play(Write(dof_text))
        self.play(LaggedStart(GrowArrow(dofs1[0]), GrowArrow(dofs1[2]), lag_ratio=0.15))
        self.play(Write(dofs1[1]), Write(dofs1[3]))
        self.play(Create(dofs1[4]), GrowArrow(dofs1[5]), Write(dofs1[6]))

        self.play(LaggedStart(GrowArrow(dofs2[0]), GrowArrow(dofs2[2]), lag_ratio=0.15))
        self.play(Write(dofs2[1]), Write(dofs2[3]))
        self.play(Create(dofs2[4]), GrowArrow(dofs2[5]), Write(dofs2[6]))
        self.wait(1.2)

        # Clear the whole physical scene before equations (sequential)
        self.play(
            FadeOut(VGroup(beam_model, disc_text, dof_text, p1, p2, p1_label, p2_label, dofs1, dofs2))
        )
        self.wait(0.3)

        # ==========================================================
        # 5) Build displacement vector u
        # ==========================================================
        u_header = Tex("Collect all DOFs into a vector", font_size=44, color=dark_blue)
        u_vec = MathTex(
            r"u=",
            r"\begin{bmatrix} x_1\\ y_1\\ \theta_1\\ x_2\\ y_2\\ \theta_2 \end{bmatrix}",
            font_size=52,
            color=dark_blue,
        )
        u_vec.set_color_by_tex("u", yellow)
        for s in ["x_1", "y_1", r"\theta_1", "x_2", "y_2", r"\theta_2"]:
            u_vec.set_color_by_tex(s, yellow)

        u_group = VGroup(u_header, u_vec).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        show_then_clear(u_group, hold=1.6, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 6) Equation of motion: M u¨ + K u = 0
        # ==========================================================
        e1_header = Tex("Matrix equation of motion", font_size=44, color=dark_blue)
        eq_motion = MathTex(r"M\ddot{u}+Ku=0", font_size=64, color=dark_blue)
        eq_motion.set_color_by_tex_to_color_map({"M": blue, "K": blue, "u": yellow, r"\ddot{u}": yellow})

        labels = VGroup(
            Tex("mass matrix", font_size=34, color=dark_blue).next_to(eq_motion, DOWN, buff=0.3).shift(2.4 * LEFT),
            Tex("stiffness matrix", font_size=34, color=dark_blue).next_to(eq_motion, DOWN, buff=0.3).shift(2.4 * RIGHT),
        )

        e1_group = VGroup(e1_header, eq_motion, labels).arrange(DOWN, buff=0.5).move_to(ORIGIN)
        self.play(Write(e1_header))
        self.play(Write(eq_motion))
        self.play(FadeIn(labels, shift=0.2 * UP))
        self.wait(1.6)
        self.play(FadeOut(e1_group))
        self.wait(0.3)

        # ==========================================================
        # 7) Multiply by M^{-1}, define A
        # ==========================================================
        e2_header = Tex("Standard form using $A=M^{-1}K$", font_size=44, color=dark_blue)

        eq_A = MathTex(r"\ddot{u}+Au=0", font_size=64, color=dark_blue)
        eq_A.set_color_by_tex_to_color_map({"A": blue, "u": yellow, r"\ddot{u}": yellow})

        def_A = MathTex(r"A=M^{-1}K", font_size=56, color=dark_blue)
        def_A.set_color_by_tex_to_color_map({"A": blue, "M": blue, "K": blue})

        e2_group = VGroup(e2_header, eq_A, def_A).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        show_then_clear(e2_group, hold=1.8, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 8) Eigenvalue problem: Av_i = λ_i v_i, λ_i = ω_i^2
        # ==========================================================
        e3_header = Tex("Eigenvalues and eigenvectors", font_size=44, color=dark_blue)
        eig1 = MathTex(r"Av_i=\lambda_i v_i", font_size=64, color=dark_blue)
        eig1.set_color_by_tex_to_color_map({"A": blue, r"\lambda_i": red})

        eig2 = MathTex(r"\lambda_i=\omega_i^2", font_size=64, color=dark_blue)
        eig2.set_color_by_tex_to_color_map({r"\lambda_i": red, r"\omega_i": red})

        e3_group = VGroup(e3_header, eig1, eig2).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        show_then_clear(e3_group, hold=1.8, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 9) Diagonalization: A = P D P^{-1}, D = diag(ω_i^2)
        # ==========================================================
        e4_header = Tex("Diagonalize to decouple", font_size=44, color=dark_blue)
        diag = MathTex(r"A=PDP^{-1}", font_size=64, color=dark_blue)
        diag.set_color_by_tex_to_color_map({"A": blue, "P": blue, "D": blue})

        D_def = MathTex(
            r"D=\mathrm{diag}(\omega_1^2,\omega_2^2,\dots,\omega_n^2)",
            font_size=46,
            color=dark_blue,
        )
        D_def.set_color_by_tex("D", blue)
        D_def.set_color_by_tex(r"\omega", red)

        e4_group = VGroup(e4_header, diag, D_def).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        show_then_clear(e4_group, hold=1.9, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 10) Change of variables: y = P^{-1}u, then y¨ + Dy = 0
        # ==========================================================
        e5_header = Tex("Change coordinates", font_size=44, color=dark_blue)

        y_def = MathTex(r"y=P^{-1}u", font_size=64, color=dark_blue)
        y_def.set_color_by_tex_to_color_map({"y": yellow, "P": blue, "u": yellow})

        y_eq = MathTex(r"\ddot{y}+Dy=0", font_size=64, color=dark_blue)
        y_eq.set_color_by_tex_to_color_map({"y": yellow, "D": blue, r"\ddot{y}": yellow})

        e5_group = VGroup(e5_header, y_def, y_eq).arrange(DOWN, buff=0.55).move_to(ORIGIN)
        show_then_clear(e5_group, hold=1.9, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 11) Decoupled scalar equations: y_i¨ + ω_i^2 y_i = 0
        # ==========================================================
        e6_header = Tex("Independent oscillators", font_size=44, color=dark_blue)
        sho = MathTex(r"\ddot{y}_i+\omega_i^2 y_i=0", font_size=72, color=dark_blue)
        sho.set_color_by_tex("y", yellow)
        sho.set_color_by_tex(r"\omega", red)

        e6_group = VGroup(e6_header, sho).arrange(DOWN, buff=0.6).move_to(ORIGIN)
        show_then_clear(e6_group, hold=2.0, in_anim=Write, out_anim=FadeOut)

        # ==========================================================
        # 12) Mode shapes (separate, centered visual payoff)
        # ==========================================================
        mode_title = Tex("Eigenvectors = mode shapes", font_size=48, color=dark_blue).to_edge(UP)

        # Rebuild a centered beam (clean slate)
        beam2 = Rectangle(
            width=8.5,
            height=0.35,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_color=ManimColor("#FFFFFF"),
            fill_opacity=1.0,
        ).move_to(ORIGIN + 0.4 * DOWN)

        wall2 = Rectangle(
            width=0.5,
            height=1.8,
            stroke_color=dark_blue,
            stroke_width=4,
            fill_color=ManimColor("#FFFFFF"),
            fill_opacity=1.0,
        ).next_to(beam2, LEFT, buff=0)

        hatch2 = VGroup()
        for k in range(9):
            hatch2.add(
                Line(
                    start=wall2.get_left() + 0.05 * RIGHT + (-0.85 + 0.22 * k) * UP,
                    end=wall2.get_left() + 0.45 * RIGHT + (-0.65 + 0.22 * k) * UP,
                    color=dark_blue,
                    stroke_width=3,
                )
            )

        # simple deforming curve for mode shapes
        L = beam2.get_width()
        x_left = beam2.get_left()[0]
        y0 = beam2.get_center()[1]

        def mode1(s):
            return (s**2) * (3 - 2 * s)

        def mode2(s):
            return (s**2) * (3 - 2 * s) * (1 - 2.2 * s)

        t = ValueTracker(0.0)

        def make_curve(shape_func, amp=0.9):
            curve = VMobject(color=dark_blue, stroke_width=6)
            pts = []
            for k in range(70):
                s = k / 69
                x = x_left + s * L
                y = y0 + 0.75 * np.sin(t.get_value()) * shape_func(s) * amp
                pts.append([x, y, 0])
            curve.set_points_smoothly(pts)
            return curve

        curve1 = always_redraw(lambda: make_curve(mode1, amp=1.0))
        curve2 = always_redraw(lambda: make_curve(mode2, amp=1.0))

        m_label = Tex("mode 1", font_size=38, color=dark_blue).next_to(beam2, DOWN, buff=0.6)

        # Show mode 1
        self.play(Write(mode_title))
        self.play(Create(wall2), Create(hatch2), Create(beam2))
        self.wait(0.3)
        self.play(FadeOut(beam2), FadeIn(curve1), Write(m_label))
        self.play(t.animate.set_value(2 * PI), run_time=2.0, rate_func=linear)
        self.play(t.animate.set_value(4 * PI), run_time=2.0, rate_func=linear)

        # Switch to mode 2
        self.remove(curve1)
        self.add(curve2)
        self.play(Transform(m_label, Tex("mode 2", font_size=38, color=dark_blue).move_to(m_label)))
        self.play(t.animate.set_value(6 * PI), run_time=2.0, rate_func=linear)
        self.play(t.animate.set_value(8 * PI), run_time=2.0, rate_func=linear)

        takeaway = Tex(
            r"eigenvalues $\lambda_i=\omega_i^2$ set the frequencies",
            font_size=40,
            color=dark_blue,
        ).to_edge(DOWN)
        takeaway.set_color_by_tex(r"\omega", red)

        self.play(Write(takeaway))
        self.wait(2.0)

        # Optional final clear (keep grid if you want)
        self.play(FadeOut(VGroup(mode_title, wall2, hatch2, curve2, m_label, takeaway)))
        self.wait(0.5)
