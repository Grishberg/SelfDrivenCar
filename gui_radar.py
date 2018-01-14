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

        #points = {0: 3.64, 64: 110.51, 4: 4.83, -120: 40.14, 44: 8.1, -116: 39.6, -112: 39.99, 24: 5.18, -108: 39.67, 104: 4.41, -104: 40.01, 68: 110.0, -100: 40.49, 88: 110.94, -96: 38.86, 48: 11.37, -92: 40.37, 116: 4.41, -88: 38.71, 28: 5.59, -84: 39.17, 80: 111.07, -80: 11.67, 8: 4.42, -76: 11.89, -72: 40.46, 52: 12.64, -68: 40.51, 72: 109.95, -64: 42.21, 32: 6.04, -60: 12.19, 100: 4.39, -56: 9.04, 12: 4.84, -52: 9.07, 112: 4.85, 108: 4.41, -48: 10.19, 56: 110.93, -44: 10.61, 92: 111.34, -40: 110.74, 36: 6.35, -36: 110.41, -32: 110.8, 16: 4.92, -28: 109.98, 84: 111.05, -24: 110.93, 60: 110.81, -20: 110.57, 96: 3.12, -16: 110.79, 40: 6.78, -12: 110.62, 76: 110.33, -8: 110.79, 20: 5.18, -4: 109.95}

        #self.paint(points)
    def start(self):
        self.master.after(100, on_gui_created_listener)
        self.master.mainloop()

    def paint(self, points):
        self._canvas.delete("all")
        delta = (canvas_width / 2) - border
        for key, value in points.iteritems():
            x = delta + (key / 100.) * delta + border
            y = int(value / 2)
            print x, y
            self._canvas.create_line(x, canvas_height, x, canvas_height - y, fill="#476042")
        self.master.update()


def on_gui_created_listener():
    global r
    print "on_gui_created_listener"

    gpio.setmode(gpio.BCM)

    o = ServoObserver(0)

    try:
        o.start(10, r.paint)
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
