let taskIdToDelete = null;

// Fetch tasks from the server and render them in the table
function fetchManageTasks() {
    if (window.location.pathname.includes('/manage_tasks/'))
    {
        fetch('/manage_tasks/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // Mark this as an AJAX request
            }
        })
        .then(response => response.json())
        .then(tasks => {
            renderManageTasks(tasks);  // Render the tasks in the table
        })
        .catch(error => console.error('Error fetching tasks:', error));
    }
}

// Handle form submission for adding a new task
document.getElementById('addTaskForm')?.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    const taskData = {
        name: document.getElementById('add_task_name').value,
        description: document.getElementById('add_task_description').value,
        status: document.getElementById('add_task_status').value,
        level: document.getElementById('add_task_level').value,
        due_date: document.getElementById('add_task_due_date').value,
        assigned_user: document.getElementById('add_task_assigned_user').value
    };

    // Send the task data via AJAX
    fetch('/manage_tasks/0/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),  // Include the CSRF token for Django
            'X-Requested-With': 'XMLHttpRequest'  // Mark as an AJAX request
        },
        body: new URLSearchParams(taskData)  // Format the data as URL-encoded
    })
    .then(response => response.json())
    .then(data => {
        if (data.task) {
            console.log('Task added:', data.task);
            addTaskToTable(data.task);  // Add the task to the table dynamically
            closeAddModal();  // Close the modal after successful submission
        } else if (data.errors) {
            console.error('Form validation errors:', data.errors);
            // Handle form validation errors (e.g., display errors in the modal)
        }
    })
    .catch(error => console.error('Error adding task:', error));
});

// Render the fetched tasks in the table
function renderManageTasks(tasks) {
    const tableBody = document.getElementById('tasks-table-body');
    tableBody.innerHTML = '';  // Clear existing rows

    tasks.forEach(task => {
        const row = createManageTaskRow(task);  // Create each row
        tableBody.appendChild(row);  // Append the row to the table body
    });
}

// Add a new task to the table
function addTaskToTable(task) {
    const tableBody = document.getElementById('tasks-table-body');
    const row = createManageTaskRow(task);  // Create the row
    tableBody.appendChild(row);  // Append the new row to the table
}

// Helper function to get CSRF token
function getCsrfToken() {
    return document.querySelector('input[name="csrfmiddlewaretoken"]').value;
}

// Call the fetchTasks function when the page loads
document.addEventListener('DOMContentLoaded', fetchManageTasks);

// Functions to open and close modals
function openAddModal(taskId, taskName) {

    var nameField = document.getElementById('add_task_name');
    if (nameField) nameField.value = "";

    var descriptionField = document.getElementById('add_task_description');
    if (descriptionField) descriptionField.value = "";

    var statusField = document.getElementById('add_task_status');
    if (statusField) statusField.value = 'pending';

    var levelField = document.getElementById('add_task_level');
    if (levelField) levelField.value = 'easy';

    var dueDateField = document.getElementById('add_task_due_date');
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    dueDateField.value = tomorrow.toISOString().split('T')[0];

    var assignedUserField = document.getElementById('add_task_assigned_user');
    assignedUserField.options[0].selected = true;

    $("#addModal").show(); // Show the modal with jQuery
}

function closeAddModal() {
    $("#addModal").hide(); // Hide the modal with jQuery
}

function updateTaskInTable(updatedTask) {
    const taskRow = document.querySelector(`tr[data-task-id="${updatedTask.id}"]`);
    if (!taskRow) {
        console.error(`Task row with ID ${updatedTask.id} not found!`);
        return;
    }

    // Log task row for debugging
    console.log("Updating task:", updatedTask);
    
    taskRow.querySelector('.task-name').textContent = updatedTask.name;
    taskRow.querySelector('.task-description').textContent = updatedTask.description;

    // Update task level, handle missing element
    const levelElement = taskRow.querySelector('.task-level');
    if (levelElement) {
        levelElement.textContent = updatedTask.level;
    } else {
        console.warn(`Task level element not found for task ID ${updatedTask.id}`);
    }

    taskRow.querySelector('.task-assigned-user').textContent = updatedTask.assigned_user;
    taskRow.querySelector('.task-created-by').textContent = updatedTask.created_by || 'Unknown';
    taskRow.querySelector('.task-status').textContent = updatedTask.status;

    // Optionally, update the due date if it exists
    const dueDateElement = taskRow.querySelector('.task-due-date');
    if (dueDateElement) {
        dueDateElement.textContent = updatedTask.due_date ? updatedTask.due_date : 'N/A';
    }
    const editButton = taskRow.querySelector('.edit-button');
    editButton.setAttribute('onclick', `openEditModal('${updatedTask.id}', '${updatedTask.name}', '${updatedTask.description}', '${updatedTask.status}', '${updatedTask.level}', '${updatedTask.due_date}', '${updatedTask.assigned_user}',)`);
    const deleteButton = taskRow.querySelector(`.delete-button`);
    deleteButton.setAttribute('onclick', `openDeleteModal('${updatedTask.id}', '${updatedTask.name}')`);
    // Highlight the updated row
    taskRow.classList.add('task-updated');  // Add a class to indicate that the row was updated
    setTimeout(() => taskRow.classList.remove('task-updated'), 3000);  // Remove the class after 3 seconds
    
}


