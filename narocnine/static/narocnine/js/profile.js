document.addEventListener("DOMContentLoaded", () => {
    fetch("/api/profile/", {
        method: "GET",
        credentials: "same-origin" // sends session cookie
    })
    .then(res => {
        if (!res.ok) throw new Error("Unauthorized or bad response: " + res.status);
        return res.json();
    })
    .then(data => {
        document.querySelector('input[name="email"]').value = data.email;
        document.querySelector('input[name="username"]').value = data.username;
        document.querySelector('input[name="firs_name"]').value = data.firs_name;
        document.querySelector('input[name="last_name"]').value = data.last_name;
        document.querySelector('input[name="password"]').value = "******";
    })
    .catch(err => console.error(err));

    const backbtn = document.getElementById("return");
    backbtn.addEventListener('click', async () =>{
        window.location.href = '/homepage/';
    })
});
