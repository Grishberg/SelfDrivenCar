from Tkinter import *
import RPi.GPIO as gpio
from servo_observer import *

canvas_width = 320
canvas_height = 240
border = 20


class RadarGui:
    def __init__(self, on_end_listener=None):
        self.master = Tk()
        self._canvas = Canvas(self.master,
                              width=canvas_width,
                              height=canvas_height)
        self._canvas.pack()
        self.points = {}
        self.on_end_listener = on_end_listener
        self.counter = 0
        self._running = False

    def start_mainloop(self):
        self.master.after(0, self.tick)
        self.master.after(100, self.invalidate)
        self.master.mainloop()

    def tick(self):
        print "tick"
        if self.counter > 10:
            if self.on_end_listener is not None:
                self.on_end_listener()
            return
        self.master.after(1000, self.tick)
        self.counter += 1

    def update_points(self, points):
        self.points = points
        print "called paint with ", self.points

    def invalidate(self):
        if not self._running:
            return
        print "invalidate"
        self._canvas.delete("all")
        delta = (canvas_width / 2) - border
        for key, value in self.points.iteritems():
            x = delta + (key / 100.) * delta + border
            y = int(value / 2)
            print x, y
            self._canvas.create_line(x, canvas_height, x, canvas_height - y, fill="#476042")
        self.master.after(100, self.invalidate)

    def stop(self):
        self._running = False


class ServoController:
    def __init__(self):
        gpio.setmode(gpio.BCM)
        self._observer = ServoObserver(0, True)

        self._radar = RadarGui(self.on_end_listener)
        self._observer.start(100, self._radar.update_points)

        self._radar.start_mainloop()

    def on_end_listener(self):
        print "on_end_listener"
        try:
            self._radar.stop()
            self._observer.stop()
            self._observer.cleanup()
        finally:
            print ("cleanup gpio")
            gpio.cleanup()


if __name__ == '__main__':
    controller = ServoController()
