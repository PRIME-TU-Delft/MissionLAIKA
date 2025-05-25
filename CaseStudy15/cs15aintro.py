from manim import *
config.background_color = ManimColor('#00FF00') #ManimColor('#002213')
class Plane(MovingCameraScene):
    def construct(self):
        dark_blue = ManimColor('#0C2340')
        red = ManimColor('#E03C31') #ManimColor('#FF5132')
        yellow = ManimColor('#FFB81C') #ManimColor('#FFCC12')
        blue = ManimColor('#0076C2') #ManimColor('#46A6FF')

        #Airplane is drawn in a different animation on green screen
        airplane_svg = SVGMobject("../assets/AirplaneFront.svg")
        airplane_svg.set_color(WHITE).scale(1.35).shift(UP * 0.3)

        self.play(LaggedStart(*(Write(i) for i in airplane_svg.submobjects), lag_ratio=0.1))
        self.wait(1)
