組員：凃少麒 宋儼哲

網站使用Flask架設

下載dependencies
```
pip install -r requirements.txt
```
開啟網站
```
FLASK_APP=run.py flask run
```

The way to create "data.db"
1. run "sqlite3 data/data.db"
2. run the code below
```
.mode csv
.separator ","
.import data/USER.csv user
.import data/SHOP.csv shop
.import data/ORDER.csv order_
.exit
```