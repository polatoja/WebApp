let completedTaskIdToDelete = null;

// fetch completed tasks from the server and put them in the table
function fetchCompletedTasks() {
    if (window.location.pathname.includes('/completed_tasks/'))
    {
        fetch('/completed_tasks/', {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'  // an ajax request
            }
        })
        .then(response => response.json())
        .then(tasks => {
            renderCompletedTasks(tasks);
        })
        .catch(error => console.error('Error fetching completed tasks:', error));
    }
}

function renderCompletedTasks(tasks) {
    console.log('Rendering completed tasks:', tasks);
    const tableBody = document.getElementById('completed-tasks-table-body');

    const userRole = document.getElementById('user-role').getAttribute('data-role');
    tableBody.innerHTML = '';  // clear existing rows

    tasks.forEach(task => {
        const row = createCompletedTaskRow(task, userRole);
        tableBody.appendChild(row);  // adding the row to table
        if(task.rating)
            if(task.rating > 0) document.getElementById(`${task.id}-star-1`).style.color = "yellow";
            if(task.rating > 1) document.getElementById(`${task.id}-star-2`).style.color = "yellow";
            if(task.rating > 2) document.getElementById(`${task.id}-star-3`).style.color = "yellow";
            if(task.rating > 3) document.getElementById(`${task.id}-star-4`).style.color = "yellow";
            if(task.rating > 4) document.getElementById(`${task.id}-star-5`).style.color = "yellow";
    });
}

function removeCompletedTaskFromTable(taskId) {
    const row = document.querySelector(`tr[data-task-id="${taskId}"]`);
    if (row) {
        row.remove();
    }
}

function createCompletedTaskRow(task, userRole) {
    const row = document.createElement('tr');
    row.setAttribute('data-task-id', task.id);
    row.innerHTML = `
    <td class="task-name">${task.name}</td>
    <td class="task-description">${task.description}</td>
    <td>${task.level}</td>`
    
    if(userRole != 'user')
    {
        row.innerHTML += `<td>${task.assigned_user || 'None'}</td>`;
    }
    if(userRole != 'manager')
    {
        row.innerHTML += `<td>${task.created_by || 'Unknown'}</td>`;
    }
    if(task.rating)
        row.innerHTML += `<td><i class="fa-solid fa-star" id="${task.id}-star-1"></i>
                            <i class="fa-solid fa-star" id="${task.id}-star-2"></i>
                            <i class="fa-solid fa-star" id="${task.id}-star-3"></i>
                            <i class="fa-solid fa-star" id="${task.id}-star-4"></i>
                            <i class="fa-solid fa-star" id="${task.id}-star-5"></i>
                            </td>`;
    if (!task.rating)
    {
        if(userRole === 'user')
         {
            row.innerHTML += `<td>
                <i class="fa-solid fa-star rating-star" id="${task.id}-star-1" onclick="rateTask(${task.id}, 1)"></i>
                <i class="fa-solid fa-star rating-star" id="${task.id}-star-2" onclick="rateTask(${task.id}, 2)"></i>
                <i class="fa-solid fa-star rating-star" id="${task.id}-star-3" onclick="rateTask(${task.id}, 3)"></i>
                <i class="fa-solid fa-star rating-star" id="${task.id}-star-4" onclick="rateTask(${task.id}, 4)"></i>
                <i class="fa-solid fa-star rating-star" id="${task.id}-star-5" onclick="rateTask(${task.id}, 5)"></i>
                </td>`;
        }
        else
        {
            row.innerHTML += `<td>
                <i class="fa-solid fa-star non-rated-start" id="${task.id}-star-1"></i>
                <i class="fa-solid fa-star non-rated-start" id="${task.id}-star-2"></i>
                <i class="fa-solid fa-star non-rated-start" id="${task.id}-star-3"></i>
                <i class="fa-solid fa-star non-rated-start" id="${task.id}-star-4"></i>
                <i class="fa-solid fa-star non-rated-start" id="${task.id}-star-5"></i>
                </td>`;
        }
    }
    if (userRole != 'user')
        row.innerHTML +=`<td></button>
                    <button class="delete-completed" onclick="openDeleteModal('${task.id}', '${task.name}')">
                    <i class="fa-solid fa-trash"></i>
                    </button></td>`;
    return row;
}

$(document).ready(function() {
    // event delegation for dynamically added stars
    $(document).on('mouseenter', '.rating-star', function() {
        var taskId = $(this).attr('id').split('-')[0];
        var starNumber = $(this).attr('id').split('-')[2];  // getting star number from the star's id

        // highlight stars to go with rating
        for (var i = 1; i <= starNumber; i++) {
            console.log(`Lightning star with id ${"#" + taskId + "-star-" + i}`);
            $("#" + taskId + "-star-" + i).addClass('star-hovered');
        }
    });

    $(document).on('mouseleave', '.rating-star', function() {
        var taskId = $(this).attr('id').split('-')[0];

        // remove the hover effect from all stars for the same task
        for (var i = 1; i <= 5; i++) {
            $("#" + taskId + "-star-" + i).removeClass('star-hovered');
        }
    });
});

// fetch completed tasks when the page loads
document.addEventListener('DOMContentLoaded', fetchCompletedTasks);
