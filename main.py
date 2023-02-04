import json
import os
import sys

import pygame
import requests

FPS = 50
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 450))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ВВОД ДАННЫХ", "",
                  "Введите через пробел координаты (долгота, широта),",
                  "Масштаб отображения карты в градусах,",
                  "После данных нажмите enter"]
    screen.fill(pygame.Color('white'))
    font = pygame.font.Font(None, 30)
    text_coord = 130
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 30
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    string = ''
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print(string)
                    return string.split('space')
                else:
                    string += pygame.key.name(event.key)

        pygame.display.flip()
        clock.tick(FPS)


api_server = "http://static-maps.yandex.ru/1.x/"

data = start_screen()

params = {
    "ll": ",".join([data[0], data[1]]),
    "spn": ",".join([data[2], data[2]]),
    "l": "map"
}
response = requests.get(api_server, params=params)

map_file = "map.png"
with open('map.png', "wb") as file:
    file.write(response.content)

running = True

screen.blit(pygame.image.load(map_file), (0, 0))

pygame.display.flip()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(pygame.Color('cyan'))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()
