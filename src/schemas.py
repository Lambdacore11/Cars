'''Validation module'''

NAME_WITHOUT_DIGITS = r'^[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ\-]*$'
NAME_WITH_DIGITS = r'^[a-zA-Zа-яА-ЯёЁ][a-zA-Zа-яА-ЯёЁ\-0-9]*$'

CAR_NAME_SCHEMA = {
    'pattern': NAME_WITH_DIGITS,
    'examples': ['camry', 'rx-7']
}
CAR_COLOR_SCHEMA = {
    'pattern': NAME_WITHOUT_DIGITS,
    'examples': ['red', 'blue']
}
MANUFACTURER_NAME_SCHEMA = {
    'pattern': NAME_WITHOUT_DIGITS,
    'examples': ['volvo', 'mazda']
}
