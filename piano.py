import pygame
from pygame.locals import *
import copy

import notes
from vector import Vector2
from music import Cannon

SIZE = Vector2(1080, 800)

BLACK_KEYS = [1, 3, 6, 8, 10]
WHITE_IDX = [i for i in range(notes.KEY_NUMS) if (i % 12) not in BLACK_KEYS]
BLACK_IDX = [i for i in range(notes.KEY_NUMS) if (i % 12) in BLACK_KEYS]
K_WIDTH = 36
K_HEIGHT = 300
PIANO_POS = Vector2((SIZE[0] - len(WHITE_IDX) * K_WIDTH) // 2, 300)

white_pos = []
black_pos = []
is_playing = {}

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Piano Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Consolas",20)


class Note:
    def __init__(self, pitch, length, start=0):
        self.pitch = pitch
        self.key = notes.keys[pitch]
        self.hit = False
        self.finish = start + length
        self.start = start
        self.note = notes.KEYS[self.key]
        self.done = False

    def play(self, tempo, bar_time):
        global is_playing

        if self.start * tempo <= bar_time < self.finish * tempo - 1:
            is_playing[self.key] = True
            if not self.hit:
                self.note.play(fade_ms=50)
                self.hit = True
        elif bar_time >= self.finish * tempo:
            if not self.done:
                self.stop()
                self.done = True

    def stop(self):
        is_playing[self.key] = False
        self.note.fadeout(50)

    def reset(self):
        self.hit = False
        self.stop()
        self.done = False


class Music:
    def __init__(self, tempo, score, length=4):
        self.tempo = tempo
        self.length = length
        self.score = score
        self.time = -3000
        self.bar = 0
        self.bar_time = -3000

    def play(self, time):

        if self.time >= 0:
            if self.bar_time >= self.tempo * self.length:
                self.bar_time = time
                for n in self.score[self.bar]:
                    n.reset()
                self.bar = (self.bar + 1) % len(self.score)
            for n in self.score[self.bar]:
                n.play(self.tempo, self.bar_time)

        self.bar_time += time
        self.time += time

    def reset(self):
        global is_playing
        self.time = -3000
        self.bar_time = -3000
        is_playing = {k: False for k in notes.KEYS}


def get_keys_pos():
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

    demo = font.render("Press 'SPACE' to watch the demo !", True, (0, 0, 0))
    screen.blit(demo, ((SIZE[0] - demo.get_width( ))//2, 100))
    for idx, i in enumerate(white_pos):
        x = i[0] + PIANO_POS[0]
        y = i[1] + PIANO_POS[1]
        k = notes.keys[WHITE_IDX[idx]]
        color = (192, 247, 252) if is_playing[k] else (250, 250, 250)
        pygame.draw.rect(screen, color, (x, y, K_WIDTH, K_HEIGHT))
        pygame.draw.rect(screen, (10, 10, 10), (x-1, y, K_WIDTH+1, K_HEIGHT+1), 1)
    for idx, i in enumerate(black_pos):
        x = i[0] + PIANO_POS[0]
        y = i[1] + PIANO_POS[1]
        k = notes.keys[BLACK_IDX[idx]]
        color = (192, 247, 252) if is_playing[k] else (10, 10, 10)
        pygame.draw.rect(screen, color, (x, y, K_WIDTH//2, K_HEIGHT * 2 // 3))
        pygame.draw.rect(screen, (200, 200, 200), (x-1, y, K_WIDTH//2+1,  K_HEIGHT * 2 // 3 + 1), 1)


def init_game():
    global screen, clock, white_pos, black_pos, is_playing, game_mode
    game_mode = 1
    white_pos, black_pos = get_keys_pos()
    is_playing = {k: False for k in notes.KEYS}


def parse_score(score):
    music = []
    music_bar = []
    for bar in score:
        music_bar = []
        for note in bar:
            pitch = WHITE_IDX[note[0]]
            length = note[1]
            start = note[2]
            music_bar.append(Note(pitch, length, start))
        music.append(music_bar)
    return music


score = parse_score(Cannon)
demo = Music(400, score)


if __name__ == '__main__':
    init_game()
    t = 0

    while True:
        if game_mode == 0:
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
                elif event.key == pygame.K_SPACE:
                    game_mode = 1
                    demo.reset()

            elif event.type == pygame.KEYUP and key in notes.KEYS.keys():
                # Stops with 50ms fadeout
                notes.KEYS[key].fadeout(50)
                is_playing[key] = False
        else:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_mode = 0
                        demo.reset()

            demo.play(t)

        t = clock.tick(200)
        screen.fill((255, 255, 255))
        draw_piano(screen, white_pos, black_pos)
        pygame.display.update()

