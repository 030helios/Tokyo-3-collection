import json
from urllib.request import urlopen
myfile = urlopen("http://140.113.167.23/se2020/product/all").read()
myfile = json.loads(myfile)
for dic in myfile:
    for inf in dic:
        print(dic[inf].replace(',', ''), end='')
        if inf != 'img_url':
            print(',', end='')
    print()
