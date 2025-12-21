console.log("login.js loaded");

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return response;
}

document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded");

    const loginBtn = document.getElementById('login-button');
    const registerBtn = document.getElementById('register-button');

    console.log("login button ", loginBtn);
    console.log("register button ", registerBtn);

    // LOGIN
    loginBtn.addEventListener('click', async () => {
        console.log("Login button clicked");

        const username = document.getElementById('login-username').value;
        const password = document.getElementById('password').value;

        const response = await postData('/login/', { username, password });
        console.log("Response status:", response.status);

        if(response.status === 200){
            const tokens = await response.json();
            console.log("Tokens:", tokens);

            localStorage.setItem('access', tokens.access);
            localStorage.setItem('refresh', tokens.refresh);
            localStorage.setItem('user_id', tokens.user_id);
            localStorage.setItem('username', tokens.username);

            document.getElementById('login-message').style.color = 'green';
            document.getElementById('login-message').innerText = 'Login successful!';

            window.location.href = '/homepage/';
        } else if (response.status === 401){
            document.getElementById('login-message').innerText = 'User does not exist or wrong password';
        } else {
            document.getElementById('login-message').innerText = 'Something went wrong';
        }
    });

    // REGISTER
    registerBtn.addEventListener('click', async () => {
        console.log("Register button clicked");

        const data = {
            firs_name: document.getElementById('firs_name').value,
            last_name: document.getElementById('last_name').value,
            username: document.getElementById('username').value,
            email: document.getElementById('email').value,
            password: document.getElementById('reg-password').value
        };
        console.log("data for registration", data);

        const response = await postData('/register/', data);
        if(response.status === 201){
            document.getElementById('register-message').style.color = 'green';
            document.getElementById('register-message').innerText = 'Registration successful!';
        } else {
            const err = await response.json();
            document.getElementById('register-message').innerText = err.detail || 'Registration failed!';
        }
    });
});
