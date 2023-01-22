$(document).ready(function () {

    if (sessionStorage.getItem('current_user_id') === null){
        window.location.href = '/'
        alert('Korisnik nije ulogovan')
    }

    $.ajax({
        url: 'http://127.0.0.1:5001/load-profile',
        type: 'GET',
        data: {
            "id": sessionStorage.getItem('current_user_id')
        },
        success: function(response) {
            document.getElementById('userId').value = response.id;
            document.getElementById('userIdCard').value = response.id;
            document.getElementById('firstName').value = response.name;
            document.getElementById('lastName').value = response.lastname;
            document.getElementById('address').value = response.address;
            document.getElementById('city').value = response.city;
            document.getElementById('country').value = response.country;
            document.getElementById('phoneNum').value = response.phoneNumber;
            document.getElementById('email').value = response.email;
            document.getElementById('balance').value = response.balance;
            document.getElementById('user').value = response.name;
            if(response.expDate != ""){
                document.getElementById('expDate').value = response.expDate;
                document.getElementById('expDate').readOnly = true;
            }
            if(response.cardNumber != ""){
                document.getElementById('cardNumber').value = response.cardNumber;
                document.getElementById('cardNumber').readOnly = true;
            }
            if(response.securityCode != ""){
                document.getElementById('code').value = response.securityCode;
                document.getElementById('code').readOnly = true;
            }
            if(response.verificated != false){
                document.getElementById('btnVerify').style.display = "none";
                document.getElementById('depositBtn').style.display = "block";
            }
            else{
                document.getElementById('btnVerify').style.display = "block";
                document.getElementById('depositBtn').style.display = "none";
            }
        }
    });
    $('#edit').submit(function(e){
        e.preventDefault();
        let id = $('#userId').val()
        let name = $('#firstName').val();
        let lastname = $('#lastName').val()
        let address = $('#address').val();
        let city = $('#city').val()
        let country = $('#country').val();
        let phoneNumber = $('#phoneNum').val()
        let email = $('#email').val();
        let password = $('#password').val()

        $.post('http://127.0.0.1:5001/update-profile', $('#edit').serialize(),
                        function (data, status) {
                            document.getElementById('userId').value = data.id;
                            document.getElementById('firstName').value = data.name;
                            document.getElementById('lastName').value = data.lastname;
                            document.getElementById('address').value = data.address;
                            document.getElementById('city').value = data.city;
                            document.getElementById('country').value = data.country;
                            document.getElementById('phoneNum').value = data.phoneNumber;
                            document.getElementById('email').value = data.email;
                            document.getElementById('user').value = data.name;
                        });
    });

    $('#verification').submit(function(e){
        e.preventDefault();
        $.post('http://127.0.0.1:5001/verify-account', $('#verification').serialize(),
                        function (data, status) {
                            if(data.cardNumber == "4244-4244-4244-4244"  && data.securityCode == "123" && data.expDate == "02/23"){
                                alert("kartica verifikovana")
                                location.reload()
                            }
                            else{
                                alert("neuspesna verifikacija kartice, probajte ponovo")
                                document.getElementById('expDate').value = "";
                                document.getElementById('code').value = "";
                                document.getElementById('cardNumber').value = "";
                                location.reload()
                            }
                        });
    });

    $('#btnDeposit').click(function () {
        money = $('#inputDeposit').val()
        if(money){
            $.post('http://127.0.0.1:5001/deposit-money', {'money': money, 'id': sessionStorage.getItem('current_user_id')},
            function (data, status) {
                document.getElementById('balance').value = JSON.stringify(data)
                location.reload()
            });
        }
        document.getElementById('inputDeposit').value = null
    });

    $.ajax({
        url: 'http://127.0.0.1:5001/accountCrypto',
        type: 'GET',
        data: {
            'id': sessionStorage.getItem('current_user_id')
        },
        success: function(response) {
            var cryptolist = "";
            console.log(response);

            $.each(response, function(key, value){
                console.log(value.name);
                console.log(value);
                cryptolist += '<tr class="table">';
                cryptolist += '<td class="table-info">' + value.cryptocurrency + '</td>';
                cryptolist += '<td class="table-info">' + value.balance + '</td>';
                cryptolist += '</tr>';
            });

            var x = document.getElementById('cryptotable');
            x.innerHTML = cryptolist;
        }
    });

    $.ajax({
        url:'http://127.0.0.1:5001/cryptolist',
        type:'GET',
        data: {
            'id': sessionStorage.getItem('current_user_id')
        },
        success: function(response) {
            var dynamicSelect = document.getElementById('filterCrypto');
            var firstOption = document.createElement('option');
            firstOption.text = "Choose crypto";
            dynamicSelect.appendChild(firstOption);
            $.each(response, function(key, value){
                var newOption = document.createElement('option');
                newOption.text = value.name;
                dynamicSelect.appendChild(newOption);
            });
            
        }
    });


    function loadTransactions(){
        $.ajax({
            url: 'http://127.0.0.1:5001/getMyTransactions',
            type: 'GET',
            data: {
                'id': sessionStorage.getItem('current_user_id')
            },
            success: function(response) {
                var table = $('#tableContent');
                table.append('<tr><th>Crypto</th><th>Amount</th><th>Price</th><th>Total</th><th>Sender</th><th>Receiver</th><th>Date</th><th>Status</th></tr>');
    
                var status;
                var i;
                for(i = 0; i < response.length; i++) {
                    if(response[i].status == 0) {
                        if(response[i].senderId === '/' )
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                    } else if(response[i].status == 2) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                    } else if(response[i].status == 1) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                    }
                }
            },
            error: function(x, y, z){
                alert(x + y + z);
            }
        });
    }
   
    loadTransactions()

    $(document).on('click', '#idSortTransactions', function() {
        var x = document.getElementById("trSort");
        if (x.style.display === "none") {
            x.style.display = "table-row";
        } else {
            x.style.display = "none";
        }
    });

    $(document).on('click', '#idFilterTransactions', function() {
        var x = document.getElementById("trFilter");
        if (x.style.display === "none") {
            x.style.display = "table-row";
        } else {
            x.style.display = "none";
        }
    });

    $(document).on('click', '#buttonSortTransactions', function(e) {
        e.preventDefault();
        var sortBy = $('#sortBy').val();
        var sortAscDesc = $('#sortAscDesc').val();

        if(sortBy.length === 0) {
            alert('Choose Sort by value!');
            return;
        }
        if(sortAscDesc.length === 0) {
            alert('Choose Sort Asc/Desc value!');
            return;
        }

        if(sortBy != "Amount" && sortBy != "Price" && sortBy != "Total" && sortBy != "Date") {
            alert('Invalid Sort by value!');
            return;
        }

        if(sortAscDesc != "Ascending" && sortAscDesc != "Descending") {
            alert('Invalid Sort Asc/Desc value!');
            return;
        }

        $.ajax({
            url: 'http://127.0.0.1:5001/getSortMyTransactions',
            type: 'POST',
            data: {
                'sortBy': sortBy,
                'sortAscDesc': sortAscDesc,
                'id': sessionStorage.getItem('current_user_id')
            },
            success: function(response) {
                var table = $('#tableContent');
                table.empty();

                table.append('<tr><th>Crypto</th><th>Amount</th><th>Price</th><th>Total</th><th>Sender</th><th>Receiver</th><th>Date</th><th>Status</th></tr>');
    
                var status;
                var i;
                for(i = 0; i < response.length; i++) {
                    if(response[i].status == 0) {
                        if(response[i].senderId === '/' )
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                    } else if(response[i].status == 2) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                    } else if(response[i].status == 1) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                    }
                }
            }
        });
    });

    $(document).on('click', '#buttonFilterTransactions', function(e) {
        e.preventDefault();

        var filterCrypto = $('#filterCrypto').val();
        var filterAmountFrom = $('#filterAmountFrom').val();
        var filterAmountTo = $('#filterAmountTo').val();
        var filterPriceFrom = $('#filterPriceFrom').val();
        var filterPriceTo = $('#filterPriceTo').val();
        var filterTotalFrom = $('#filterTotalFrom').val();
        var filterTotalTo = $('#filterTotalTo').val();
        var filterSender = $('#filterSender').val();
        var filterReceiver = $('#filterReceiver').val();
        var filterDateFrom = $('#filterDateFrom').val();
        var filterDateTo = $('#filterDateTo').val();
        var filterStatus = $('#filterStatus').val();
        
        if(filterCrypto == "Choose crypto") {
            filterCrypto = "0";
        }
        if(filterAmountFrom.length == 0) {
            filterAmountFrom = "0";
        }
        if(filterAmountTo.length == 0) {
            filterAmountTo = "0";
        }
        if(filterPriceFrom.length == 0) {
            filterPriceFrom = "0";
        }
        if(filterPriceTo.length == 0) {
            filterPriceTo = "0";
        }
        if(filterTotalFrom.length == 0) {
            filterTotalFrom = "0";
        }
        if(filterTotalTo.length == 0) {
            filterTotalTo = "0";
        }
        if(filterSender.length == 0) {
            filterSender = "0";
        }
        if(filterReceiver.length == 0) {
            filterReceiver = "0";
        }
        if(filterDateFrom.length == 0) {
            filterDateFrom = "0";
        }
        if(filterDateTo.length == 0) {
            filterDateTo = "0";
        }
        if(filterStatus == "") {
            filterStatus = "0";
        }
        
        $.ajax({
            url: 'http://127.0.0.1:5001/filterTransactions',
            type: 'POST',
            data: {
                'id': sessionStorage.getItem('current_user_id'),
                'filterCrypto': filterCrypto,
                'filterAmountFrom': filterAmountFrom,
                'filterAmountTo': filterAmountTo,
                'filterPriceFrom': filterPriceFrom,
                'filterPriceTo': filterPriceTo,
                'filterTotalFrom': filterTotalFrom,
                'filterTotalTo': filterTotalTo,
                'filterSender': filterSender,
                'filterReceiver': filterReceiver,
                'filterDateFrom': filterDateFrom,
                'filterDateTo': filterDateTo,
                'filterStatus': filterStatus
            },
            success: function(response) {
                console.log('x');
                var table = $('#tableContent');
                table.empty();

                table.append('<tr><th>Crypto</th><th>Amount</th><th>Price</th><th>Total</th><th>Sender</th><th>Receiver</th><th>Date</th><th>Status</th></tr>');
                var i;
                for(i = 0; i < response.length; i++) {
                    if(response[i].status == 0) {
                        if(response[i].senderId === '/' )
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: blue;">PROCESSING</td></tr>');
                        }
                    } else if(response[i].status == 2) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: green;">APPROVED</td></tr>');
                        }
                    } else if(response[i].status == 1) {
                        if(response[i].senderId === '/')
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                        else
                        {
                            table.append('<tr><td class="table-info">' + response[i].cryptocurrency + '</td><td class="table-info">' + response[i].amount + '</td><td class="table-info">' + response[i].price + '</td><td class="table-info">' + response[i].total + '</td><td class="table-info">' + response[i].senderId + '</td><td class="table-info">' + response[i].receiverId + '</td><td class="table-info">' + response[i].date + '</td><td class="table-info" style="color: red;">REJECTED</td></tr>');
                        }
                    }
                }
            }
        });
    });
});