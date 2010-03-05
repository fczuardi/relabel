import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from relabel import Relabel
  
def web():
  http_server = tornado.httpserver.HTTPServer(Relabel.application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()