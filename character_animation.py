from math import sqrt

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 1024
SPRITE_SIZE = 100
FRAME_COUNT = 8
FRAME_DURATION = 0.08
MOVE_SPEED = 300

IDLE_RIGHT_ROW = 3
IDLE_LEFT_ROW = 2
MOVE_RIGHT_ROW = 1
MOVE_LEFT_ROW = 0


def handle_events(keys):
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                return False
            if event.key in keys:
                keys[event.key] = True
        elif event.type == SDL_KEYUP and event.key in keys:
            keys[event.key] = False
    return True


def get_movement(keys):
    horizontal = int(keys[SDLK_RIGHT]) - int(keys[SDLK_LEFT])
    vertical = int(keys[SDLK_UP]) - int(keys[SDLK_DOWN])

    if horizontal and vertical:
        diagonal_scale = 1 / sqrt(2)
        return horizontal * diagonal_scale, vertical * diagonal_scale
    return horizontal, vertical


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def draw_character(character, x, y, frame, moving, facing_right):
    if moving:
        row = MOVE_RIGHT_ROW if facing_right else MOVE_LEFT_ROW
    else:
        row = IDLE_RIGHT_ROW if facing_right else IDLE_LEFT_ROW
    character.clip_draw(
        frame * SPRITE_SIZE,
        row * SPRITE_SIZE,
        SPRITE_SIZE,
        SPRITE_SIZE,
        x,
        y,
    )


def main():
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    background = load_image('TUK_GROUND.png')
    character = load_image('animation_sheet.png')

    keys = {
        SDLK_UP: False,
        SDLK_DOWN: False,
        SDLK_LEFT: False,
        SDLK_RIGHT: False,
    }
    x, y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    frame = 0
    animation_time = 0
    facing_right = True
    running = True
    previous_time = get_time()

    while running:
        current_time = get_time()
        elapsed_time = min(current_time - previous_time, 0.1)
        previous_time = current_time

        running = handle_events(keys)
        horizontal, vertical = get_movement(keys)
        moving = horizontal != 0 or vertical != 0

        if horizontal > 0:
            facing_right = True
        elif horizontal < 0:
            facing_right = False

        x += horizontal * MOVE_SPEED * elapsed_time
        y += vertical * MOVE_SPEED * elapsed_time
        half_sprite = SPRITE_SIZE / 2
        x = clamp(x, half_sprite, SCREEN_WIDTH - half_sprite)
        y = clamp(y, half_sprite, SCREEN_HEIGHT - half_sprite)

        if moving:
            animation_time += elapsed_time
            while animation_time >= FRAME_DURATION:
                animation_time -= FRAME_DURATION
                frame = (frame + 1) % FRAME_COUNT
        else:
            animation_time = 0
            frame = 0

        clear_canvas()
        background.draw(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        draw_character(character, x, y, frame, moving, facing_right)
        update_canvas()

    close_canvas()


if __name__ == '__main__':
    main()