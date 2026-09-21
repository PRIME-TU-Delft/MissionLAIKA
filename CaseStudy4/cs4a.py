import numpy as np
from math import pi
from manim import *
from primescene import *

config.background_color = ManimColor("#FFFFFF")


# --- Airfoil helper ---
def cosine_spacing(n: int) -> np.ndarray:
    k = np.arange(n)
    theta = pi * k / (n - 1)
    return (1.0 - np.cos(theta)) * 0.5


def naca4_coordinates(
    code: str,
    n: int = 201,
    chord: float = 1.0,
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

    # Flip horizontally and center
    pts[:, 0] = -pts[:, 0]
    pts[:, 0] -= (pts[:, 0].max() + pts[:, 0].min()) / 2
    pts[:, 1] -= (pts[:, 1].max() + pts[:, 1].min()) / 2
    return pts


class Lecture4Scene(PrimeScene, MovingCameraScene):
    def construct(self):
        super().construct()
        UNIT = 3 / 4
        dark_blue = ManimColor("#0C2340")
        red = ManimColor("#E03C31")
        yellow = ManimColor("#cc9316")
        blue = ManimColor("#0076C2")

        # Plane body
        plane = (
            SVGMobject("plane.svg", stroke_color=dark_blue, stroke_width=4)
            .scale(0.53)
            .shift(UP * 0.33 + LEFT * 0.13)
        )
        ax = Axes(x_range=[-5, 5, 1], y_range=[-3, 3, 0.5], x_length=14, y_length=8)

        # --- Replace ellipse wing with real airfoil ---
        airfoil_pts = naca4_coordinates(
            "2412", n=201, chord=1.5
        )  # Adjust chord to size wing
        airfoil_shape = VMobject(color=dark_blue, stroke_width=4)
        airfoil_shape.set_points_smoothly(
            [ax.coords_to_point(px, py) for px, py in airfoil_pts]
        )
        airfoil_shape.shift(DOWN * 0.15 + LEFT * 0.13).scale(
            0.4
        )  # Adjust position & size

        # Add plane + wing
        self.add(plane, airfoil_shape)
        self.wait(2)

        # Background grid
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
        self.play(Write(grid))
        self.wait(1)

        self.play(
            LaggedStart(
                Unwrite(plane),
                airfoil_shape.animate.scale(1 / 0.4)
                .shift(UP * 0.15 + RIGHT * 0.13)
                .scale(4 / 1.5),
                lag_ratio=0.5,
            )
        )
        self.wait(1)
