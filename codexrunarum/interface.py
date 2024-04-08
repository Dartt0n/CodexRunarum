import sys

import pygame

WIDTH = 900
HEIGHT = 750

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.init()
background = pygame.Surface((WIDTH, HEIGHT))

game_over = False

preparation_bar_rect = pygame.Rect(0, 550, 900, 200)
preparation_bar_color = pygame.Color("gray")
spell_frame_color = pygame.Color("white")
spell_inside_color = pygame.Color("black")
spell_1_out = pygame.Rect(100, 570, 160, 160)
spell_2_out = pygame.Rect(260, 570, 160, 160)
spell_3_out = pygame.Rect(420, 570, 160, 160)
spell_4_out = pygame.Rect(580, 570, 160, 160)
spell_5_out = pygame.Rect(740, 570, 160, 160)
spell_1_field = list()
spell_2_field = list()
spell_3_field = list()
spell_4_field = list()
spell_5_field = list()
for i in range(105, 206, 50):
    for j in range(575, 676, 50):
        spell_1_field.append(pygame.Rect(i, j, 50, 50))
for i in range(265, 366, 50):
    for j in range(575, 676, 50):
        spell_2_field.append(pygame.Rect(i, j, 50, 50))
for i in range(425, 526, 50):
    for j in range(575, 676, 50):
        spell_3_field.append(pygame.Rect(i, j, 50, 50))
for i in range(585, 686, 50):
    for j in range(575, 676, 50):
        spell_4_field.append(pygame.Rect(i, j, 50, 50))
for i in range(745, 846, 50):
    for j in range(575, 676, 50):
        spell_5_field.append(pygame.Rect(i, j, 50, 50))



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

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, preparation_bar_color, preparation_bar_rect)
    pygame.draw.rect(screen, spell_frame_color, spell_1_out)
    pygame.draw.rect(screen, spell_frame_color, spell_2_out)
    pygame.draw.rect(screen, spell_frame_color, spell_3_out)
    pygame.draw.rect(screen, spell_frame_color, spell_4_out)
    pygame.draw.rect(screen, spell_frame_color, spell_5_out)
    for i in spell_1_field:
        pygame.draw.rect(screen, spell_inside_color, i)
    for i in spell_2_field:
        pygame.draw.rect(screen, spell_inside_color, i)
    for i in spell_3_field:
        pygame.draw.rect(screen, spell_inside_color, i)
    for i in spell_4_field:
        pygame.draw.rect(screen, spell_inside_color, i)
    for i in spell_5_field:
        pygame.draw.rect(screen, spell_inside_color, i)
    all_sprites.draw(screen)
    pygame.display.update()
