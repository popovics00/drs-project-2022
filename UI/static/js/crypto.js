$(document).on('click', '#buycrypto', function() {
    var cryptoName = $(this).closest('tr').find('td:eq(0)').text();
    var price = $(this).closest('tr').find('td:eq(1)').text();
    var amount = $(this).closest('tr').find("td:eq(3) input[type='text']").val();
    var element =  $(this).closest('tr').find("td:eq(3) input[type='text']");

    $.ajax({
        url: 'http://127.0.0.1:5001/buycrypto',
        type: 'POST',
        data: {
            'amount': amount,
            'crypto': cryptoName,
            'price': price,
            'id': sessionStorage.getItem('current_user_id')
        },
        success: function(response) {
            alert(response);
            element.val('');
        },
        error: function(x, y, z) {
            alert(x + y + z);
        }
    })
})

$(document).ready(function () {
    $.ajax({
        url: 'http://127.0.0.1:5001/cryptolist',
        type: 'GET',
        success: function(response) {
            var cryptolist = "";
            // console.log(response);
            // console.log(sessionStorage)

            $.each(response, function(key, value){
                cryptolist += '<tr>';
                cryptolist += '<td>' + value.name + '</td>';
                cryptolist += '<td>' + value.value + '</td>';
                cryptolist += '<td>' + value.change24h + '</td>';
                if(sessionStorage.getItem("current_user_id") != null){
                    cryptolist += '<td> <input type="text"> </td>';
                    cryptolist += '<td> <button id="buycrypto" class="btn btn-primary">Buy</button></td>';
                }
                else
                {
                    cryptolist += '<td> <input disabled type="text"> </td>';
                    cryptolist += '<td> <button disabled id="buycrypto" class="btn btn-primary">Buy</button></td>';
                }
                cryptolist += '</tr>';
            })

            var x = document.getElementById('cryptotable');
            x.innerHTML = cryptolist;
        }
    })

})
