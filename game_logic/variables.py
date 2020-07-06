size = width, height = 900, 500
running = True

game_stage = 'beginning of the game'
game_event = ''
video_name = 'Возникновение вселеной'

shown_video = []

UFOs_video_number = 0
UFO_video = ['Жизнь на Марсе', 'Инопланетяне и мы', 'Сигнал для инопланетян']

planet_sprite = None
earthquake_sprite = None
thunderbolt_sprite = None
meteorite_sprite = None
hurricane_sprite = None

planet_name = 'Turquesa'
changed_planet = 'Turquesa'

highest_temperature = 65
lowest_temperature = -75
temperature_for_rain = [0, 40]
favorable_temperature = [-15, 40]
normal_level_of_oxygen = [20, 80]
optimal_wind_speed = [0, 30]
level_of_water_for_tsunami = 30
highest_level_of_oxygen = 100
magnetic_fields = ['weak', 'more strong', 'strong', 'the strongest']

planets_parameters = {
    'Turquesa': {
        'UFO': False,
        'life': 0,
        'people':  0,
        'first_life': False,
        'oxygen': 2,
        'hurricane': False,
        'tsunami': False,
        'water_level': 0,
        'meteorite': False,
        'earthquake': False,
        'wind_speed': 20,
        'temperature': -75,
        'show_question': 0,
        'magnetic_field': 2,
        'auspiciousness': 0,
        'mountain_coordination': [],
        'game_over_question': False
    }
}

achievement_name = {'достижение_метеорит': 'Падение метеорита',
                    'достижение_первая_жизнь': 'Первая жизнь',
                    'достижение_первая_планета': 'Первая планета',
                    'Broken_turquesa_achievement': 'Полное разрушение',
                    'достижение_первый_контакт': 'Внеземная жизнь',
                    'конец_игры': 'Максимально благопрятные условия'}

rain_coordinate_x, rain_coordinate_y = 300, 90
thunderbolt_coordinate_x, thunderbolt_coordinate_y = 0, 0
aliens_coordinates = (340, 80)


class TestCondition:
    def test_tsunami(self):
        if planets_parameters['Turquesa']['water_level'] >= level_of_water_for_tsunami:
            return True

    def test_rain(self):
        if temperature_for_rain[0] <= planets_parameters[planet_name]['temperature'] <= temperature_for_rain[1]:
            return True

    def test_water_level(self):
        if planets_parameters[planet_name]['water_level'] > 10:  # 10%
            return True

    def test_temperature(self):
        if lowest_temperature <= planets_parameters[planet_name]['temperature'] < highest_temperature:
            return True

    def test_low_temperature(self):
        if lowest_temperature <= planets_parameters[planet_name]['temperature'] <= lowest_temperature + 10:  # degree
            return True

    def test_high_temperature(self):
        if temperature_for_rain[1] <= planets_parameters[planet_name]['temperature'] <= highest_temperature:
            return True

    def test_favorable_temperature(self):
        if favorable_temperature[0] <= planets_parameters[planet_name]['temperature'] <= favorable_temperature[1]:
            return True

    def test_magnetic_field(self):
        if planets_parameters[planet_name]['magnetic_field'] <= 2:
            return True

    def test_auspiciousness_condition(self):
        if planets_parameters[planet_name]['auspiciousness'] >= 60:
            return True

    def test_oxygen_level(self):
        if normal_level_of_oxygen[0] <= planets_parameters[planet_name]['oxygen'] <= normal_level_of_oxygen[1]:
            return True

    def test_wind_speed(self):
        if optimal_wind_speed[0] <= planets_parameters[planet_name]['wind_speed'] <= optimal_wind_speed[1]:
            return True

    def test_adverse_condition(self):
        if planets_parameters[planet_name]['earthquake'] is False \
                and planets_parameters[planet_name]['tsunami'] is False\
                and planets_parameters[planet_name]['meteorite'] is False:
            return True
        else:
            return False

    def test_favorable_magnetic_field(self):
        if magnetic_fields[planets_parameters[planet_name]['magnetic_field']] in ['strong', 'the strongest']:
            return True

    def test_weak_magnetic_field(self):
        if magnetic_fields[planets_parameters[planet_name]['magnetic_field']] in ['weak', 'more strong']:
            return True

    def test_life_exist(self):
        if planets_parameters[planet_name]['life'] == 0 and planets_parameters[planet_name]['first_life'] is False:
            return True

    def test_planet_condition(self):
        if self.test_favorable_magnetic_field() and self.test_adverse_condition() and self.test_wind_speed() \
                and self.test_water_level() and self.test_oxygen_level() and self.test_favorable_temperature():
            return True
        else:
            return False

    def test_game_end(self):
        if planets_parameters[planet_name]['auspiciousness'] >= 95 \
                and planets_parameters[planet_name]['people'] >= 10000:
            return True
