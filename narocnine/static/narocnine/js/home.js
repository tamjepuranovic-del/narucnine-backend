document.addEventListener("DOMContentLoaded", () => {

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let cookie of cookies) {
                cookie = cookie.trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    const button = document.getElementById('user_interface');
    const menu = document.getElementById('dropdownMenu');

    // Toggle dropdown on button click
    button.addEventListener('click', () => {
        if (menu.style.display === 'block') {
            menu.style.display = 'none';
        } else {
            menu.style.display = 'block';
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener('click', (event) => {
        if (!button.contains(event.target) && !menu.contains(event.target)) {
            menu.style.display = 'none';
        }
    });


    document.querySelector('#dropdownMenu a[href="/logout/"]').addEventListener('click', async (e) => {
        e.preventDefault();
        // Call backend logout endpoint
        await fetch('/logout/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken') // required if CSRF is enabled
            }
        });
        localStorage.clear();
        window.location.href = "/";
    });

    const addbtn = document.getElementById('add');
    addbtn.addEventListener('click', ()=>{
       console.log("addbtn clicked");
       window.location.href = "/rezervisanje/"
    });
});
