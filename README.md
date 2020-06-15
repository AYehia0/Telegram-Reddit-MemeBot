# **TeleRedd MemeBot** 
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



**Features** :
  - Nothing

**Bugs** :
  - As telegram API deletes the messages log every 24 hours : https://core.telegram.org/bots/api#getting-updates
  
     ```Incoming updates are stored on the server until the bot receives them either way, but they will not be kept longer than 24 hours.```
     
     this error ocurred while fetching the last messege from the empty log: 
  
    ```update_id = last_data('getUpdates')['update_id']```
  
  - some other unknown trash problems in addition to messy code (**ineffective**)
