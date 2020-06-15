# TeleRedd MemeBot 
This is a telegram bot which fetches latest memes in r/Memes using both Telegram and Reddit APIs
bot link in case you want to try : https://t.me/memes_fetcher_bot

I used sqlite to store userID and the urls/memes they received to avoid sending duplicate memes by creating a small database
```connection = sqlite3.connect('links.sqlite3')```
and creating tables with connections in between:
```curr.executescript('''
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
```

First time using the bot 

<img src="https://github.com/AYehia0/Telegram-Reddit-MemeBot/blob/master/imgs/start.png" width="400" height="800">



some features :
  - Nothing
