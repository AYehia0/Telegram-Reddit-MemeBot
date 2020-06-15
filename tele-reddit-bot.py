import telegram 
import requests
import json
import praw
import time
import sqlite3
from datetime import datetime


#You must first send a msg to the bot : memes_fetcher_bot to get the chat_id

# For getting current time
# now = datetime.now()
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)


#Memes sent to the user - 1
memesLimit = 8

#Tokens for telegram 
my_token = ''
link = f'https://api.telegram.org/bot{my_token}/'

#Reddit Requiried constants 
clientID = ''
clientSecret = ''
reddit = praw.Reddit(client_id = clientID , client_secret = clientSecret , user_agent = 'Memes Fetchers' )

# Creating the database sqlite file and The cursor as a connection handler 
connection = sqlite3.connect('links.sqlite3')
curr = connection.cursor()

# Droping all tables 

# curr.execute('DROP TABLE IF EXISTS URLS')
# curr.execute('DROP TABLE IF EXISTS USERS')
# curr.execute('DROP TABLE IF EXISTS Receive')

#Creating the tables 
curr.executescript('''
CREATE TABLE IF NOT EXISTS USERS ( 
    
    chatID INT(10) UNIQUE,
    ask INT DEFAULT 0
    
);
CREATE TABLE IF NOT EXISTS URLS ( 
    
    linkID TEXT UNIQUE 

);
CREATE TABLE IF NOT EXISTS Receive ( 
    USER_ID INTEGER ,
    URL_ID INTEGER ,
    PRIMARY KEY (USER_ID , URL_ID)

)

''')


def get_msg(data):
    msg = data['message']['text']
    return msg

def get_chat_id(data):
    #data = last_data('getUpdates')
    chat_id = data['message']['chat']['id']
    return chat_id

def send_msg(msg):

    data = last_data('getUpdates')
    chat_id = get_chat_id(data)
    info = {'chat_id':chat_id , 'text':msg}
    response = requests.post(link + 'sendMessage' , data = info)
    #return response

#sending images with captions
def send_pic(image_url , cap_num):
    data = last_data('getUpdates')
    para = {'chat_id': get_chat_id(data) , 'photo': image_url , 'caption':cap_num }
    response = requests.post(link + 'sendPhoto' , data=para )
    #return response

#For debugging and logs
#Check existing methods : https://core.telegram.org/bots/api#getting-updates:
def all_updates (cmd = 'getFile'):
    response = requests.get(link + cmd).text
    js = json.loads(response)
    print(json.dumps(js , indent = 4))

#https://i.redd.it/aojyd4n3i3351.jpg
#urlId = 'aojyd4n3i3351'
def get_from_reddit():

    info = last_data('getUpdates')
    userid = get_chat_id(info)

    for subm in reddit.subreddit('Memes').hot(limit=memesLimit):
        
        if subm.url.endswith('.png') or subm.url.endswith('.jpg'):
            urlId = subm.url[18:][:-4] 
       
            curr.execute('INSERT OR IGNORE INTO USERS (chatID) VALUES (?) ', (userid ,))
            curr.execute('SELECT rowid FROM USERS WHERE chatID = ? ', (userid , ))
            id1 = curr.fetchone()[0]
            #print(id1)

            curr.execute('INSERT OR IGNORE INTO URLS (linkID) VALUES (?) ', (urlId ,))
            curr.execute('SELECT rowid FROM URLS WHERE linkID = ? ', (urlId , ))
            id2 = curr.fetchone()[0]
            #print(id2)
            
            try:
                curr.execute('INSERT INTO Receive (USER_ID , URL_ID) VALUES (? , ?)' ,(id1 , id2))
                send_pic(subm.url , subm.title)
                time.sleep(1.5)
                connection.commit()
            
            except sqlite3.IntegrityError as e:
                # curr.execute('SELECT rowid FROM USERS WHERE chatID = ? ', (userid , ))
                # askfor = curr.fetchone()[0]
                curr.execute('UPDATE USERS SET ask = ask + 1 WHERE chatID = ? ', (userid , ))
                connection.commit()

#Get the last number of tries by the user           
def tries():
    info = last_data('getUpdates')
    uid = get_chat_id(info)

    try:
        curr.execute('SELECT ask FROM USERS WHERE chatID = ? ', (uid , ))   
        numOfTries = curr.fetchone()[0]
        return numOfTries        
    except Exception as e:
        return 0

#Reset the number of tries
def restAsk():
    info = last_data('getUpdates')
    uid = get_chat_id(info)
    curr.execute('UPDATE USERS SET ask = 0 WHERE chatID = ? ', (uid , ))
    connection.commit()

#Getting the last messege from the telegram log
def last_data (cmd):
    response = requests.get(link + cmd).text
    js = json.loads(response)
    last_updates = js['result']

    if len(last_updates) > 0:
        fin = last_updates[ len(last_updates) - 1 ]
    else:
        fin = None
    return fin
    #return last_updates[ len(last_updates) - 1 ]



update_id = last_data('getUpdates')['update_id']

while True:
    in_update = last_data('getUpdates')
    #print(json.dumps(in_update , indent = 4))

    if update_id == in_update['update_id']:
        if get_msg(in_update).lower() == '/start':
            send_msg( f"Hey there, This bot will send you memes every time you use : /memes or memes . Please don't overuse it as it won't send and you will have to wait for latest memes in r/memes")
        if get_msg(in_update).lower() == 'memes' or get_msg(in_update).lower() == '/memes':
            get_from_reddit()
        if  tries() >= 2*(memesLimit-1) :
            send_msg('Dude, stop get a real life')
            restAsk()
                   
        update_id += 1


