# Music Generator Bot

**https://t.me/music_gen_bot**

Here you can find a telegram bot that generates a simple melody from given sounds.

## How to use

You can write `/start` and the bot will send you simple instructions. 

You can write `1` and the bot will generate a random melody from random Samples, using random Instrumental as the base.

You can send bot your `.wav` files(not too big, 5 seconds is enough) and after you send bot `3` it will generate a melody from your files 

## How to create your bot

1) You need to install some libraries:

```pip3 install pyTelegramBotApi requests psycopg2 wave```

2) Generate your Bot's token, using [Bot Father](https://t.me/BotFather)
3) Create config.py file which contains one line:
```python
token = "insert your token here"
```
4) You need to create your local database, for example on macOS:
```brew services start postgresql
initdb /usr/local/var/postgres -E utf8
psql -h localhost -d postgres
CREATE DATABASE name_of_base;
CREATE USER user_name WITH ENCRYPTED PASSWORD 'your_password';
GRANT ALL ON DATABASE name_of_base TO user_name;
```
5) At ```database.py``` input information about your database and uncomment code which creates a table
6) Run ```python3 generator.py``` if everything is ok you will see ```connceted to db created a table```
7) Comment code which creates the table and run ```python3 bot.py```
8) Now you can download more `.wav` samples in `Samples` and `Instrumental` directories, to make your music
