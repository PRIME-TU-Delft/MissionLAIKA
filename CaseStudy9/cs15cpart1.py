from manim import *
from primescene import *
config.background_color = ManimColor('#FFFFFF') #ManimColor('#002213')
class Plane(MovingCameraScene, PrimeScene):
    def construct(self):
        super().construct()
        UNIT = 3/4
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31') #ManimColor('#FF5132')
        yellow = ManimColor('#cc9316') #ManimColor('#FFCC12')
        blue = ManimColor('#0076C2') #ManimColor('#46A6FF')

        grid = NumberPlane(background_line_style={
                "stroke_color": dark_blue,
                "stroke_width": 1,
                "stroke_opacity": 0.15
            },
            x_range=(0,72,1),
            y_range=(0, 36, 1),
        ).scale(UNIT)

        self.add(grid)

        #Masses
        left_square = Square(color=dark_blue, side_length=2*UNIT).shift(LEFT * UNIT * 5)
        center_square = Square(color=dark_blue, side_length=4*UNIT)
        right_square = Square(color=dark_blue, side_length=2*UNIT).shift(RIGHT * UNIT * 5)

        self.add(left_square, center_square, right_square)

        spring_color = dark_blue
        #Add springs
        def get_spring():
            start = left_square.get_right()
            end = center_square.get_left()

            def spring_func(t):
                interp = start + t * (end - start)
                offset = np.array([0, 0.2 * np.sin(30 * t), 0])
                return interp + offset

            return ParametricFunction(spring_func, t_range=[0, 1], color=spring_color)

        def get_spring2():
            start = center_square.get_right()
            end = right_square.get_left()

            def spring_func(t):
                interp = start + t * (end - start)
                offset = np.array([0, 0.2 * np.sin(30 * t), 0])
                return interp + offset

            return ParametricFunction(spring_func, t_range=[0, 1], color=spring_color)

        spring_left = always_redraw(get_spring)
        spring_right = always_redraw(get_spring2)
        self.play(Write(spring_left), Write(spring_right))

        group = Group(left_square, right_square)


        self.play(
            LaggedStart(center_square.animate.shift(1 * UNIT * DOWN), group.animate.shift(1 * UNIT * DOWN), lag_ratio=0.3),
        )

        self.play(
            LaggedStart(center_square.animate.shift(2*UNIT* UP), group.animate.shift(2 * UNIT * UP), lag_ratio=0.3),
        )

        for _ in range(3):
            self.play(
                LaggedStart(center_square.animate.shift(2 * UNIT * DOWN), group.animate.shift(2 * UNIT * DOWN),
                            lag_ratio=0.3),
            )

            self.play(
                LaggedStart(center_square.animate.shift(2 * UNIT * UP), group.animate.shift(2 * UNIT * UP),
                            lag_ratio=0.3),
            )


        self.wait()
