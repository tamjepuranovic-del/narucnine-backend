document.addEventListener("DOMContentLoaded", () => {
    const updateBtn = document.getElementById("update-status");
    const statusSelect = document.getElementById("status");
    const backbtn = document.getElementById("return");

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

    const csrftoken = getCookie('csrftoken');

    updateBtn.addEventListener("click", () => {
        const appointmentId = updateBtn.dataset.id;
        const status = statusSelect.value;

        fetch(`/api/update-status/${appointmentId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrftoken,
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `status=${status}`
        })
        .then(res => res.json())
        .then(res => {
            if(res.error){
                alert(res.error);
            } else {
                alert(res.message);
            }
        })
        .catch(err => console.error(err));
    });

    backbtn.addEventListener('click',()=>{
        window.location.href = "/homepage/";
    })

});
