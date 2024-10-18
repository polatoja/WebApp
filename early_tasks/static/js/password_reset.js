document.getElementById('reset-password-form')?.addEventListener('submit', function(event) {
    event.preventDefault();
    
    const email = {email: document.getElementById('email').value};
    console.log(email);

    fetch('/password_reset/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),  // Django-specific if CSRF is enabled
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: new URLSearchParams(email)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Reset link sent to console (for dev purposes).');
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});
