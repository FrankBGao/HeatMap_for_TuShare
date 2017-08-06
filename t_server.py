from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer
from stock_price import app


server = HTTPServer(WSGIContainer(app))
server.listen(5001)
IOLoop.current().start()