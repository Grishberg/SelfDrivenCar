import RPi.GPIO as gpio
import time


# from ultrasonic import distance

class Driver:
    def __init__(self):
        pass

    def init(self):
        gpio.setmode(gpio.BCM)
        gpio.setup(27, gpio.OUT)
        gpio.setup(22, gpio.OUT)
        gpio.setup(23, gpio.OUT)
        gpio.setup(24, gpio.OUT)

    def wait_and_clean(self, t):
        time.sleep(t)
        # gpio.cleanup()

    def release(self):
        gpio.output(27, False)
        gpio.output(22, False)
        gpio.output(23, False)
        gpio.output(24, False)

    def forward(self, tf):
        gpio.output(27, True)
        gpio.output(22, False)
        gpio.output(23, True)
        gpio.output(24, False)
        self.wait_and_clean(tf)

    def reverse(self, tf):
        gpio.output(27, False)
        gpio.output(22, True)
        gpio.output(23, False)
        gpio.output(24, True)
        self.wait_and_clean(tf)

    def right(self, t):
        gpio.output(27, True)
        gpio.output(22, False)
        gpio.output(23, False)
        gpio.output(24, True)
        self.wait_and_clean(t)

    def left(self, t):
        gpio.output(27, False)
        gpio.output(22, True)
        gpio.output(23, True)
        gpio.output(24, False)
        self.wait_and_clean(t)

    def turn_left(self):
        self.left(0.85)

    def turn_right(self):
        self.right(0.85)

    @staticmethod
    def clean():
        gpio.cleanup()
