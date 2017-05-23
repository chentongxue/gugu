# coding=utf-8
from ..exceptions import WebsocketRPCConnectError
from .tornado_websocket import WebSocket


class WsRPC(object):
    def __init__(self, app=None):
        self.app = None
        self.ws = None

    def init_app(self, app):
        self.app = app
        address = (app.settings.get('GATE_HOST'), app.settings.get('GATE_PORT'))
        headers = {'node_name': app.node_name}
        self.ws = TornadoWebSocket('ws://%s:%s/rpc' % address, extra_headers=headers)


class TornadoWebSocket(WebSocket):
    def on_open(self):
        self.write_message('hello, world')

    def on_message(self, data):
        print data

    def on_ping(self):
        print 'I was pinged'

    def on_pong(self):
        print 'I was ponged'

    def on_close(self):
        print 'Socket closed.'


wsrpc = WsRPC()
