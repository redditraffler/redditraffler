function initListControl() {
    var INITIAL_ROW_COUNT = 10;
    var rowCount = $(".raffle-box").length;
    var visibleRowCount = 10;
    if (rowCount > visibleRowCount) {
        $("#table-control").show();
    }

    $(".raffle-box").hide();
    $(".raffle-box:lt(" + visibleRowCount + ")").show();

    $("#show-more").click(function() {
        visibleRowCount = (visibleRowCount + 10 <= rowCount) ? visibleRowCount + 10 : rowCount;
        $(".raffle-box:lt(" + visibleRowCount + ")").show();
        if (visibleRowCount == rowCount) {
            $("#show-more").hide();
        }
    });
}

$(function() {
    $(".raffle-box").click(function() {
        var raffle_id = $(this).attr('data-raffle-id');
        window.location.href = "/raffles/" + raffle_id;
    });

    initListControl();
});
