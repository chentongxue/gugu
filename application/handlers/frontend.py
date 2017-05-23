# coding=utf-8
from application.handlers import BaseHandler, Route


@Route('/')
class FrontendHandler(BaseHandler):
    def get(self):
        return self.write('hello world')
