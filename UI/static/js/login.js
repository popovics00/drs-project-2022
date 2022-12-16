$(document).ready(function () {

    $('form').submit(function(e){
        e.preventDefault();
        let email = $('#email').val();
        let password = $('#password').val()

        $.post('http://127.0.0.1:5001/login', $('form').serialize(),
                        function (data, status) {
                            alert(data)
                            if (JSON.stringify(data) === "true") {
                                alert("Korisnik uspesno prijavljen na sistem!")
                                window.location.href = '/';
                            }
                            else {
                                alert('Korisnik ne postoji!')
                            }
                        });
    });

});