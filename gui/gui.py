import os
import random
import time
import pygame
from gui import sprites
from db import db
from game_logic import variables

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)


def load_image(name, colorkey=None):
    fullname = os.path.join('img', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


def load_sprites():
    x, y = random.randint(290, 620), random.randint(90, 410)

    variables.planet_sprite = sprites.Sprites(load_image('спрайт_планеты.png'), 6, 7, 520, 150)
    variables.earthquake_sprite = sprites.Sprites(load_image('спрайт_землетрясение.png'), 4, 2, 280, 75)
    variables.thunderbolt_sprite = sprites.Sprites(load_image('молния_спрайт.png', True), 10, 1, x, y)
    variables.meteorite_sprite = sprites.Sprites(load_image('падение_метеорита_спрайт.jpg'), 4, 3, 280, 75)
    variables.hurricane_sprite = sprites.Sprites(load_image('спрайт_урагана.png', True), 8, 3, x, y)


def game_beginning(screen):
    screen.blit(load_image('main_view.jpg'), (-20, 0))
    screen.blit(load_image('logo.jpg'), (0, 0))
    start_game_button = pygame.draw.rect(screen, (255, 255, 255), (785, 443, 115, 30), 3)
    screen.blit(load_image('кнопка_start_game.jpg'), (785, 445))
    achievements_button = pygame.draw.rect(screen, (255, 255, 255), (0, 443, 125, 30), 3)
    screen.blit(load_image('кнопка_achievements.jpg'), (1, 445))
    information_button = pygame.draw.rect(screen, (255, 255, 255), (150, 443, 30, 30), 3)
    screen.blit(load_image('кнопка_information.jpg'), (150, 445))
    return start_game_button, achievements_button, information_button


def choose_planet(screen, planet_sprite):
    screen.blit(load_image('выбор планеты.jpg'), (375, 0))
    screen.blit(load_image('характеристика_планеты_turquesa.jpg'), (80, 80))
    planet_sprite.update(screen)
    clock.tick(10)


def show_information(screen):
    screen.blit(load_image('информация.jpg'), (380, 0))
    screen.blit(load_image('описание.jpg'), (30, 100))


def load_achievements(screen):
    screen.blit(load_image('достижения.jpg'), (375, 0))

    achievements = db.DATABASE().get_all_achievements()
    img_x_coordinate, img_y_coordinate = 70, 80
    max_number_of_element = 7

    for element_number in range(1, len(achievements) + 1):
        if element_number % max_number_of_element == 0:
            img_x_coordinate = 70
            img_y_coordinate += 120
        else:
            screen.blit(load_image(f'{achievements[element_number - 1]}.jpg'), (img_x_coordinate, img_y_coordinate))
            img_x_coordinate += 110

    text = font.render('Всего достижений: 14', 1, (255, 255, 255))
    screen.blit(text, (30, 470))

    pygame.display.flip()


def show_continue_button(screen):
    continue_button = pygame.draw.rect(screen, (255, 255, 255), (795, 5, 98, 30), 3)
    screen.blit(load_image('кнопка_continue.jpg'), (797, 6))
    return continue_button


def show_back_button(screen):
    screen.fill((0, 0, 0))
    back_button = pygame.draw.rect(screen, (255, 255, 255), (5, 5, 70, 30), 3)
    screen.blit(load_image('кнопка_back.jpg'), (7, 7))
    return back_button


def show_change_planet_widgets(screen):
    function_widgets = {'rain_widget': pygame.draw.rect(screen, (255, 255, 255), (30, 100, 85, 55), 3),
                        'sun_widget': pygame.draw.rect(screen, (255, 255, 255), (30, 150, 85, 55), 3),
                        'lightnings_widget': pygame.draw.rect(screen, (255, 255, 255), (30, 200, 85, 55), 3),
                        'wind_widget': pygame.draw.rect(screen, (255, 255, 255), (30, 250, 85, 55), 3),
                        'meteorite_widget': pygame.draw.rect(screen, (255, 255, 255), (30, 350, 85, 55), 3),
                        'hurricane_widget': pygame.draw.rect(screen, (255, 255, 255), (790, 100, 85, 55), 3),
                        'earthquake_widget': pygame.draw.rect(screen, (255, 255, 255), (790, 150, 85, 55), 3),
                        'tsunami_widget': pygame.draw.rect(screen, (255, 255, 255), (790, 200, 85, 55), 3),
                        'mountains_widget': pygame.draw.rect(screen, (255, 255, 255), (790, 250, 85, 55), 3),
                        'people_widget': pygame.draw.rect(screen, (255, 255, 255), (790, 350, 85, 55), 3),
                        'low_temperature_widget': pygame.draw.rect(screen, (255, 255, 255), (250, 430, 100, 55), 3),
                        'increase_magnetic_field_widget': pygame.draw.rect(screen, (255, 255, 255),
                                                                           (350, 430, 100, 55), 3),
                        'increase_oxygen_widget': pygame.draw.rect(screen, (255, 255, 255), (450, 430, 100, 55), 3),
                        'alien_invasion_widget': pygame.draw.rect(screen, (255, 255, 255), (550, 430, 100, 55), 3)}
    condition_widgets = {'condition': pygame.draw.rect(screen, (255, 255, 255), (775, 30, 100, 30), 3),
                         'temperature': pygame.draw.rect(screen, (255, 255, 255), (30, 30, 150, 30), 3),
                         'oxygen': pygame.draw.rect(screen, (255, 255, 255), (200, 30, 100, 30), 3)}
    return function_widgets, condition_widgets


def load_pictures_for_widgets(screen):
    screen.blit(load_image('rain_widget.png'), (40, 103))
    screen.blit(load_image('sun_widget.png'), (55, 156))
    screen.blit(load_image('lightnings_widget.png'), (45, 208))
    screen.blit(load_image('wind_widget.png'), (40, 260))
    screen.blit(load_image('meteorite_widget.png'), (50, 353))
    screen.blit(load_image('hurricane_widget.png'), (810, 103))
    screen.blit(load_image('earthquake_widget.png'), (810, 156))
    screen.blit(load_image('tsunami_widget.png'), (805, 205))
    screen.blit(load_image('mountains_widget.png'), (810, 256))
    screen.blit(load_image('people_widget.png'), (800, 356))
    screen.blit(load_image('кнопка_уменьшить_температуру.jpg'), (253, 433))
    screen.blit(load_image('кнопка_увеличить_магнитное_поле.jpg'), (353, 431))
    screen.blit(load_image('кнопка_увеличить_кислород.jpg'), (453, 433))
    screen.blit(load_image('кнопка_инопланетное_вторжение.png'), (553, 433))


def draw_temperature_condition_widgets(screen):
    screen.blit(font.render("Температура", 1, (255, 255, 255)), (30, 10))
    temperature = variables.planets_parameters[variables.planet_name]['temperature']
    if temperature >= 0:
        pygame.draw.rect(screen, pygame.Color('red'), (32, 32, 75 + temperature, 27))
    else:
        pygame.draw.rect(screen, pygame.Color('blue'), (32, 32, 75 + temperature, 27))


def draw_auspiciousness_condition_widgets(screen):
    screen.blit(font.render("Благоприятность", 1, (255, 255, 255)), (765, 10))
    auspiciousness = variables.planets_parameters[variables.planet_name]['auspiciousness']
    pygame.draw.rect(screen, pygame.Color('green'), (778, 32, auspiciousness - 3, 27))


def draw_oxygen_condition_widgets(screen):
    screen.blit(font.render("Уровнь кислорода", 1, (255, 255, 255)), (185, 10))
    oxygen = variables.planets_parameters[variables.planet_name]['oxygen']
    pygame.draw.rect(screen, pygame.Color('blue'), (202, 32, oxygen, 27))


def load_preview(screen, name):
    screen.fill((0, 0, 0))
    text = font.render(name, 1, (255, 255, 255))
    text_x, text_y = 450 - (text.get_width() // 2), 150 - (text.get_height() // 2)
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()


def change_planet(screen):
    screen.fill((0, 0, 0))
    screen.blit(load_image(f'{variables.changed_planet}.jpg'), (280, 75))


def show_new_planets_parameter(screen, condition_name, changed_planet_parameter):
    text = font.render(f'{condition_name.title()}: {changed_planet_parameter}', 1, (255, 255, 255))
    screen.blit(text, (30, 430))
    draw_oxygen_condition_widgets(screen)
    draw_temperature_condition_widgets(screen)
    draw_auspiciousness_condition_widgets(screen)
    pygame.display.flip()
    time.sleep(3.0)


def earthquake_occurs(screen, earthquake_sprite):
    for i in range(7):
        earthquake_sprite.update(screen)
        pygame.display.flip()
        clock.tick(5)
    variables.changed_planet = 'turquesa_after_earthquake'
    variables.game_event = ''


def rain_comes_down(screen):
    x = variables.rain_coordinate_x
    y = variables.rain_coordinate_y
    screen.blit(load_image('rain.png', True), (x, y))
    pygame.display.flip()


def draw_northern_lights(screen):
    screen.blit(load_image('северное_сияние_часть_1.png', True), (280, 20))
    screen.blit(load_image('северное_сияние_часть_2.png', True), (445, 15))


def create_thunderbolt(screen):
    variables.thunderbolt_sprite.update(screen)
    pygame.display.flip()
    clock.tick(10)


def mountains_rise(screen):
    mountains_coordinates = variables.planets_parameters[variables.planet_name]['mountain_coordination']
    for i in range(len(mountains_coordinates)):
        screen.blit(load_image('turquesa_горы.png', True), mountains_coordinates[i])
    pygame.display.flip()


def meteorite_fall(screen):
    pygame.draw.rect(screen, pygame.Color('black'), (280, 75, 342, 342))
    for i in range(11):
        variables.meteorite_sprite.update(screen)
        pygame.display.flip()
        clock.tick(5)
    variables.changed_planet = 'turquesa_after_meteorite_fall'
    variables.game_event = ''


def aliens_fly_to_the_planet(screen, aliens_coordinates):
    screen.blit(load_image('НЛО.png', True), aliens_coordinates)


def create_hurricane(screen, hurricane_sprite):
    hurricane_sprite.update(screen)
    pygame.display.flip()
    clock.tick(5)


def ask_about_video(screen, video_name):
    screen.fill((0, 0, 0))
    text = font.render(f'Хотите ли Вы посмотреть научное видео {video_name}?', 1, (255, 255, 255))
    text2 = font.render('Это займет небольше 10-15 минут.', 1, (255, 255, 255))
    text_x, text_y = 450 - (text.get_width() // 2), 250 - (text.get_height() // 2)

    screen.blit(text, (text_x, text_y))
    screen.blit(text2, (300, 450))

    yes_button = pygame.draw.rect(screen, (255, 255, 255), (750, 280, 50, 30), 3)
    skip_button = pygame.draw.rect(screen, (255, 255, 255), (100, 280, 50, 30), 3)

    screen.blit(load_image('кнопка_yes.png'), (753, 283))
    screen.blit(load_image('кнопка_skip.png'), (103, 283))
    return yes_button, skip_button


def show_change_optional_planet_widgets(screen):  # в разработке...
    new_function_widgets = {'cities': pygame.draw.rect(screen, (255, 255, 255), (30, 300, 85, 55), 3),
                            'wars': pygame.draw.rect(screen, (255, 255, 255), (790, 300, 85, 55), 3),
                            'racket': pygame.draw.rect(screen, (255, 255, 255), (30, 400, 85, 55), 3),
                            'natural satellite': pygame.draw.rect(screen, (255, 255, 255), (790, 400, 85, 55), 3)}
    return new_function_widgets


def is_game_over(screen):
    screen.fill((0, 0, 0))
    text = font.render('Вы достигли максимального уровня развития. Хотите ли вы закончить игру?', 1, (255, 255, 255))
    text_x, text_y = 450 - (text.get_width() // 2), 250 - (text.get_height() // 2)
    screen.blit(text, (text_x, text_y))

    yes_button = pygame.draw.rect(screen, (255, 255, 255), (750, 280, 50, 30), 3)
    no_button = pygame.draw.rect(screen, (255, 255, 255), (100, 280, 50, 30), 3)

    screen.blit(load_image('кнопка_yes.png'), (753, 283))
    screen.blit(load_image('кнопка_skip.png'), (103, 283))
    return yes_button, no_button


def show_new_achievement(screen, achievement_name, end_game=False):
    screen.fill((0, 0, 0))
    text = font.render('Вы получили новое достижение:', 1, (255, 255, 255))
    text_x, text_y = 450 - (text.get_width() // 2), 100 - (text.get_height() // 2)
    screen.blit(text, (text_x, text_y))

    achievement_img = f'{achievement_name}.jpg'
    screen.blit(load_image(achievement_img), (400, 150))

    img_name = font.render(f'{variables.achievement_name[f"{achievement_name}"]}', 1, (255, 255, 255))
    screen.blit(img_name, (400, 270))

    pygame.display.flip()
    time.sleep(5)

    if end_game:
        variables.game_stage = 'choose planet'
