$(function() {
    const registerForm = document.getElementById('form-register');
    const loginForm = document.getElementById('form-login');

    if (registerForm !== null) {
        registerForm.addEventListener('submit', function(event) {
            event.preventDefault();
            onRegister();
        })
    } else if (loginForm !== null) {
        loginForm.addEventListener('submit', function(event) {
            event.preventDefault();
            onLogin();
        })
    }
})

function onRegister() {
    $('.auth-content').children().removeClass('input-error');

    const email = $('#register-email').val().trim();
    const username = $('#register-username').val().trim();
    const password = $('#register-password').val().trim();
    const confirmPass = $('#register-confirm').val().trim();

    if (validateRegistration(email, username, password, confirmPass)) {
        const registerData = {
            "username": username,
            "password": password,
            "email": email,
        }
        $.ajax({
            url: "/register",
            method: "POST",
            contentType: "application/json; charset=UTF-8",
            dataType: "json",
            data: JSON.stringify(registerData),
            success: function(response) {
                console.log(response);
                window.location.href="/auth";
            },
            error: function (err) {
                console.log(err);
            }
        });
    } else {
        console.log("invalid form!");
    }
}

function validateRegistration(email, username, password, confirmPass) {
    if (password !== confirmPass) {
        console.log("passwords do not match!");
        $('#register-confirm').addClass("input-error");
        return false;
    } else {
        return true;
    }
}

function onLogin() {
    const username = $('#login-user').val().trim();
    const password = $('#login-pass').val().trim();

    const loginData = {
        "username": username,
        "password": password
    };

    $.ajax({
        url: "/login",
        method: "POST",
        contentType: "application/json; charset=UTF-8",
        dataType: "json",
        data: JSON.stringify(loginData),
        success: function(response) {
            console.log(response);
        },
        error: function (err) {
            console.log(err);
        }
    });
}
