function getDateFromUnixTime(timestamp) {
    return new Date(timestamp * 1000).toDateString();
}

function initTableControl() {
    var INITIAL_ROW_COUNT = 10;
    var rowCount = $("#submissions > tbody > tr").length;
    var visibleRowCount = 10;
    if (rowCount > visibleRowCount) {
        $("#table-control").show();
    }

    $("#submissions > tbody > tr:lt(" + visibleRowCount + ")").show();

    $("#show-more").click(function() {
        visibleRowCount = (visibleRowCount + 10 <= rowCount) ? visibleRowCount + 10 : rowCount;
        $("#submissions > tbody > tr:lt(" + visibleRowCount + ")").show();
        if (visibleRowCount == rowCount) {
            $("#show-more").hide();
        }
    });
}

function showSelectedSubmission($tr) {
    var title = $tr.children("td:first").text().trim();

    if ($("#submission-selection-error").length > 0) {
        $("#submission-selection-error").remove();
    }

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
        $("#submission-selection").val("https://redd.it/" + $(this).attr("id"));
        showSelectedSubmission($(this));
    });
}

function buildSubmissionsTable(submissions) {
    $("#loading-container").hide();

    var $table = $("#submissions");

    if (!submissions) {
        var noSubmissionsHtml = "<div id='no-submission-error' class='content has-text-centered has-text-danger'><p>Either you don't have any submissions yet or all your eligible submissions are already existing raffles.</p></div>";
        $table.html(noSubmissionsHtml);
        return;
    }

    // Add headers
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
    var $msg = $("#submission-url-msg");

    // Clear any previous messages and styling
    $msg.empty().attr("class", "help");
    $inputField.attr("class", "input is-success");

    var submissionDetailsTemplate = "<a href='{0}'>'{1}'</a> in /r/{2} by {3} on {4}";
    var authorHtml = submission.author ? "<a href='https://reddit.com/u/{0}'>/u/{0}</a>".format(submission.author) : "an unknown user";
    $msg.html(
        submissionDetailsTemplate.format(
            submission.url,
            submission.title,
            submission.subreddit,
            authorHtml,
            getDateFromUnixTime(submission.created_at_utc)
        )
    );
}

function showSubmissionError(url) {
    var $container = $("#submission-url-container");
    var $inputField = $("#submission-url");
    var $msg = $("#submission-url-msg");

    // Clear any previous messages and styling
    $msg.empty().attr("class", "help");
    $inputField.attr("class", "input is-danger");

    $msg.addClass("is-danger");
    if (url) {
        $msg.html("There is already an <a href='" + url + "'>existing raffle</a> for this submission");
    } else {
        $msg.text("This is not a valid submission URL.");
    }
}

function showValidationResults(jqXHR) {
    switch (jqXHR.status) {
        case 200:
            showSubmissionDetails(jqXHR.responseJSON);
            break;
        case 303:
            showSubmissionError(jqXHR.responseJSON.url);
            break;
        default:
            showSubmissionError();
    }
}

function validateUrl() {
    var $msg = $("#submission-url-msg");
    var url = $(this).val();

    var URL_REGEX = /[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:\/~+#-]*[\w@?^=%&amp;\/~+#-])?/;
    if (!url || !URL_REGEX.test(url)) {
        window._prevUrl = url;
        showSubmissionError();
        return;
    }

    var PROTOCOL_REGEX = /^((http|https):\/\/)/;
    if (!PROTOCOL_REGEX.test(url)) {
        url = "https://" + url; // Add https if protocol not present
    } else {
        url = url.replace(/^http:\/\//i, 'https://'); // Replace http with https
    }

    // Skip validation if input value hasn't changed
    if (url != window._prevUrl) {
        window._prevUrl = url;
        $msg.html("<div class='la-ball-clip-rotate la-sm la-reddit'><div></div></div>");
        $.ajax({
            dataType: "json",
            data: { url: url },
            url: "/api/submission",
            complete: showValidationResults
        });
    }
}

function validateSubmissionSelection(event) {
    if ($("#submission-selection").length > 0 && !$("#submission-selection").val()) {
        if ($("#submission-selection-error").length == 0 && $("#no-submission-error").length == 0) {
            $("#submissions").before("<div id='submission-selection-error' class='content has-text-centered'><p class='has-text-danger'>Please select a submission.</p></div>");
        }
        $(document).scrollTop($("#submission-selection").offset().top);
        event.preventDefault();
    }

    if ($("#submission-url").length > 0 && !$("#submission-url").hasClass("is-success")) {
        $(document).scrollTop($("#submission-url").offset().top);
        event.preventDefault();
    }
}

function addIgnoredUser(username) {
    // Add user to internal list and add tag
    var $ignoredUserTemplate = "<span class='tag is-medium is-reddit is-rounded'><span name='username'>{0}</span><a class='delete is-small'></a></span>";
    ignoredUsersList.push(username.toLowerCase());
    $("#ignored-users").append($ignoredUserTemplate.format(username));
}

function removeIgnoredUser() {
    // Remove user from internal list and remove tag
    var $tag = $(this).parent("span");
    var $username = $(this).siblings("span[name='username']");
    ignoredUsersList = ignoredUsersList.filter(function (elem) { return elem != $username.text().toLowerCase(); });
    $tag.remove();
}

function setDefaultIgnoredUsers() {
    var DEFAULT_USERS = ["AutoModerator"];
    DEFAULT_USERS.forEach(function(user) {
        addIgnoredUser(user);
    });
}

function isValidUsername(username) {
    var USERNAME_REGEX = /^[\w-]+$/;
    return (username.length >= 3 && username.length <= 20 &&
            USERNAME_REGEX.test(username) &&
            ignoredUsersList.indexOf(username.toLowerCase()) < 0);
}

function validateAndAddIgnoredUser() {
    var MAX_IGNORED_USERS_COUNT = 25;
    var $input = $("input[name='ignoredUser']");
    var $msg = $("#ignored-user-msg");
    var username = $input.val();

    $msg.empty().attr('class', 'help is-danger');
    $input.removeClass('is-danger');


    if (ignoredUsersList.length >= MAX_IGNORED_USERS_COUNT) {
        $input.addClass('is-danger');
        $msg.text("Too many ignored usernames. Remove some of them before trying to add to the list again.");
        return;
    }

    if (isValidUsername(username)) {
        // Add to ignored users list and reset input
        addIgnoredUser(username);
        $input.val('');
    } else {
        // Add helper message if failed validation
        $input.addClass('is-danger');
        $msg.text("This is not a valid Reddit username.");
    }
}

// Validate and add ignored user when enter is pressed
function validateOnEnter(event) {
    if (event.keyCode == 13) {
        event.preventDefault();
        validateAndAddIgnoredUser();
    }
}

var ignoredUsersList = [];
$(function() {
    if ($("#submissions").length > 0) {
        $.ajax({
            dataType: "json",
            url: "/api/submissions",
            success: buildSubmissionsTable,
        });
    }

    if($("#submission-url").length > 0) {
        $("#submission-url").focusout(validateUrl);
    }

    $("#raffle-form").submit(validateSubmissionSelection);

    // Ignored User section
    setDefaultIgnoredUsers();
    $("#ignored-user-btn").click(validateAndAddIgnoredUser);
    $("#ignored-users").on("click", "a.delete", removeIgnoredUser);
    $("input[name='ignoredUser']").keydown(validateOnEnter);
});
