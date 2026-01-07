document.addEventListener("DOMContentLoaded", () => {

    fetch("/api/profile/", {
        method: "GET",
        credentials: "same-origin"
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
        document.querySelector('input[name="password_hash"]').value = "******";
    })
    .catch(err => console.error(err));

    // back button
    const backbtn = document.getElementById("return");
    backbtn.addEventListener('click', () => {
        window.location.href = '/homepage/';
    });

    // update button
    const updateBtn = document.getElementById("update");
    updateBtn.addEventListener("click", async () => {
        const email = document.querySelector('input[name="email"]').value;
        const username = document.querySelector('input[name="username"]').value;
        const firs_name = document.querySelector('input[name="firs_name"]').value;
        const last_name = document.querySelector('input[name="last_name"]').value;
        const password_hash = document.querySelector('input[name="password_hash"]').value;

        try {
            const res = await fetch("/api/profile/", {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ email, username, firs_name, last_name, password_hash })
            });

            if (!res.ok) throw new Error("Update failed: " + res.status);
            alert("Profile updated successfully!");
        } catch (err) {
            console.error(err);
            alert("Error updating profile.");
        }
    });

    // Delete button with confirmation
    const deleteBtn = document.getElementById("delete");
    deleteBtn.addEventListener("click", async () => {
        const confirmed = confirm("Are you sure you want to delete your account? This action cannot be undone.");
        if (!confirmed) return;

        try {
            const res = await fetch("/api/delete/", {
                method: "DELETE",
                credentials: "same-origin"
            });

            if (res.status === 204) {
                alert("Account deleted successfully.");
                window.location.href = "/";
            } else {
                const data = await res.json();
                throw new Error(data.detail || "Delete failed");
            }
        } catch (err) {
            console.error(err);
            alert("Error deleting account.");
        }
    });

    const profilePicInput = document.getElementById("profile-picture-input");
    const profilePicImg = document.getElementById("profile-pic");

    profilePicInput.addEventListener("change", async (event) => {
        const file = event.target.files[0];
        if (!file) return;

    // Preview immediately
        const reader = new FileReader();
        reader.onload = () => profilePicImg.src = reader.result;
        reader.readAsDataURL(file);

    // Upload to server
        const formData = new FormData();
        formData.append("profile_picture", file);

        const res = await fetch("/api/upload-profile-picture/", {
            method: "POST",
            body: formData,
            credentials: "same-origin"
        });
        const data = await res.json();
        if (!res.ok) alert("Failed to upload picture");
    });

});
