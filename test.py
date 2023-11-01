import threading, time
import multiprocessing
import concurrent.futures
import mss
import mss.tools
from PIL import ImageGrab


def work(n):
    for i in range(n):
        continue


def foo(n):
    start = time.time()
    for i in range(1):
        work(50_000_000)
    end = time.time() - start
    print(f'[{n}]', end)
    return True


def capture_screenshot():
    # Создаем объект mss для захвата скриншота
    with mss.mss() as sct:
        # Захватываем экран
        monitor = sct.monitors[1]  # Выбираем второй монитор (индексация начинается с 0)
        screenshot = sct.grab(monitor)


def main():
    st = time.time()
    obl = ImageGrab.grab()
    en = time.time() - st
    print(en)

    st = time.time()
    left = 0
    top = 0
    width = 20
    height = 1400

    # Создание объекта mss для захвата экрана
    with mss.mss() as sct:
        # Захват области экрана
        screenshot = sct.grab({"left": left, "top": top, "width": width, "height": height})

    # Преобразование полученного изображения в массив numpy

    en = time.time() - st
    print(en)


if __name__ == "__main__":
    main()
