"""
Vortex Panel Method with Cosine Spacing + Manim Visualization (Flipped, Centered, and Improved)
- Airfoil flipped horizontally
- Flow direction flipped horizontally
- Airfoil drawn as a single continuous line
- Adds static arrow vector field showing velocity field
- Airfoil centered at the origin
- Streamlines colored by divergence from free-stream angle (blue→red)
"""
from __future__ import annotations

import numpy as np
from math import pi
from typing import Tuple
from matplotlib.path import Path
from manim import *

from primescene import *

config.background_color = ManimColor('#FFFFFF')


def cosine_spacing(n: int) -> np.ndarray:
    k = np.arange(n)
    theta = pi * k / (n - 1)
    return (1.0 - np.cos(theta)) * 0.5


def naca4_coordinates(code: str, n: int = 201, chord: float = 2.0,
                      cosine: bool = True, closed: bool = True) -> np.ndarray:
    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    t = int(code[2:]) / 100.0
    x = cosine_spacing(n) if cosine else np.linspace(0.0, 1.0, n)
    yt = 5 * t * (0.2969 * np.sqrt(
        np.maximum(x, 1e-12)) - 0.1260 * x - 0.3516 * x ** 2 + 0.2843 * x ** 3 - 0.1015 * x ** 4)
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    for i, xi in enumerate(x):
        if p > 1e-12:
            if xi < p:
                yc[i] = m / (p ** 2) * (2 * p * xi - xi ** 2)
                dyc_dx[i] = 2 * m / (p ** 2) * (p - xi)
            else:
                yc[i] = m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xi - xi ** 2)
                dyc_dx[i] = 2 * m / ((1 - p) ** 2) * (p - xi)
    theta = np.arctan(dyc_dx)
    x_u = x - yt * np.sin(theta)
    y_u = yc + yt * np.cos(theta)
    x_l = x + yt * np.sin(theta)
    y_l = yc - yt * np.cos(theta)
    upper = np.stack([x_u, y_u], axis=1)
    lower = np.stack([x_l, y_l], axis=1)
    pts = np.vstack([upper[::-1], lower[1:]]) * chord
    if closed:
        pts[-1] = pts[0]
    pts[:, 0] = -pts[:, 0]  # Flip horizontally
    pts[:, 0] -= (pts[:, 0].max() + pts[:, 0].min()) / 2
    pts[:, 1] -= (pts[:, 1].max() + pts[:, 1].min()) / 2
    return pts


def build_vortex_collocation(pts: np.ndarray, s_vort=0.25, s_coll=0.75):
    xv = pts[:-1, 0] + s_vort * (pts[1:, 0] - pts[:-1, 0])
    yv = pts[:-1, 1] + s_vort * (pts[1:, 1] - pts[:-1, 1])
    xc = pts[:-1, 0] + s_coll * (pts[1:, 0] - pts[:-1, 0])
    yc = pts[:-1, 1] + s_coll * (pts[1:, 1] - pts[:-1, 1])
    dx = pts[1:, 0] - pts[:-1, 0]
    dy = pts[1:, 1] - pts[:-1, 1]
    L = np.hypot(dx, dy)
    nx = dy / L
    ny = -dx / L
    return xv, yv, xc, yc, nx, ny


def build_A(xv, yv, xc, yc, nx, ny):
    N = len(xv)
    A = np.zeros((N, N))
    inv2pi = 1.0 / (2.0 * np.pi)
    for i in range(N):
        dx = xc[i] - xv
        dy = yc[i] - yv
        r2 = dx * dx + dy * dy + 1e-14
        u = inv2pi * dy / r2
        v = -inv2pi * dx / r2
        A[i, :] = u * nx[i] + v * ny[i]
        A[i, i] = 0.0
    return A


def build_rhs(U_inf, alpha_deg, nx, ny):
    a = np.deg2rad(alpha_deg)
    Ux, Uy = -U_inf * np.cos(a), U_inf * np.sin(a)
    return -(Ux * nx + Uy * ny)


