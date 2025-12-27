

document.addEventListener("DOMContentLoaded", () => {

    const user_id = localStorage.getItem('user_id');




    // UPDATE BUTTON
    const btn = document.getElementById("update");

    btn.addEventListener("click", () => {
        //const csrftoken = getCookie('csrftoken');
        const data = new FormData();
        data.append('username', document.getElementById('username').value);
        data.append('email', document.getElementById('email').value);
        data.append('first_name', document.getElementById('first_name').value);
        data.append('last_name', document.getElementById('last_name').value);
        data.append('password', document.getElementById('password').value);

        console.log("data", data);

    });
});



