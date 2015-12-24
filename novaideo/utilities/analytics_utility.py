
import random


def random_color():
    value = int(random.random() % (10 ** 8) * 255)
    value2 = int(float('0.'+str(value+20)) * 255)
    value3 = int(float('0.'+str(value+40)) * 255)
    return '#%02x%02x%02x' % (value, value2, value3)


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i+int(lv/3)], 16) for i in range(0, lv, int(lv/3)))


def hover_color(color):
    rgb = hex_to_rgb(color)
    value = rgb[0] - 30
    value2 = rgb[1] - 30
    value3 = rgb[2] - 30
    value = value if value >= 0 else 0
    value2 = value2 if value2 >= 0 else 0
    value3 = value3 if value3 >= 0 else 0
    return '#%02x%02x%02x' % (value, value2, value3)
