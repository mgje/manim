from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import VMobject

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.numerals import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from mobject.vectorized_mobject import *

from topics.matrix import *
from topics.vector_space_scene import *
from eola.chapter3 import MatrixVectorMultiplicationAbstract


class OpeningQuote(Scene):
    def construct(self):
        words = TextMobject([
            "It is my experience that proofs involving",
            "matrices",
            "can be shortened by 50\\% if one",
            "throws the matrices out."
        ])
        words.scale_to_fit_width(2*SPACE_WIDTH - 2)
        words.to_edge(UP)
        words.split()[1].highlight(GREEN)
        words.split()[3].highlight(BLUE)
        author = TextMobject("-Emil Artin")
        author.highlight(YELLOW)
        author.next_to(words, DOWN, buff = 0.5)

        self.play(FadeIn(words))
        self.dither(2)
        self.play(Write(author, run_time = 3))
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

class ExampleTransformation(LinearTransformationScene):
    def construct(self):
        self.setup()
        self.apply_transposed_matrix([[3, 0], [1, 2]])
        self.dither(2)

class RecapTime(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.teacher_says("Quick recap time!")
        self.random_blink()
        self.dither()
        student = self.get_students()[0]
        everyone = self.get_mobjects()
        everyone.remove(student)
        everyone = VMobject(*everyone)
        self.play(
            ApplyMethod(everyone.fade, 0.7),
            ApplyMethod(student.change_mode, "confused")
        )
        self.play(Blink(student))
        self.dither()
        self.play(ApplyFunction(
            lambda m : m.change_mode("pondering").look(LEFT),
            student
        ))
        self.play(Blink(student))
        self.dither()

class DeterminedByTwoBasisVectors(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors" : False
    }
    def construct(self):
        self.setup()
        i_hat = self.add_vector([1, 0], color = X_COLOR)
        self.add_transformable_label(
            i_hat, "\\hat{\\imath}", "\\hat{\\imath}",
            color = X_COLOR
        )
        j_hat = self.add_vector([0, 1], color = Y_COLOR)
        self.add_transformable_label(
            j_hat, "\\hat{\\jmath}", "\\hat{\\jmath}",
            color = Y_COLOR
        )

        t_matrix = np.array([[2, 2], [-2, 1]])
        matrix = t_matrix.transpose()
        matrix1 = np.array(matrix)
        matrix1[:,1] = [0, 1]
        matrix2 = np.dot(matrix, np.linalg.inv(matrix1))

        self.dither()
        self.apply_transposed_matrix(matrix1.transpose())
        self.apply_transposed_matrix(matrix2.transpose())
        self.dither()

class FollowLinearCombination(LinearTransformationScene):
    def construct(self):
        vect_coords = [-1, 2]
        t_matrix = np.array([[2, 2], [-2, 1]])

        #Draw vectors
        self.setup()
        i_label = self.add_transformable_label(
            self.i_hat, "\\hat{\\imath}", animate = False,
            direction = "right", color = X_COLOR
        )
        j_label = self.add_transformable_label(
            self.j_hat, "\\hat{\\jmath}", animate = False,
            direction = "right", color = Y_COLOR
        )
        vect = self.add_vector(vect_coords)
        vect_array = Matrix(["x", "y"])
        v_equals = TexMobject(["\\vec{\\textbf{v}}", "="])
        v_equals.split()[0].highlight(YELLOW)
        v_equals.next_to(vect_array, LEFT)
        vect_array.add(v_equals)
        vect_array.to_edge(UP, buff = 0.2)
        background_rect = BackgroundRectangle(vect_array)
        vect_array.get_entries().highlight(YELLOW)
        self.play(ShowCreation(background_rect), Write(vect_array))
        self.add_foreground_mobject(background_rect, vect_array)

        #Show scaled vectors
        x, y = vect_array.get_entries().split()
        scaled_i_label = VMobject(x.copy(), i_label)
        scaled_j_label = VMobject(y.copy(), j_label)
        scaled_i = self.i_hat.copy().scale(vect_coords[0])
        scaled_j = self.j_hat.copy().scale(vect_coords[1])
        for mob in scaled_i, scaled_j:
            mob.fade(0.3)
        scaled_i_label_target = scaled_i_label.copy()
        scaled_i_label_target.arrange_submobjects(buff = 0.1)
        scaled_i_label_target.next_to(scaled_i, DOWN)
        scaled_j_label_target = scaled_j_label.copy()
        scaled_j_label_target.arrange_submobjects(buff = 0.1)
        scaled_j_label_target.next_to(scaled_j, LEFT)

        self.show_scaled_vectors(vect_array, vect_coords, i_label, j_label)
        self.apply_transposed_matrix(t_matrix)
        self.show_scaled_vectors(vect_array, vect_coords, i_label, j_label)
        self.record_basis_coordinates(vect_array, vect)

    def show_scaled_vectors(self, vect_array, vect_coords, i_label, j_label):
        x, y = vect_array.get_entries().split()
        scaled_i_label = VMobject(x.copy(), i_label.copy())
        scaled_j_label = VMobject(y.copy(), j_label.copy())
        scaled_i = self.i_hat.copy().scale(vect_coords[0])
        scaled_j = self.j_hat.copy().scale(vect_coords[1])
        for mob in scaled_i, scaled_j:
            mob.fade(0.3)
        scaled_i_label_target = scaled_i_label.copy()
        scaled_i_label_target.arrange_submobjects(buff = 0.1)
        scaled_i_label_target.next_to(scaled_i.get_center(), DOWN)
        scaled_j_label_target = scaled_j_label.copy()
        scaled_j_label_target.arrange_submobjects(buff = 0.1)
        scaled_j_label_target.next_to(scaled_j.get_center(), LEFT)

        self.play(
            Transform(self.i_hat.copy(), scaled_i),
            Transform(scaled_i_label, scaled_i_label_target)
        )
        scaled_i = self.get_mobjects_from_last_animation()[0]
        self.play(
            Transform(self.j_hat.copy(), scaled_j),
            Transform(scaled_j_label, scaled_j_label_target)
        )
        scaled_j = self.get_mobjects_from_last_animation()[0]
        self.play(*[
            ApplyMethod(mob.shift, scaled_i.get_end())
            for mob in scaled_j, scaled_j_label
        ])
        self.dither()
        self.play(*map(FadeOut, [
            scaled_i, scaled_j, scaled_i_label, scaled_j_label,
        ]))

    def record_basis_coordinates(self, vect_array, vect):
        i_label = vector_coordinate_label(self.i_hat)
        i_label.highlight(X_COLOR)
        j_label = vector_coordinate_label(self.j_hat)
        j_label.highlight(Y_COLOR)
        for mob in i_label, j_label:
            mob.scale_in_place(0.8)
            background = BackgroundRectangle(mob)
            self.play(ShowCreation(background), Write(mob))

        self.dither()
        x, y = vect_array.get_entries().split()
        pre_formula = VMobject(
            x, i_label, TexMobject("+"),
            y, j_label
        )
        post_formula = pre_formula.copy()
        pre_formula.split()[2].fade(1)
        post_formula.arrange_submobjects(buff = 0.1)
        post_formula.next_to(vect, DOWN)
        background = BackgroundRectangle(post_formula)
        everything = self.get_mobjects()
        everything.remove(vect)
        self.play(*[
            ApplyMethod(m.fade) for m in everything
        ] + [
            ShowCreation(background, run_time = 2, rate_func = squish_rate_func(smooth, 0.5, 1)),
            Transform(pre_formula.copy(), post_formula, run_time = 2),
            ApplyMethod(vect.set_stroke, width = 7)
        ])
        self.dither()

class MatrixVectorMultiplicationCopy(MatrixVectorMultiplicationAbstract):
    pass ## Here just for stage_animations.py purposes

class RecapOver(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.teacher_says("Recap over!")

class TwoSuccessiveTransformations(LinearTransformationScene):
    CONFIG = {
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_WIDTH,
            "secondary_line_ratio" : 0
        },
    }
    def construct(self):
        self.setup()
        self.apply_transposed_matrix([[2, 1],[1, 2]])
        self.apply_transposed_matrix([[-1, -0.5],[0, -0.5]])
        self.dither()

class RotationThenShear(LinearTransformationScene):
    CONFIG = {
        "foreground_plane_kwargs" : {
            "x_radius" : SPACE_WIDTH,
            "y_radius" : 2*SPACE_WIDTH,
            "secondary_line_ratio" : 0
        },
    }
    def construct(self):
        self.setup()
        rot_words = TextMobject("$90^\\circ$ rotation counterclockwise")
        shear_words = TextMobject("followed by a shear")
        rot_words.highlight(YELLOW)
        shear_words.highlight(PINK)
        VMobject(rot_words, shear_words).arrange_submobjects(DOWN).to_edge(UP)
        for words in rot_words, shear_words:
            words.add_background_rectangle()

        self.play(Write(rot_words, run_time = 1))
        self.add_foreground_mobject(rot_words)
        self.apply_transposed_matrix([[0, 1], [-1, 0]])

        self.play(Write(shear_words, run_time = 1))
        self.add_foreground_mobject(shear_words)
        self.apply_transposed_matrix([[1, 0], [1, 1]])
        self.dither()

class IntroduceIdeaOfComposition(RotationThenShear):
    def construct(self):
        self.setup()
        self.show_composition()
        matrix = self.track_basis_vectors()
        self.show_overall_effect(matrix)

    def show_composition(self):
        words = TextMobject([
            "``Composition''",
            "of a",
            "rotation",
            "and a",
            "shear"
        ])
        words.split()[0].submobject_gradient_highlight(YELLOW, PINK)
        words.split()[2].highlight(YELLOW)
        words.split()[4].highlight(PINK)
        words.add_background_rectangle()
        words.to_edge(UP)

        self.apply_transposed_matrix([[0, 1], [-1, 0]], run_time = 2)
        self.apply_transposed_matrix([[1, 0], [1, 1]], run_time = 2)
        self.play(
            ApplyMethod(self.plane.fade),
            Write(words),
            Animation(self.i_hat),
            Animation(self.j_hat),
        )
        self.dither()

    def track_basis_vectors(self):
        last_words = self.get_mobjects_from_last_animation()[1]
        words = TextMobject([
            "Record where",
            "$\\hat{\\imath}$",
            "and",
            "$\\hat{\\jmath}$",
            "land:"
        ])
        rw, i_hat, a, j_hat, l = words.split()
        i_hat.highlight(X_COLOR)
        j_hat.highlight(Y_COLOR)
        words.add_background_rectangle()
        words.next_to(last_words, DOWN)

        i_coords = vector_coordinate_label(self.i_hat)
        j_coords = vector_coordinate_label(self.j_hat)
        i_coords.highlight(X_COLOR)
        j_coords.highlight(Y_COLOR)
        i_background = BackgroundRectangle(i_coords)
        j_background = BackgroundRectangle(j_coords)

        matrix = Matrix(np.append(
            i_coords.copy().get_mob_matrix(),
            j_coords.copy().get_mob_matrix(),
            axis = 1
        ))
        matrix.next_to(words, RIGHT, aligned_edge = UP)
        col1, col2 = [
            VMobject(*matrix.get_mob_matrix()[:,i])
            for i in 0, 1
        ]
        matrix_background = BackgroundRectangle(matrix)

        self.play(Write(words))
        self.dither()
        self.play(ShowCreation(i_background), Write(i_coords), run_time = 2)
        self.dither()
        self.play(
            Transform(i_background.copy(), matrix_background),
            Transform(i_coords.copy().get_brackets(), matrix.get_brackets()),
            ApplyMethod(i_coords.copy().get_entries().move_to, col1)
        )
        self.dither()
        self.play(ShowCreation(j_background), Write(j_coords), run_time = 2)
        self.dither()
        self.play(
            ApplyMethod(j_coords.copy().get_entries().move_to, col2)
        )
        self.dither()
        matrix = VMobject(matrix_background, matrix)
        return matrix

    def show_overall_effect(self, matrix):
        everything = self.get_mobjects()
        everything = list_difference_update(
            everything, matrix.submobject_family()
        )
        self.play(*map(FadeOut, everything) + [Animation(matrix)])
        new_matrix = matrix.copy()
        new_matrix.center().to_edge(UP)
        self.play(Transform(matrix, new_matrix))
        self.dither()
        self.remove(matrix)

        self.setup()
        everything = self.get_mobjects()
        self.play(*map(FadeIn, everything) + [Animation(matrix)])
        func = self.get_matrix_transformation([[1, 1], [-1, 0]])
        bases = VMobject(self.i_hat, self.j_hat)
        new_bases = VMobject(*[
            Vector(func(v.get_end()), color = v.get_color())
            for v in bases.split()
        ])
        self.play(
            ApplyPointwiseFunction(func, self.plane),
            Transform(bases, new_bases),
            Animation(matrix),
            run_time = 3
        )
        self.dither()

class PumpVectorThroughRotationThenShear(RotationThenShear):
    def construct(self):
        self.setup()
        self.add_vector([2, 3])
        self.apply_transposed_matrix([[0, 1], [-1, 0]], run_time = 2)
        self.apply_transposed_matrix([[1, 0], [1, 1]], run_time = 2)
        self.dither()

class ExplainWhyItsMatrixMultiplication(Scene):
    def construct(self):
        vect = Matrix(["x", "y"])
        vect.get_entries().highlight(YELLOW)

        rot_matrix = Matrix([[0, -1], [1, 0]])
        rot_matrix.highlight(TEAL)
        shear_matrix = Matrix([[1, 1], [0, 1]])
        shear_matrix.highlight(PINK)
        l_paren, r_paren = map(TexMobject, ["\\Big(", "\\Big)"])
        for p in l_paren, r_paren:
            p.scale_to_fit_height(1.4*vect.get_height())
        long_way = VMobject(
            shear_matrix, l_paren, rot_matrix, vect, r_paren
        )
        long_way.arrange_submobjects(buff = 0.1)
        long_way.to_edge(LEFT).shift(UP)

        equals = TexMobject("=").next_to(long_way, RIGHT)

        comp_matrix = Matrix([[1, -1], [1, 0]])
        comp_matrix.highlight_columns(X_COLOR, Y_COLOR)
        vect_copy = vect.copy()
        short_way = VMobject(comp_matrix, vect_copy)
        short_way.arrange_submobjects(buff = 0.1)
        short_way.next_to(equals, RIGHT)

        pairs = [
            (rot_matrix, "Rotation"),
            (shear_matrix, "Shear"),
            (comp_matrix, "Composition"),
        ]
        for matrix, word in pairs:
            brace = Brace(matrix)
            text = TextMobject(word).next_to(brace, DOWN)
            brace.highlight(matrix.get_color())
            text.highlight(matrix.get_color())
            matrix.add(brace, text)
        comp_matrix.split()[-1].submobject_gradient_highlight(TEAL, PINK)

        self.add(vect)
        groups = [
            [rot_matrix],
            [l_paren, r_paren, shear_matrix],
            [equals, comp_matrix, vect_copy],
        ]
        for group in groups:
            self.play(*map(Write, group))
            self.dither()
        self.play(*map(FadeOut, [l_paren, r_paren, vect, vect_copy]))
        comp_matrix.add(equals)
        matrices = VMobject(shear_matrix, rot_matrix, comp_matrix)
        self.play(ApplyMethod(
            matrices.arrange_submobjects, buff = 0.1,
            aligned_edge = UP
        ))
        self.dither()

        arrow = Arrow(rot_matrix.get_right(), shear_matrix.get_left())
        arrow.shift((rot_matrix.get_top()[1]+0.2)*UP)
        words = TextMobject("Read right to left")
        words.submobjects.reverse()
        words.next_to(arrow, UP)
        functions = TexMobject("f(g(x))")
        functions.next_to(words, UP)

        self.play(ShowCreation(arrow))
        self.play(Write(words))
        self.dither()
        self.play(Write(functions))
        self.dither()

class MoreComplicatedExampleVisually(LinearTransformationScene):
    CONFIG = {
        "t_matrix1" : [[1, 1], [-2, 0]],
        "t_matrix2" : [[0, 1], [2, 0]],
    }
    def construct(self):
        self.setup()
        t_matrix1 = np.array(self.t_matrix1)
        t_matrix2 = np.array(self.t_matrix2)
        t_m1_inv = np.linalg.inv(t_matrix1.transpose()).transpose()
        t_m2_inv = np.linalg.inv(t_matrix2.transpose()).transpose()

        m1_mob, m2_mob, comp_matrix = self.get_matrices()

        self.play(Write(m1_mob))
        self.add_foreground_mobject(m1_mob)
        self.dither()
        self.apply_transposed_matrix(t_matrix1)
        self.dither()
        self.play(Write(m1_mob.label))
        self.add_foreground_mobject(m1_mob.label)
        self.dither()
        self.apply_transposed_matrix(t_m1_inv, run_time = 0)
        self.dither()

        self.play(Write(m2_mob))
        self.add_foreground_mobject(m2_mob)
        self.dither()
        self.apply_transposed_matrix(t_matrix2)
        self.dither()
        self.play(Write(m2_mob.label))
        self.add_foreground_mobject(m2_mob.label)
        self.dither()
        self.apply_transposed_matrix(t_m2_inv, run_time = 0)
        self.dither()

        for matrix in t_matrix1, t_matrix2:
            self.apply_transposed_matrix(matrix, run_time = 1)
        self.play(Write(comp_matrix))
        self.add_foreground_mobject(comp_matrix)
        self.dither()
        self.play(*map(FadeOut, [
            self.background_plane,
            self.plane,
            self.i_hat,
            self.j_hat,
        ]) + [
            Animation(m) for m in self.foreground_mobjects
        ])
        self.remove(self.i_hat, self.j_hat)
        self.dither()

    def get_matrices(self):
        m1_mob = Matrix(np.array(self.t_matrix1).transpose())
        m2_mob = Matrix(np.array(self.t_matrix2).transpose())
        comp_matrix = Matrix([["?", "?"], ["?", "?."]])
        #comp_matrix = Matrix([["b", "e"], ["a", "b"]])
        m1_mob.highlight(YELLOW)
        m2_mob.highlight(PINK)
        comp_matrix.get_entries().submobject_gradient_highlight(YELLOW, PINK)

        equals = TexMobject("=")
        equals.next_to(comp_matrix, LEFT)
        comp_matrix.add(equals)
        m1_mob = VMobject(BackgroundRectangle(m1_mob), m1_mob)
        m2_mob = VMobject(BackgroundRectangle(m2_mob), m2_mob)
        comp_matrix = VMobject(BackgroundRectangle(comp_matrix), comp_matrix)
        VMobject(
            m2_mob, m1_mob, comp_matrix
        ).arrange_submobjects(buff = 0.1).to_corner(UP+LEFT).shift(DOWN)

        for i, mob in enumerate([m1_mob, m2_mob]):
            brace = Brace(mob, UP)
            text = TexMobject("M_%d"%(i+1))
            text.next_to(brace, UP)
            brace.add_background_rectangle()
            text.add_background_rectangle()
            brace.add(text)
            mob.label = brace
        return m1_mob, m2_mob, comp_matrix

class MoreComplicatedExampleNumerically(MoreComplicatedExampleVisually):
    def get_result(self):
        return np.dot(self.t_matrix1, self.t_matrix2).transpose()

    def construct(self):
        m1_mob, m2_mob, comp_matrix = self.get_matrices()
        self.add(m1_mob, m2_mob, m1_mob.label, m2_mob.label, comp_matrix)
        result = self.get_result()

        col1, col2 = [
            VMobject(*m1_mob.split()[1].get_mob_matrix()[:,i])
            for i in 0, 1
        ]
        col1.target_color = X_COLOR
        col2.target_color = Y_COLOR
        for col in col1, col2:
            circle = Circle()
            circle.stretch_to_fit_height(m1_mob.get_height())
            circle.stretch_to_fit_width(m1_mob.get_width()/2.5)
            circle.highlight(col.target_color)
            circle.move_to(col)
            col.circle = circle

        triplets = [
            (col1, "i", X_COLOR),
            (col2, "j", Y_COLOR),
        ]
        for i, (col, char, color) in enumerate(triplets):
            self.add(col)
            start_state = self.get_mobjects()
            question = TextMobject(
                "Where does $\\hat{\\%smath}$ go?"%char
            )
            question.split()[-4].highlight(color)
            question.split()[-5].highlight(color)
            question.scale(1.2)
            question.shift(DOWN)
            first = TextMobject("First here")
            first.highlight(color)
            first.shift(DOWN+LEFT)
            first_arrow = Arrow(
                first, col.circle.get_bottom(), color = color
            )
            second = TextMobject("Then to whatever this is")
            second.highlight(color)
            second.to_edge(RIGHT).shift(DOWN)

            m2_copy = m2_mob.copy()
            m2_target = m2_mob.copy()
            m2_target.next_to(m2_mob, DOWN, buff = 1)
            newV = col.copy().split()
            arr = [e.get_tex_string() for e in newV]
            col_vect = Matrix(arr)
            col_vect.highlight(color)
            col_vect.next_to(m2_target, RIGHT, buff = 0.1)
            second_arrow = Arrow(second, col_vect, color = color)

            new_m2_copy = m2_mob.copy().split()[1]
            intermediate = VMobject(
                TexMobject("="),
                col_vect.copy().get_entries().split()[0],
                Matrix(new_m2_copy.get_mob_matrix()[:,0]),
                TexMobject("+"),
                col_vect.copy().get_entries().split()[1],
                Matrix(new_m2_copy.get_mob_matrix()[:,1]),
                TexMobject("=")
            )
            intermediate.arrange_submobjects(buff = 0.1)
            intermediate.next_to(col_vect, RIGHT)

            #product = Matrix(result[:,i
            product = result
            product.next_to(intermediate, RIGHT)

            comp_col = VMobject(*comp_matrix.split()[1].get_mob_matrix()[:,i])

            self.play(Write(question, run_time = 1 ))
            self.dither()
            self.play(
                Transform(question, first),
                ShowCreation(first_arrow),
                ShowCreation(col.circle),
                ApplyMethod(col.highlight, col.target_color)
            )
            self.dither()
            self.play(
                Transform(m2_copy, m2_target, run_time = 2),
                ApplyMethod(col.copy().move_to, col_vect, run_time = 2),
                Write(col_vect.get_brackets()),
                Transform(first_arrow, second_arrow),
                Transform(question, second),
            )
            self.dither()
            self.play(*map(FadeOut, [question, first_arrow]))
            self.play(Write(intermediate))
            self.dither()
            self.play(Write(product))
            self.dither()
            product_entries = product.get_entries()
            self.play(
                ApplyMethod(comp_col.highlight, BLACK),
                ApplyMethod(product_entries.move_to, comp_col)
            )
            self.dither()

            start_state.append(product_entries)
            self.play(*[
                FadeOut(mob)
                for mob in self.get_mobjects()
                if mob not in start_state
            ] + [
                Animation(product_entries)
            ])
            self.dither()

class GeneralMultiplication(MoreComplicatedExampleNumerically):
    def get_result(self):
        # entries = map(TexMobject, [
        #     "ae+bg", "af+bh", "ce+dg", "cf+dh"
        # ])
        # for mob in entries:
        #     mob.split()[0].highlight(PINK)
        #     mob.split()[3].highlight(PINK)
        # for mob in entries[0], entries[2]:
        #     mob.split()[1].highlight(X_COLOR)
        #     mob.split()[4].highlight(X_COLOR)
        # for mob in entries[1], entries[3]:
        #     mob.split()[1].highlight(Y_COLOR)
        #     mob.split()[4].highlight(Y_COLOR)
        # print entries
        # print np.asarray(entries)
        # return np.array(entries).reshape((2, 2))
        #m =  Matrix([["ae+bg", "af+bh"], ["ce+dg", "cf+dh"]])
        m = Matrix([["1", "2"], ["3", "4"]])
        print m
        return m

    def get_matrices(self):
        m1, m2, comp = MoreComplicatedExampleNumerically.get_matrices(self)
        self.add(m1, m2, m1.label, m2.label, comp)
        m1_entries = m1.split()[1].get_entries()
        m2_entries = m2.split()[1].get_entries()
        m2_entries_target = VMobject(*[
            TexMobject(char).move_to(entry).highlight(entry.get_color())
            for entry, char in zip(m2_entries.split(), "abcd")
        ])
        m1_entries_target = VMobject(*[
            TexMobject(char).move_to(entry).highlight(entry.get_color())
            for entry, char in zip(m1_entries.split(), "efgh")
        ])

        words = TextMobject("This method works generally")
        self.play(Write(words, run_time = 2))
        self.play(Transform(
            m1_entries, m1_entries_target,
            submobject_mode = "lagged_start"
        ))
        self.play(Transform(
            m2_entries, m2_entries_target,
            submobject_mode = "lagged_start"
        ))
        self.dither()

        new_comp = Matrix(self.get_result())
        new_comp.next_to(comp.split()[1].submobjects[-1], RIGHT)
        new_comp.get_entries().highlight(BLACK)
        self.play(
            Transform(comp.split()[1].get_brackets(), new_comp.get_brackets()),
            *[
                ApplyMethod(q_mark.move_to, entry)
                for q_mark, entry in zip(
                    comp.split()[1].get_entries().split(),
                    new_comp.get_entries().split()
                )
            ]
        )
        self.dither()
        self.play(FadeOut(words))
        return m1, m2, comp

class MoreComplicatedExampleWithJustIHat(MoreComplicatedExampleVisually):
    CONFIG = {
        "show_basis_vectors" : False,
        "v_coords" : [1, 0],
        "v_color" : X_COLOR,
    }
    def construct(self):
        self.setup()
        self.add_vector(self.v_coords, self.v_color)
        self.apply_transposed_matrix(self.t_matrix1)
        self.dither()
        self.apply_transposed_matrix(self.t_matrix2)
        self.dither()

class MoreComplicatedExampleWithJustJHat(MoreComplicatedExampleWithJustIHat):
    CONFIG = {
        "v_coords" : [0, 1],
        "v_color" : Y_COLOR,
    }

class RoteMatrixMultiplication(NumericalMatrixMultiplication):
    CONFIG = {
        "left_matrix" : [[-3, 1], [2, 5]],
        "right_matrix" : [[5, 3], [7, -3]]
    }

class NeverForget(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.teacher_says("Never forget what \\\\ this represents!")
        self.random_blink()
        self.student_thinks("", student_index = 0)
        def warp(point):
            point += 2*DOWN+RIGHT
            return 20*point/np.linalg.norm(point)
        self.play(ApplyPointwiseFunction(
            warp,
            VMobject(*self.get_mobjects())
        ))

class AskAboutCommutativity(Scene):
    def construct(self):
        l_m1, l_m2, eq, r_m2, r_m1 = TexMobject([
            "M_1",  "M_2", "=", "M_2", "M_1"
        ]).scale(1.5).split()
        VMobject(l_m1, r_m1).highlight(YELLOW)
        VMobject(l_m2, r_m2).highlight(PINK)
        q_marks = TextMobject("???")
        q_marks.highlight(TEAL)
        q_marks.next_to(eq, UP)
        neq = TexMobject("\\neq")
        neq.move_to(eq)

        self.play(*map(Write, [l_m1, l_m2, eq]))
        self.play(
            Transform(l_m1.copy(), r_m1),
            Transform(l_m2.copy(), r_m2),
            path_arc = -np.pi,
            run_time = 2
        )
        self.play(Write(q_marks))
        self.dither()
        self.play(Transform(
            VMobject(eq, q_marks),
            VMobject(neq),
            submobject_mode = "lagged_start"
        ))
        self.dither()

class ShowShear(LinearTransformationScene):
    CONFIG = {
        "title" : "Shear",
        "title_color" : PINK,
        "t_matrix" : [[1, 0], [1, 1]]
    }
    def construct(self):
        self.setup()
        title = TextMobject(self.title)
        title.scale(1.5).to_edge(UP)
        title.highlight(self.title_color)
        title.add_background_rectangle()
        self.add_foreground_mobject(title)

        self.dither()
        self.apply_transposed_matrix(self.t_matrix)
        self.dither()

class ShowRotation(ShowShear):
    CONFIG = {
        "title" : "$90^\\circ$ rotation",
        "title_color" : YELLOW,
        "t_matrix" : [[0, 1], [-1, 0]]
    }

class FirstShearThenRotation(LinearTransformationScene):
    CONFIG = {
        "title" : "First shear then rotation",
        "t_matrix1" : [[1, 0], [1, 1]],
        "t_matrix2" : [[0, 1], [-1, 0]],
        "foreground_plane_kwargs" : {
            "x_radius" : 2*SPACE_WIDTH,
            "y_radius" : 2*SPACE_WIDTH,
            "secondary_line_ratio" : 0
        },
    }
    def construct(self):
        self.setup()
        title_parts = self.title.split(" ")
        title = TextMobject(title_parts)
        for i, part in enumerate(title_parts):
            if part == "rotation":
                title.split()[i].highlight(YELLOW)
            elif part == "shear":
                title.split()[i].highlight(PINK)
        title.scale(1.5)
        self.add_title(title)

        self.apply_transposed_matrix(self.t_matrix1)
        self.apply_transposed_matrix(self.t_matrix2)
        self.i_hat.rotate(-0.01)##Laziness
        self.dither()
        self.write_vector_coordinates(self.i_hat, color = X_COLOR)
        self.dither()
        self.write_vector_coordinates(self.j_hat, color = Y_COLOR)
        self.dither()

class RotationThenShear(FirstShearThenRotation):
    CONFIG = {
        "title" : "First rotation then shear",
        "t_matrix1" : [[0, 1], [-1, 0]],
        "t_matrix2" : [[1, 0], [1, 1]],
    }

class NoticeTheLackOfComputations(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.teacher_says("""
            Notice the lack
            of computations!
        """)
        self.random_blink()

        students = self.get_students()
        random.shuffle(students)
        unit = np.array([-0.5, 0.5])
        self.play(*[
            ApplyMethod(
                pi.change_mode, "pondering",
                rate_func = squish_rate_func(smooth, *np.clip(unit+0.5*i, 0, 1))
            )
            for i, pi in enumerate(students)
        ])
        #self.random_blink()
        self.dither()

class AskAssociativityQuestion(Scene):
    def construct(self):
        morty = Mortimer()
        morty.scale(0.8)
        morty.to_corner(DOWN+RIGHT)
        morty.shift(0.5*LEFT)
        title = TextMobject("Associativity:")
        title.to_corner(UP+LEFT)

        lhs = TexMobject(list("(AB)C"))
        lp, a, b, rp, c = lhs.split()
        rhs = VMobject(*[m.copy() for m in a, lp, b, c, rp])
        point = VectorizedPoint()
        start = VMobject(*[m.copy() for m in point, a, b, point, c])
        for mob in lhs, rhs, start:
            mob.arrange_submobjects(buff = 0.1)
        a, lp, b, c, rp = rhs.split()
        rhs = VMobject(lp, a, b, rp, c)##Align order to lhs
        eq = TexMobject("=")
        q_marks = TextMobject("???")
        q_marks.submobject_gradient_highlight(TEAL_B, TEAL_D)
        q_marks.next_to(eq, UP)
        lhs.next_to(eq, LEFT)
        rhs.next_to(eq, RIGHT)
        start.move_to(lhs)


        self.add(morty, title)
        self.dither()
        self.play(Blink(morty))
        self.play(Write(start))
        self.dither()
        self.play(Transform(start, lhs))
        self.dither()
        self.play(
            Transform(lhs, rhs, path_arc = -np.pi),
            Write(eq)
        )
        self.play(Write(q_marks))
        self.play(Blink(morty))
        self.play(morty.change_mode, "pondering")

        lp, a, b, rp, c = start.split()
        self.show_full_matrices(morty, a, b, c, title)

    def show_full_matrices(self, morty, a, b, c, title):
        everything = self.get_mobjects()
        everything.remove(morty)
        everything.remove(title)
        everything = VMobject(*everything)

        matrices = map(matrix_to_mobject, [
            np.array(list(m)).reshape((2, 2))
            for m in "abcd", "efgh", "ijkl"
        ])
        VMobject(*matrices).arrange_submobjects()

        self.play(everything.to_edge, UP)
        for letter, matrix in zip([a, b, c], matrices):
            self.play(Transform(
                letter.copy(), matrix,
                submobject_mode = "lagged_start"
            ))
            self.remove(*self.get_mobjects_from_last_animation())
            self.add(matrix)
        self.dither()
        self.move_matrix_parentheses(morty, matrices)

    def move_matrix_parentheses(self, morty, matrices):
        m1, m2, m3 = matrices
        parens = TexMobject(["(", ")"])
        parens.scale_to_fit_height(1.2*m1.get_height())
        lp, rp = parens.split()
        state1 = VMobject(
            VectorizedPoint(m1.get_left()),
            m1, m2,
            VectorizedPoint(m2.get_right()),
            m3
        )
        state2 = VMobject(*[
            m.copy() for m in lp, m1, m2, rp, m3
        ])
        state3 = VMobject(*[
            m.copy() for m in m1, lp, m2, m3, rp
        ])
        for state in state2, state3:
            state.arrange_submobjects(RIGHT, buff = 0.1)
        m1, lp, m2, m3, rp = state3.split()
        state3 = VMobject(lp, m1, m2, rp, m3)

        self.play(morty.change_mode, "angry")
        for state in state2, state3:
            self.play(Transform(state1, state))
            self.dither()
        self.play(morty.change_mode, "confused")
        self.dither()

class ThreeSuccessiveTransformations(LinearTransformationScene):
    CONFIG = {
        "t_matrices" : [
            [[2, 1], [1, 2]],
            [[np.cos(-np.pi/6), np.sin(-np.pi/6)], [-np.sin(-np.pi/6), np.cos(-np.pi/6)]],
            [[1, 0], [1, 1]]
        ],
        "symbols_str" : "A(BC)",
        "include_background_plane" : False,
    }
    def construct(self):
        self.setup()
        symbols = TexMobject(list(self.symbols_str))
        symbols.scale(1.5)
        symbols.to_edge(UP)
        a, b, c = None, None, None
        for mob, letter in zip(symbols.split(), self.symbols_str):
            if letter == "A":
                a = mob
            elif letter == "B":
                b = mob
            elif letter == "C":
                c = mob

        symbols.add_background_rectangle()
        self.add_foreground_mobject(symbols)

        brace = Brace(c, DOWN)
        words = TextMobject("Apply this transformation")
        words.add_background_rectangle()
        words.next_to(brace, DOWN)
        brace.add(words)

        self.play(Write(brace, run_time = 1))
        self.add_foreground_mobject(brace)

        last = VectorizedPoint()
        for t_matrix, sym in zip(self.t_matrices, [c, b, a]):
            self.play(
                brace.next_to, sym, DOWN,
                sym.highlight, YELLOW,
                last.highlight, WHITE
            )
            self.apply_transposed_matrix(t_matrix, run_time = 1)
            last = sym
        self.dither()

class ThreeSuccessiveTransformationsAltParens(ThreeSuccessiveTransformations):
    CONFIG = {
        "symbols_str" : "(AB)C"
    }

class ThreeSuccessiveTransformationsSimple(ThreeSuccessiveTransformations):
    CONFIG = {
        "symbols_str" : "ABC"
    }

class ExplanationTrumpsProof(Scene):
    def construct(self):
        greater = TexMobject(">")
        greater.shift(RIGHT)
        explanation = TextMobject("Good explanation")
        explanation.highlight(BLUE)
        proof = TextMobject("Symbolic proof")
        proof.highlight(LIGHT_BROWN)
        explanation.next_to(greater, LEFT)
        proof.next_to(greater, RIGHT)
        explanation.get_center = lambda : explanation.get_right()
        proof.get_center = lambda : proof.get_left()

        self.play(
            Write(explanation),
            Write(greater),
            Write(proof),
            run_time = 1
        )
        self.play(
            explanation.scale_in_place, 1.5,
            proof.scale_in_place, 0.7
        )
        self.dither()

class GoPlay(TeacherStudentsScene):
    def construct(self):
        self.setup()
        self.teacher_says("Go play!", height = 3, width = 5)
        self.play(*[
            ApplyMethod(student.change_mode, "happy")
            for student in self.get_students()
        ])
        self.random_blink()
        student = self.get_students()[-1]
        bubble = ThoughtBubble(direction = RIGHT, width = 6, height = 5)
        bubble.pin_to(student, allow_flipping = False)
        bubble.make_green_screen()
        self.play(
            ShowCreation(bubble),
            student.look, UP+LEFT,
        )
        self.play(student.change_mode, "pondering")
        for x in range(3):
            self.random_blink()
            self.dither(2)

class NextVideo(Scene):
    def construct(self):
        title = TextMobject("""
            Next video: Linear transformations in three dimensions
        """)
        title.scale_to_fit_width(2*SPACE_WIDTH - 2)
        title.to_edge(UP)
        rect = Rectangle(width = 16, height = 9, color = BLUE)
        rect.scale_to_fit_height(6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.dither()
