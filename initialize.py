import json
from urllib.request import urlopen
myfile = urlopen("http://140.113.167.23/se2020/product/all").read()
myfile = json.loads(myfile)

shop = open("data/SHOP.csv", "w")
shop.write("ID,itemname,category,stock,price,img_url\n")

for dic in myfile:
    for inf in dic:
        shop.write(dic[inf].replace(',', ''))
        if inf != 'img_url':
            shop.write(',')
    shop.write('\n')
shop.close()