function openEditModal(taskId, taskName, taskDescription, taskStatus, taskLevel, taskDueDate, taskAssignedUser) {
    var editModal = document.getElementById('editModal');
    if (!editModal) return;

    // Open the modal
    editModal.style.display = 'block';

    // Populate the form fields with the task data
    var nameField = document.getElementById('id_name');
    if (nameField) nameField.value = taskName;

    var descriptionField = document.getElementById('id_description');
    if (descriptionField) descriptionField.value = taskDescription;

    var statusField = document.getElementById('id_status');
    if (statusField) statusField.value = taskStatus;

    var levelField = document.getElementById('id_level');
    if (levelField) levelField.value = taskLevel;

    var dueDateField = document.getElementById('id_due_date');
    var dateParts = taskDueDate.split('.');
    var formattedDate = `${dateParts[2]}-${dateParts[1]}-${dateParts[0]}`;
    var dateToAssign = new Date(formattedDate).toISOString().split('T')[0];
    if (dueDateField) dueDateField.value = dateToAssign;

    var assignedUserField = document.getElementById('id_assigned_user');
    if (assignedUserField) {
        for (let i = 0; i < assignedUserField.options.length; i++) {
            if (assignedUserField.options[i].text == taskAssignedUser) {
                assignedUserField.options[i].selected = true;
                break;
            }
        }
    }

    // Set a hidden input to pass the taskId
    let taskIdInput = document.querySelector('input[name="task_id"]');
    if (!taskIdInput) {
        taskIdInput = document.createElement('input');
        taskIdInput.type = 'hidden';
        taskIdInput.name = 'task_id';
        document.getElementById('editForm').appendChild(taskIdInput);
    }
    taskIdInput.value = taskId;
}


document.getElementById('editForm')?.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent traditional form submission

    const taskId = document.querySelector('input[name="task_id"]').value;  // Get task ID
    // Collect updated task data
    const taskData = {
        name: document.getElementById('id_name').value,
        description: document.getElementById('id_description').value,
        status: document.getElementById('id_status').value,
        level: document.getElementById('id_level').value,
        due_date: document.getElementById('id_due_date').value,
        assigned_user: document.getElementById('id_assigned_user').value
    };

    // Send the data via AJAX to the backend
    fetch(`/manage_tasks/${taskId}/edit/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCsrfToken(),  // Include the CSRF token
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: new URLSearchParams(taskData)  // Convert taskData to URL-encoded format
    })
    .then(response => response.json())
    .then(data => {
        if (data.task) {
            console.log('Task updated:', data.task);
            updateTaskInTable(data.task);  // Update the task row in the table
            closeEditModal();  // Close the modal after successful update
        } else if (data.errors) {
            console.error('Form validation errors:', data.errors);
            // Handle validation errors (e.g., display them in the modal)
        }
    })
    .catch(error => console.error('Error editing task:', error));
});


function closeEditModal() {
    $("#editModal").hide(); // Hide the modal with jQuery
}

// Create a table row for a task
function createManageTaskRow(task) {
    const row = document.createElement('tr');
    row.setAttribute('data-task-id', task.id);
    
    row.innerHTML = `
        <td class="task-name">${task.name}</td>
        <td class="task-description">${task.description}</td>
        <td class="task-level">${task.level}</td>
        <td class="task-assigned-user">${task.assigned_user || 'None'}</td>
        <td class="task-created-by">${task.created_by || 'Unknown'}</td>
        <td class="task-status">${task.status}</td>
        <td class="task-due-date">${task.due_date}</td>
        <td>
            <button class="edit-button" onclick="openEditModal(
                '${task.id}', 
                '${task.name}', 
                '${task.description}', 
                '${task.status}', 
                '${task.level}', 
                '${task.due_date}', 
                '${task.assigned_user || 'None'}'
            )">
            <i class="fa-solid fa-pen-to-square"></i>
            </button>
            <button class="delete-button" onclick="openDeleteModal('${task.id}', '${task.name}')">
            <i class="fa-solid fa-trash"></i>
            </button>
        </td>
    `;
    return row;
}