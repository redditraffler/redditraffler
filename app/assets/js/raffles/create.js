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

function buildSubmissionsTable(submissions) {
    var $table = $("#submissions-list");
    var tableHeaders = "<thead><th>Title</th><th>Subreddit</th><th>Created On</th></thead>";
    $table.append(tableHeaders);

    submissions.forEach(function(submission) {
        var $tableBody = $("#submissions-list > tbody");

        var rowTemplate = "<tr><td><a href='{0}'>{1}</a></td><td>{2}</td><td>{3}</td></tr>";

        $tableBody.append(
            rowTemplate.format(
                submission.link,
                submission.title,
                submission.subreddit,
                getDateFromUnixTime(submission.created_at_utc)
            )
        );
    });
}

$(function() {
    if ($("#submissions-list").length > 0) {
        $.ajax({
            dataType: "json",
            url: $APP_ROOT + "api/submissions",
            success: buildSubmissionsTable,
        });
    }
});
