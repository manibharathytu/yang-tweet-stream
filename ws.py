
global ws
global winner
ws = []
leaderboard = {}
winner = ""
import json
import helper
import pickle
from datetime import datetime
import os

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
            champ = {'winner':winner}
            self.write_message(lb)
            self.write_message(champ)
        def check_origin(self, origin):
            return True     
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
		self.id = json["id_str"]

def send_tweet(msg):
    jsonData = json.loads(msg)
    tweet = Tweet(jsonData)
    update_lb(str(tweet.username))
    send_to_all(json.dumps(tweet.__dict__))


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

def send_lb():
    lb = {'lb':leaderboard}
    send_to_all(lb)


def send_winner():

    send_to_all({'winner':winner})

  

def send_to_all(msg):
    for conn in ws :
        try:
            conn.write_message(msg)
        except:
            print("exception in conn.write_message")

def reset_lb() :
    print('reset lb')
    set_winner()
    print(winner)
    global leaderboard
    leaderboard = {}
    send_lb()
    send_winner()

def set_winner():
     global winner
     winner =   max(leaderboard, key=leaderboard.get)
def reset_lb_daily():
    import schedule, time
    schedule.every().day.at("00:00").do(reset_lb) #00:00 ET is 05:00 in GMT, #yang2020.com follows ET
    while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
        schedule.run_pending() 
        time.sleep(10) 

def backup_mem():
    with open('lb.pickle', 'wb') as handle:
            pickle.dump(leaderboard, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('winner.pickle', 'wb') as handle:
            pickle.dump(winner, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_data():
    global leaderboard
    global winner
    if is_same_day() :
        try :
            with open('lb.pickle', 'rb') as handle:
                leaderboard = pickle.load(handle)
            with open('winner.pickle', 'rb') as handle:
                winner = pickle.load(handle)
        except :
            print('backup error') 

def is_same_day():   
    current_date = datetime.now().strftime('%Y-%m-%d')
    backup_date = datetime.fromtimestamp(os.stat('lb.pickle').st_mtime).strftime('%Y-%m-%d')
    return current_date == backup_date
    
load_data()
helper.set_interval(send_lb, 10)
helper.set_interval(backup_mem, 100)
import threading
threading.Thread(target=start_ws_server).start()
threading.Thread(target=reset_lb_daily).start()



