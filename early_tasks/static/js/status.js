function openStatusModal(taskId, taskName) {
    $("#statusModal").show();
    $('input[name="task_id"]').val(taskId);  // setting the task ID in the hidden field
}

function closeStatusModal() {
    $("#statusModal").hide();
}

document.getElementById('statusForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const taskId = document.querySelector('input[name="task_id"]').value;
    const status = document.getElementById('status').value;

    fetch(`/view_tasks/${taskId}/status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams({ 'status': status })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Status submitted successfully!');
            closeStatusModal();
            location.reload();
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

function updateTaskStatusInTable(taskId, status) {
    const taskRow = document.querySelector(`tr[data-task-id="${taskId}"]`);
    if (taskRow) {
        taskRow.querySelector('.task-status').textContent = status;
    }
}