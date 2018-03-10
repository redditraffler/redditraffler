$(function() {
    $(".raffle-box").click(function() {
        var raffle_id = $(this).attr('data-raffle-id');
        window.location.href = "/raffles/" + raffle_id;
    });
});
