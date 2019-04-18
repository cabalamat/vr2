# server.py

"""
For running app on Tornado server
"""

from tornado import wsgi
from tornado import httpserver, ioloop
from main import *

if __name__ == "__main__":
    container = wsgi.WSGIContainer(app)
    http_server = httpserver.HTTPServer(container)
    
    ##### PH changes 2-Feb-2019
    http_server.bind(8300)
    http_server.start(8300)
    
    ioloop.IOLoop.instance().start()


#end
