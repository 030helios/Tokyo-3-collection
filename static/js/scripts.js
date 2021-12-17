$(document).ready(function () {
});

$("#LoginBtn").bind("click", function () {
    const form = document.forms["Login"];
    const Account = form.elements.Account.value;
    const Password = form.elements.Password.value;
    var data = {
        Account: Account,
        Password: Password
    }
    $.ajax({
        url: '/_login',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            if (result['Passed'])
                window.location = '/home';
            else
                alert("login failed")
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$("#RegisterBtn").bind("click", function () {
    const form = document.forms["Register"];
    const Account = form.elements.Account.value;
    const Password = form.elements.Password.value;
    const ConfirmPassword = form.elements.ConfirmPassword.value;
    const PhoneNumber = form.elements.PhoneNumber.value;
    var data = {
        Account: Account,
        Password: Password,
        ConfirmPassword: ConfirmPassword,
        PhoneNumber: PhoneNumber
    }
    errHead = '<nobr id="errMsg">';
    errEnd = '</nobr>';
    $.ajax({
        url: '/_register',
        type: 'GET',
        data: data,
        beforeSend: function () {
            $("nobr").remove('#errMsg');
        },
        success: function (result) {
            if (result[0] == 'Register success!') {
                alert(result[0]);
                window.location = '/';
            }
            else {
                if (result[0] != '')
                    $('#M0').append(errHead + result[0] + errEnd)
                if (result[1] != '')
                    $('#M1').append(errHead + result[1] + errEnd)
                if (result[2] != '')
                    $('#M2').append(errHead + result[2] + errEnd)
                if (result[3] != '')
                    $('#M3').append(errHead + result[3] + errEnd)
            }
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$("#SearchGoodsbtn").bind("click", function () {
    const form = document.forms["ShopSelect"];
    const Itemname = form.elements.Itemname.value;
    const LowPrice = form.elements.LowPrice.value;
    const HighPrice = form.elements.HighPrice.value;
    var data = {
        Itemname: Itemname,
        LowPrice: LowPrice,
        HighPrice: HighPrice
    }
    $.ajax({
        url: '/_searchGoods',
        type: 'GET',
        data: data,
        beforeSend: function () {
            $('#goodsWrap').empty();
        },
        success: function (result) {
            var insertText = '';
            for (var i = 0; i < result.data.length; i++) {
                insertText += '<div class="col-lg-3 col-sm-6 col-md-3"><a><div class="box-img"><h5>'
                insertText += result.data[i][0];
                insertText += '<br>$'
                insertText += result.data[i][2];
                insertText += ' '
                insertText += result.data[i][3];
                insertText += ' left<br><input type="text" name="Amount" id="_';
                insertText += result.data[i][0];
                insertText += '" size="';
                insertText += Math.ceil(Math.log(parseInt(result.data[i][3]))).toString()
                insertText += '"/>  <button type="button" class="OrderBtn" id="';
                insertText += result.data[i][0];
                insertText += '">Buy!</button></h5><img src="';
                insertText += result.data[i][1];
                insertText += '" width="300" height="300" alt="" /></div></a></div>';
            }
            $('#goodsWrap').append(insertText);
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$("#goodsWrap").on("click", ".OrderBtn", function () {
    var data = {
        Shop: this.id,
        Amount: document.getElementById('_' + this.id).value
    }
    $.ajax({
        url: '/_Order',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            alert(result.data)
            location.reload();
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$("#SearchMyOrderbtn").bind("click", function () {
    const form = document.forms["OrderSelect"];
    const Status = form.elements.Status.value;
    var data = {
        Status: Status
    }
    $.ajax({
        url: '/_searchMyOrderList',
        type: 'GET',
        data: data,
        beforeSend: function () {
            $("table").remove('#orderWrapData');
        },
        success: function (result) {
            var insertText = '<table class="table" id="orderWrapData"><thead>';
            insertText += '<tr><td>OID</td>\
            <td>Status</td>\
            <td>Start</td>\
            <td>End</td>\
            <td>Item name</td>\
            <td>Total price</td>\
            <td>Action</td>\
            </tr></thead>';
            for (var i = 0; i < result.data.length; i++) {
                insertText += '<tr><td>';
                if (result.data[i][1] == "Not Finished") {
                    insertText += '<label class="switch"><input type="checkbox" class="chkboxName" id="';
                    insertText += result.data[i][0] + '"value="' + result.data[i][0];
                    insertText += '"></label>';
                }
                insertText += result.data[i][0];
                insertText += '</td>';
                for (var j = 1; j < result.data[i].length; j++) {
                    insertText += '<td>';
                    insertText += result.data[i][j];
                    insertText += '</td>';
                }
                insertText += '<td><button type="button" class="DelOrderBtn" id="';
                insertText += result.data[i][0];
                insertText += '">X</button></td></tr>';
            }
            insertText += '</table>';

            $('#orderWrap').append(insertText);
        }
    })
})

$("#orderWrap").on("click", ".DelOrderBtn", function () {
    var data = {
        OID: this.id
    }
    $.ajax({
        url: '/_DelOrder',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            alert(result.data)
            location.reload();
        },
        complete: function () {
        },
        error: function () {
        }
    })
})
$("#orderWrap").on("click", ".DoneOrderBtn", function () {
    var data = {
        OID: this.id
    }
    $.ajax({
        url: '/_DoneOrder',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            alert(result.data)
            location.reload();
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$(".DelAllOrderBtn").bind("click", function () {
    var checkboxesChecked = "";
    $("input[type=checkbox]:checked").each(function () {
        checkboxesChecked += ($(this).val());
        checkboxesChecked += " ";
    });
    var data = {
        OIDs: checkboxesChecked
    }
    $.ajax({
        url: '/_DelAllOrder',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            alert(result.data)
            location.reload();
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$(".DoneAllOrderBtn").bind("click", function () {
    var checkboxesChecked = "";
    $("input[type=checkbox]:checked").each(function() {
        checkboxesChecked+=($(this).val());
        checkboxesChecked+=" ";
    });
    var data = {
        OIDs: checkboxesChecked
    }
    $.ajax({
        url: '/_DoneAllOrder',
        type: 'GET',
        data: data,
        beforeSend: function () {
        },
        success: function (result) {
            alert(result.data)
            location.reload();
        },
        complete: function () {
        },
        error: function () {
        }
    })
})

$("#SearchShopOrderbtn").bind("click", function () {
    const form = document.forms["OrderSelect"];
    const Status = form.elements.Status.value;
    const Itemname = form.elements.Itemname.value;
    var data = {
        Status: Status,
        Shop: Itemname
    }
    $.ajax({
        url: '/_searchShopOrderList',
        type: 'GET',
        data: data,
        beforeSend: function () {
            $("table").remove('#searchWrapData');
        },
        success: function (result) {
            var insertText = '<table class="table" id="searchWrapData"><thead>';
            insertText += '<tr><td>OID</td>\
            <td>Orderer</td>\
            <td>Status</td>\
            <td>Start</td>\
            <td>End</td>\
            <td>Item name</td>\
            <td>Total price</td>\
            <td>Action</td>\
            </tr></thead>';
            for (var i = 0; i < result.data.length; i++) {
                insertText += '<tr><td>';
                if (result.data[i][2] == "Not Finished") {
                    insertText += '<label class="switch"><input type="checkbox" class="chkboxName" id="';
                    insertText += result.data[i][0] + '"value="' + result.data[i][0];
                    insertText += '"></label>';
                }
                insertText += result.data[i][0];
                insertText += '</td>';
                for (var j = 1; j < result.data[i].length; j++) {
                    insertText += '<td>';
                    insertText += result.data[i][j];
                    insertText += '</td>';
                }
                if (result.data[i][1] == "Not Finished") {

                    insertText += '<td><button type="button" class="DoneOrderBtn" id="';
                    insertText += result.data[i][0];
                    insertText += '">Done</button><button type="button" class="DelOrderBtn" id="';
                    insertText += result.data[i][0];
                    insertText += '">X</button></td>';
                }
                insertText += '</tr>';
            }
            insertText += '</table>';
            $('#searchWrap').append(insertText);
        }
    })
})
