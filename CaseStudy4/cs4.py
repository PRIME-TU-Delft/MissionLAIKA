from manim import *
import numpy as np

class EllipseFlow2D(Scene):
    def construct(self):
        # Parameters for the ellipse (streamlined body) and flow
        a, b = 1.5, 0.5      # semi-major and semi-minor axes
        U_inf = -1.0         # free-stream velocity (negative: right→left)

        # Create coordinate plane
        plane = NumberPlane(
            x_range=[-4, 4, 1],
            y_range=[-2, 2, 1],
            axis_config={"stroke_color": GREY, "include_ticks": False}
        )
        self.add(plane)

        # Draw the ellipse representing the plane cross-section
        ellipse = Ellipse(width=2*a, height=2*b, color=WHITE)
        self.add(ellipse)

        # Velocity field around ellipse via circle mapping
        def velocity(point):
            x, y = point
            # map to unit-circle coords
            u = x / a
            v = y / b
            r2 = u**2 + v**2
            if r2 < 1:
                return np.array([0.0, 0.0])
            r = np.sqrt(r2)
            # potential flow around unit circle
            Ur = U_inf * (1 - 1/r2) * (u/r)
            Utheta = -U_inf * (1 + 1/r2) * (v/r)
            # convert to (u,v) components
            Uu = Ur * (u/r) - Utheta * (v/r)
            Uv = Ur * (v/r) + Utheta * (u/r)
            # map back to physical (x,y)
            vx = a * Uu
            vy = b * Uv
            return np.array([vx, vy])

        # Seed points: dense near the body, sparse further away
        seeds = []
        for y0 in np.linspace(-1.0, 1.0, 20):  # more sparse  # dense
            seeds.append([4.0, y0])
        for y0 in np.concatenate((np.linspace(-2.0, -1.2, 4), np.linspace(1.2, 2.0, 4))):  # more sparse  # sparse
            seeds.append([4.0, y0])

        # Compute streamlines
        streamlines = VGroup()
        dt = 0.03
        steps = 220
        for seed in seeds:
            traj = [np.array(seed)]
            p = np.array(seed)
            for _ in range(steps):
                v = velocity(p)
                p = p + v * dt
                traj.append(p)
            path = VMobject()
            path.set_points_smoothly([plane.c2p(x, y) for x, y in traj])
            path.set_stroke(TEAL, 1)
            streamlines.add(path)

        # Animate streamlines drawing around the ellipse
        self.play(LaggedStartMap(Create, streamlines, run_time=7, lag_ratio=0.015))
        self.wait(2)

def ellipse_velocity(x, y, a=1.5, b=0.5, U_inf=-1.0):
    # map to unit-circle coords
    u = x / a
    v = y / b
    r2 = u**2 + v**2
    if r2 < 1:
        return np.array([0.0, 0.0])
    r = np.sqrt(r2)
    # potential flow around unit circle
    Ur = U_inf * (1 - 1/r2) * (u/r)
    Utheta = -U_inf * (1 + 1/r2) * (v/r)
    # convert to (u,v) components
    Uu = Ur * (u/r) - Utheta * (v/r)
    Uv = Ur * (v/r) + Utheta * (u/r)
    # map back to physical (x,y)
    vx = a * Uu
    vy = b * Uv
    return np.array([vx, vy])

class EllipseFlowStreamlines(Scene):
    def construct(self):
        a, b = 1.5, 0.5
        plane = NumberPlane(x_range=[-4,4,1], y_range=[-2,2,1], axis_config={"stroke_color":GREY, "include_ticks":False})
        self.add(plane)
        ellipse = Ellipse(width=2*a, height=2*b, color=WHITE)
        self.add(ellipse)

        # seed points (sparser)
        seeds = []
        for y0 in np.linspace(-1.0, 1.0, 20):
            seeds.append([4.0, y0])
        for y0 in np.concatenate((np.linspace(-2.0, -1.2, 4), np.linspace(1.2, 2.0, 4))):
            seeds.append([4.0, y0])

        streamlines = VGroup()
        dt = 0.03
        steps = 220
        for seed in seeds:
            p = np.array(seed)
            traj = [p.copy()]
            for _ in range(steps):
                v = ellipse_velocity(p[0], p[1], a, b)
                p = p + v * dt
                traj.append(p.copy())
            path = VMobject()
            path.set_points_smoothly([plane.c2p(x, y) for x, y in traj])
            path.set_stroke(TEAL, 1)
            streamlines.add(path)

        self.play(LaggedStartMap(Create, streamlines, run_time=7, lag_ratio=0.015))
        self.wait(2)

class EllipseFlowVectors(Scene):
    def construct(self):
        a, b = 1.5, 0.5
        plane = NumberPlane(x_range=[-4,4,1], y_range=[-2,2,1], axis_config={"stroke_color":GREY, "include_ticks":False})
        self.add(plane)
        ellipse = Ellipse(width=2*a, height=2*b, color=WHITE)
        self.add(ellipse)

        # sample grid points with increased density but shorter vectors
        xs = np.linspace(-4, 4, 25)
        ys = np.linspace(-2, 2, 20)  # grid density unchanged
        ys = np.linspace(-2, 2, 20)
        vectors = VGroup()
        for x in xs:
            for y in ys:
                vx, vy = 0.3 * ellipse_velocity(x, y, a, b)
                # skip inside ellipse
                if (x/a)**2 + (y/b)**2 < 1:
                    continue
                start = plane.c2p(x, y)
                # shorter arrows for clarity
                end = plane.c2p(x + 0.4*vx, y + 0.4*vy)  # increase arrow length
                arrow = Arrow(
                    start, end,
                    buff=0,
                    stroke_width=0.8,  # slightly thicker arrows,
                    tip_length=0.08,  # slightly larger tips,
                    max_stroke_width_to_length_ratio=20
                )
                vectors.add(arrow)

        self.play(*(GrowArrow(i) for i in vectors), run_time=4)
        self.wait(2)