def solve_gamma(A, rhs):
    N = A.shape[0]
    A_aug = np.vstack([A, np.eye(N)[0], np.eye(N)[-1]])
    rhs_aug = np.concatenate([rhs, [0.0, 0.0]])
    Gamma, *_ = np.linalg.lstsq(A_aug, rhs_aug, rcond=None)
    return Gamma


def field_from_vortices(xv, yv, Gamma, U_inf, alpha_deg, X, Y, pts=None):
    Ux = -U_inf * np.cos(np.deg2rad(alpha_deg))
    Uy = U_inf * np.sin(np.deg2rad(alpha_deg))
    u = Ux * np.ones_like(X)
    v = Uy * np.ones_like(Y)
    inv2pi = 1.0 / (2.0 * np.pi)
    for j in range(Gamma.size):
        dx = X - xv[j]
        dy = Y - yv[j]
        r2 = dx * dx + dy * dy + 1e-14
        u += inv2pi * Gamma[j] * (dy / r2)
        v += -inv2pi * Gamma[j] * (dx / r2)
    if pts is not None:
        poly = Path(pts)
        mask = poly.contains_points(np.vstack([X.ravel(), Y.ravel()]).T).reshape(X.shape)
        u[mask] = 0.0
        v[mask] = 0.0
    return u, v


try:
    from manim import Scene, Axes, VGroup, VMobject, StreamLines, ArrowVectorField, BLUE, YELLOW
    from manim.utils.color import color_gradient, BLUE as B, RED as R
except ImportError:
    class Scene:
        pass


    class Axes:
        pass


    class VGroup:
        pass


    class VMobject:
        pass


    class StreamLines:
        pass


    class ArrowVectorField:
        pass


    BLUE = None
    YELLOW = None


