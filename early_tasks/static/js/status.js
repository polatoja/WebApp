function openStatusModal(taskId, taskName) {
    $("#statusModal").show();  // Show the modal
    $('input[name="task_id"]').val(taskId);  // Set the task ID in the hidden field
}

function closeStatusModal() {
    $("#statusModal").hide();  // Hide the modal
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
            location.reload();  // Reload the page to see the updated status
        } else {
            console.error('Error:', data.error);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Update the task status in the table dynamically
function updateTaskStatusInTable(taskId, status) {
    const taskRow = document.querySelector(`tr[data-task-id="${taskId}"]`);
    if (taskRow) {
        // Update the row with the new status (assuming you want to show the status in a specific column)
        taskRow.querySelector('.task-status').textContent = status;
    }
}

// Call this function where you want to open the status modal
// Example usage: openStatusModal(taskId);
