import pygame
from pygame.locals import *

import notes
from vector import Vector2

SIZE = Vector2(1000, 800)
key_idx = set(range(24))
BLACK_KEYS = [1, 3, 6, 8, 10]
WHITE_IDX = [i for i in key_idx if (i % 12) not in BLACK_KEYS]
BLACK_IDX = [i for i in key_idx if (i % 12) in BLACK_KEYS]
K_WIDTH = 60
K_HEIGHT = 400
PIANO_POS = Vector2((SIZE[0] - 14 * K_WIDTH) // 2, 200)

white_pos = []
black_pos = []

screen = pygame.display.set_mode((SIZE))
pygame.display.set_caption("Piano Game")
clock = pygame.time.Clock()


def get_keys_pos(screen):

    j = 0
    for i, idx in enumerate(WHITE_IDX):
        x = i * K_WIDTH
        y = 0
        white_pos.append((x, y))
        if j < len(BLACK_IDX) and BLACK_IDX[j] - idx == 1:
            x1 = x + K_WIDTH // 4 * 3
            j += 1
            black_pos.append((x1, y + 1))
    return (white_pos, black_pos)


def draw_piano(screen, white_pos, black_pos):
    for i in white_pos:
        x = i[0] + PIANO_POS[0]
        y = i[1] + PIANO_POS[1]
        pygame.draw.rect(screen, (250, 250, 250), (x, y, K_WIDTH, K_HEIGHT))
        pygame.draw.rect(screen, (10, 10, 10), (x-1, y, K_WIDTH+1, K_HEIGHT+1), 1)
    for i in black_pos:
        x = i[0] + PIANO_POS[0]
        y = i[1] + PIANO_POS[1]
        pygame.draw.rect(screen, (5, 5, 5), (x, y, K_WIDTH//2, K_HEIGHT * 2 // 3))
        pygame.draw.rect(screen, (200, 200, 200), (x-1, y, K_WIDTH//2+1,  K_HEIGHT * 2 // 3 + 1), 1)


def init_game():
    global screen, clock, white_pos, black_pos, is_playing

    white_pos, black_pos = get_keys_pos(screen)
    is_playing = {k: False for k in notes.KEYS}


if __name__ == '__main__':
    init_game()

    while True:
        event = pygame.event.wait()
        if event.type == QUIT:
            exit()

        if event.type in (pygame.KEYDOWN, pygame.KEYUP):
            key = pygame.key.name(event.key)

        if event.type == pygame.KEYDOWN:
            if (key in notes.KEYS.keys()) and (not is_playing[key]):
                notes.KEYS[key].play(fade_ms=50)
                is_playing[key] = True

            elif event.key == pygame.K_ESCAPE:
                exit()

        elif event.type == pygame.KEYUP and key in notes.KEYS.keys():
            # Stops with 50ms fadeout
            notes.KEYS[key].fadeout(50)
            is_playing[key] = False

        clock.tick()
        screen.fill((255, 255, 255))
        draw_piano(screen, white_pos, black_pos)
        pygame.display.update()