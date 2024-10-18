function openDeleteModal(taskId, taskName) {
    taskIdToDelete = taskId;  // remembering the task id for deletion
    document.getElementById('deleteTaskName').textContent = `Task: ${taskName}`;
    document.getElementById('deleteModal').style.display = 'block';
}

function closeDeleteModal() {
    document.getElementById('deleteModal').style.display = 'none';
    taskIdToDelete = null;  // reset
}

document.getElementById('confirmDeleteButton')?.addEventListener('click', function() {
    if (taskIdToDelete) {
        deleteTask(taskIdToDelete);  // calling function
        closeDeleteModal();
    }
});

function deleteTask(taskId) {
    const baseUrl = window.location.pathname;

    fetch(`${baseUrl}${taskId}/delete/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'  // making sure it's an ajax request
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'deleted') {
            console.log(`Task ${data.task_id} deleted.`);
            removeTaskFromTable(data.task_id);
        } else {
            console.error('Failed to delete task:', data);
        }
    })
    .catch(error => console.error('Error deleting task:', error));
}

function removeTaskFromTable(taskId) {
    const row = document.querySelector(`tr[data-task-id="${taskId}"]`);
    if (row) {
        row.remove();
    }
}