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
        self.points = {0: 7.6, -64: 146.62, 4: 7.92, 8: 8.04, -20: 7.96, 12: 8.02, 16: 7.96, -40: 8.83, -72: 114.2,
                       20: 8.5, 24: 8.5, -60: 114.03, -76: 114.42, 28: 8.92, 32: 11.37, -16: 8.03, -80: 135.79,
                       36: 113.38, 40: 15.91, -36: 8.87, -84: 115.57, 44: 14.17, 48: 14.92, -56: 113.81, -88: 114.67,
                       52: 12.11, 56: 10.77, -12: 7.99, -92: 135.21, 60: 10.36, 64: 12.47, -32: 11.29, -96: 115.25,
                       68: 9.51, 72: 9.52, -52: 10.2, -100: 114.2, 76: 10.41, 80: 11.68, -8: 7.62, -104: 146.36,
                       84: 112.45, 88: 120.07, -28: 8.06, -108: 113.83, 92: 116.66, 96: 114.58, -48: 9.81, -112: 113.69,
                       100: 104.56, 104: 103.37, -68: 121.75, -116: 114.08, 108: 92.37, 112: 113.62, -24: 7.97,
                       116: 112.4, 120: 114.08, -44: 9.28, -4: 7.49}
        self.on_end_listener = on_end_listener
        self.counter = 0
        self._running = True

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
        #self.points = points
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
