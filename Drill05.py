from pico2d import *
import random

TUK_WIDTH, TUK_HEIGHT = 1280, 1024


def load_resources():
    global TUK_ground, character, arrow
    arrow = load_image('hand_arrow.png')
    TUK_ground = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False


def reset_world():
    global running, cx, cy, frame
    global hx, hy
    global sx, sy
    global t
    global action
    running = True
    cx, cy = TUK_WIDTH // 2, TUK_HEIGHT // 2
    frame = 0
    action = 3;
    set_new_target_arrow()


def set_new_target_arrow():
    global t, sx, sy, hx, hy
    t = 0.0
    sx, sy = cx, cy
    hx, hy = random.randint(0, TUK_WIDTH), random.randint(0, TUK_HEIGHT)
    # hx, hy = TUK_WIDTH - 50, TUK_HEIGHT - 50


def render_world():
    clear_canvas()
    TUK_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    arrow.draw(hx, hy)
    character.clip_draw(frame * 100, 100 * action, 100, 100, cx, cy)
    update_canvas()


def update_world():
    global frame
    global cx, cy
    global t
    global action
    frame = (frame + 1) % 8
    action = 1 if cx < hx else 0
    if t <= 1.0:
        cx = (1 - t) * sx + t * hx
        cy = (1 - t) * sy + t * hy
        t += 0.01
    else:
        cx, cy = hx, hy     # 캐릭터 위치를 목적지 위치와 강제로 정확히 일치시킨다.
        set_new_target_arrow()

reset_world()
open_canvas(TUK_WIDTH, TUK_HEIGHT)
hide_cursor()
load_resources()

while running:
    render_world()  # 월드의 현재 내용을 그린다.
    handle_events()  # 사용자 입력을 받아들인다.
    update_world()  # 월드 안의 객체들의 상호작용을 계산하고 그 결과를 update 한다.

    handle_events()

close_canvas()
