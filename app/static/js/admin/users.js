$(document).ready(function () {
    // console.log("skrf");
    $('.table_row .select-input.content input').on('click', function () {
        $(this).toggleClass('checked');
    });
    $('#delete_users').on('click', function () {
        let usersDelete = {'data': []};
        $('.table_row .select-input.content input.checked').each(function () {
            let userName = $(this).parents('.table_row').children('.user-name').text();
            if (userName != 'ucmc2020ssRoot')
                usersDelete.data.push(userName);
            // console.log($(this).parents('.table_row').children('.user-name').text());
        });
        console.log(JSON.stringify(usersDelete.data));
        $.getJSON($SCRIPT_ROOT + '/_add_numbers', {
            "data": "data"
        }, function (data) {
            $("#result").text(data.result);
        });
        // $.ajax({
        //     type: 'POST',
        //     // contentType: 'application/json',
        //     url: '/admin/users',
        //     dataType: 'json',
        //     data: JSON.stringify({"data": "data"}),
        //     success: (data) => {
        //         console.log('isChat response: ' + data)
        //     },
        //     error: (data) => {
        //         console.log(data)
        //     }
        // });
        // $.post('/admin/users', JSON.stringify(usersDelete))
        // console.log($('.table_row .select-input.content input.checked').pa);
    });
});