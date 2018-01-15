from Tkinter import *
import RPi.GPIO as gpio
from servo_observer import *

canvas_width = 320
canvas_height = 240
border = 20
r = None


class RadarGui:
    def __init__(self, on_gui_created_listener):
        self.master = Tk()
        self._canvas = Canvas(self.master,
                              width=canvas_width,
                              height=canvas_height)
        self._canvas.pack()
        self.points = {}

    def start(self):
        self.master.after(100, on_gui_created_listener)
        self.master.after(100, self.invalidate)
        self.master.mainloop()

    def update_points(self, points):
        self.points = points
        print "called paint with ", self.points

    def invalidate(self):
        self._canvas.delete("all")
        delta = (canvas_width / 2) - border
        for key, value in self.points.iteritems():
            x = delta + (key / 100.) * delta + border
            y = int(value / 2)
            print x, y
            self._canvas.create_line(x, canvas_height, x, canvas_height - y, fill="#476042")
        self.master.after(100, self.invalidate)


def on_gui_created_listener():
    global r
    print "on_gui_created_listener"

    gpio.setmode(gpio.BCM)

    o = ServoObserver(0, True)

    try:
        o.start(100, r.update_points)
        time.sleep(20)
        o.stop()
    finally:
        print ("cleanup observer")
        o.cleanup()
        print ("cleanup gpio")
        gpio.cleanup()


if __name__ == '__main__':
    r = RadarGui(on_gui_created_listener)
    r.start()
