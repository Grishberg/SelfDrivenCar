from Tkinter import *
import RPi.GPIO as gpio
from servo_observer import *

canvas_width = 320
canvas_height = 240
border = 20


class RadarGui:
    def __init__(self, on_gui_created_listener):
        self.master = Tk()
        self._canvas = Canvas(self.master,
                              width=canvas_width,
                              height=canvas_height)
        self._canvas.pack()

        points = {-100: 60, 0: 20, 100: 60}

        self.paint(points)
        self.master.after(0, on_gui_created_listener)
        self.master.mainloop()

    def paint(self, points):
        self._canvas.delete("all")
        delta = (canvas_width / 2) - border
        for key, value in points.iteritems():
            x = delta + (key / 100) * delta + border
            y = int(value / 2)
            print x, y
            self._canvas.create_line(x, canvas_height, x, canvas_height - y, fill="#476042")


def on_gui_created_listener():
    print "on_gui_created_listener"
    gpio.setmode(gpio.BCM)

    o = ServoObserver(0)

    try:
        o.start(10, test_callback)
        time.sleep(20)
        o.stop()
    finally:
        print ("cleanup observer")
        o.cleanup()
        print ("cleanup gpio")
        gpio.cleanup()


if __name__ == '__main__':
    r = RadarGui(on_gui_created_listener)
