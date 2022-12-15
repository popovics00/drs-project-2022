$(document).ready(function () {

    $('form').submit(function(e){
        e.preventDefault();
        let name = $('#firstName').val();
        let lastname = $('#lastName').val()
        let address = $('#address').val();
        let city = $('#city').val()
        let country = $('#country').val();
        let phoneNumber = $('#phoneNum').val()
        let email = $('#email').val();
        let password = $('#password').val()

        $.post('http://127.0.0.1:5001/sign-up', {"name": "dadada"},
                        function (data, status) {
                            if (data) {
                                alert(JSON.stringify(data))
                                window.location.href = '/';
                            }
                            else {
                                alert('Korisnik vec postoji!')
                            }
                        });
    });

});