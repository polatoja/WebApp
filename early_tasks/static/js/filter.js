$(document).ready(function(){
    $(".ajaxLoader").hide();

    $(".filter-checkbox").on('click', function(){
        var _filterObj = {};

        // collect selected levels
        $(".filter-checkbox").each(function(index, ele){
            var _filterKey = $(this).data('filter'); 
            _filterObj[_filterKey] = Array.from(document.querySelectorAll('input[data-filter=' + _filterKey + ']:checked')).map(function(el){
                if (el.value === "None") {
                    return "null";
                }
                return el.value; // returning values of selected checkboxes
            });
        });
        var url = $(".filter-container").data('url');
        var renderFunctionName = $(".filter-container").data('render-function');
        var renderFunction = window[renderFunctionName];
        // Run ajax to filter tasks
        $.ajax({
            url: url, // django url for view_tasks
            data: _filterObj, // selected levels as data
            dataType: 'html',
            beforeSend: function(){
                $(".ajaxLoader").show();
            },
            success: function(res){                
                if (res) {
                    var tasks = JSON.parse(res);
                    if (typeof renderFunction === 'function') {
                        renderFunction(tasks);  // call the dynamically passed render function
                    } else {
                        console.error('Render function not found: ' + renderFunctionName);
                    }
                }
                $(".ajaxLoader").hide();
            },
            error: function(xhr, status, error){
                console.error('AJAX Error:', status, error);
                $(".ajaxLoader").hide();
            }
        });
        
    });
});