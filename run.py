from flask import Flask, render_template, request, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'dd06be55a06c03312b2ab109b5f8f6ab'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'logout'

# config
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


class User(UserMixin):
    pass


# users to [phone,shop]
users = {}


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get('user_id')
    if username not in users:
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form['password'] == users[username]['password']

    return user


@app.route('/')
def logout():
    logout_user()
    return render_template('login.html')


@app.route('/_login', methods=['GET'])
def index():
    from queryfunc import tryLogin
    Acc = request.args.get('Account')
    Password = request.args.get('Password')

    data = tryLogin(Acc, Password)
    if data['Passed']:
        Phone = data['Phone']
        users[Acc] = [Phone, '']
        user = User()
        user.id = Acc
        login_user(user)

    return jsonify(data)


@app.route('/register')
def registerPage():
    return render_template('register.html')


@app.route('/home')
@login_required
def homePage():
    Acc = current_user.get_id()
    if(Acc == 'admin'):
        from queryfunc import getItemNames
        Itemnames = getItemNames()
        Status = ['All', 'Paid', 'Not Finished', 'Finished', 'Cancelled']
        return render_template('admin.html', Status=Status, Itemnames=Itemnames)
    else:
        return render_template('home.html', Acc=Acc, Phone=users[Acc][0])


@app.route('/shop')
@login_required
def shopPage():
    from queryfunc import EmployeesOfShop, hasShop, getCities
    Acc = current_user.get_id()
    Cities = getCities()
    dic = hasShop(Acc)
    HasShop = dic['HasShop']
    MyShop = dic['Shop']
    MyCity = dic['City']
    MyPrice = dic['Price']
    MyAmount = dic['Amount']
    Employees = EmployeesOfShop(MyShop)
    if(HasShop == True):
        users[Acc][1] = MyShop
        return render_template('shop.html', MyShop=MyShop, MyCity=MyCity, MyPrice=MyPrice, MyAmount=MyAmount, Employees=Employees)
    return render_template('registerShop.html', Cities=Cities)


@app.route('/myOrder')
@login_required
def myOrder():
    Status = ['All', 'Paid', 'Not Finished', 'Finished', 'Cancelled']
    return render_template('myOrder.html', Status=Status)


@app.route('/_register', methods=['GET'])
def _tryRegister():
    from queryfunc import tryRegister
    Acc = request.args.get('Account')
    Pwd = request.args.get('Password')
    ConPwd = request.args.get('ConfirmPassword')
    Phone = request.args.get('PhoneNumber')
    data = tryRegister(Acc, Pwd, ConPwd, Phone)
    return jsonify(data)


@app.route('/_searchGoods', methods=['GET'])
def _searchGoods():
    from queryfunc import searchGoods
    Itemname = request.args.get('Itemname')
    LowPrice = request.args.get('LowPrice')
    HighPrice = request.args.get('HighPrice')
    data = searchGoods(Itemname, LowPrice, HighPrice)
    return jsonify(data)


@app.route('/_PriceChange', methods=['GET'])
def _PriceChange():
    from queryfunc import PriceChange
    Price = request.args.get('Price')
    Itemname = request.args.get('Itemname')
    data = PriceChange(Itemname, Price)
    return jsonify(data)


@app.route('/_AmountChange', methods=['GET'])
def _AmountChange():
    from queryfunc import AmountChange
    Amount = request.args.get('Amount')
    Itemname = request.args.get('Itemname')
    data = AmountChange(Itemname, Amount)
    return jsonify(data)


@app.route('/_searchMyOrderList', methods=['GET'])
def _searchMyOrderList():
    from queryfunc import searchMyOrderList
    Status = request.args.get('Status')
    Acc = current_user.get_id()
    data = searchMyOrderList(Acc, Status)
    return jsonify(data)


@app.route('/_searchShopOrderList', methods=['GET'])
def _searchShopOrderList():
    from queryfunc import searchShopOrderList
    _Shop = request.args.get('Shop')
    Status = request.args.get('Status')
    data = searchShopOrderList(_Shop, Status)
    return jsonify(data)


@app.route('/_Order', methods=['GET'])
def _Order():
    from queryfunc import Order
    Amount = request.args.get('Amount')
    _Shop = request.args.get('Shop')
    Acc = current_user.get_id()
    data = Order(Acc, _Shop, Amount)
    # return message: success or fail and why
    return jsonify(data)


@app.route('/_DelOrder', methods=['GET'])
def _DelOrder():
    from queryfunc import DelOrder
    OID = request.args.get('OID')
    Acc = current_user.get_id()
    data = DelOrder(Acc, OID)
    # return message: success or fail and why
    return jsonify(data)


@app.route('/_DoneOrder', methods=['GET'])
def _DoneOrder():
    from queryfunc import DoneOrder
    OID = request.args.get('OID')
    Acc = current_user.get_id()
    data = DoneOrder(Acc, OID)
    # return message: success or fail and why
    return jsonify(data)


@app.route('/_DelAllOrder', methods=['GET'])
def _DelAllOrder():
    from queryfunc import DelAllOrder
    Acc = current_user.get_id()
    OIDs = request.args.get('OIDs').split()
    data = DelAllOrder(Acc, OIDs)
    # return message: success or fail and why
    return jsonify(data)


@app.route('/_PayAllOrder', methods=['GET'])
def _PayAllOrder():
    from queryfunc import PayAllOrder
    Acc = current_user.get_id()
    OIDs = request.args.get('OIDs').split()
    data = PayAllOrder(Acc, OIDs)
    # return message: success or fail and why
    return jsonify(data)


@app.route('/_DoneAllOrder', methods=['GET'])
def _DoneAllOrder():
    from queryfunc import DoneAllOrder
    Acc = current_user.get_id()
    OIDs = request.args.get('OIDs').split()
    data = DoneAllOrder(Acc, OIDs)
    # return message: success or fail and why
    return jsonify(data)
