import serial
from struct import *
import math


def waitData(ser):
    while ser.inWaiting() <= 0:
        pass


def sendInt(ser, val):
    ser.write((val).to_bytes(4, byteorder='little'))


def recvInt(ser):
    raw = ser.read(4)
    return int.from_bytes(raw, 'little')


def recvByte(ser):
    raw = ser.read(1)
    return int.from_bytes(raw, 'little')


def syncSend(ser):
    sendInt(ser, 0xDEADBEEF)


def syncWait(ser):
    sync = recvInt(ser)
    if (sync == 0xDEADBEEF):
        return

    sync <<= 8
    while (1):
        sync |= recvByte(ser)
        if (sync == 0xDEADBEEF):
            return
        sync <<= 8


def readData(ser, val):
    raw = b''
    while (1):
        if (ser.inWaiting() > 0):
            raw += ser.read(ser.inWaiting())

        if (len(raw) >= val):
            return raw


def hsv_to_rgb(h, s, v):
    h = h / 360
    s = s / 100
    v = v / 100

    i = math.floor(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r, g, b = [
        (v, t, p),
        (q, v, p),
        (p, v, t),
        (p, q, v),
        (t, p, v),
        (v, p, q),
    ][int(i % 6)]

    return int(r * 255), int(g * 255), int(b * 255)


def setLed(ser, n, color):
    r, g, b = color
    # print("%d %d %d %d" % (n, r, g, b))
    data = pack("<HBBB", n, r, g, b)
    syncSend(ser)
    sendInt(ser, 1)
    ser.write(data)


def setRefreshRate(ser, rate):
    data = pack("<I", rate)
    syncSend(ser)
    sendInt(ser, 2)
    ser.write(data)


def path(ser, num, direct, colorActive, colorInactive):
    num = num - 1
    r = range(num, 0, -1) if direct else range(0, num, 1)
    prev = 0 if direct else num

    for j in r:
        setLed(ser, j, colorActive)
        setLed(ser, prev, colorInactive)
        prev = j
