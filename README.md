# 軟體工程概論
## 組員：凃少麒 宋儼哲
網站使用Flask架設
## 下載dependencies
```
pip install -r requirements.txt
```
## 開啟網站
```
FLASK_APP=run.py flask run
```
## 資料庫重啓
```
python3 initialize.py
rm data/data.db
```
```
sqlite3 data/data.db
.mode csv
.separator ","
.import data/USER.csv user
.import data/SHOP.csv shop
.import data/ORDER.csv order_
.exit
```
