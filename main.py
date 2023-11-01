from sreen import *
from tape import *
import concurrent.futures
import threading, time

ser = serial.Serial(
    port="COM11",
    baudrate=230400,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)


def main():
    for i in range(104):
        setLed(ser, i, (0, 0, 0))

    screenshot = ImageGrab.grab()
    none_range = 20
    count_x = 34
    count_y = 18
    while True:
        # bottom
        st = time.time()
        bottom = screen_range(none_range, screenshot.size[1] - none_range, screenshot.size[0] - none_range,
                              screenshot.size[1])
        res = divide_pixels_by_width(asarray(bottom), count_x)[::-1]
        _ = getLEDRange(LightingSides.RBOTTOM, count_x, count_y)[::-1]
        for i in _:
            pixel = average_color(res[i])
            setLed(ser, i, pixel)
        # left
        left = screen_range(0, none_range, none_range, screenshot.size[1] - none_range)
        res = divide_pixels_by_width(asarray(left), count_y)[::-1]
        _ = getLEDRange(LightingSides.RLEFT, count_x, count_y)
        for i in _:
            pixel = average_color(res[i-_[0]])
            setLed(ser, i, pixel)
        # top
        top = screen_range(none_range, 0, screenshot.size[0] - none_range, none_range)
        res = divide_pixels_by_width(asarray(top), count_x)
        _ = getLEDRange(LightingSides.RTOP, count_x, count_y)
        for i in _:
            pixel = average_color(res[i - _[0]])
            setLed(ser, i, pixel)

        # right
        right = screen_range(screenshot.size[0] - none_range, none_range, screenshot.size[0],
                             screenshot.size[1] - none_range)
        res = divide_pixels_by_width(asarray(right), count_y)
        _ = getLEDRange(LightingSides.RRIGHT, count_x, count_y)
        for i in _:
            pixel = average_color(res[i - _[0]])
            setLed(ser, i, pixel)
        en = time.time() - st
        print(en)
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
