from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

from hex_grid_scene import *

config.transparent = True

class ThumbnailScene(HexGridScene):

    def construct(self):
        # Generates grid with 15 M-lines and transparent background. Actual
        # thumbnail made with Gimp.
        self.create_grid()
        self.create_labels()
        self.change_labels(range(19), '?')
        self.move_to_grid(range(19), range(19))
        self.add(self.grid, self.labels)
        self.verify(three_rows=True, four_rows=True, five_rows=True, m='M', fade=False)
