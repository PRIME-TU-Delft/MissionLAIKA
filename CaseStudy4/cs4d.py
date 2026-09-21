from __future__ import annotations

import numpy as np
from math import pi
from typing import Tuple
from matplotlib.path import Path
from manim import *

from primescene import *


config.background_color = ManimColor("#FFFFFF")


def cosine_spacing(n: int) -> np.ndarray:
    k = np.arange(n)
    theta = pi * k / (n - 1)
    return (1.0 - np.cos(theta)) * 0.5


def naca4_coordinates(
    code: str,
    n: int = 201,
    chord: float = 2.0,
    cosine: bool = True,
    closed: bool = True,
) -> np.ndarray:
    m = int(code[0]) / 100.0
    p = int(code[1]) / 10.0
    t = int(code[2:]) / 100.0
    x = cosine_spacing(n) if cosine else np.linspace(0.0, 1.0, n)
    yt = (
        5
        * t
        * (
            0.2969 * np.sqrt(np.maximum(x, 1e-12))
            - 0.1260 * x
            - 0.3516 * x**2
            + 0.2843 * x**3
            - 0.1015 * x**4
        )
    )
    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)
    for i, xi in enumerate(x):
        if p > 1e-12:
            if xi < p:
                yc[i] = m / (p**2) * (2 * p * xi - xi**2)
                dyc_dx[i] = 2 * m / (p**2) * (p - xi)
            else:
                yc[i] = m / ((1 - p) ** 2) * ((1 - 2 * p) + 2 * p * xi - xi**2)
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
        mask = poly.contains_points(np.vstack([X.ravel(), Y.ravel()]).T).reshape(
            X.shape
        )
        u[mask] = 0.0
        v[mask] = 0.0
    return u, v


