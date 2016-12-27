#!/usr/bin/env python
# -*- coding: utf-8 -*-


__version__ = '0.999a'
__license__ = 'GPLv3'
__author__ = 'georgi.kolev_[at]_gmail.com'
__name__ = 'carpcp-web'


import os
import json
import carpcp_conf as conf
from tornado import websocket, web, ioloop
try:
    from procname import setprocname
    setprocname(__name__)
except:
    print('Warning: "import procname" failed :(')
    print('Warning: Skipping process rename!')


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("static/index.html")


class SocketHandler(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in cl:
            cl.append(self)

    def on_message(self, message):
        for c in cl:
            c.write_message(message)

    def on_close(self):
        if self in cl:
            cl.remove(self)


class ApiHandler(web.RequestHandler):

    @web.asynchronous
    def get(self, *args):
        self.finish()
        try:
            id = self.get_argument("id")
            value = self.get_argument("value")
            data = {"id": id, "value": value}
            data = json.dumps(data)
            for c in cl:
                c.write_message(data)
        except:
            print 'MSG Error'

    @web.asynchronous
    def post(self):
        pass


cl = []
settings = {
    "static_path": os.path.join(conf.CARPCP_DIR, "static"),
}
settings = { "static_path": '/home/l4m3rx/Desktop/Car/x/dev/static'}

app = web.Application([
    (r'/', IndexHandler),
    (r'/api', ApiHandler),
    (r'/ws', SocketHandler),
    (r'/(.*).js', web.StaticFileHandler, dict(path=settings['static_path'])),
    (r'/(.*).css', web.StaticFileHandler, dict(path=settings['static_path'])),
    (r'/(.*).map', web.StaticFileHandler, dict(path=settings['static_path'])),
], **settings)

#if __name__ == '__main__':
if 1==1:
    print ('App starting...')
    app.listen(7350)
    ioloop.IOLoop.instance().start()
# eof
