function openDeleteModal(taskId, taskName) {
    taskIdToDelete = taskId;  // Store the task ID for deletion
    document.getElementById('deleteTaskName').textContent = `Task: ${taskName}`;
    document.getElementById('deleteModal').style.display = 'block';
}

// Close the delete confirmation modal
function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
    taskIdToDelete = null;  // Reset the task ID
}

// Confirm deletion of the task
document.getElementById('confirmDeleteButton')?.addEventListener('click', function() {
    if (taskIdToDelete) {
        deleteTask(taskIdToDelete);  // Call the delete function
        closeDeleteModal();  // Close the modal after deletion
    }
});

function deleteTask(taskId) {
    const baseUrl = window.location.pathname;

    fetch(`${baseUrl}${taskId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),  // Include the CSRF token
            'X-Requested-With': 'XMLHttpRequest'  // Ensure it's an AJAX request
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'deleted') {
            console.log(`Task ${data.task_id} deleted.`);
            removeTaskFromTable(data.task_id);  // Remove the task from the table
        } else {
            console.error('Failed to delete task:', data);
        }
    })
    .catch(error => console.error('Error deleting task:', error));
}

// Remove a task row from the table
function removeTaskFromTable(taskId) {
    const row = document.querySelector(`tr[data-task-id="${taskId}"]`);
    if (row) {
        row.remove();  // Remove the row from the table
    }
}