from manim import *
from math import pi

WIDTH = 14.2
HALF_WIDTH = WIDTH / 2
QUARTER_WIDTH = WIDTH / 4

HEIGHT = 8
HALF_HEIGHT = HEIGHT / 2
QUARTER_HEIGHT = HEIGHT / 4

TITLE_SIZE = 45
TEXT_SIZE = 30
LEGEND_TEXT_SIZE = 25

class PrimeScene(Scene):
    def construct(self):
        print("Installing PRIME template...")

        texTemplate = TexTemplate()

        # Install the default font for latex
        texTemplate.add_to_preamble(r"\usepackage{amsmath}")
        texTemplate.add_to_preamble(r"\usepackage{amsfonts}")
        texTemplate.add_to_preamble(r"\usepackage{amssymb}")
        texTemplate.add_to_preamble(r"\usepackage{cmbright}")
        texTemplate.add_to_preamble(r"\usepackage[none]{hyphenat}")
        texTemplate.add_to_preamble(r"\usepackage[T1]{fontenc}")
        texTemplate.add_to_preamble(r"\usepackage{color}")
        texTemplate.add_to_preamble(r"\usepackage{tikz}")
        texTemplate.add_to_preamble(r"\usepackage{pgfplots}")
        texTemplate.add_to_preamble(r"\usepackage{graphicx}")
        texTemplate.add_to_preamble(r"\usepackage{adjustbox}")
        texTemplate.add_to_preamble(r"\usepackage{ragged2e}")
        texTemplate.add_to_preamble(r"\usetikzlibrary{arrows,calc,backgrounds}")
        texTemplate.add_to_preamble(r"\renewcommand{\vec}[1]{\mathbf{#1}}")
        texTemplate.add_to_preamble(r"\setlength{\textwidth}{11.346cm}")

        MathTex.set_default(tex_template=texTemplate)

        # Install the default font for normal text
        Text.set_default(font="CMU Bright", slant=ITALIC)

        print("Successfully installed PRIME template")