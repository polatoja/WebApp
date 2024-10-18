// Fetch tasks from the server and render them in the table
function fetchViewTasks() {
    if (window.location.pathname.includes('/view_tasks/'))
    {
        fetch('/view_tasks/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(response => response.json())
        .then(tasks => {
            renderViewTasks(tasks);
        })
        .catch(error => console.error('Error fetching tasks:', error));
    }
}

// Render the fetched tasks in the table
function renderViewTasks(tasks) {
    const tableBody = document.getElementById('tasks-table-body');

    const userRole = document.getElementById('user-role').getAttribute('data-role');
    tableBody.innerHTML = '';  // Clear existing rows

    tasks.forEach(task => {
        const row = createViewTaskRow(task, userRole);
        tableBody.appendChild(row);
    });
}

// Create a table row for a task
function createViewTaskRow(task, userRole) {
    const row = document.createElement('tr');
    row.setAttribute('data-task-id', task.id);
    row.innerHTML = `
        <td class="task-name">${task.name}</td>
        <td class="task-description">${task.description}</td>
        <td>${task.level}</td>`;
    if(userRole != 'user')
    {
        row.innerHTML += `<td>${task.assigned_user || 'None'}</td>`;
    }
    if(userRole != 'manager')
    {
        row.innerHTML += `<td>${task.created_by || 'Unknown'}</td>`;
    }
    row.innerHTML += `     
        <td class="task-status">${task.status}</td>
        <td>
            <button class="edit-status" onclick="openStatusModal('${task.id}', '${task.status}')">
                Change Status
            </button>
        </td>
    `;
    return row;
}

// Open the status modal
function openStatusModal(taskId, currentStatus) {
    const modal = document.getElementById('statusModal');
    if (!modal) return;

    const statusSelect = document.getElementById('modal_status');
    if (statusSelect) statusSelect.value = currentStatus;

    const taskIdInput = document.getElementById('modal_task_id');
    if (taskIdInput) taskIdInput.value = taskId;

    modal.style.display = 'block';
}

// Close the status modal
function closeStatusModal() {
    const modal = document.getElementById('statusModal');
    if (modal) modal.style.display = 'none';
}

// Handle form submission for updating task status
// listener zanim strona si ewladowuje - stad wszedzie error a dziala
document.getElementById('statusForm')?.addEventListener('submit', function(event) {
    event.preventDefault();

    const taskId = document.getElementById('modal_task_id').value;
    const newStatus = document.getElementById('modal_status').value;

    const statusData = {
        status: newStatus
    };

    fetch(`/view_tasks/${taskId}/edit/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams(statusData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.task) {
            updateTaskStatusInTable(data.task);
            closeStatusModal();
        } else if (data.errors) {
            console.error('Form validation errors:', data.errors);
        }
    })
    .catch(error => console.error('Error updating task status:', error));
});

// Update the task row in the table after status change
function updateTaskStatusInTable(updatedTask) {
    const taskRow = document.querySelector(`tr[data-task-id="${updatedTask.id}"]`);
    if (taskRow) {
        taskRow.querySelector('.task-status').textContent = updatedTask.status;
    }
}

// Helper function to get CSRF token
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}

// Call fetchTasks when the page loads
document.addEventListener('DOMContentLoaded', fetchViewTasks);
