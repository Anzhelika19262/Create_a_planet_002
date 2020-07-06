from game_logic import variables
import random
from gui import gui, video
from db import db
import pygame


def check_game_stage(screen):
    auspiciousness_condition = variables.TestCondition().test_auspiciousness_condition()

    if variables.game_stage == 'beginning of the game':
        gui.game_beginning(screen)
        gui.load_sprites()

    elif variables.game_stage == 'information':
        gui.show_back_button(screen)
        gui.show_information(screen)

    elif variables.game_stage == 'achievements':
        gui.show_back_button(screen)
        gui.load_achievements(screen)

    elif 'show video about' in variables.game_stage:
        gui.ask_about_video(screen, variables.video_name)

    elif variables.game_stage == 'choose planet':
        gui.show_back_button(screen)
        gui.show_continue_button(screen)
        gui.choose_planet(screen, variables.planet_sprite)

    elif variables.game_stage == 'change planet':
        if check_achievements('достижение_первая_планета'):
            gui.show_new_achievement(screen, 'достижение_первая_планета')

        gui.change_planet(screen)
        gui.load_pictures_for_widgets(screen)
        gui.show_change_planet_widgets(screen)

        gui.draw_temperature_condition_widgets(screen)
        gui.draw_oxygen_condition_widgets(screen)
        change_auspiciousness()
        gui.draw_auspiciousness_condition_widgets(screen)

        WeatherParameter(screen).check_water_level_parameter()
        WeatherParameter(screen).check_temperature()

        if variables.TestCondition().test_weak_magnetic_field():
            WeatherParameter(screen).change_temperature_parameter(10)  # 10 degrees

        if variables.planets_parameters[variables.planet_name]['wind_speed'] >= 5:  # 5 km/h
            WeatherParameter(screen).change_wind_speed_parameter(-1)

        if auspiciousness_condition:
            LifeParameters(screen).change_life_parameter(5, auspiciousness_condition)

            if variables.planets_parameters[variables.planet_name]['people']:
                LifeParameters(screen).change_people_parameter(5, auspiciousness_condition)

        check_game_event(screen)
        gui.mountains_rise(screen)
        WeatherParameter(screen).check_magnetic_field_parameter()

        if variables.planets_parameters[variables.planet_name]['UFO'] and auspiciousness_condition:
            gui.aliens_fly_to_the_planet(screen, variables.aliens_coordinates)
        elif variables.planets_parameters[variables.planet_name]['UFO']:
            gui.show_new_planets_parameter(screen, 'aliens', 'Goodbye')
            variables.planets_parameters[variables.planet_name]['UFO'] = False

        if variables.TestCondition().test_game_end():
            if check_achievements('конец_игры'):
                gui.show_new_achievement(screen, 'конец_игры')

            if variables.planets_parameters[variables.planet_name]['game_over_question'] is False:
                variables.game_stage = 'game_over'

    elif variables.game_stage == 'game_over':
        gui.is_game_over(screen)


def check_game_event(screen):
    if variables.game_event == 'earthquake':
        gui.earthquake_occurs(screen, variables.earthquake_sprite)

    elif variables.game_event == 'rain':
        gui.rain_comes_down(screen)

    elif variables.game_event == 'lightnings':
        gui.create_thunderbolt(screen)

    elif variables.game_event == 'hurricane':
        gui.create_hurricane(screen, variables.hurricane_sprite)

    elif variables.game_event == 'tsunami':
        WeatherParameter(screen).check_water_level_parameter()

    elif variables.game_event == 'meteorite':
        gui.meteorite_fall(screen)

        if check_achievements('достижение_метеорит'):
            gui.show_new_achievement(screen, 'достижение_метеорит')

    elif variables.game_event == 'UFO':
        gui.aliens_fly_to_the_planet(screen, variables.aliens_coordinates)

    elif variables.game_event == 'mountains':
        max_number_of_mountains = 12
        mountains_coordinate_x, mountains_coordinate_y = random.randint(310, 520), random.randint(90, 310)
        mountains_coordinates = (mountains_coordinate_x, mountains_coordinate_y)

        if len(variables.planets_parameters['Turquesa']['mountain_coordination']) <= max_number_of_mountains:
            variables.planets_parameters['Turquesa']['mountain_coordination'].append(mountains_coordinates)
        variables.game_event = ''

    elif variables.game_event == 'destroy':
        variables.changed_planet = 'Broken_turquesa'
        check_achievements('Broken_turquesa_achievement')

        gui.show_new_achievement(screen, 'Broken_turquesa_achievement', True)


