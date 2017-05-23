# coding=utf-8
import sys
import logging

import tornado
import tornado.log
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options
import tornado.websocket

from application.utils.config_parser import ConfigParser
from application.handlers.rpc import RPCHandler


def setup_logging_to_stream(stream, log_level):
    logger = logging.getLogger()
    channel = logging.StreamHandler(stream)
    channel.setLevel(log_level)
    channel.setFormatter(tornado.log.LogFormatter())
    logger.addHandler(channel)


def setup_logging(log_level=None):
    if log_level is None:
        log_level = getattr(logging, options.logging.upper())

    logger = logging.getLogger()
    logger.setLevel(log_level)

    setup_logging_to_stream(stream=sys.stdout, log_level=log_level)
    setup_logging_to_stream(stream=sys.stderr, log_level=logging.ERROR)


class Application(tornado.web.Application):
    def __init__(self, cfg):
        settings = ConfigParser(cfg)
        super(Application, self).__init__(
            handlers=[('/rpc', RPCHandler)],
            autoreload=settings.get('DEBUG'),
            cookie_secret=settings.get('SECRET_KEY'),
            compiled_template_cache=not settings.get('DEBUG'),
            gzip=True,
            **settings
        )

    def configure_websocket(self):
        pass

    def run(self):
        port = self.settings.get('GATE_PORT')
        address = self.settings.get('GATE_HOST')
        setup_logging()
        tornado.log.enable_pretty_logging()
        http_server = tornado.httpserver.HTTPServer(self, xheaders=True)
        http_server.listen(port, address=address)
        self._print_starting_info(address, port)
        tornado.ioloop.IOLoop.current().start()

    def _print_starting_info(self, address, port):
        print ' * Running gate server on http://{HOST}:{PORT}/ (Press CTRL+C to quit)'.format(
            HOST=self.settings.get('HOST', address),
            PORT=self.settings.get('PORT', port),
        )