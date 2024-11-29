from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

from hex_grid_scene import *

class SolveScene(HexGridScene):

    def construct(self):
        self.add(self.grid, self.labels)

        self.select_grid(O[0])
        self.choose_first(0, 0)

        self.select_grid(O[1])
        self.try_second(1, 1, 34)
        self.try_second(1, 2, 33)
        # skipping ahead
        self.play(self.labels[3:17].animate.set_color(RED_D))
        self.choose_second_and_third(1, 17, 18, range(1, 17))
        self.deselect_grid(O[2])

        self.select_grid(O[3])
        self.choose_second_and_third(3, 1, 16, range(2, 16))
        self.deselect_grid(O[4])

        self.select_grid(O[5])
        self.try_second(5, 2, 17)
        self.try_second(5, 3, 16)
        self.choose_second_and_third(5, 4, 15, set(range(2, 15)) - {4})
        self.deselect_grid(O[6])

        # skipping ahead
        self.move_to_grid((6, 14), (O[7], O[8]))

        self.select_grid(O[9], bad={2, 3, 5, 7})
        self.choose_second_and_third(9, 8, 13, {2, 3, 5, 7, 9, 10, 11, 12})
        hint = self.add_hint(O[11], 23, RED_D)
        self.play(Write(hint))
        self.play(FadeOut(hint))
        self.move_to_shelf(13, color=RED_D)
        self.deselect_grid(O[10])
        self.select_grid(O[9], {2, 3, 5, 7})
        self.move_to_shelf(8, color=RED_D)
        self.move_to_grid((9,), (O[9],))
        hint = self.add_hint(O[10], 12, GREEN_D)
        self.play(Write(hint))
        self.deselect_grid(O[9])

        # skipping ahead
        self.play(FadeOut(hint))
        self.move_to_shelf(*range(19))
        self.move_to_grid((2, 16, 17, 10, 8, 13, 14, 12, 9, 11, 15), O[:-1])
        hint = self.add_hint(O[11], 18, GREEN_D)
        self.play(Write(hint))
        self.select_grid(O[11], bad={0, 1, 3, 4, 5, 6, 7})
        self.choose_first(11, 18)
        self.play(FadeOut(hint))
        self.verify(three_rows=True)
        self.wait(2)

        self.select_grid(I[0])
        self.try_inner(0, (6, -1, 13, -3, 7, 4), (GREEN_D, RED_D, RED_D, RED_D, GREEN_D, GREEN_D))
        self.try_inner(1, (5, 0, 12, -2, 6, 4), (GREEN_D, GREEN_D, RED_D, RED_D, GREEN_D, GREEN_D))
        # skipping ahead
        self.play(self.labels[3:6].animate.set_color(RED_D))
        self.move_to_grid((6,), (I[0],))
        hints = self.add_inner_hints((0, 5, 7, 3, 1, 4), [GREEN_D] * 6)
        self.play(LaggedStart(*(Write(hint) for hint in hints), lag_ratio=0.5))
        self.deselect_grid(I[0])
        self.move_to_grid((0, 5, 7, 3, 1, 4), I[1:])
        self.remove(*hints)
        self.verify(three_rows=True, four_rows=True, five_rows=True)
        self.wait(2)

        hexagons = (self.grid[i] for i in (1, 6, 15, 17, 12, 3))
        rotations = (0, -PI/3, -PI*2/3, PI, PI*2/3, PI/3)
        nums = VGroup(*(
            Text(str(i+1), color=LIGHT_PINK)
                .rotate(rotation)
                .move_to(hex).shift(1.2 * normalize(hex.get_center()))  # pyright: ignore[reportArgumentType]
            for i, (hex, rotation) in enumerate(zip(hexagons, rotations))
        ))
        self.play(Write(nums), run_time=1.5)
        everything = VGroup(self.grid, self.labels, nums)
        for _ in range(6):
            self.play(Rotate(everything, angle=PI/3, about_point=ORIGIN), run_time=0.45)  # pyright: ignore[reportArgumentType]
            self.wait(0.2)
        self.play(FadeOut(nums))
        everything.remove(nums)

        line = Line(self.grid_pts[1], self.grid_pts[17], color=LIGHT_PINK)
        line.set_z_index(2)
        line.stroke_width = 8
        line.set_length(float(line.get_length()) + 3 * self.radius)
        self.play(Create(line))
        self.play(Rotate(everything, PI, axis=UP))
        self.play(Rotate(everything, PI, axis=UP))
        self.play(FadeOut(line))
        self.wait(2)