def control_mouse_event(event, screen):
    if event.type == pygame.MOUSEBUTTONUP:
        start_game, achievements, information = gui.game_beginning(screen)
        back_button, continue_button = gui.show_back_button(screen), gui.show_continue_button(screen)

        if variables.game_stage == 'beginning of the game':
            if start_game.collidepoint(event.pos):
                variables.game_stage = 'choose planet'
            elif achievements.collidepoint(event.pos):
                variables.game_stage = 'achievements'
            elif information.collidepoint(event.pos):
                variables.game_stage = 'information'
        elif variables.game_stage in ['information', 'achievements', 'choose planet']:
            if back_button.collidepoint(event.pos):
                variables.game_stage = 'beginning of the game'
            elif continue_button.collidepoint(event.pos) and variables.game_stage == 'choose planet':
                variables.game_stage = 'show video about universe'

        elif 'show video' in variables.game_stage and variables.game_stage not in variables.shown_video:
            yes_button, skip_button = gui.ask_about_video(screen, variables.video_name)

            if skip_button.collidepoint(event.pos):
                variables.game_stage = 'change planet'

            elif yes_button.collidepoint(event.pos):
                gui.load_preview(screen, variables.video_name)
                video.load_video_file(f'позновательные видео/{variables.video_name}.mp4')
                variables.game_stage = 'change planet'

        elif variables.game_stage == 'change planet':
            gui.change_planet(screen)
            gui.load_pictures_for_widgets(screen)
            change_planet_widgets, condition_widgets = gui.show_change_planet_widgets(screen)
            control_change_planet_widgets(screen, change_planet_widgets, event)

            change_coordinates_of_weather(event)

        elif variables.game_stage == 'game_over':
            yes_button, no_button = gui.is_game_over(screen)

            if no_button.collidepoint(event.pos):
                variables.game_stage = 'change planet'
                variables.planets_parameters[variables.planet_name]['game_over_question'] = True

            if yes_button.collidepoint(event.pos):
                variables.running = False

    elif event.type == pygame.MOUSEBUTTONDOWN:
        pass


def control_change_planet_widgets(screen, change_planet_widgets, event):
    weather = WeatherParameter(screen)
    auspiciousness_condition = variables.TestCondition().test_auspiciousness_condition()

    if change_planet_widgets['rain_widget'].collidepoint(event.pos):
        weather.change_water_level_parameter(5, True)  # increase water_level on 5%
        weather.change_temperature_parameter(-5)  # low temperature on 5 degree

    elif change_planet_widgets['sun_widget'].collidepoint(event.pos):
        weather.change_temperature_parameter(5, True)  # increase temperature on 5 degree
        variables.game_event = ''

    elif change_planet_widgets['lightnings_widget'].collidepoint(event.pos):
        variables.game_event = 'lightnings'
        gui.load_sprites()

        AirAndSoilComposition(screen).change_oxygen_parameter(-2, True)

        variables.game_stage = 'show video about lightnings'
        variables.video_name = 'Влияние молнии на атмосферу'

    elif change_planet_widgets['wind_widget'].collidepoint(event.pos):
        weather.change_wind_speed_parameter(1, True)  # the wind gets up on 1 km/h
        weather.change_water_level_parameter(-5)  # decrease water_level on 5 %
        variables.game_event = ''

    elif change_planet_widgets['meteorite_widget'].collidepoint(event.pos):
        variables.game_event = 'meteorite'
        weather.check_meteorite_parameter()

        variables.game_stage = 'show video about destraction'
        variables.video_name = 'Уничтожение планеты.(Способ 3)'

    elif change_planet_widgets['hurricane_widget'].collidepoint(event.pos):
        gui.load_sprites()

        weather.change_wind_speed_parameter(40, True)  # the wind gets up on 40 km/h
        variables.game_event = 'hurricane'

        if variables.planets_parameters[variables.planet_name]['hurricane'] is False:
            variables.planets_parameters[variables.planet_name]['hurricane'] = True
            variables.game_stage = 'show video about hurricane'
            variables.video_name = 'Торнадо'

    elif change_planet_widgets['earthquake_widget'].collidepoint(event.pos):
        weather.change_earthquake_parameter()

    elif change_planet_widgets['tsunami_widget'].collidepoint(event.pos):
        weather.change_water_level_parameter(30, True)  # increase water_level on 30 %
        variables.game_event = ''

    elif change_planet_widgets['mountains_widget'].collidepoint(event.pos):
        magnetic_field = variables.magnetic_fields[
            variables.planets_parameters[variables.planet_name]['magnetic_field']]
        if magnetic_field in ['strong', 'the strongest']:
            if variables.planets_parameters[variables.planet_name]['wind_speed'] <= variables.optimal_wind_speed[1]:
                variables.game_event = 'mountains'

    elif change_planet_widgets['people_widget'].collidepoint(event.pos):
        LifeParameters(screen).change_people_parameter(10, auspiciousness_condition, True)
        # increase number of people

    elif change_planet_widgets['low_temperature_widget'].collidepoint(event.pos):
        weather.change_temperature_parameter(-5, True)  # low temperature on 10 degree

    elif change_planet_widgets['increase_magnetic_field_widget'].collidepoint(event.pos):
        weather.change_magnetic_field_parameter(True)

    elif change_planet_widgets['increase_oxygen_widget'].collidepoint(event.pos):
        AirAndSoilComposition(screen).change_oxygen_parameter(5, True)

    elif change_planet_widgets['alien_invasion_widget'].collidepoint(event.pos):
        LifeParameters(screen).change_ufo_parameter(auspiciousness_condition)


