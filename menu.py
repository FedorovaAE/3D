import pygame
from pygame.locals import *
from cube_game import *

mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('КУБИК РУБИКА')
screen = pygame.display.set_mode((1300, 750), 0, 32)
font = pygame.font.SysFont('impact', 70)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


click = False


def main_menu():
    global click
    while True:
        screen.fill((255, 192, 203))
        cat_surf = pygame.image.load('textures/cubik.png')
        cat_rect = cat_surf.get_rect(bottomright=(1000, 700))
        screen.blit(cat_surf, cat_rect)
        draw_text('Кубик рубика 3D', font, (199, 21, 133), screen, 30, 30)
        mx, my = pygame.mouse.get_pos()
        button_1 = pygame.Rect(100, 200, 300, 100)
        button_2 = pygame.Rect(100, 400, 300, 100)
        if button_1.collidepoint((mx, my)):
            button_12 = pygame.Rect(90, 190, 320, 120)
            pygame.draw.rect(screen, (255, 105, 180), button_12)
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            button_12 = pygame.Rect(90, 390, 320, 120)
            pygame.draw.rect(screen, (255, 105, 180), button_12)
            if click:
                count_sid = 5
                Game(count_sid).run()
        # внешний вид кнопок
        pygame.draw.rect(screen, (199, 21, 133), button_1)
        draw_text('3 X 3', font, (255, 182, 193), screen, 180, 210)
        pygame.draw.rect(screen, (199, 21, 133), button_2)
        draw_text('5 X 5', font, (255, 182, 193), screen, 180, 410)

        # нажатие на кнопку
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(60)


def game():
    running = True
    while running:
        screen.fill((0, 0, 0))
        count_sid = 3
        Game(count_sid).run()
        draw_text('game', font, (123, 104, 238), screen, 20, 20)
        count_sid = 3
        Game(count_sid).run()


        pygame.display.update()
        mainClock.tick(60)


main_menu()
