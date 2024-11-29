from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

from hex_grid_scene import HexGridScene

class IntroScene(HexGridScene):

    def construct(self):
        self.play(Create(self.grid))
        self.play(Write(self.labels))
        permutations = (
            (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18),
            (17, 16, 5, 10, 1, 15, 18, 12, 8, 14, 0, 7, 6, 9, 11, 13, 4, 2, 3),
            (6, 12, 14, 3, 18, 1, 16, 11, 17, 9, 15, 13, 0, 8, 7, 5, 10, 4, 2),
            (0, 3, 15, 7, 2, 13, 11, 9, 18, 6, 1, 8, 5, 16, 4, 12, 14, 10, 17),
        )
        for permutation in permutations:
            self.move_to_grid(range(19), permutation)
        self.change_labels(range(19), '?')

        red_lines, red_sums = self.add_sum_lines(
            ((0, 2), (3, 6), (7, 11), (12, 15), (16, 18)), RED_B, 'M'
        )
        green_lines, green_sums = self.add_sum_lines(
            ((7, 0), (12, 1), (16, 2), (17, 6), (18, 11)), GREEN_B, 'M'
        )
        blue_lines, blue_sums = self.add_sum_lines(
            ((7, 16), (3, 17), (0, 18), (1, 15), (2, 11)), BLUE_B, 'M'
        )
        sum_text = Tex('every line sums to $M$').next_to(self.grid, UP, buff=0.55)
        self.play(Write(sum_text))
        self.play(Create(red_lines), Write(red_sums))
        self.play(ReplacementTransform(red_lines, green_lines),
                  ReplacementTransform(red_sums, green_sums))
        self.play(ReplacementTransform(green_lines, blue_lines),
                  ReplacementTransform(green_sums, blue_sums))
        self.wait(2)  # Discuss pausing to solve puzzle

        self.play(FadeOut(sum_text, self.grid, self.labels))
        color = BLUE_B
        eq = (
            MathTex('5', 'M', '=', r'\sum_{n=1}^{19} n',           color=color),
            MathTex('5', 'M', '=', r'\frac{19(20)}{2}',            color=color),
            MathTex('5', 'M', '=',      '190',                     color=color),
            MathTex(     'M', '=', '{', '190', r'\over', '5', '}', color=color),
            MathTex(     'M', '=', '38',                           color=color),
        )
        self.play(ReplacementTransform(blue_lines, eq[0][3]))
        self.play(ReplacementTransform(blue_sums, eq[0][:2]))
        self.play(Write(eq[0][2]))  # pyright: ignore[reportArgumentType]
        self.play(TransformMatchingTex(eq[0], eq[1], transform_mismatches=True))
        self.play(TransformMatchingTex(eq[1], eq[2], transform_mismatches=True))
        self.play(TransformMatchingTex(eq[2], eq[3]))
        self.play(TransformMatchingTex(eq[3], eq[4], transform_mismatches=True))
        self.play(FadeOut(eq[4]))
