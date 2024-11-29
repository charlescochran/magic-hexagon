import random

from manim import *  # pyright: ignore[reportWildcardImportFromLibrary]

def gen_txt(m):
    color = random.choice((RED_D, GREEN_D, BLUE_D, GOLD, LIGHT_PINK, BLUE))
    size = 36 * random.uniform(0.25, 3)
    x = random.uniform(-7, 7)
    y = random.uniform(-4, 4)
    speed = random.uniform(0.1, 0.6)
    direction = random.choice((LEFT, RIGHT))
    txt = MathTex(m, font_size=size, color=color).move_to((x, y, 0)).set_opacity(0.35)
    def move(mob, dt):
        mob.shift(direction * speed * dt)
    txt.add_updater(move)

    return txt

class WelcomeScene(Scene):

    def construct(self):
        txts = VGroup(*(gen_txt('M') for _ in range(50)))
        self.add(txts)
        self.wait(2)
        msg1 = Text('Solving the')
        msg2 = Text('Magic Hexagon').next_to(msg1, DOWN)
        msgs = VGroup(msg1, msg2).move_to(ORIGIN)
        self.play(Write(msgs), run_time=2)
        self.wait(1)
        self.play(FadeOut(msgs))
        self.wait(1)

class ThanksScene(Scene):

    def construct(self):
        txts = VGroup(*(gen_txt('38') for _ in range(50)))
        self.add(txts)
        self.wait(2)
        thanks = Text('Thanks for watching!')
        self.play(Write(thanks), run_time=2)
        self.wait(10)
        self.play(FadeOut(thanks))
