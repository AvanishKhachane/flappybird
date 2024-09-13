import json
from random import randint
from time import process_time

import pygame
from pygame import *

from objs import *

init(), display.set_caption("flapy bird")
screen = display.set_mode((86, 30))


def show_txt(font_family, font_size, text, x, y, tf=None, rgb=None):
    show.text(None, font_family, font_size, text, x, y, screen, tf, rgb)


gap = 0
run = True

k = ""
while run:
    screen.fill((255, 255, 255))
    show_txt("Sans Serif.ttf", 20, f"gap: {k}", 0, 0, rgb=(0, 0, 0))
    draw.rect(screen, (0, 0, 0), rect.Rect(38, 0, 47, 30), 1)
    for event in pygame.event.get():
        if event.type == QUIT: run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: run = False
            if [globals()[f"K_{i}"] for i in range(0, 10)].__contains__(event.key) and len(k) < 3: k += str(
                event.key - 48)
            if event.key == K_BACKSPACE: k = k[:-1]
            if event.key == K_RETURN:
                if 108 <= int(k) <= 588 and k != "333": gap = int(k); run = False
                if k == "000": json.dump({"high score": {}}, open("info.json", "w"))
                if k == "333": print(json.load(open("info.json", "r")))
    display.update()

quit()
if gap:
    init(), display.set_caption("flapy bird")
    screen = display.set_mode((360, 640))

def show_obj(obj, x, y, tf=None, part=None): show.object(None, obj, x, y, tf, part, screen)

def sprite(sprite_surface, size, x, y, pos=None):
    return sprites(sprite_surface, size, x, y, screen, pos=pos)


bird_ani = [image.load(f"bird{i}.png") for i in [1, 2, 3]]
bird = sprite("bird1.png", "34x24", 90, 320)
bg = sprite("bg.png", "360x640", 180, 320)
base = sprite("base.png", "360x120", 180, 580)
score_board = sprite("score board.png", "128x128", 184, 215)
pipe_b = sprite("pipe.png", "52x320", 386, randint(360, 588))
pipe_t = sprite("pipe.png", "52x320", pipe_b.x - 26, pipe_b.y - 588)
pipe_t.surface = transform.flip(pipe_b.surface, False, True)
v = 0
g = 0.7
max_v = 10
is_jumping = False
is_falling = True
pv = 2
flaping_speed = 10


def jump():
    global is_jumping, v, is_falling
    if is_falling:
        v += g
        bird.y += v
    if is_jumping:
        v -= g
        bird.y -= v
    if v == 0:
        is_jumping = False
        is_falling = True


score = 0
sc = 0


def base_n_pipes():
    if pipe_b.x >= 386:
        pipe_b.y = randint(360, 588)
        pipe_t.y = pipe_b.y - (320 + gap)
    pipe_b.x -= pv
    pipe_t.x = pipe_b.x
    if pipe_b.x <= -26:
        pipe_b.x = 386
        pipe_t.x = 386
    for i in [1, 2]:
        if base.x <= 0: base.x = 180
    pipe_b.show(), pipe_t.show()
    base.x -= pv
    base.show(), base.show(x=base.x + 180)


t = process_time() + 5
run = True

while process_time() < t and run and gap:
    bg.show(), base.show()
    bird.surface = bird_ani[round(process_time() * flaping_speed) % 3]
    bird.show()
    show_txt("Pinewood.ttf", 40, f"starting in {round(t) - round(process_time())}", 40, 100, rgb=(161, 102, 47))
    for event in pygame.event.get():
        if event.type == QUIT: run = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: run = False
    display.update()


def end(score):
    global run
    pt = round(process_time()) + 5
    base.x = 180
    bird.rotate(0)
    data = json.load(open("info.json", "r"))
    if data["high score"].keys().__contains__(str(gap)):
        if score > data["high score"][str(gap)]: data["high score"][str(gap)] = score
    else:
        data["high score"][str(gap)] = score
    json.dump(data, open("info.json", "w"), indent=4)
    while run and process_time() < pt:
        bg.show()
        base.show()
        bird.surface = bird_ani[round(process_time() * flaping_speed) % 3]
        bird.show()
        score_board.show()
        show_txt("Pinewood.ttf", 20, score, 160, 190, rgb=(161, 102, 47))
        show_txt("Pinewood.ttf", 20, f'for gap {gap} is {json.load(open("info.json", "r"))["high score"][str(gap)]}',
                 130, 250, rgb=(161, 102, 47))
        show_txt("Pinewood.ttf", 40, f"restarting in {pt - round(process_time())}", 15, 100, rgb=(161, 102, 47))
        for event in pygame.event.get():
            if event.type == QUIT: run = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: run = False
        display.update()


def bg_run():
    global score, v, sc
    for i in [1, 2]:
        base.x *= i
        if bird.collision(base):
            bird.y = 260
            pipe_b.x = 386
            v = 0
            end(score)
            score = 0
            break
        base.x /= i
    if bird.collision(pipe_b) or bird.collision(pipe_t):
        bird.y = 260
        pipe_b.x = 386
        v = 0
        end(score)
        score = 0
    if pipe_b.x >= bird.x: sc = score
    if pipe_b.x < bird.x and sc == score: score += 1
    jump()


clock = time.Clock()
while run and gap:
    clock.tick(60), screen.fill((0, 183, 239)), bg.show(), bg_run()
    for event in pygame.event.get():
        if event.type == QUIT: run = False
        if event.type == MOUSEBUTTONDOWN:
            print(mouse.get_pos())
            v = max_v
            is_jumping = True
            is_falling = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: run = False
            if event.key == K_SPACE:
                v = max_v
                is_jumping = True
                is_falling = False
    if not run: break
    base_n_pipes()
    bird.surface = bird_ani[round(process_time() * flaping_speed) % 3]
    bird.rotate(v * 2), bird.show()
    show_txt("Pinewood.ttf", 40, f"score {score}", 0, 0, rgb=(161, 102, 47)), display.update()
