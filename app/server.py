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
    
    http_server.listen(80)
    
    ioloop.IOLoop.instance().start()


#end
