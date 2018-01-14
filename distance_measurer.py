import RPi.GPIO as gpio
import time

MAX_DISTANCE = 999. / 17150.


class DistanceMeasurer:
    def __init__(self, trig, echo):
        self._trig = trig
        self._echo = echo

        gpio.setup(self._trig, gpio.OUT)
        gpio.setup(self._echo, gpio.IN)

        gpio.output(self._trig, False)

    def measure(self):
        pulse_start = 0
        pulse_end = MAX_DISTANCE

        gpio.output(self._trig, True)
        time.sleep(0.00001)
        gpio.output(self._trig, False)

        for i in range(100000):
            if gpio.input(self._echo) == 0:
                pulse_start = time.time()
                pulse_end = pulse_start - MAX_DISTANCE
                break

        for i in range(100000):
            if gpio.input(self._echo) == 1:
                pulse_end = time.time()
                break

        pulse_duration = pulse_end - pulse_start
        return round(pulse_duration * 17150.0, 2)


if __name__ == '__main__':
    gpio.setmode(gpio.BCM)

    d = DistanceMeasurer(4, 17)
    print d.measure()

    gpio.cleanup()
