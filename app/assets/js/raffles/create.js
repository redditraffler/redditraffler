$(function() {
    if ($("#submissions-list").length > 0) {
        $.ajax({
            dataType: "json",
            url: $APP_ROOT + "api/submissions",
            success: function (data) {
                console.log(data);
            },
            error: function (data) {
                console.log("error");
            }
        });
    }
});
