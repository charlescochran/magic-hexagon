import math

from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

# Indices of outer ring (clockwise)
O = (0, 1, 2, 6, 11, 15, 18, 17, 16, 12, 7, 3)
# Indices of inner ring (clockwise) and center hex
I = (4, 5, 10, 14, 13, 8, 9)

class HexGridScene(Scene):

    # Hack to prevent Pyright from reporting erroneous reportArgumentType errors
    def play(self, *args, **kwargs):
        super().play(*args, **kwargs)

    def setup(self):
        self.radius = 0.65  # hex size in manim units
        self.grid_pts = []
        for r in range(-2, 3):
            for q in range(-2, 3):
                if abs(r + q) < 3:  # Condition to form hex grid instead of diamond
                    self.grid_pts.append(self.axial_to_cartesian(r, q))
        self.create_grid()
        self.create_labels()

    def axial_to_cartesian(self, r: int, q: int):
        # Coordinate directions:
        # +x points E, +y points N
        # +q points E, +r points SE
        x = self.radius * math.sqrt(3) * (q + r / 2)
        y = self.radius * 3 / 2 * -r  # Negating r because y is up instead of down
        return (x, y, 0)

    def create_grid(self):
        self.grid = VGroup()
        for center in self.grid_pts:
            self.grid.add(
                RegularPolygon(n=6, radius=self.radius, color=BLUE).rotate(PI / 2).move_to(center)
            )
        for hex in self.grid:
            hex.save_state()

    def create_labels(self, permutation=None):
        if permutation is None:
            permutation = range(1, 20)
        self.labels = VGroup(*(Text(str(n), font_size=38) for n in permutation)).arrange()
        self.labels.next_to(self.grid, DOWN, buff=0.35)
        self.shelf_pts = tuple(label.get_center() for label in self.labels)

    def add_sum_lines(self, indices, color, txt, buff=1.0):
        lines = VGroup()
        sums = VGroup()
        for index in indices:
            line, sum = self.add_sum_line(index, color, txt, buff=buff)
            lines.add(line)
            sums.add(sum)
        return lines, sums

    def add_sum_line(self, indices, color, txt, buff=1.0):
        line = Line(self.grid_pts[indices[0]], self.grid_pts[indices[1]])
        line.color = color
        line.set_opacity(0.3)
        line.set_length(float(line.get_length()) + self.radius)
        line.stroke_width = 25
        sum = MathTex(txt, font_size=52, color=color)
        sum.move_to(self.grid_pts[indices[1]])
        sum.shift(buff * line.get_unit_vector())
        return line, sum

    def verify(self, three_rows=False, four_rows=False, five_rows=False, m='38', fade=True):
        lines = []
        sums = []
        if three_rows:
            green_lines, green_sums = self.add_sum_lines(
                ((0, 2), (2, 11), (11, 18), (18, 16), (16, 7), (7, 0)), GREEN_D, m,
            )
            lines.extend(green_lines)
            sums.extend(green_sums)
            self.play(Create(green_lines, lag_ratio=0), Write(green_sums, lag_ratio=0))
        if four_rows:
            self.wait(1)
            blue_lines, blue_sums = self.add_sum_lines(
                ((3, 6), (6, 17), (17, 3)), BLUE_D, m,
            )
            gold_lines, gold_sums = self.add_sum_lines(
                ((1, 15), (15, 12), (12, 1)), GOLD, m,
            )
            lines.extend(blue_lines)
            lines.extend(gold_lines)
            sums.extend(blue_sums)
            sums.extend(gold_sums)
            self.play(
                Create(VGroup(*blue_lines, *gold_lines), lag_ratio=0),
                Write(VGroup(*blue_sums, *gold_sums), lag_ratio=0)
            )
        if five_rows:
            self.wait(1)
            maroon_lines, maroon_sums = self.add_sum_lines(
                ((7, 11), (0, 18), (2, 16)), MAROON_D, m,
            )
            lines.extend(maroon_lines)
            sums.extend(maroon_sums)
            self.play(Create(maroon_lines, lag_ratio=0), Write(maroon_sums, lag_ratio=0))
        if fade and lines and sums:
            self.play(FadeOut(*lines, *sums))

    def choose_first(self, k, first, outer=True):
        K = O if outer else I
        self.move_to_grid((first,), (K[k],))
        self.deselect_grid(K[k])

    def try_second(self, k, second, third, outer=True):
        K = O if outer else I
        self.move_to_grid((second,), (K[k],))
        hint = self.add_hint(K[k+1], third, RED_D)
        self.play(Write(hint))
        self.play(FadeOut(hint))
        self.move_to_shelf(second, color=RED_D)

    def choose_second_and_third(self, k, second, third, bad, outer=True):
        K = O if outer else I
        self.move_to_grid((second,), (K[k],))
        hint = self.add_hint(K[k+1], third, GREEN_D)
        self.play(Write(hint))
        self.deselect_grid(K[k])
        self.select_grid(K[k+1], bad=bad)
        self.move_to_grid((third,), (K[k+1],))
        self.remove(hint)

    def try_inner(self, first, rest, colors):
        self.move_to_grid((first,), (I[0],))
        hints = self.add_inner_hints(rest, colors)
        self.play(LaggedStart(*(Write(hint) for hint in hints), lag_ratio=0.5))
        self.play(FadeOut(*hints))
        self.move_to_shelf(first, color=RED_D)

    def add_inner_hints(self, vals, colors):
        return tuple(self.add_hint(I[i+1], vals[i], colors[i], z_idx=0) for i in range(len(vals)))

    def add_hint(self, grid_idx, n, color, z_idx=-1):
        hint = Text(str(n + 1), font_size=38, color=color)
        hint.set_z_index(z_idx).move_to(self.grid[grid_idx])
        return hint

    def select_grid(self, idx, bad={}):
        self.grid[idx].set_z_index(1)
        self.play(
            self.grid[idx].animate.set_color(LIGHT_PINK).set_stroke(width=8),
            *(self.labels[i].animate.set_color(RED_D) for i in bad),
        )

    def deselect_grid(self, idx):
        self.play(
            self.grid[idx].animate.set_color(BLUE).set_stroke(width=DEFAULT_STROKE_WIDTH),
            self.labels.animate.set_color(WHITE),
        )
        self.grid[idx].set_z_index(0)

    def move_to_grid(self, label_indices, grid_indices):
        self.play(self.labels[label_idx].animate.move_to(self.grid[grid_idx])
                  for label_idx, grid_idx in zip(label_indices, grid_indices))

    def move_to_shelf(self, *indices, color=WHITE):
        self.play(self.labels[idx].animate.move_to(self.shelf_pts[idx]).set_color(color)
                  for idx in indices)

    def change_labels(self, indices, txt):
        self.play(
            Transform(self.labels[i], Text(txt, font_size=38).move_to(self.labels[i].get_center()))
            for i in indices
        )
