function updateClock() {
    $("#clock").html(moment().utc().format('MMMM Do YYYY, h:mm:ssa'));
}

$(function() {
    updateClock();
    setInterval(updateClock, 1000);
});
