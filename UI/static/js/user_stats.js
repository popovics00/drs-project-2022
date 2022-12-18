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
            document.getElementById('firstName').value = response.name
            document.getElementById('lastName').value = response.lastname;
            document.getElementById('address').value = response.address;
            document.getElementById('city').value = response.city;
            document.getElementById('country').value = response.country;
            document.getElementById('phoneNum').value = response.phoneNumber;
            document.getElementById('email').value = response.email;
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
                            document.getElementById('firstName').value = data.name
                            document.getElementById('lastName').value = data.lastname;
                            document.getElementById('address').value = data.address;
                            document.getElementById('city').value = data.city;
                            document.getElementById('country').value = data.country;
                            document.getElementById('phoneNum').value = data.phoneNumber;
                            document.getElementById('email').value = data.email;
                            window.location.href = '/user-stats'
                        });
    });
});