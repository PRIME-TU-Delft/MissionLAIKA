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


try:
    from manim import (
        Scene,
        Axes,
        VGroup,
        VMobject,
        StreamLines,
        ArrowVectorField,
        BLUE,
        YELLOW,
    )
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
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

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
        self.add(grid)

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

        sl = StreamLines(
            lambda p: vfield_func(ax.point_to_coords(p)),
            x_range=[-7, 9, 0.15],
            y_range=[-4, 4, 0.15],
            stroke_opacity=0.7,
            max_anchors_per_line=50,
            colors=[RED, BLUE, RED],
        )

        arrow_field = ArrowVectorField(
            lambda p: vfield_func(ax.point_to_coords(p)),
            x_range=[-5, 5, 0.5],
            y_range=[-3, 3, 0.5],
            length_func=lambda norm: 0.3 * norm,
            color=dark_blue,
        )

        self.add(airfoil_shape)
        self.wait(1)
        self.play(Write(arrow_field))
        self.wait(1)
        self.play(ApplyWave(arrow_field))
        self.wait(1)
        self.add(sl)
        sl.start_animation(warm_up=True, flow_speed=2.0)
        self.wait(9)
        self.play(sl.end_animation())


if __name__ == "__main__":
    code = "0012"
    pts = naca4_coordinates(code, n=101, chord=4.0)
    xv, yv, xc, yc, nx, ny = build_vortex_collocation(pts)
    A = build_A(xv, yv, xc, yc, nx, ny)
    rhs = build_rhs(1.0, 4.0, nx, ny)
    Gamma = solve_gamma(A, rhs)
    print("Γ (first 5):", Gamma[:5])
