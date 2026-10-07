from math import sqrt

from pico2d import *


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 1024
BACKGROUND_FILE = 'TUK_GROUND.png'
CHARACTER_FILE = 'animation_sheet.png'
EXIT_KEY = SDLK_ESCAPE
INITIAL_X, INITIAL_Y = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
SPRITE_SIZE = 100
SCREEN_MARGIN = SPRITE_SIZE / 2
SPRITE_COLUMNS = 8
FRAME_COUNT = SPRITE_COLUMNS
INITIAL_FRAME = 0
FRAME_DURATION = 0.08
MOVE_SPEED = 300
MAX_ELAPSED_TIME = 0.1

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
            if event.key == EXIT_KEY:
                return False
            if event.key in keys:
                keys[event.key] = True
        elif event.type == SDL_KEYUP and event.key in keys:
            keys[event.key] = False
    return True


def create_key_state():
    return {
        SDLK_UP: False,
        SDLK_DOWN: False,
        SDLK_LEFT: False,
        SDLK_RIGHT: False,
    }


def load_resources():
    return load_image(BACKGROUND_FILE), load_image(CHARACTER_FILE)


def get_movement(keys):
    horizontal = int(keys[SDLK_RIGHT]) - int(keys[SDLK_LEFT])
    vertical = int(keys[SDLK_UP]) - int(keys[SDLK_DOWN])

    if horizontal and vertical:
        diagonal_scale = 1 / sqrt(2)
        return horizontal * diagonal_scale, vertical * diagonal_scale
    return horizontal, vertical


def is_moving(horizontal, vertical):
    return horizontal != 0 or vertical != 0


def clamp(value, minimum, maximum):
    return max(minimum, min(value, maximum))


def update_position(x, y, horizontal, vertical, elapsed_time):
    x += horizontal * MOVE_SPEED * elapsed_time
    y += vertical * MOVE_SPEED * elapsed_time
    x = clamp(x, SCREEN_MARGIN, SCREEN_WIDTH - SCREEN_MARGIN)
    y = clamp(y, SCREEN_MARGIN, SCREEN_HEIGHT - SCREEN_MARGIN)
    return x, y


def get_animation_row(moving, facing_right):
    if moving:
        return MOVE_RIGHT_ROW if facing_right else MOVE_LEFT_ROW
    return IDLE_RIGHT_ROW if facing_right else IDLE_LEFT_ROW


def update_animation(frame, animation_time, moving, elapsed_time):
    if not moving:
        return INITIAL_FRAME, 0

    animation_time += elapsed_time
    while animation_time >= FRAME_DURATION:
        animation_time -= FRAME_DURATION
        frame = (frame + 1) % FRAME_COUNT
    return frame, animation_time


def get_frame_source_x(frame):
    return frame * SPRITE_SIZE


def draw_background(background):
    background.draw(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)


def update_facing(horizontal, facing_right):
    if horizontal > 0:
        return True
    if horizontal < 0:
        return False
    return facing_right


def draw_character(character, x, y, frame, moving, facing_right):
    row = get_animation_row(moving, facing_right)
    character.clip_draw(
        get_frame_source_x(frame),
        row * SPRITE_SIZE,
        SPRITE_SIZE,
        SPRITE_SIZE,
        x,
        y,
    )


def render(background, character, x, y, frame, moving, facing_right):
    clear_canvas()
    draw_background(background)
    draw_character(character, x, y, frame, moving, facing_right)
    update_canvas()


def get_elapsed_time(previous_time):
    current_time = get_time()
    return current_time, min(current_time - previous_time, MAX_ELAPSED_TIME)


def main():
    open_canvas(SCREEN_WIDTH, SCREEN_HEIGHT)
    background, character = load_resources()

    keys = create_key_state()
    x, y = INITIAL_X, INITIAL_Y
    frame = INITIAL_FRAME
    animation_time = 0
    facing_right = True
    running = True
    previous_time = get_time()

    while running:
        current_time, elapsed_time = get_elapsed_time(previous_time)
        previous_time = current_time

        running = handle_events(keys)
        horizontal, vertical = get_movement(keys)
        moving = is_moving(horizontal, vertical)

        facing_right = update_facing(horizontal, facing_right)

        x, y = update_position(x, y, horizontal, vertical, elapsed_time)

        frame, animation_time = update_animation(
            frame, animation_time, moving, elapsed_time
        )

        render(background, character, x, y, frame, moving, facing_right)

    close_canvas()


if __name__ == '__main__':
    main()