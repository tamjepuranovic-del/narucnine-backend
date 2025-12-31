document.addEventListener("DOMContentLoaded", ()=>{
    console.log("rezervisanje.js loaded");

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    const backbtn = document.getElementById('back');
    const canclebtn = document.getElementById('cancel');

    canclebtn.addEventListener('click', ()=>{
        console.log("cancel button clicked");
        window.location.href = "/homepage/";
    });

    backbtn.addEventListener('click', ()=>{
        console.log("back button clicked");
        window.location.href = "/homepage/";
    });


    document.getElementById("rezervForm").addEventListener("submit", function(e){
        e.preventDefault();
        console.log("FORM SUBMITTED");

        let formData = new FormData(this);

        for (let pair of formData.entries()) {
            console.log(pair[0], pair[1]);
        }

        fetch("/api/rezervacija/", {
            method: "POST",
            body: formData,
            credentials: "same-origin",
            headers: {
                "X-CSRFToken": csrftoken
            }
        })
        .then(res => res.json())
        .then(res => {
            if(res.error){
                alert(res.error);
            } else {
                alert(res.message);
                // optionally reset form or redirect
            }
        })
        .catch(err => console.error(err));
    });


});