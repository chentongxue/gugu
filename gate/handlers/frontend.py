# coding=utf-8
import logging
from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler
from .rpc import RPCHandler


class BaseHandler(RequestHandler):
    pass


class FrontendHandler(WebSocketHandler):
    """
    处理用户websocket
    """
    USER_CLIENTS = dict()

    def open(self):
        # TODO validate token
        node_name = self.request.headers.get('node_name')
        if node_name not in self.settings.get('NODE_LIST'):
            return self.write_error(400)

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True


class TestWebHandler(BaseHandler):
    def get(self):
        RPCHandler.send_all_nodes(100, {'s': 'suzaku'})
        return self.write('calling command[%s]' % 100)