class FlowAroundAirfoil(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31')
        yellow = ManimColor('#cc9316')
        blue = ManimColor('#0076C2')
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
        self.add(grid)

        code = "2412";
        n_pts = 201;
        U_inf = 1.0;
        alpha_deg = 0.0
        pts = naca4_coordinates(code, n=n_pts, chord=4.0, cosine=True, closed=True)
        xv, yv, xc, yc, nx, ny = build_vortex_collocation(pts)
        A = build_A(xv, yv, xc, yc, nx, ny)
        rhs = build_rhs(U_inf, alpha_deg, nx, ny)
        Gamma = solve_gamma(A, rhs)

        xs = np.linspace(-5.0, 5.0, 250)
        ys = np.linspace(-3.0, 3.0, 200)
        XX, YY = np.meshgrid(xs, ys)
        UU, VV = field_from_vortices(xv, yv, Gamma, U_inf, alpha_deg, XX, YY, pts=pts)
        free_angle = np.arctan2(UV := U_inf * np.sin(np.deg2rad(alpha_deg)), -U_inf * np.cos(np.deg2rad(alpha_deg)))
        angles = np.arctan2(VV, UU)
        divergence = np.abs(np.unwrap(angles - free_angle))
        max_div = divergence.max()

        def vfield_func(pos):
            x, y = float(pos[0]), float(pos[1])
            i = np.abs(xs - x).argmin();
            j = np.abs(ys - y).argmin()
            return np.array([UU[j, i], VV[j, i], 0.0])

        ax = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 0.5], x_length=14, y_length=8)
        airfoil_shape = VMobject(color=dark_blue)
        airfoil_shape.set_points_smoothly([ax.coords_to_point(px, py) for px, py in pts])

        arrow_field = ArrowVectorField(lambda p: vfield_func(ax.point_to_coords(p)),
                                       x_range=[-5, 5, 0.5], y_range=[-3, 3, 0.5],
                                       length_func=lambda norm: 0.3 * norm, color=dark_blue, )

        self.add(airfoil_shape, arrow_field)

        # === square boundary advected as a smooth closed curve ===
        square_center = np.array([2.5, 0.4])  # world coords
        side = 0.2
        half = side / 2

        # Sample many points along the boundary (no duplicate corners)
        samples_per_side = 30
        # bottom: x from -half -> +half, y = -half
        bottom = np.column_stack([
            np.linspace(-half, +half, samples_per_side, endpoint=False),
            np.full(samples_per_side, -half),
        ])
        # right: y from -half -> +half, x = +half
        right = np.column_stack([
            np.full(samples_per_side, +half),
            np.linspace(-half, +half, samples_per_side, endpoint=False),
        ])
        # top: x from +half -> -half, y = +half
        top = np.column_stack([
            np.linspace(+half, -half, samples_per_side, endpoint=False),
            np.full(samples_per_side, +half),
        ])
        # left: y from +half -> -half, x = -half
        left = np.column_stack([
            np.full(samples_per_side, -half),
            np.linspace(+half, -half, samples_per_side, endpoint=False),
        ])

        boundary_world = np.vstack([bottom, right, top, left]) + square_center

        # Invisible marker dots that will be advected (in SCENE coords)
        markers = [
            Dot(ax.coords_to_point(x, y), radius=0).set_opacity(0)
            for (x, y) in boundary_world
        ]
        self.add(*markers)

        # Same velocity-based motion you already use, but applied to every marker
        speed_scale = 0.5  # tune me

        start = ValueTracker(0.0)  # 0 = frozen, 1 = move

        def advect_point(m, dt):
            if start.get_value() < 0.5:
                return
            xw, yw = ax.point_to_coords(m.get_center())
            vx, vy, _ = vfield_func(np.array([xw, yw, 0.0]))
            m.move_to(ax.coords_to_point(xw + speed_scale * vx * dt, yw + speed_scale * vy * dt))

        for m in markers:
            m.add_updater(advect_point)

        # Helper to build a smooth, closed VMobject from current marker positions
        def shape_from_markers(group, color=red, fill=0.25, stroke=2):
            pts = [m.get_center() for m in group]
            shp = VMobject(color=color, stroke_width=stroke, fill_opacity=fill)
            shp.set_points_smoothly(pts)
            shp.close_path()
            return shp

        # Static snapshot (initial boundary) for reference
        static_shell = shape_from_markers(markers, color=red, fill=0.25, stroke=2)
        # Live, advecting “square of air”
        moving_shell = VMobject(color=red, stroke_width=2, fill_opacity=0.25)

        def update_shell(m):
            # Current marker positions (scene coords)
            pts = np.array([mk.get_center() for mk in markers])
            if len(pts) < 3:
                return

            # Order points around centroid to keep a non-zigzag boundary
            c = pts.mean(axis=0)
            ang = np.arctan2(pts[:, 1] - c[1], pts[:, 0] - c[0])
            order = np.argsort(ang)
            pts = pts[order]

            # Build a smooth closed curve (looks like a deforming "shell")
            m.set_points_smoothly(pts)
            m.close_path()

        moving_shell.add_updater(update_shell)

        x_arrow = Line(start=ORIGIN, end=static_shell.get_center(), color=blue, stroke_width=2)
        x_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        x_arrow_label = MathTex(r"\mathbf{x}", color=blue, font_size=32).move_to(x_arrow.get_center() + 0.4 * DOWN)

        self.play(Write(static_shell))
        self.wait(1)
        self.play(self.camera.frame.animate.scale(0.50).shift(1 * UP + 0.55 * RIGHT))
        self.wait(1)

        grid1 = NumberPlane(background_line_style={
            "stroke_color": dark_blue,
            "stroke_width": 1,
            "stroke_opacity": 0.15
        },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 2  # thicker lines
            },
            x_range=(-36, 36, 1),
            y_range=(-18, 18, 1),
        ).scale(UNIT)

        self.play(FadeOut(grid), FadeIn(grid1))
        self.wait(1)
        self.play(arrow_field.animate.fade(0.7))
        self.wait(1)
        self.play(Write(x_arrow), Write(x_arrow_label))
        self.wait(1)
        self.add(moving_shell)
        self.play(start.animate.set_value(1.0))
        self.wait(6)

        for mk in markers:
            mk.remove_updater(advect_point)

        moving_shell.remove_updater(update_shell)
        update_shell(moving_shell)

        self.wait(1)

        ux_arrow = Line(start=static_shell.get_center(), end=moving_shell.get_center(), color=dark_blue, stroke_width=2)
        ux_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        ux_arrow_label = MathTex(r"\mathbf{u}( \mathbf{x}) - \mathbf{x}", color=dark_blue, font_size=32)[0].move_to(
            ux_arrow.get_center() + 0.5 * UP)
        ux_arrow_label[5].set_color(blue)
        ux_arrow_label[:4].set_color(yellow)
        xux_arrow = Line(start=ORIGIN, end=moving_shell.get_center(), color=yellow,
                         stroke_width=2)
        xux_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        xux_arrow_label = MathTex(r"\mathbf{u}( \mathbf{x})", font_size=32, color=yellow)[0].move_to(
            xux_arrow.get_center() + LEFT)

        x0_arrow = Line(start=ORIGIN, end=static_shell.get_corner(DL), color=dark_blue, stroke_width=2)
        x0_arrow.add_tip(tip_shape=StealthTip, tip_width=0.15, tip_length=0.15)
        x0_arrow_label = MathTex(r"\mathbf{x}_0", color=dark_blue, font_size=32)[0].move_to(x_arrow.get_center() + 0.44 * DOWN)

        self.play(LaggedStart(Write(xux_arrow), Write(xux_arrow_label), lag_ratio=0.5))
        self.wait(1)
        self.play(LaggedStart(Write(ux_arrow), Write(ux_arrow_label), lag_ratio=0.5))
        self.wait(1)
        self.play(FadeOut(moving_shell), FadeOut(ux_arrow), FadeOut(ux_arrow_label), FadeOut(x_arrow),
                  FadeOut(x_arrow_label), FadeOut(xux_arrow), FadeOut(xux_arrow_label))
        self.wait(1)
        self.play(LaggedStart(Write(x0_arrow), Write(x0_arrow_label), lag_ratio=0.5))
        self.wait(1)
        self.play(FadeOut(airfoil_shape), FadeOut(arrow_field))

        axes_defaults = {
            "color": dark_blue,
            "include_numbers": True
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

        square = Square(color=red, fill_color=red, fill_opacity=0.5, side_length=unit_length, shade_in_3d=True
                        ).shift(unit_length * (0.5 * UP + 0.5 * RIGHT))

        x0 = Sphere(axes.c2p(0, 0, 0), radius=0.05)
        x0.set_color(dark_blue)
        x0_label2d = MathTex(r"\mathbf{x}_0", color=dark_blue).next_to(x0.get_center(), DOWN)[0]

        self.play(self.camera.frame.animate.scale(2).shift(1 * DOWN + 0.55 * LEFT),
                  grid1.animate.scale(unit_length/UNIT),
                  ReplacementTransform(static_shell, square),
                  ReplacementTransform(x0_arrow, x0),
                  ReplacementTransform(x0_arrow_label, x0_label2d),)
        self.wait(1)

if __name__ == "__main__":
    code = "0012";
    pts = naca4_coordinates(code, n=101, chord=4.0)
    xv, yv, xc, yc, nx, ny = build_vortex_collocation(pts)
    A = build_A(xv, yv, xc, yc, nx, ny)
    rhs = build_rhs(1.0, 4.0, nx, ny)
    Gamma = solve_gamma(A, rhs)
    print("Γ (first 5):", Gamma[:5])