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
    }

    $('#submissions > tbody > tr:lt(' + visibleRowCount + ')').show();

    $('#show-more').click(function() {
        visibleRowCount = (visibleRowCount + 10 <= rowCount) ? visibleRowCount + 10 : rowCount;
        $('#submissions > tbody > tr:lt(' + visibleRowCount + ')').show();
        if (visibleRowCount == rowCount) {
            $('#show-more').hide();
        }
    });
}

function initTableRows() {
    var $rows = $("#submissions > tbody > tr");
    $rows.click(function() {
        $rows.removeClass("is-selected");
        $(this).addClass("is-selected");
        $("#submission-id").val($(this).attr('id'));
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
        var rowTemplate = "<tr id='{0}'><td>{1} <a href='{2}' target='_blank'><i class='fas fa-external-link-alt fa-fw fa-xs'></i></a></td><td>{3}</td><td>{4}</td></tr>";
        $tableBody.append(
            rowTemplate.format(
                submission.id,
                submission.title,
                submission.url,
                submission.subreddit,
                getDateFromUnixTime(submission.created_at_utc)
            )
        );
    });


    initTableControl(); // Add collapse/expand control
    initTableRows(); // Add row click handlers
}

function showSubmissionDetails(submission) {
    console.log(submission);
}

function validateUrl() {
    var URL_REGEX = /[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;
    if (!$(this).val() || !URL_REGEX.test($(this).val())) return;

    var PROTOCOL_PATTERN = /^((http|https):\/\/)/;
    var url = $(this).val();
    if (!PROTOCOL_PATTERN.test(url)) url = 'https://' + url;
    $.ajax({
        dataType: "json",
        data: { url: url },
        url: $APP_ROOT + "api/submission",
        success: showSubmissionDetails
    });
}

$(function() {
    if ($("#submissions").length > 0) {
        $.ajax({
            dataType: "json",
            url: $APP_ROOT + "api/submissions",
            success: buildSubmissionsTable,
        });
    }

    if($("#submission-url").length > 0) {
        $("#submission-url").focusout(validateUrl);
    }
});
