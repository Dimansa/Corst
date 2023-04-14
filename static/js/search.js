$(document).ready(function(){
    var selected_items = [];
    $(".chk").click(function(){
        var selected_item = $(this).val();
        var index = selected_items.indexOf(selected_item);
        if(index == -1)
        {
           selected_items.push(selected_item);
        }
        else{
           selected_items.splice(index, 1);
        }
    });
    $("#submit-button").click(function(){
        $.ajax({
            url: "search",
            data: {'checkboxes': selected_items.join(",")},
            dataType: 'json',
            type: 'get',
            success: function (data) {
                console.log(data)
            }
        });
    });
})