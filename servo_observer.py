#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from pca9685 import *
import RPi.GPIO as gpio
from hcsr04 import *

STEP = 4

ECHO = 17
TRIG = 4
DEBUG = True


class ServoObserver:
    def __init__(self, channel):
        self._running = False
        self._servo = PCA9685()
        self._measurer = hcsr04(TRIG, ECHO)
        self._channel = channel
        self._thread = None
        self._min_range = 0
        self._min_range_listener = None

        self._servo.servos[self._channel].set(signed=True, reverse=True,
                                              min=100, max=100,
                                              trim=0, exp=0)
        self._servo.setServo(self._channel, 0)
        time.sleep(1)

    def start(self, min_range, min_range_listener):
        self._running = True
        # init threads
        self._min_range = min_range
        self._min_range_listener = min_range_listener
        self._thread = threading.Thread(target=self._run, args=())
        if DEBUG:
            print ("self._thread.start()")
        self._thread.start()

    def stop(self):
        self._running = False
        self._thread.join()

    def cleanup(self):
        self._servo.off()

    def _run(self):
        if DEBUG:
            print ("_run")
        last_distance_greater = False
        start_range = -120
        end_range = 120
        step = STEP
        while self._running:
            distance_array = {}
            min_distance = 999
            min_angle = 0

            for a in xrange(start_range, end_range, step):
                if not self._running:
                    return
                # turn servo into angle
                self._servo.setServo(self._channel, a)
                time.sleep(0.01)
                # measure distance
                distance = 999
                for i in range(10):
                    distance = self._measurer.get_distance()
                    if distance < 999:
                        break
                if DEBUG and a == 0:
                    print ('{} distance is {}'.format(a, distance))
                if min_distance > distance:
                    distance = min_distance
                    min_angle = a
                # store distance for angle
                distance_array[a] = distance

            # swap ranges
            start_range, end_range, step = end_range, start_range, -step

            if min_distance < self._min_range:
                if last_distance_greater and self._min_range_listener is not None:
                    self._min_range_listener(distance_array)
                    last_distance_greater = False
            else:
                last_distance_greater = True


def test_callback(arrays):
    print "callback:"
    print arrays


if __name__ == '__main__':
    gpio.setmode(gpio.BCM)

    o = ServoObserver(0)

    try:
        o.start(10, test_callback)
        time.sleep(10)
        o.stop()
    finally:
        print ("cleanup observer")
        o.cleanup()
        print ("cleanup gpio")
        gpio.cleanup()
