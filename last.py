import multiprocessing
import queue
from datetime import datetime
from multiprocessing import Process

from PIL import ImageGrab
from numpy import asarray

from sreen import *
from tape import *
import concurrent.futures
import time

screenshot = ImageGrab.grab()
none_range = 20
count_x = 34
count_y = 18


def work(obj):
    vector = obj['img'].crop(obj['screen_range'])
    if obj['is_x']:
        if obj['is_revers']:
            res = divide_pixels_by_width(asarray(vector), count_x)[::-1]
        else:
            res = divide_pixels_by_width(asarray(vector), count_x)
    else:
        if obj['is_revers']:
            res = divide_pixels_by_width(asarray(vector), count_y)[::-1]
        else:
            res = divide_pixels_by_width(asarray(vector), count_y)

    _ = getLEDRange(getattr(LightingSides, obj['position']), count_x, count_y)
    pixels = []
    for i in _:
        tmp = average_color(res[i - _[0]])
        pixels.append(tmp)

    return [_, pixels]


def main():
    ser = serial.Serial(
        port="COM11",
        baudrate=230400,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS
    )
    for i in range(104):
        setLed(ser, i, (0, 0, 0))

    bottom = {
        'position': 'RBOTTOM',
        'screen_range': [none_range, screenshot.size[1] - none_range, screenshot.size[0] - none_range,
                         screenshot.size[1]],
        'is_revers': True,
        'is_x': True
    }
    left = {
        'position': 'RLEFT',
        'screen_range': [0, none_range, none_range, screenshot.size[1] - none_range],
        'is_revers': True,
        'is_x': False
    }
    top = {
        'position': 'RTOP',
        'screen_range': [none_range, 0, screenshot.size[0] - none_range, none_range],
        'is_revers': False,
        'is_x': True
    }
    right = {
        'position': 'RRIGHT',
        'screen_range': [screenshot.size[0] - none_range, none_range, screenshot.size[0],
                         screenshot.size[1] - none_range],
        'is_revers': False,
        'is_x': False
    }
    sides = [bottom, left, top, right]
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        while True:
            img = ImageGrab.grab()

            for el in sides:
                el['img'] = img
            res = ex.map(work, sides)
            results = list(res)
            for res in results:
                for i in range(len(res[0])):
                    setLed(ser, res[0][i], res[1][i])


        # res = work(bottom)
        # i = 0
        # while i < len(res[0]):
        #     setLed(ser, res[0][i], res[1][i])
        #     i += 1
        # for side in res:
        #     i = 0
        #     while i < len(side[0]):
        #         setLed(ser, side[0][i], side[1][i])
        #         i += 1

    # # right
    # right = screen_range(screenshot.size[0] - none_range, none_range, screenshot.size[0],
    #                      screenshot.size[1] - none_range)
    # res = divide_pixels_by_width(asarray(right), count_y)
    # _ = getLEDRange(LightingSides.RRIGHT, count_x, count_y)
    # for i in _:
    #     pixel = average_color(res[i - _[0]])
    #     setLed(ser, i, pixel)

    # bottom
    # bottom = screen_range(none_range, screenshot.size[1] - none_range, screenshot.size[0] - none_range,
    #                       screenshot.size[1])
    # res = divide_pixels_by_width(asarray(bottom), count_x)
    # for i in range(count_x):
    #     pixel = average_color(res[i])
    #     setLed(ser, count_x - i, pixel)
    # left
    # left = screen_range(0, none_range, none_range, screenshot.size[1] - none_range)
    # res = divide_pixels_by_width(asarray(left), count_y)
    # for i in range(count_y):
    #     pixel = average_color(res[i])
    #     setLed(ser, (count_y + count_x) - i, pixel)
    # # top
    # top = screen_range(none_range, 0, screenshot.size[0] - none_range, none_range)
    # res = divide_pixels_by_width(asarray(top), count_x)
    # for i in range(count_x):
    #     pixel = average_color(res[i])
    #     setLed(ser, (count_y + (count_x * 2)) - i, pixel)

    # right
    # right = screen_range(screenshot.size[0] - none_range, none_range, screenshot.size[0],
    #                      screenshot.size[1] - none_range)
    # res = divide_pixels_by_width(asarray(right), count_y)
    # for i in range(count_y):
    #     pixel = average_color(res[i])
    #     setLed(ser, ((count_y * 2) + (count_x * 2)) - i, pixel)


if __name__ == "__main__":
    main()
