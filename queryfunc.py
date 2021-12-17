# Remember to put string in '' when writing query

def prevent(target):
    if target.find('=') != -1 or target.find("'") != -1 or target.find('#') != -1:
        return False  # Illegal character detected
    else:
        return True


def tryLogin(Acc, pwd):
    import sqlite3
    import hashlib
    m = hashlib.md5()

    data = {'Passed': False, 'Phone': ''}

    if prevent(Acc) == False or prevent(pwd) == False:
        print("Not passed")
        return data

    query = \
        "select username, pwd, phone \
        from user \
        where username = '" + str(Acc) + "'"

    db = sqlite3.connect("data.db")
    cursor = db.cursor()
    cursor.execute(query)
    row = cursor.fetchone()

    print(row)

    if row == None:
        print("Not passed")
        db.close()
        return data

    else:
        m.update(pwd.encode('utf-8'))
        h = m.hexdigest()

        if h == row[1]:
            print("Passed")
            db.close()
            data['Passed'] = True
            data['Phone'] = row[2]
            return data
        else:
            print("Not passed")
            db.close()
            return data


def tryRegister(Acc, Pwd, ConPwd, Phone):
    import sqlite3
    import hashlib
    import random
    m = hashlib.md5()

    data = {'0': "", '1': "", '2': "", '3': ""}

    noEx = True

    if Acc == "":
        data['0'] = "Required!"
        noEx = False
    if Pwd == "":
        data['1'] = "Required!"
        noEx = False
    if ConPwd == "":
        data['2'] = "Required!"
        noEx = False
    if Phone == "":
        data['3'] = "Required!"
        noEx = False
    if Pwd != ConPwd:
        data['2'] = "Password_mismatch"
        noEx = False
    if Pwd.isalnum() == False and Pwd != "":
        data['1'] = "Invalid password format"
        noEx = False
    if Phone.isdigit() == False and Phone != "":
        data['3'] = "Invalid phone format"
        noEx = False
    # error here when register
        '''
    if target(Acc) == False:
        data['0'] = "Illegal character detected"
        noEx = False     
        '''

    if not noEx:
        return data

    query1 = \
        "select username\
    from user\
    where username = '" + str(Acc) + "'"

    print(query1)

    db = sqlite3.connect("data.db")
    print(db)
    cursor = db.cursor()
    print(cursor)
    cursor.execute(query1)
    # error here no such column username

    row = cursor.fetchall()
    print(row)

    if row != []:
        print("repeated")
        data['0'] = "Username is repeated"
        noEx = False

    if noEx:
        data['0'] = "Register success!"
        print("insert")
        m.update(Pwd.encode('utf-8'))
        h = m.hexdigest()

        U_ID = str(random.randint(1000000, 9999999))

        query2 = "insert into user\
        values('" + U_ID + "','" + str(Acc) + "','" + str(h) + "','" + str(Phone) + "')"
        print(query2)

        cursor.execute(query2)
        db.commit()

    db.close()
    return data


def searchGoods(Itemname, LowPrice, HighPrice, name):
    import sqlite3
    data = {'data': []}
    query = \
        "select itemname, img_url, price, stock from shop where "
    if LowPrice != "" and HighPrice != "":
        if int(LowPrice) > int(HighPrice):
            LowPrice, HighPrice = HighPrice, LowPrice

    if Itemname != "" and prevent(Itemname) != False:
        query += "itemname like '%" + str(Itemname) + "%' and  "
    if LowPrice != "" and prevent(LowPrice) != False:
        query += "price >= " + str(LowPrice) + " and  "
    if HighPrice != "" and prevent(HighPrice) != False:
        query += "price <= " + str(HighPrice) + " and  "
    query = query[0:-6]

    print(query)
    db = sqlite3.connect("data.db")
    cursor = db.execute(query)
    for row in cursor:
        print(row)
        if(row[-1] != "0"):
            insert = []
            for r in row:
                insert.append(r)
            data['data'].append(insert)

    return data


def PriceChange(Shop, Price):
    import sqlite3
    Price.replace(' ', '')
    data = {"data": ""}
    db = sqlite3.connect("data.db")

    if Price.isdigit() == False:
        data["data"] = "Invalid format"
        return data
    if int(Price) < 0:
        data["data"] = "Invalid value"
        return data

    query = "update shop\
        set price = " + str(Price) + " where itemname = '" + str(Shop) + "'"
    cursor = db.execute(query)
    db.commit()
    data["data"] = "Price succesfully changed"
    return data


def AmountChange(Shop, Amount):
    import sqlite3
    Amount.replace(' ', '')
    data = {"data": ""}
    db = sqlite3.connect("data.db")

    if Amount.isdigit() == False:
        data["data"] = "Invalid format"
        return data
    if int(Amount) < 0:
        data["data"] = "Invalid value"
        return data

    query = "update shop\
        set stock = " + str(Amount) + " where itemname = '" + str(Shop) + "'"
    cursor = db.execute(query)
    db.commit()
    data["data"] = "Amount succesfully changed"
    return data


