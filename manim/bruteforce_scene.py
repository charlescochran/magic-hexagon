from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

from hex_grid_scene import HexGridScene

class BruteforceScene(HexGridScene):

    def construct(self):
        permutation = [13, 1, 11, 18, 3, 15, 12, 6, 4, 14, 10, 5, 17, 2, 19, 9, 7, 8, 16]
        self.create_labels(permutation)
        self.play(FadeIn(self.grid, self.labels))
        self.move_to_grid(range(19), range(19))
        line, sum = self.add_sum_line((0, 2), RED_D, r'25\neq38', buff=1.8)
        self.play(Create(line), Create(sum))
        self.change_labels(range(3, 19), '?')
        self.play(FadeOut(self.labels, self.grid, line, sum))
