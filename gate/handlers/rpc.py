# coding=utf-8
import logging
from tornado.websocket import WebSocketHandler
from gate.packer import DataPack


class RPCHandler(WebSocketHandler):
    NODE_CLIENTS = dict()

    def open(self):
        # TODO validate token
        node_name = self.request.headers.get('node_name')
        if node_name not in self.settings.get('NODE_LIST'):
            return self.write_error(400)
        self.NODE_CLIENTS[node_name] = self
        logging.info('Node [%s] connected.' % node_name)

    @property
    def node_name(self):
        return self.request.headers.get('node_name')

    def on_message(self, message):
        packer = DataPack()
        command_id, data = packer.unpack(message)
        # TODO Forwarding message to net server
        logging.info('receive result from node [%s] command_id: %s, data: %s' % (self.node_name, command_id, data))

    def on_close(self):
        print("WebSocket closed")

    def check_origin(self, origin):
        return True

    @classmethod
    def send_all_nodes(cls, command_id, msg):
        packer = DataPack()
        msg = packer.pack(command_id, msg)
        # TODO non-blocking here
        for client in cls.NODE_CLIENTS.values():
            client.write_message(msg)
        print 'calling command_id, [%s]' % command_id
