# from tornado import websocket
# import tornado.ioloop

# class EchoWebSocket(websocket.WebSocketHandler):
#     def open(self):
#         print ("Websocket Opened")

#     def on_message(self, message):
#         self.write_message(u"You said: %s" % message)

#     def on_close(self):
#         print ("Websocket closed")

# application = tornado.web.Application([(r"/", EchoWebSocket),])

# if __name__ == "__main__":
#     application.listen(9000)
#     tornado.ioloop.IOLoop.instance().start()

# from simple_websocket_server import WebSocketServer, WebSocket


# class SimpleEcho(WebSocket):
#     def handle(self):
#         # echo message back to client
#         self.send_message(self.data)

#     def connected(self):
#         print(self.address, 'connected')

#     def handle_close(self):
#         print(self.address, 'closed')


# server = WebSocketServer('', 8000, SimpleEcho)
# server.serve_forever()
global ws
ws = []

def start_ws_server():
    import tornado.ioloop
    import tornado.web
    import tornado.websocket
    import tornado.template



    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            loader = tornado.template.Loader(".")
            self.write(loader.load("index.html").generate())

    class WSHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            print 'connection opened...'
            global ws
            ws.append(self)
            self.write_message("Live YangGang tweets stream is starting...")

        def on_message(self, message):
            self.write_message("The server says: " + message + " back at you")
            print 'received:', message

        def on_close(self):
            print 'stream closed...'
            remove_conn_from_list()


    def start():
            application = tornado.web.Application([
        (r'/ws', WSHandler),
        (r'/', MainHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
        ])
            application.listen(80)
            tornado.ioloop.IOLoop.instance().start()
    
    start()

def send_all(msg):
    for conn in ws :
        try:
            conn.write_message(msg)
        except:
            print("exception in conn.write_message")

def remove_conn_from_list():
    global ws
    for i, conn in enumerate(ws):
        if conn.close_code is not None:
            ws[i] = None
    
    ws = [x for x in ws if x is not None]
    print(ws)
    

import threading
threading.Thread(target=start_ws_server).start()


