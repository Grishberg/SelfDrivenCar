import RPi.GPIO as GPIO
import time


class DistanceMeasurer:
    def __init__(self, trig, echo):
        self._running = True
        self.min_dist = 10
        self.interval = 0.100
        self.distance = 0.
        self._trig = trig
        self._echo = echo
        self._thread = None
        self._measure_listener = None

        GPIO.setup(self._trig, GPIO.OUT)
        GPIO.setup(self._echo, GPIO.IN)

        GPIO.output(self._trig, False)

    def measure(self):
        pulse_start = 0
        pulse_end = 17150 * 999

        GPIO.output(self._trig, True)
        time.sleep(0.00001)
        GPIO.output(self._trig, False)

        while GPIO.input(self._echo) == 0:
            pulse_start = time.time()

        while GPIO.input(self._echo) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        return round(pulse_duration * 17150, 2)


if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)

    d = DistanceMeasurer(4, 17)
    print d.measure()

    GPIO.cleanup()
