document.getElementById('new-password-form')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const uid = document.getElementById('uid').value;
    const token = document.getElementById('token').value;
    const newPassword = {newPassword: document.getElementById('new_password').value};
    const confirmNewPassword = {confirmNewPassword: document.getElementById('confirm_new_password').value};


    fetch(`/password_reset_confirm/${uid}/${token}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(), 
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams(newPassword)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Password reset successful!');
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});