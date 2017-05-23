# coding=utf-8
import logging
from tornado.websocket import WebSocketHandler


class RPCHandler(WebSocketHandler):
    CLIENTS = dict()

    def open(self):
        # TODO validate token
        node_name = self.request.headers.get('node_name')
        if node_name not in self.settings.get('NODE_LIST'):
            return self.write_error(400)
        self.CLIENTS[node_name] = self
        logging.info('Node [%s] connected.' % node_name)

    def on_message(self, message):
        self.write_message(message)

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True
