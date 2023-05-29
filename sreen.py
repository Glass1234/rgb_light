from PIL import ImageGrab
from numpy import asarray

from enum import IntEnum


class LightingSides(IntEnum):
    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3

    RTOP = 4
    RBOTTOM = 5
    RLEFT = 6
    RRIGHT = 7


def getLEDRange(side: LightingSides, x_count, y_count):
    led_zero = 0
    led_top = x_count
    led_bottom = x_count
    led_left = y_count
    led_right = y_count

    ret = [
        range(led_bottom + led_left, led_bottom + led_left + led_top - 1),
        range(led_zero, led_bottom - 1),
        range(led_bottom, led_bottom + led_left - 1),
        range(led_bottom + led_left + led_top, led_bottom + led_left + led_top + led_right - 1),

        range(led_bottom + led_left + led_top - 1, led_bottom + led_left, -1),
        range(led_bottom - 1, led_zero, -1),
        range(led_bottom + led_left- 1, led_bottom , -1),
        range(led_bottom + led_left + led_top + led_right - 1, led_bottom + led_left + led_top, -1)
    ]

    return ret[int(side)]


def average_color(arr):
    num_rows = len(arr)
    num_cols = len(arr[0])

    # Инициализация счетчиков цветовых каналов
    red_sum = 0
    green_sum = 0
    blue_sum = 0

    # Перебор всех пикселей и суммирование значений цветовых каналов
    for i in range(0, len(arr), 2):
        for j in range(0, len(arr[i]), 2):
            red_sum += arr[i][j][0]
            green_sum += arr[i][j][1]
            blue_sum += arr[i][j][2]

    # Вычисление среднего значения для каждого цветового канала
    red_avg = int(red_sum / (num_rows * num_cols))
    green_avg = int(green_sum / (num_rows * num_cols))
    blue_avg = int(blue_sum / (num_rows * num_cols))

    # Возвращение среднего цвета в виде кортежа
    return (red_avg, green_avg, blue_avg)


def divide_pixels_by_width(arr, num_parts):
    num_cols = len(arr[0])

    # Вычисление ширины каждой части
    part_width = num_cols // num_parts

    divided_parts = []

    # Разделение массива пикселей по ширине
    for i in range(num_parts):
        start_col = i * part_width
        end_col = start_col + part_width

        # Отдельная часть массива пикселей
        part = [row[start_col:end_col] for row in arr]

        divided_parts.append(part)

    return divided_parts


def screen_range(start_x, start_y, end_x, end_y):
    obl = ImageGrab.grab(bbox=(start_x, start_y, end_x, end_y))
    return obl

# screenshot = ImageGrab.grab()
# none_range = 100
# top
# top = screen_range(none_range, 0, screenshot.size[0] - none_range, none_range)
# res = divide_pixels_by_width(asarray(top), 20)
# for i in range(len(res)):
#     print(average_color(res[i]))
# top.show()
# left
# left = screen_range(0, none_range, none_range, screenshot.size[1] - none_range)
# bottom
# bottom = screen_range(none_range, screenshot.size[1]-none_range, screenshot.size[0] - none_range, screenshot.size[1])
# right
# right = screen_range(screenshot.size[0] - none_range, none_range, screenshot.size[0], screenshot.size[1] - none_range)
# right.show()
