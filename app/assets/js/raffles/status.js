function updateStatus(data) {
    var REFRESH_RATE_MS = 500;
    var status = data.status;

    if (status == "Done!") {
        $("#loader").hide();
        $("#status-container").html(
            "<p><i class='fas fa-check fa-6x'></i></p>" +
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
