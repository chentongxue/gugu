# coding=utf-8
import logging

from ..exceptions import WebsocketRPCConnectError
from .tornado_websocket import WebSocket
from gate.packer import DataPack
from tornado import gen


class WsRPC(object):
    def __init__(self, app=None):
        self.app = app
        self.ws = None
        self.funcs = dict()

    def init_app(self, app):
        self.app = app
        address = (app.settings.get('GATE_HOST'), app.settings.get('GATE_PORT'))
        headers = {'node_name': app.node_name}
        self.ws = TornadoWebSocket('ws://%s:%s/rpc' % address, extra_headers=headers)

    def register(self, command_id, func):
        self.funcs[command_id] = func

    def execute(self, command_id, *args, **kwargs):
        command = self.funcs[command_id]
        result = command(*args, **kwargs)
        return result


class TornadoWebSocket(WebSocket):
    def on_open(self):
        print 'on open'

    @gen.coroutine
    def on_message(self, data):
        packer = DataPack()
        command_id, kwargs = packer.unpack(data)
        # TODO non-blocking
        data = wsrpc.execute(command_id, **kwargs)
        result = packer.pack(command_id, data)
        self.write_message(result)

    def on_ping(self):
        print 'I was pinged'

    def on_pong(self):
        print 'I was ponged'

    def on_close(self):
        print 'Socket closed.'


def echo(s):
    return 'hello:' + s

wsrpc = WsRPC()
wsrpc.register(100, echo)
