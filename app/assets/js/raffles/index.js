$(function() {
    $("#raffles").DataTable({
        "lengthChange": false,
        "order": [[2, "desc"]]
    });

    $("#raffles tbody tr").click(function() {
        var raffle_id = $(this).attr('data-raffle-id');
        window.location.href = "raffles/" + raffle_id;
    });
});
