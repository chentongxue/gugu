# coding=utf-8
import os
import sys
import logging

import tornado
import tornado.log
import tornado.web
import tornado.ioloop
import tornado.httpserver
from tornado.options import options, define, parse_command_line

from application.utils.config_parser import ConfigParser
from application.handlers import Route
from application.handlers.frontend import *
from application.extensions.websocket_rpc import wsrpc


define('node_name', type=str, help="run on the given node name")


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
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            autoreload=settings.get('DEBUG'),
            cookie_secret=settings.get('SECRET_KEY'),
            compiled_template_cache=not settings.get('DEBUG'),
            gzip=True,
            **settings
        )
        parse_command_line()
        node_name = options.node_name
        self.node_name = node_name

        self.configure_routes()
        self.configure_extensions()

    def configure_routes(self):
        Route.register_routes(self)

    def configure_extensions(self):
        wsrpc.init_app(self)

    def run(self):
        settings = self.settings['NODE_LIST'].get(self.node_name)
        port = settings.get('PORT')
        address = settings.get('HOST')
        tornado.log.enable_pretty_logging()
        http_server = tornado.httpserver.HTTPServer(self, xheaders=True)
        http_server.listen(port, address=address)
        self._print_starting_info(address, port)
        tornado.ioloop.IOLoop.current().start()

    def _print_starting_info(self, address, port):
        print ' * Running node server on http://{HOST}:{PORT}/ (Press CTRL+C to quit)'.format(
            HOST=self.settings.get('HOST', address),
            PORT=self.settings.get('PORT', port),
        )
