function updateStatus(data) {
    var REFRESH_RATE_MS = 500;
    var status = data.status;
    var error = data.error;

    if (error == true) {
        $("#loader").hide();
        $("#status-container").html(
            "<p><i class='fas fa-times fa-6x has-text-reddit'></i><p>" +
            "<p class='title'>Something went wrong :(</p>" +
            "<p>This most likely happened because your raffle parameters were too strict (i.e. we couldn't find enough winners to match your parameters).</p>" +
            "<p>Please see <a href='/faq'>the FAQ</a> for more information.</p>" +
            "<p>If you think this is unrelated to your raffle parameters, please <a href='/about#contact'>contact us</a> with the code '" + jobId + "' and we'll look into it ASAP.</p>"
        );
    } else if (status == "Done!") {
        $("#loader").hide();
        $("#status-container").html(
            "<p><i class='fas fa-check fa-6x has-text-reddit'></i></p>" +
            "<p class='title'>Done!</p>" +
            "<p>Redirecting you to the results page...</p>"
        );
        setTimeout(function() {
            window.location.href = "/raffles/" + jobId;
        }, 1500);
    } else {
        $("#job-status").text(status);
        setTimeout(pollJobStatus, REFRESH_RATE_MS);
    }
}

function pollJobStatus() {
    $.ajax({
        dataType: "json",
        data: { job_id: jobId },
        url: "/api/job_status",
        success: updateStatus
    });
}

$(function() {
    pollJobStatus();
});
