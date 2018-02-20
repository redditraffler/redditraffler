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

function showSelectedSubmission($tr) {
    var title = $tr.children('td:first').text().trim();

    if ($("#selected-submission").length > 0) {
        $("#selected-submission").html("<p>Your selection: \"{0}\"</p>".format(title));
    } else {
        $("#submissions").before("<div id='selected-submission' class='content has-text-centered'><p>Your selection: \"{0}\"</p></div>".format(title));
    }
}

function initTableRows() {
    var $rows = $("#submissions > tbody > tr");
    $rows.click(function() {
        $rows.removeClass("is-selected");
        $(this).addClass("is-selected");
        $("#submission-id").val($(this).attr('id'));
        showSelectedSubmission($(this));
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
    var $container = $("#submission-url-container");
    var $inputField = $("#submission-url");

    $inputField.attr("class", "input"); // Remove all other styling classes
    $inputField.addClass("is-success");

    var submissionDetailsTemplate = "<p class='help'><a href='{0}'>'{1}'</a> in /r/{2} by {3} on {4}</p>";
    var authorHtml = submission.author ? "<a href='https://reddit.com/u/" + submission.author + "'>/u/" + submission.author + "</a>" : "an unknown user";
    $container.append(
        submissionDetailsTemplate.format(
            submission.url,
            submission.title,
            submission.subreddit,
            authorHtml,
            getDateFromUnixTime(submission.created_at_utc)
        )
    );
}

function showSubmissionError() {
    var $container = $("#submission-url-container");
    var $inputField = $("#submission-url");

    $inputField.attr("class", "input"); // Remove all other styling classes
    $inputField.addClass("is-danger");

    var errorMsgHtml = "<p class='help is-danger'>This is not a valid submission URL.</p>";
    $container.append(errorMsgHtml);
}

function validateUrl() {
    var URL_REGEX = /[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;
    if (!$(this).val() || !URL_REGEX.test($(this).val())) return;

    $("#submission-url-container").children(":not(#submission-url)").remove(); // Clear previous error messages if any

    var PROTOCOL_PATTERN = /^((http|https):\/\/)/;
    var url = $(this).val();
    if (!PROTOCOL_PATTERN.test(url)) url = 'https://' + url;
    $.ajax({
        dataType: "json",
        data: { url: url },
        url: $APP_ROOT + "api/submission",
        success: showSubmissionDetails,
        error: showSubmissionError
    });
}

function validateSubmissionSelection(event) {
    if (!$("#submission-id").val()) {
        $("#submissions").before("<div class='content has-text-centered'><p class='has-text-danger'>Please select a submission.</p></div>");
        $(document).scrollTop($("#submission-id").offset().top);
        event.preventDefault();
    }
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

    $("#raffle-form").submit(validateSubmissionSelection);
});
