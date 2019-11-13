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
leaderboard = {}
import json

def start_ws_server():
    import tornado.ioloop
    import tornado.web
    import tornado.websocket
    import tornado.template



    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            loader = tornado.template.Loader(".")
            self.write(loader.load("index.html").generate())
        
        # def set_default_headers(self):
        #     print("setting headers!!!")
        #     self.set_header("Access-Control-Allow-Origin", "*")
        #     self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        #     self.set_header('Access-Control-Allow-Methods', ' PUT, DELETE, OPTIONS')

        # def options(self):
        #     # no body
        #     self.set_status(204)
        #     self.finish()

    class WSHandler(tornado.websocket.WebSocketHandler):
        def open(self):
            print 'connection opened...'
            global ws
            ws.append(self)
            lb = {'lb':leaderboard}
            self.write_message(lb)

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


#Tweet class with all the information we need for this program (Hashtags and the actual tweet text)
class Tweet:
        text = str()
	hashtags = []

        def __init__(self, json):
		self.text = json["text"] 
		self.username = json["user"]["screen_name"]
		self.hashtags = json["entities"]["hashtags"]

def send_all(msg):
    jsonData = json.loads(msg)
    tweet = Tweet(jsonData)
    update_lb(str(tweet.username))

    # print(tweet.text.encode('utf-8'))
    # print(tweet.username.encode('utf-8'))
    # print(tweet.hashtags)
    for conn in ws :
        try:
            conn.write_message(json.dumps((tweet.__dict__)))
        except:
            print("exception in conn.write_message")

def update_lb(name):
    try :
        leaderboard[name] = leaderboard[name] + 1
    except KeyError:
        leaderboard[name] = 1

def remove_conn_from_list():
    global ws
    for i, conn in enumerate(ws):
        if conn.close_code is not None:
            ws[i] = None
    
    ws = [x for x in ws if x is not None]
    print(ws)
    

import threading
threading.Thread(target=start_ws_server).start()