class Lecture4Scene(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")
        green = ManimColor("#009B77")

        grid = NumberPlane(
            background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15,
            },
            axis_config={
                "stroke_color": dark_blue,  # axes color
                "stroke_width": 2,  # thicker lines
            },
            x_range=(0, 72, 1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        eq4a = MathTex(
            r"J = \frac{\partial(u_1, u_2)}{\partial(x_1, x_2)} = \begin{bmatrix}\frac{\partial u_1}{\partial x_1}(\mathbf{x}_0) & "
            r"\frac{\partial u_1}{\partial x_2}(\mathbf{x}_0)\\\frac{\partial u_2}{\partial x_1}(\mathbf{x}_0)"
            r" & \frac{\partial u_2}{\partial x_2}(\mathbf{x}_0)\end{bmatrix}",
            color=dark_blue,
            font_size=48,
        )[0]
        eq4a.shift(eq4a[0].get_bottom()[1] * DOWN + 3 * UNIT * DOWN)
        eq4a[4:6].set_color(yellow)
        eq4a[7:9].set_color(yellow)
        eq4a[13:15].set_color(blue)
        eq4a[16:18].set_color(blue)
        eq4a[22:24].set_color(yellow)
        eq4a[26:28].set_color(blue)
        eq4a[29:31].set_color(green)
        eq4a[33:35].set_color(yellow)
        eq4a[37:39].set_color(blue)
        eq4a[40:42].set_color(green)
        eq4a[44:46].set_color(yellow)
        eq4a[48:50].set_color(blue)
        eq4a[51:53].set_color(green)
        eq4a[55:57].set_color(yellow)
        eq4a[59:61].set_color(blue)
        eq4a[62:64].set_color(green)

        eq6b = MathTex(
            r"\mathbf{x}_0+\Delta \mathbf{x}", color=dark_blue, font_size=60
        )[0]
        eq6b.shift(eq6b[0].get_bottom()[1] * DOWN).shift(
            3 * UNIT * RIGHT + 3 * UNIT * UP
        )
        eq6b[:2].set_color(green)
        eq6b[4].set_color(blue)

        eq7 = MathTex(
            r"\Delta \mathbf{x}=\begin{bmatrix} \Delta x_1 \\ \Delta x_2 \end{bmatrix}",
            color=dark_blue,
            font_size=60,
        )[0]
        eq7.shift(3 * UNIT * UP + eq7[0].get_bottom()[1] * DOWN + 3 * UNIT * LEFT)
        eq7[1].set_color(blue)
        eq7[5:7].set_color(blue)
        eq7[8:10].set_color(blue)

        eq9 = MathTex(
            r"\mathbf{u}(\mathbf{x}_0+\Delta \mathbf{x}) \approx \mathbf{u}(\mathbf{x}_0) + J \Delta \mathbf{x}",
            color=dark_blue,
            font_size=60,
        )[0]
        eq9.shift(eq9[0].get_bottom()[1] * DOWN)
        eq9[0].set_color(yellow)
        eq9[2:4].set_color(green)
        eq9[6].set_color(blue)
        eq9[9].set_color(yellow)
        eq9[11:13].set_color(green)
        eq9[17].set_color(blue)

        self.add(grid, eq6b, eq7, eq9, eq4a)
        self.wait(1)
        self.play(FadeOut(eq6b), FadeOut(eq7), FadeOut(eq9))

        code = "2412"
        n_pts = 201
        U_inf = 1.0
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
        free_angle = np.arctan2(
            UV := U_inf * np.sin(np.deg2rad(alpha_deg)),
            -U_inf * np.cos(np.deg2rad(alpha_deg)),
        )
        angles = np.arctan2(VV, UU)
        divergence = np.abs(np.unwrap(angles - free_angle))
        max_div = divergence.max()

        def vfield_func(pos):
            x, y = float(pos[0]), float(pos[1])
            i = np.abs(xs - x).argmin()
            j = np.abs(ys - y).argmin()
            return np.array([UU[j, i], VV[j, i], 0.0])

        ax = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 0.5], x_length=14, y_length=8)
        airfoil_shape = VMobject(color=dark_blue)
        airfoil_shape.set_points_smoothly(
            [ax.coords_to_point(px, py) for px, py in pts]
        )

        self.play(Write(airfoil_shape))

        # === square boundary advected as a smooth closed curve ===
        square_center = np.array([2.5, 0.4])  # world coords
        side = 0.2
        half = side / 2

        # Sample many points along the boundary (no duplicate corners)
        samples_per_side = 30
        # bottom: x from -half -> +half, y = -half
        bottom = np.column_stack(
            [
                np.linspace(-half, +half, samples_per_side, endpoint=False),
                np.full(samples_per_side, -half),
            ]
        )
        # right: y from -half -> +half, x = +half
        right = np.column_stack(
            [
                np.full(samples_per_side, +half),
                np.linspace(-half, +half, samples_per_side, endpoint=False),
            ]
        )
        # top: x from +half -> -half, y = +half
        top = np.column_stack(
            [
                np.linspace(+half, -half, samples_per_side, endpoint=False),
                np.full(samples_per_side, +half),
            ]
        )
        # left: y from +half -> -half, x = -half
        left = np.column_stack(
            [
                np.full(samples_per_side, -half),
                np.linspace(+half, -half, samples_per_side, endpoint=False),
            ]
        )

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
            m.move_to(
                ax.coords_to_point(
                    xw + speed_scale * vx * dt, yw + speed_scale * vy * dt
                )
            )

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
            pts = [mk.get_center() for mk in markers]
            m.set_points_as_corners(pts)
            m.close_path()

        moving_shell.add_updater(update_shell)

        self.play(Write(static_shell))
        self.wait(1)
        self.play(self.camera.frame.animate.scale(0.75).shift(0.5 * DOWN))

        self.wait(1)
        self.add(moving_shell)  # markers are frozen here
        self.play(start.animate.set_value(1.0))  # start moving (no jump)
        self.wait(6)

        # Stop advection and clean up
        for m in markers:
            m.remove_updater(advect_point)
        self.wait()
        moving_shell.remove_updater(update_shell)
        self.wait(1)
        self.play(self.camera.frame.animate.scale(4 / 3).shift(0.5 * UP))
        self.wait(1)
        self.play(
            FadeOut(moving_shell),
            FadeOut(static_shell),
            FadeOut(airfoil_shape),
            eq4a.animate.shift(3 * UNIT * UP),
        )
        self.wait(1)
        self.play(FadeOut(eq4a))
        self.wait(2)
