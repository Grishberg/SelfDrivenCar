#!/usr/bin/env python
# -*- coding: utf-8 -*-
import threading
from pca9685 import *
import RPi.GPIO as gpio
from Queue import Queue, Empty
import time

DEBUG = True
SERVO_EXECUTING_TIME = 0.25


class CameraController:
    def __init__(self, channel_horizontal, channel_vertical):
        self._stop_event = None
        self._horizontal_queue = Queue()
        self._vertical_queue = Queue()

        self._running = False
        self._channel_horizontal = channel_horizontal
        self._channel_vertical = channel_vertical
        self._vertical_thread = None
        self._horizontal_thread = None
        self._servo = None

    def init(self):
        # start threads
        self._stop_event = threading.Event()

        self._horizontal_thread = threading.Thread(target=self._horizontal_run, args=())
        self._horizontal_thread.start()

        self._vertical_thread = threading.Thread(target=self._vertical_run, args=())
        self._vertical_thread.start()

        self._servo = PCA9685()
        self._servo.servos[self._channel_horizontal].set(signed=True, reverse=True,
                                                         min=100, max=100,
                                                         trim=0, exp=0)
        self._servo.servos[self._channel_vertical].set(signed=True, reverse=True,
                                                       min=100, max=100,
                                                       trim=0, exp=0)
        self._servo.setServo(self._channel_horizontal, 0)
        self._servo.setServo(self._channel_vertical, 0)

        time.sleep(1)

    def set_horizontal_angle(self, angle):
        if DEBUG:
            print "set horizontal angle %s" % angle
        self._horizontal_queue.put(angle)

    def set_vertical_angle(self, angle):
        if DEBUG:
            print "set vertical angle %s" % angle
        self._vertical_queue.put(angle)

    def _horizontal_run(self):
        print "start _horizontal_run"
        while not self._stop_event.is_set():
            try:
                next_angle = self._horizontal_queue.get(timeout=1)
                print "    next horizontal angle %s" % next_angle
                self._servo.setServo(self._channel_horizontal, next_angle)
                self._stop_event.wait(SERVO_EXECUTING_TIME)
            except Empty:
                pass
        print "stop _horizontal_run"

    def _vertical_run(self):
        print "start _vertical_run"
        while not self._stop_event.is_set():
            try:
                next_angle = self._vertical_queue.get(timeout=1)
                print "    next vertical angle %s" % next_angle
                self._servo.setServo(self._channel_vertical, next_angle)
                self._stop_event.wait(SERVO_EXECUTING_TIME)
            except Empty:
                pass
        print "stop _vertical_run"

    def clean(self):
        print "clean"
        self._stop_event.set()

        self._horizontal_queue.queue.clear()
        self._vertical_queue.queue.clear()

        self._servo.off()


if __name__ == '__main__':
    gpio.setmode(gpio.BCM)

    cc = CameraController(1, 2)

    try:
        cc.set_horizontal_angle(-100)
        cc.set_horizontal_angle(0)
        cc.set_horizontal_angle(100)
        cc.set_vertical_angle(100)
        cc.set_vertical_angle(0)
        cc.set_vertical_angle(-100)
        time.sleep(6)
        cc.set_horizontal_angle(0)
        cc.set_vertical_angle(0)
        time.sleep(1.5)
    finally:
        print ("cleanup controller")
        cc.clean()
        gpio.cleanup()
    print "done"
