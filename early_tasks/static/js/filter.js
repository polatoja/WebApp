$(document).ready(function(){
    $(".ajaxLoader").hide(); // Hide loader initially

    // Task Filter Start
    $(".filter-checkbox").on('click', function(){
        var _filterObj = {};

        // Collect selected levels
        $(".filter-checkbox").each(function(index, ele){
            var _filterKey = $(this).data('filter'); 
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function(el){
                if (el.value === "None") {
                    return "null";
                }
                return el.value; // Get values of selected checkboxes
            });
        });
        var url = $(".filter-container").data('url');
        var renderFunctionName = $(".filter-container").data('render-function');
        var renderFunction = window[renderFunctionName];
        // Run Ajax to filter tasks
        $.ajax({
            url: url, // Django URL for view_tasks
            data: _filterObj, // Pass selected levels as data
            dataType: 'html', // Expect HTML response
            beforeSend: function(){
                $(".ajaxLoader").show(); // Show loader before request
            },
            success: function(res){                
                if (res) {
                    var tasks = JSON.parse(res);
                    if (typeof renderFunction === 'function') {
                        renderFunction(tasks);  // Call the dynamically passed render function
                    } else {
                        console.error('Render function not found: ' + renderFunctionName);
                    }  // Use the function to render tasks
                }
                // $("#tasksContainer").html(res); // Update task list
                $(".ajaxLoader").hide(); // Hide loader after response
            },
            error: function(xhr, status, error){
                console.error('AJAX Error:', status, error);
                $(".ajaxLoader").hide(); // Hide loader on error
            }
        });
        
    });
});