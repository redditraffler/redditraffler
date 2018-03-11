function updateClock() {
    $("#clock").html(moment().utc().format('MMMM Do YYYY, h:mm:ssa'));
}

function setCopyrightYear() {
    $("#year").html(moment().utc().format('YYYY'));
}

$(function() {
    setCopyrightYear();
    updateClock();
    setInterval(updateClock, 1000);
});