def searchMyOrderList(Acc, Status):
    import sqlite3
    data = {'data': []}

    query = \
        "select orderID, stat, time_start, time_end, itemname, order_price\
    from order_\
    where orderer = '" + str(Acc) + "'         "

    if Status != "All":
        query += " and stat = '" + str(Status) + "'      "
    query = query[0:-6]

    print(query)

    db = sqlite3.connect("data.db")
    cursor = db.execute(query)

    print(cursor)

    for row in cursor:
        insert = []
        for i in row:
            insert.append(i)
        data['data'].append(insert)

    print(data)

    return data


def Order(Acc, Shop, Amount):
    import sqlite3
    import time

    data = {"data": ""}

    if Amount.isdigit() == False or int(Amount) <= 0:
        data["data"] = "Illegal input Amount"
        return data

    query1 = "select stock, price\
    from shop\
    where itemname = '" + str(Shop) + "'"
    print(query1)

    db = sqlite3.connect("data.db")
    cursor = db.execute(query1)
    row = cursor.fetchone()

    inventory = int(row[0])
    price = int(row[1])

    if int(Amount) > inventory:
        data["data"] = "Amount is larger than the inventory of the shop"
        return data

    result = inventory - int(Amount)

    query_ = "update shop\
    set stock = " + str(result) + " where itemname = '" + str(Shop) + "'"
    cursor = db.execute(query_)
    db.commit()

    query2 = 'select count (distinct orderID)\
    from order_'
    cursor = db.execute(query2)
    row = cursor.fetchone()
    OID = row[0] + 1

    print(OID)

    t = time.localtime()
    time_start = time.strftime("%Y_%m_%d_%H_%M_%S")

    query3 = "insert into order_\
    values(" + str(OID) + ",'Not Finished','" + str(Acc) + "','" + str(Shop) + "','" + str(time_start) + "','" + "" + "'," + str(Amount) + "," + str(int(Amount) * price) + ")"
    print(query3)

    cursor = db.execute(query3)
    db.commit()

    data["data"] = "Successfully ordered"

    return data


def DelOrder(Acc, OID):
    import sqlite3
    import time
    data = {"data": ""}
    query = "select orderID, stat, order_amount, itemname\
    from order_\
    where orderID = " + str(OID) + ""

    db = sqlite3.connect("data.db")
    cursor = db.execute(query)
    row = cursor.fetchone()

    print(row)
    amount = int(row[2])
    shop = str(row[3])

    if row == None:
        data["data"] = "Order doesn't exist"
        return data

    if str(row[1]) == "Cancelled":
        data["data"] = "The order number " + str(OID) + " is already cancelled"
        return data

    if str(row[1]) == "Finished":
        data["data"] = "Finished order can't be cancelled"
        return data

    t = time.localtime()
    time_end = time.strftime("%Y_%m_%d_%H_%M_%S")

    query1 = "update order_\
    set stat = " + "'Cancelled'\
    where orderID = " + str(OID) + ""

    cursor = db.execute(query1)
    db.commit()

    query2 = "update order_\
    set time_end = '" + str(time_end) + "'\
    where orderID = " + str(OID) + ""

    cursor = db.execute(query2)
    db.commit()

    query3 = "select stock\
    from shop\
    where itemname = '" + shop + "'"

    cursor = db.execute(query3)
    row = cursor.fetchone()

    remain = int(row[0])
    result = remain + amount

    query4 = "update shop\
    set stock = " + str(result) + " where itemname = '" + shop + "'"
    cursor = db.execute(query4)
    db.commit()

    data["data"] = "Order successfully cancelled"
    return data


def DelAllOrder(Acc, OIDs):
    import sqlite3
    import time

    data = {"data": ""}
    print("DelAllOrder")
    print(OIDs)

    for OID in OIDs:
        d = DelOrder(Acc, OID)
        if(d["data"] != "Order successfully cancelled"):
            data["data"] += d["data"] + "<br>"

    if data["data"].endswith("<br>"):
        data["data"] = data["data"][:-6]

    if data["data"] == "":
        data["data"] = "Orders successfully cancelled"

    return data


def DoneOrder(Acc, OID):
    import sqlite3
    import time
    data = {"data": ""}
    query1 = "select itemname, order_amount, stat\
    from order_\
    where orderID = " + str(OID) + ""

    db = sqlite3.connect("data.db")
    cursor = db.execute(query1)
    row = cursor.fetchone()

    shop = str(row[0])
    amount = int(row[1])
    stat = str(row[2])

    if stat == "Cancelled":
        data["data"] = "The order is already cancelled"
        return data

    if stat == "Finished":
        data["data"] = "Finished order can't be cancelled"
        return data

    t = time.localtime()
    time_end = time.strftime("%Y_%m_%d_%H_%M_%S")

    query4 = "update order_\
    set stat = " + "'Finished'\
    where orderID = " + str(OID) + ""

    cursor = db.execute(query4)
    db.commit()

    query5 = "update order_\
    set time_end = '" + str(time_end) + "'\
    where orderID = " + str(OID) + ""

    cursor = db.execute(query5)
    db.commit()

    query6 = "update order_\
    set seller = '" + str(Acc) + "'\
    where orderID = " + str(OID) + ""

    cursor = db.execute(query6)
    db.commit()

    data["data"] = "Order successfully done"

    return data
