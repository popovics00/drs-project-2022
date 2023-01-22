$(document).ready(function () {
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
            var dynamicSelect = document.getElementById('cryptos');
            $.each(response, function(key, value){
                var newOption = document.createElement('option');
                newOption.text = value;
                dynamicSelect.appendChild(newOption);
            })
            
        }
    })

    $('#transform').submit(function(e) {
        e.preventDefault(e);

        $.ajax({
            url: 'http://127.0.0.1:5001/executeTransaction',
            data: $('form').serialize() + "&id=" + sessionStorage.getItem('current_user_id'),
            type: 'POST',
            success: function(response) {
                alert(response)
                document.getElementById('idReceiverEmail').value = ""
                document.getElementById('idValue').value = ""
            },
            error: function(x, y, z){
                alert(z);
            }
        })
    })
})