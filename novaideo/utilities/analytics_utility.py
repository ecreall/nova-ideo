
import randomcolor

rand_color = randomcolor.RandomColor()


def random_color(count=1):
    colors = [{'background': c, 'hover': hover_color(c)}
              for c in rand_color.generate(count=count)]
    if count == 1:
        return colors[0]

    return colors


def get_colors(count=1):
    colors = COLORS[0:count]
    if count == 1:
        return colors[0]

    return colors


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

COLORS = random_color(100)
