String.prototype.format = function() {
    var s = this, i = arguments.length;
    while (i--) {
        s = s.replace(new RegExp('\\{' + i + '\\}', 'gm'), arguments[i]);
    }
    return s;
};

function getDateFromUnixTime(timestamp) {
    return new Date(timestamp * 1000).toDateString();
}

function initTableControl() {
    var INITIAL_ROW_COUNT = 10;
    var rowCount = $("#submissions > tbody > tr").length;
    var visibleRowCount = 10;
    if (rowCount > visibleRowCount) {
        $('#table-control').show();
        $('#showLess').hide();
    }

    $('#submissions > tbody > tr:lt(' + visibleRowCount + ')').show();

    $('#showMore').click(function () {
        visibleRowCount = (visibleRowCount + 10 <= rowCount) ? visibleRowCount + 10 : rowCount;
        $('#submissions > tbody > tr:lt(' + visibleRowCount + ')').show();
        $('#showLess').show();
        if (visibleRowCount == rowCount) {
            $('#showMore').hide();
        }
    });

    $('#showLess').click(function () {
        $('#submissions > tbody > tr').not(':lt(' + INITIAL_ROW_COUNT + ')').hide();
        $('#showMore').show();
        $('#showLess').hide();
    });
}

function buildSubmissionsTable(submissions) {
    $("#loading-container").hide();

    // Add headers
    var $table = $("#submissions");
    var tableHeaders = "<thead><th>Title</th><th>Subreddit</th><th>Created On</th></thead>";
    $table.append(tableHeaders);

    // Add row for each submission
    submissions.forEach(function(submission) {
        var $tableBody = $("#submissions > tbody");
        var rowTemplate = "<tr style='display:none'><td><a href='{0}'>{1}</a></td><td>{2}</td><td>{3}</td></tr>";
        $tableBody.append(
            rowTemplate.format(
                submission.link,
                submission.title,
                submission.subreddit,
                getDateFromUnixTime(submission.created_at_utc)
            )
        );
    });

    // Add collapse/expand control
    initTableControl();
}

$(function() {
    if ($("#submissions").length > 0) {
        $.ajax({
            dataType: "json",
            url: $APP_ROOT + "api/submissions",
            success: buildSubmissionsTable,
        });
    }
});