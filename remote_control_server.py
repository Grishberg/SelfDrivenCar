from tornado import websocket
import tornado.ioloop
from driver import Driver

UP = 'u'
DOWN = 'd'
LEFT = 'l'
RIGHT = 'r'
TURN_LEFT = '<'
TURN_RIGHT = '>'

PRESSED = 'p'
RELEASED = 'r'

QUIT = 'q'
DEBUG = True


class CarWebSocket(websocket.WebSocketHandler):
    def __init__(self, application, request, **kwargs):
        super(CarWebSocket, self).__init__(application, request, **kwargs)
        self._car_controller = Driver()
        self._mode = None

    def open(self):
        print "Websocket Opened"
        self._car_controller.init()

    def on_message(self, message):
        if DEBUG:
            print "on_message:", message
        if len(message) != 2:
            print "wrong command length: %s" % message
        cmd = message[0]
        action = message[1]

        self.process_cmd(cmd, action)

        self.write_message(u"You said: %s" % message)

    def on_close(self):
        print "Websocket closed"
        self._car_controller.clean()

    def process_cmd(self, cmd, action):
        if cmd == QUIT:
            self.quit()
            return
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


application = tornado.web.Application([(r"/", CarWebSocket), ])

if __name__ == "__main__":
    application.listen(9000)
    tornado.ioloop.IOLoop.instance().start()
