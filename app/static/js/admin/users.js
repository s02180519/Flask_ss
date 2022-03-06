$(document).ready(function () {
    // console.log("skrf");
    $('.table_row .select-input.content input').on('click', function () {
        $(this).toggleClass('checked');
    });
    $('#delete_users').on('click', function () {
        let usersDelete = {'usersDelete': []};
        $('.table_row .select-input.content input.checked').each(function () {
            let userName = $(this).parents('.table_row').children('.user-name').text();
            if (userName != 'ucmc2020ssRoot')
                usersDelete.usersDelete.push(userName);
        });
        // console.log(JSON.stringify(usersDelete.data));
        $.ajax({
            method: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/admin/users",
            data: JSON.stringify(usersDelete),
            dataType: "json",
            success: (data) => {
                // console.log('isChat response: ' + data)
                window.location.replace(window.location.pathname);
            },
            error: (data) => {
                console.log('request error')
            }
        });
    });
});