def change_coordinates_of_weather(event):
    new_x_coordinate, new_y_coordinate = event.pos

    if variables.game_event == 'rain':
        variables.rain_coordinate_x = new_x_coordinate
        variables.rain_coordinate_y = new_y_coordinate

    elif variables.game_event == 'hurricane':
        variables.hurricane_coordinates_x = new_x_coordinate
        variables.hurricane_coordinates_y = new_y_coordinate


class WeatherParameter:
    def __init__(self, screen):
        self.screen = screen
        self.condition = variables.TestCondition()

    def change_water_level_parameter(self, percent, show_changes=False):
        if percent == 30 and self.condition.test_tsunami():
            variables.planets_parameters[variables.planet_name]['water_level'] += percent
        elif self.condition.test_rain():
            variables.planets_parameters[variables.planet_name]['water_level'] += percent
            variables.game_event = 'rain'
        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'Water level',
                                           variables.planets_parameters[variables.planet_name]['water_level'])

    def change_temperature_parameter(self, degree, show_changes=False):
        if self.condition.test_temperature():
            variables.planets_parameters[variables.planet_name]['temperature'] += degree
        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'temperature',
                                           variables.planets_parameters[variables.planet_name]['temperature'])

    def check_temperature(self):
        if self.condition.test_low_temperature():
            variables.changed_planet = 'cold_turquesa'
            variables.planets_parameters[variables.planet_name]['life'] = 0
        elif self.condition.test_favorable_temperature():
            variables.changed_planet = 'Turquesa'
        elif self.condition.test_high_temperature():
            variables.changed_planet = 'hot_turquesa'
            variables.planets_parameters[variables.planet_name]['life'] = 0

            variables.game_stage = 'show video about destruction'
            variables.video_name = 'Уничтожение планеты.(Способ 2)'

    def change_wind_speed_parameter(self, speed, show_changes=False):
        variables.planets_parameters[variables.planet_name]['wind_speed'] += speed
        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'wind speed',
                                           variables.planets_parameters[variables.planet_name]['wind_speed'])

    def change_magnetic_field_parameter(self, show_changes=False):
        if self.condition.test_magnetic_field():
            variables.planets_parameters[variables.planet_name]['magnetic_field'] += 1
        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'magnetic field',
                                           variables.magnetic_fields[
                                               variables.planets_parameters[variables.planet_name]['magnetic_field']])

    def check_magnetic_field_parameter(self):
        if self.condition.test_weak_magnetic_field():
            gui.draw_northern_lights(self.screen)

    def change_earthquake_parameter(self):
        if variables.planets_parameters[variables.planet_name]['earthquake']:
            variables.game_event = 'destroy'
        elif variables.planets_parameters[variables.planet_name]['earthquake'] is False:
            variables.planets_parameters[variables.planet_name]['earthquake'] = True
            variables.game_event = 'earthquake'
            consequences_of_meteorite()

    def check_water_level_parameter(self):
        if self.condition.test_high_temperature():
            variables.planets_parameters[variables.planet_name]['water_level'] -= 5

        if 40 > variables.planets_parameters[variables.planet_name]['water_level'] > 20:  # 20% and 40%
            variables.changed_planet = '20-40_water_level_turquesa'

        elif 60 > variables.planets_parameters[variables.planet_name]['water_level'] > 40:  # 40% and 60%
            variables.changed_planet = '40-60_water_level_turquesa'

        elif 100 > variables.planets_parameters[variables.planet_name]['water_level'] > 80:
            variables.changed_planet = '60-80_water_level_turquesa'

    def check_meteorite_parameter(self):
        if variables.planets_parameters[variables.planet_name]['meteorite']:
            variables.game_event = 'destroy'
        else:
            variables.planets_parameters[variables.planet_name]['meteorite'] = True


