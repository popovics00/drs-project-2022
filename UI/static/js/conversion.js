$(document).ready(function() {

    if (sessionStorage.getItem('current_user_id') === null){
        window.location.href = '/'
        alert('Korisnik nije ulogovan')
    }

    $.ajax({
        url:'http://127.0.0.1:5001/getUserCryptos',
        type:'GET',
        data: {
            'id': sessionStorage.getItem('current_user_id')
        },
        success: function(response) {
            var dynamicSelect = document.getElementById('myCrypto');
            var firstOption = document.createElement('option');
            firstOption.text = "Choose your crypto";
            dynamicSelect.appendChild(firstOption);
            $.each(response, function(key, value){
                var newOption = document.createElement('option');
                newOption.text = value;
                dynamicSelect.appendChild(newOption);
            });
            
        }
    });

    var listAllCryptos;

    $.ajax({
        url:'http://127.0.0.1:5001/cryptolist',
        type:'GET',
        success: function(response) {
            listAllCryptos = response;
            var dynamicSelect = document.getElementById('allCryptos');
            var firstOption = document.createElement('option');
            firstOption.text = "Choose any crypto";
            dynamicSelect.appendChild(firstOption);
            var i;
            for(i = 0; i < response.length; i++) {
                var newOption = document.createElement('option');
                newOption.text = response[i].name;
                dynamicSelect.appendChild(newOption);
            }            
        }
    });

    $(document).on('click', '#buttonConfirmConversion', function(e) {
        e.preventDefault()
        
        var myCrypto = $('#myCrypto').val();
        var allCryptos = $('#allCryptos').val();
        var inputConvertAmount = $('#inputConvertAmount').val();

        if(myCrypto == "Choose your crypto" || allCryptos == "Choose any crypto" || inputConvertAmount.length === 0) {
            alert('You didn\'t fill the form!');
            return;
        }

        if(myCrypto == allCryptos) {
            alert('You chose the same currency to convert to!');
            return;
        }

        var cryptoValue;
        var myCryptoValue;
        var i;
        for(i = 0; i < listAllCryptos.length; i++) {
            if(listAllCryptos[i].name == allCryptos) {
                cryptoValue = listAllCryptos[i].value;
            }
            if(listAllCryptos[i].name == myCrypto) {
                myCryptoValue = listAllCryptos[i].value;
            }
        }
        console.log(myCrypto + ',' + allCryptos + ',' + inputConvertAmount + ',' + cryptoValue + ',' + myCryptoValue)
        $.ajax({
            url:'http://127.0.0.1:5001/confirmConversion',
            type:'POST',
            data: {
                'id': sessionStorage.getItem('current_user_id'),
                'myCrypto': myCrypto,
                'allCryptos': allCryptos,
                'inputConvertAmount': inputConvertAmount,
                'cryptoValue': cryptoValue,
                'myCryptoValue': myCryptoValue
            },
            success: function(response) {
                if(response == "Uspesna transakcija.") {
                    document.getElementById('allCryptos').value = "Choose any crypto";
                    document.getElementById('myCrypto').value = "Choose your crypto";
                    document.getElementById('inputConvertAmount').value = "";
                    alert('Your conversion was successfull!');
                }
                else {
                    alert('Your conversion was not successfull!');
                }
            }
        });

    })

});