#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from pca9685 import *
from distance_measurer import DistanceMeasurer
import RPi.GPIO as gpio

STEP = 3

ECHO = 17
TRIG = 4
DEBUG = True


class ServoObserver:
    def __init__(self, channel):
        self._running = False
        self._servo = PCA9685()
        self._measurer = DistanceMeasurer(TRIG, ECHO)
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

    def cleanup(self):
        self._servo.off()

    def _run(self):
        if DEBUG:
            print ("_run")
        last_distance_greater = 999
        start_range = -100
        end_range = 100
        while self._running:
            distance_array = {}
            min_distance = 999
            min_angle = 0

            for a in xrange(start_range, end_range, STEP):
                # turn servo into angle
                self._servo.setServo(self._channel, a)
                time.sleep(0.01)
                # measure distance
                distance = 999
                for i in range(10):
                    distance = self._measurer.measure()
                    if distance < 999:
                        break
                if DEBUG:
                    print ('{} distance is {}'.format(a, distance))
                if min_distance > distance:
                    distance = min_distance
                    min_angle = a
                # store distance for angle
                distance_array[a] = distance

            # swap ranges
            start_range, end_range = end_range, start_range
            if min_distance < self._min_range:
                if last_distance_greater and self._min_range_listener is not None:
                    self._min_range_listener(distance_array)
                    last_distance_greater = False
            else:
                last_distance_greater = True


def test_callback(arrays):
    print arrays


if __name__ == '__main__':
    gpio.setmode(gpio.BCM)

    o = ServoObserver(0)

    o.start(10, test_callback)
    time.sleep(10)
    o.stop()

    gpio.cleanup()
