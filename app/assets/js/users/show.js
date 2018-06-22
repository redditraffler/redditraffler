function buildRafflesTable(data) {
    var $table = $("#raffles");
    var $tbody = $table.find('tbody');

    var rowTemplate = "<tr data-raffle-id='{0}'><td>{1}</td><td>{2}</td><td data-sort='{3}'>{4}</td></tr>";
    data.forEach(function(raffle) {
        $tbody.append(rowTemplate.format(
            raffle.submission_id,
            raffle.submission_title,
            raffle.subreddit,
            raffle.created_at,
            raffle.created_at_readable
        ));
    });

    $tbody.children('tr').click(function() {
        var raffleId = $(this).attr('data-raffle-id');
        window.location.href = "/raffles/{0}".format(raffleId);
    });

    $("#raffles").DataTable({
        "pageLength": 5,
        "lengthChange": false,
        "order": [[2, "desc"]]
    });
}

function fetchUserRaffles() {
    var username = window.location.pathname.split('/').pop();
    $.ajax({
        dataType: "json",
        url: "/api/users/{0}/raffles".format(username),
        success: function(res) {
            if (res.length > 0) buildRafflesTable(res);
        }
    });
}

$(function() {
    fetchUserRaffles();
});
