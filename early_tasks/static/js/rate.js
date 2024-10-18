function rateTask(taskId, rating) {
    if (window.confirm(`Do you want to rate this task with ${rating}?`)) {
        fetch(`/completed_tasks/${taskId}/rate/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCsrfToken(),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({ 'rating': rating })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                console.error('Error:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
      }
}