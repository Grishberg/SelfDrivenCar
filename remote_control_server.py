from tornado import websocket
import tornado.ioloop
from driver import Driver
from camera_moving_controller import CameraController

UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
TURN_LEFT = '<'
TURN_RIGHT = '>'

CAMERA_HORISONT = 'hcam'
CAMERA_VERTICAL = 'vcam'

PRESSED = 1
RELEASED = 0

QUIT = 'q'
DEBUG = True

driver = Driver()
camera_controller = CameraController()


class CarWebSocket(websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        global driver
        global camera_controller

        super(CarWebSocket, self).__init__(application, request, **kwargs)
        self._car_controller = driver
        self._cam_controller = camera_controller
        self._mode = None

    def open(self):
        print "Websocket Opened"
        self._car_controller.init()

    def on_message(self, message):
        if DEBUG:
            print "on_message:", message
        lst = message.split(',')
        if len(lst) != 2:
            print "wrong command length: %s" % message
        cmd = lst[0]
        action = int(lst[1])

        self.process_cmd(cmd, action)

    def on_close(self):
        print "Websocket closed"
        self._car_controller.clean()
        self._cam_controller.clean()

    def process_cmd(self, cmd, action):
        if cmd == QUIT:
            self.quit()
            return
        if cmd == UP or cmd == DOWN or cmd == LEFT or cmd == RIGHT:
            self.process_moving_cmd(action, cmd)
        else:
            self.process_camera_cmd(action, cmd)

    def process_moving_cmd(self, action, cmd):
        if action == PRESSED:
            if cmd == UP:
                self._car_controller.forward(0.5)
            elif cmd == DOWN:
                self._car_controller.reverse(0.5)
            elif cmd == LEFT:
                self._car_controller.left(0.5)
            elif cmd == RIGHT:
                self._car_controller.right(0.5)
        elif action == RELEASED:
            self._car_controller.release()

    def quit(self):
        self.write_message("quit")

    def process_camera_cmd(self, action, angle):
        if action == CAMERA_HORISONT:
            self._cam_controller.set_horizontal_angle(angle)
        elif action == CAMERA_VERTICAL:
            self._cam_controller.set_vertical_angle(angle)


application = tornado.web.Application([(r"/", CarWebSocket), ])

if __name__ == "__main__":
    application.listen(9000)
    print "launched server on port 9000"
    try:
        tornado.ioloop.IOLoop.instance().start()
    except Exception:
        driver.clean()
        print "error"
