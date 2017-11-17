#!/usr/bin/env python

from helpers import *

from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import *

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.matrix import *
from topics.number_line import *
from topics.combinatorics import *
from topics.fractals import *
from topics.objects import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *

from mobject.vectorized_mobject import *
from nn.network import *


class PixelsAsSquares(VGroup):
    CONFIG = {
        "height" : 2,
    }
    def __init__(self, image_mobject, **kwargs):
        VGroup.__init__(self, **kwargs)
        for row in image_mobject.pixel_array:
            for rgba in row:
                square = Square(
                    stroke_width = 0,
                    fill_opacity = rgba[3]/255.0,
                    fill_color = rgba_to_color(rgba/255.0),
                )
                self.add(square)
        self.arrange_submobjects_in_grid(
            *image_mobject.pixel_array.shape[:2],
            buff = 0
        )
        self.replace(image_mobject)

class PixelsFromVect(PixelsAsSquares):
    def __init__(self, vect, **kwargs):
        PixelsAsSquares.__init__(self,
            ImageMobject(layer_to_image_array(vect)),
            **kwargs
        )

class drawSquare(Scene):
    def construct(self):
        square=Square()
        square.rotate(np.pi/8)
        self.play(ShowCreation(
            square,
            run_time = 9
        ))
        self.dither()

class drawBF(Scene):

    def construct(self):
        square=Square()
        square.rotate(np.pi/8)
        self.play(DrawBorderThenFill(
            square
        ))
        self.dither()

class Homoto(Scene):
    def myfunc(self,x, y, z, t):
        return [x*np.sin(t), y + 0.5*np.sin(2*np.pi*t)-t*1/2, z]

    def construct(self):
        square=Square()
        square.rotate(np.pi/13)
        self.play(Homotopy(self.myfunc,
            square,
            run_time = 2
        ))
        self.dither()


class applyWaveS(Scene):
    def construct(self):
        square=Square()
        square.rotate(np.pi/13)
        self.play(ApplyWave(
            square,
            run_time = 6
        ))
        self.dither()

class MatrixToBlank(Scene):
    def construct(self):
        matrix = Matrix([[3, 1], [0, 2]])
        arrow = Arrow(LEFT, RIGHT)
        matrix.to_edge(LEFT)
        arrow.next_to(matrix, RIGHT)
        matrix.add(arrow)
        self.play(Write(matrix))
        self.dither()

class RandMatrix(Scene):
    def construct(self):
        self.show_random_image()


    def show_random_image(self):
        np.random.seed(4)
        rand_vect = np.random.random(28*28)
        image = PixelsFromVect(rand_vect)
        image.to_edge(LEFT)
        image.shift(UP)
        rect = SurroundingRectangle(image)



        self.play(
            ShowCreation(rect),
            LaggedStart(
                DrawBorderThenFill, image,
                stroke_width = 0.5
            )
        )





####### examples
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.rotate(np.pi/8)
        self.play(ShowCreation(square))
        self.play(Transform(square, circle))
        self.dither()

class WarpSquare(Scene):
    def construct(self):
        square = Square()
        self.play(ApplyPointwiseFunction(
            lambda (x, y, z) : complex_to_R3(np.exp(complex(x, y))),
            square
        ))
        self.dither()


class WriteStuff(Scene):
    def construct(self):
        self.play(Write(TextMobject("Stuff").scale(3)))

class mtest1(Scene):
    def construct(self):
        m = Matrix([["?",3],["?","?"]])

        m.rotate(np.pi/13)
        self.play(ApplyWave(
            m,
            run_time = 6
        ))
        self.dither()


class mtest2(Scene):
    def construct(self):
        #m  = Matrix([[1, 0, 0.5], [0.5, 1, 0], [1, 0, 1]])
        m  = Matrix([["1", "0", "0.5"], ["0.5", "1", "0"], ["1", "0", "1"]])

        m.rotate(np.pi/13)
        self.play(ApplyWave(
            m,
            run_time = 6
        ))
        self.dither()


class SierpinskiT(Scene):

    CONFIG = {
        "order" : 4,
    }
    def construct(self):
        sierp = Sierpinski(order = self.order)
        sierp.save_state()

        self.play(FadeIn(
            sierp,
            run_time = 4,
            submobject_mode = "lagged_start"
        ))
        self.dither()

        self.play(FadeOut(
            sierp,
            run_time = 4,
            submobject_mode = "lagged_start"
        ))



        #pf=PentagonalFractal()
        #pf.save_state()

        #self.play(Rotating(
        #    pf,
        #    run_time = 4
        #))
        #self.dither()

        #self.play(FadeOut(
        #    pf,
        #    run_time = 4,
        #    submobject_mode = "lagged_start"
        #))


        sm = Speedometer()
        #sm.save_state()
        sm.move_needle_to_velocity(12)

        self.play(FadeIn(
            sm,
            run_time = 4,
            submobject_mode = "lagged_start"
        ))
        self.dither()








    def create_pi_creature(self):
        return Randolph().to_corner(DOWN+RIGHT)
