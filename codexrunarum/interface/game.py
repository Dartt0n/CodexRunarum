import sys

import pygame

pygame.font.init()

WIDTH = 900
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.init()
background = pygame.Surface((WIDTH, HEIGHT))

game_over = False

preparation_bar_color = pygame.Color("gray")
spell_frame_color = (255, 255, 255, 255)
spell_inside_color = (0, 0, 0, 255)
font1 = pygame.font.Font("arialmt.ttf", 20)


class Button:

    def __init__(self, x, y, w, h):
        self.colors_of_elements = [
            (255, 255, 255, 255),
            (255, 0, 0, 255),
            (0, 0, 255, 255),
            (0, 255, 0, 255),
        ]
        self.color_index = 0
        self.color = self.colors_of_elements[0]
        self.rect = pygame.Rect(x, y, w, h)

    def color_check(self, x, y):
        if self.rect.collidepoint(x, y):
            self.color_index = (self.colors_of_elements.index(self.color) + 1) % len(
                self.colors_of_elements
            )
            self.color = self.colors_of_elements[self.color_index]
            return True
        return False


class Cell(Button):

    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        self.colors_of_elements = [spell_inside_color, spell_frame_color]
        self.color = self.colors_of_elements[0]

    def change_color_of_activated(self, color):
        if self.color_index == 1:
            self.color = color
        self.colors_of_elements[1] = color


buttons = tuple(Button(50, 560 + 40 * i, 20, 20) for i in range(5))

preparation_bar_rect = pygame.Rect(0, 550, 900, 200)
spell_out = (
    pygame.Rect(100, 570, 160, 160),
    pygame.Rect(260, 570, 160, 160),
    pygame.Rect(420, 570, 160, 160),
    pygame.Rect(580, 570, 160, 160),
    pygame.Rect(740, 570, 160, 160),
)
spell_fields = [[] for i in range(5)]
for i in range(105, 206, 50):
    for j in range(575, 676, 50):
        spell_fields[0].append(Cell(i, j, 50, 50))
for i in range(265, 366, 50):
    for j in range(575, 676, 50):
        spell_fields[1].append(Cell(i, j, 50, 50))
for i in range(425, 526, 50):
    for j in range(575, 676, 50):
        spell_fields[2].append(Cell(i, j, 50, 50))
for i in range(585, 686, 50):
    for j in range(575, 676, 50):
        spell_fields[3].append(Cell(i, j, 50, 50))
for i in range(745, 846, 50):
    for j in range(575, 676, 50):
        spell_fields[4].append(Cell(i, j, 50, 50))
color_buttons = []
for i in range(5):
    color_buttons.append(pygame.Rect(50, 560 + 40 * i, 20, 20))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 50

    def move(self, direction_x, direction_y):
        self.rect.x += self.rect.w * direction_x
        self.rect.y += self.rect.w * direction_y


player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
clock = pygame.time.Clock()
fps = 6

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    clock.tick(fps)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        player.move(1, 0)
    if keys[pygame.K_UP]:
        player.move(0, -1)
    if keys[pygame.K_DOWN]:
        player.move(0, 1)
    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        for i in range(5):
            if spell_out[i].collidepoint(mouse_pos):
                for j in spell_fields[i]:
                    if j.color_check(*mouse_pos):
                        break
                break
        for i in range(5):
            if buttons[i].color_check(*mouse_pos):
                for j in spell_fields[i]:
                    print(j.color)
                    j.change_color_of_activated(buttons[i].color)
                    print(j.color)
                break

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, preparation_bar_color, preparation_bar_rect)
    for i in range(5):
        pygame.draw.rect(screen, spell_frame_color, spell_out[i])
    for i in range(5):
        for j in spell_fields[i]:
            pygame.draw.rect(screen, j.color, j.rect)
    all_sprites.draw(screen)
    for i in range(1, 6):
        screen.blit(font1.render(f"{i}", True, "white"), (5, 560 + 40 * (i - 1)))
    for i in buttons:
        pygame.draw.rect(screen, i.color, i.rect)
    pygame.display.update()
