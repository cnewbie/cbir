#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import tornado.auth
import tornado.escape
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options
# import hashlib
# import string
# from PIL import Image
from apps import cbir
import sys
cur_path = os.path.dirname(__file__)
#sys.path.append(os.path.abspath(os.path.join(cur_path, 'apps')))
upload_prefix = './static/upload/'
EXTS = 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'GIF', 'png', 'PNG'
define("port", default=8888, help="run one the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", cbir.MainHandler),
            (r"/search", cbir.ResultsHandler),
            (r"/test", MainHandler),
        ]
        settings = {
        	"sitename": "CBIR Web Site",
        	"template_path": os.path.join(os.path.dirname(__file__), "templates"),
        	"static_path": os.path.join(os.path.dirname(__file__), "static"),
        	# "xsrf_cookies": False,
        	# "cookie_secret": "23i8ik2KOW9kajf9EW8aJmv0/R4=",
        	# "login_url": "/auth/login",
        	"autoescape": None,
        	"debug": True,
        }
    # tornado.web.Application.__init__(self, handlers, **settings)
        super(Application, self).__init__(handlers, **settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # self.write("Hello, world")
        self.render('result.html',err_msg="",imgpath="",lists=[])
    def post(self):
        err_msg = ''
        img_path = ''
        debug_flag = self.get_argument("debug", "")
        if debug_flag:
            debug = True
        else:
            debug = False
        self.render('result.html', err_msg=err_msg, imgpath=img_path,lists=[])

def _running():
    try:
        tornado.options.parse_command_line()
        http_server = tornado.httpserver.HTTPServer(Application())
        http_server.listen(options.port)
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        tornado.ioloop.IOLoop.instance().stop()
    except Exception as e:
        tb = traceback.format_exc().replace('\n', '')
        print('tornado server failed: %s' % (tb) )

if __name__ == "__main__":
    _running()
