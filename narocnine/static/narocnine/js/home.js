document.addEventListener("DOMContentLoaded", () => {
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


    document.querySelector('#dropdownMenu a[href="/"]').addEventListener('click', (e)=>{
        e.preventDefault();
        localStorage.clear();
        window.location.href = "/";
    });

    const addbtn = document.getElementById('add');
    addbtn.addEventListener('click', ()=>{
       console.log("addbtn clicked");
       window.location.href = "/rezervisanje/"
    });
});