class LifeParameters:
    def __init__(self, screen):
        self.screen = screen
        self.condition = variables.TestCondition()

    def change_life_parameter(self, new_life, condition, show_changes=False):
        if condition:
            if self.condition.test_life_exist():
                variables.planets_parameters[variables.planet_name]['first_life'] = True
                variables.game_stage = 'show video about life'
                variables.video_name = 'Возникновение жизни'

                if check_achievements('достижение_первая_жизнь'):
                    gui.show_new_achievement(self.screen, 'достижение_первая_жизнь')

            variables.planets_parameters[variables.planet_name]['life'] += new_life

        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'life',
                                           variables.planets_parameters[variables.planet_name]['life'])

    def change_people_parameter(self, new_people, condition, show_changes=False):
        if condition:
            variables.planets_parameters[variables.planet_name]['people'] += new_people
        if show_changes:
            gui.show_new_planets_parameter(self.screen, 'People',
                                           variables.planets_parameters[variables.planet_name]['people'])

    def change_ufo_parameter(self, condition):
        if condition:
            variables.planets_parameters[variables.planet_name]['UFO'] = True
            variables.game_event = 'UFO'

            if check_achievements('достижение_первый_контакт'):
                gui.show_new_achievement(self.screen, 'достижение_первый_контакт')

            if variables.UFOs_video_number <= len(variables.UFO_video):
                variables.UFOs_video_number += 1
                variables.game_stage = 'show video about alien'
                variables.video_name = variables.UFO_video[variables.UFOs_video_number - 1]
        else:
            gui.show_new_planets_parameter(self.screen, 'Message form aliens', 'Adverse conditions')


class AirAndSoilComposition:
    def __init__(self, screen):
        self.screen = screen

    def change_oxygen_parameter(self, percent, show_changes=False):
        variables.planets_parameters[variables.planet_name]['oxygen'] += percent
        if show_changes:
            if 0 < variables.planets_parameters[variables.planet_name]['oxygen'] < variables.highest_level_of_oxygen:
                gui.show_new_planets_parameter(self.screen, 'oxygen level',
                                               variables.planets_parameters[variables.planet_name]['oxygen'])


def change_auspiciousness():
    auspiciousness = variables.planets_parameters[variables.planet_name]['auspiciousness']
    if variables.TestCondition().test_planet_condition() and auspiciousness < 100:  # 100 %
        variables.planets_parameters[variables.planet_name]['auspiciousness'] += 5
    elif auspiciousness > 0 and variables.TestCondition().test_planet_condition() is False:
        variables.planets_parameters[variables.planet_name]['auspiciousness'] -= 5


def check_achievements(achievement):
    if achievement not in db.DATABASE().get_all_achievements():
        db.DATABASE().add_to_date_base(achievement)
        return True


def consequences_of_meteorite():
    variables.planets_parameters[variables.planet_name]['auspiciousness'] = 0
    variables.planets_parameters[variables.planet_name]['life'] = 0
    variables.planets_parameters[variables.planet_name]['people'] = 0
    variables.planets_parameters[variables.planet_name]['oxygen'] = 10
    variables.planets_parameters[variables.planet_name]['temperature'] = -15
