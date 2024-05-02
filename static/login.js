$(document).ready(function() {
    $('#loginForm').on('submit', function(e) {
        e.preventDefault();  
        var email = $('#inputEmail').val();
        var password = $('#inputPassword').val();
        $.ajax({
            type: "POST",
            url: "/auth/login_trad", 
            contentType: "application/json",
            data: JSON.stringify({ email: email, password: password }),
            success: function(data) {
                if(data.success) {
                    window.location.href = '/'; 
                } else {
                    alert('Login failed!');
                }
            },
            error: function(xhr, status, error) {
                alert('Login failed. Please check your user credentials.');
             }
        });
    });
});