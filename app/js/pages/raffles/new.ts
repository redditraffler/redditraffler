import "@assets/css/raffles/new.scss";

import $ from "jquery";
import swal from "sweetalert";
import ReactDOM from "react-dom";
import React from "react";

import { escapeHtml } from "@js/util";
import { Endpoint } from "@js/api";
import NewRaffle from "@js/components/NewRaffle";

let ignoredUsersList = [];

function getDateFromUnixTime(timestamp) {
  return new Date(timestamp * 1000).toDateString();
}

function initTableControl() {
  const rowCount = $("#submissions > tbody > tr").length;
  let visibleRowCount = 10;
  if (rowCount > visibleRowCount) {
    $("#table-control").show();
  }

  $(`#submissions > tbody > tr:lt(${visibleRowCount})`).show();

  $("#show-more").click(function () {
    visibleRowCount =
      visibleRowCount + 10 <= rowCount ? visibleRowCount + 10 : rowCount;
    $(`#submissions > tbody > tr:lt(${visibleRowCount})`).show();
    if (visibleRowCount === rowCount) {
      $("#show-more").hide();
    }
  });
}

function showSelectedSubmission($tr) {
  const title = escapeHtml($tr.children("td:first").text().trim());

  if ($("#submission-selection-error").length > 0) {
    $("#submission-selection-error").remove();
  }

  if ($("#selected-submission").length > 0) {
    $("#selected-submission").html(
      `<p>Your selection: &quot;${title}&quot;</p>`
    );
  } else {
    $("#submissions").before(
      `<div id='selected-submission' class='content has-text-centered'><p>Your selection: &quot;${title}&quot;</p></div>`
    );
  }
}

/**
 * Registers event handlers on the submission selection table
 */
function initTableRows() {
  const $rows = $("#submissions > tbody > tr");
  $rows.click(function () {
    const $clickedRow = $(this);

    // Highlights the selected row
    $rows.removeClass("is-selected");
    $clickedRow.addClass("is-selected");

    $("#submission-selection").val(`https://redd.it/${$clickedRow.attr("id")}`); // Set submissionUrl in the form
    showSelectedSubmission($clickedRow); // Display the selected submission to the user

    /* eslint-disable no-use-before-define */
    // Rebuild the ignored users list with the submission author
    removeAllIgnoredUsers();
    setDefaultIgnoredUsers();
    addIgnoredUser($clickedRow.attr("data-submission-author"));
    /* eslint-enable */
  });
}

function buildSubmissionsTable(submissions) {
  $("#loading-container").hide();

  const $table = $("#submissions");

  if (!submissions) {
    const noSubmissionsHtml =
      "<div id='no-submission-error' class='content has-text-centered has-text-danger'><p>Either you don't have any submissions yet or all your eligible submissions are already existing raffles.</p></div>";
    $table.html(noSubmissionsHtml);
    return;
  }

  // Add headers
  const tableHeaders =
    "<thead><th>Title</th><th>Subreddit</th><th>Created On</th></thead>";
  $table.append(tableHeaders);

  // Add row for each submission
  submissions.forEach(function (submission) {
    const $tableBody = $("#submissions > tbody");
    $tableBody.append(`
      <tr id='${submission.id}' data-submission-author='${submission.author}'>
        <td>${escapeHtml(
          submission.title
        )} <a href='${submission.url}' target='_blank'><i class='fas fa-external-link-alt fa-fw fa-xs'></i></a></td>
        <td>${submission.subreddit}</td>
        <td>${getDateFromUnixTime(submission.created_at_utc)}</td>
      </tr>
    `);
  });

  initTableControl(); // Add collapse/expand control
  initTableRows(); // Add row click handlers
}

function showSubmissionDetails(submission) {
  const $inputField = $("#submission-url");
  const $msg = $("#submission-url-msg");

  // Clear any previous messages and styling
  $msg.empty().attr("class", "help");
  $inputField.attr("class", "input is-success");

  const authorHtml = submission.author
    ? `<a href='https://reddit.com/u/${submission.author}'>/u/${submission.author}</a>`
    : "an unknown user";

  $msg.html(`
    <a href='${submission.url}'>'${escapeHtml(submission.title)}'</a> in /r/${
    submission.subreddit
  } by ${authorHtml} on ${getDateFromUnixTime(submission.created_at_utc)}
  `);
}

function showSubmissionError(url?: string) {
  const $inputField = $("#submission-url");
  const $msg = $("#submission-url-msg");

  // Clear any previous messages and styling
  $msg.empty().attr("class", "help");
  $inputField.attr("class", "input is-danger");

  $msg.addClass("is-danger");
  if (url) {
    $msg.html(
      `There is already an <a href='${url}'>existing raffle</a> for this submission.`
    );
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
  const $msg = $("#submission-url-msg");
  let url = $(this).val() as string;

  const URL_REGEX = /[\w-]+(\.[\w-]+)+([\w.,@?^=%&amp;:/~+#-]*[\w@?^=%&amp;/~+#-])?/;
  if (!url || !URL_REGEX.test(url)) {
    // @ts-ignore
    window._prevUrl = url;
    showSubmissionError();
    return;
  }

  const PROTOCOL_REGEX = /^((http|https):\/\/)/;
  if (!PROTOCOL_REGEX.test(url)) {
    url = `https://${url}`; // Add https if protocol not present
  } else {
    url = url.replace(/^http:\/\//i, "https://"); // Replace http with https
  }

  // Skip validation if input value hasn't changed
  // @ts-ignore
  if (url !== window._prevUrl) {
    // @ts-ignore
    window._prevUrl = url;
    $msg.html(
      "<div class='la-ball-clip-rotate la-sm la-reddit'><div></div></div>"
    );
    $.ajax({
      dataType: "json",
      data: { url },
      url: Endpoint.getSubmission,
      complete: showValidationResults,
    });
  }
}

function getFormDataForSubmit() {
  const $form = $("#raffle-form");
  const useCombinedKarma = $("#combined-karma-checkbox").prop("checked");
  const data = $form.serializeArray();
  data.push({ name: "ignoredUsers", value: JSON.stringify(ignoredUsersList) });

  return data.filter(function (obj) {
    const { name } = obj;
    if (useCombinedKarma) {
      return !["minComment", "minLink"].includes(name);
    }
    return !["minCombined"].includes(name);
  });
}

function submitForm() {
  const $submitBtn = $("#submit-btn");
  const $submitBtnMsg = $("#submit-btn-msg");
  const formData = getFormDataForSubmit();

  $submitBtn.addClass("is-loading");
  $submitBtn.prop("disabled", true);

  $.ajax({
    dataType: "json",
    type: "POST",
    data: formData,
    url: Endpoint.postFormSubmit,
    complete: (jqXHR) => {
      switch (jqXHR.status) {
        case 202: // Redirect to status page
        case 303: // Redirect to existing raffle
          window.location.href = jqXHR.responseJSON.url;
          break;
        case 422: // Form validation failed
          $submitBtnMsg.text(jqXHR.responseJSON.message);
          $submitBtn.removeClass("is-loading");
          $submitBtn.prop("disabled", false);
          break;
        default:
          $submitBtnMsg.text("Something went wrong behind the scenes.");
          $submitBtn.removeClass("is-loading");
          $submitBtn.prop("disabled", false);
      }
    },
  });
}

function confirmForm() {
  swal({
    icon: "warning",
    buttons: {
      cancel: {
        text: "Go Back",
        value: false,
        visible: true,
      },
      confirm: {
        text: "Submit",
        value: true,
        visible: true,
      },
    },
    text:
      "You won't be able to edit or remove this raffle once it's created. Please make sure you've entered the options correctly!",
  }).then(function (confirmed) {
    if (confirmed) {
      submitForm();
    }
  });
}

function validateAndSubmitForm(event) {
  event.preventDefault();
  // Logged in user did not select a submission
  if (
    $("#submission-selection").length > 0 &&
    !$("#submission-selection").val()
  ) {
    if (
      $("#submission-selection-error").length === 0 &&
      $("#no-submission-error").length === 0
    ) {
      $("#submissions").before(
        "<div id='submission-selection-error' class='content has-text-centered'><p class='has-text-danger'>Please select a submission.</p></div>"
      );
    }
    $(document).scrollTop($("#submission-selection").offset().top);
    return;
  }
  // Guest user did not enter a valid submission URL
  if (
    $("#submission-url").length > 0 &&
    !$("#submission-url").hasClass("is-success")
  ) {
    $(document).scrollTop($("#submission-url").offset().top);
    return;
  }
  // Validation passed, show confirmation message for form submit
  confirmForm();
}

function addIgnoredUser(username) {
  // Add user to internal list and add tag
  ignoredUsersList.push(username);
  $("#ignored-users").append(`
    <span class='tag is-medium is-reddit is-rounded'><span name='username'>${username}</span><a class='delete is-small'></a></span>
  `);
}

function removeAllIgnoredUsers() {
  ignoredUsersList = [];
  const ignoredUsersContainer = document.getElementById("ignored-users");
  ignoredUsersContainer.innerHTML = null;
}

function removeIgnoredUser() {
  // Remove user from internal list and remove tag
  const $tag = $(this).parent("span");
  const $username = $(this).siblings("span[name='username']");
  ignoredUsersList = ignoredUsersList.filter(function (elem) {
    return elem.toLowerCase() !== $username.text().toLowerCase();
  });
  $tag.remove();
}

function setDefaultIgnoredUsers() {
  const DEFAULT_USERS = ["AutoModerator"];
  DEFAULT_USERS.forEach(function (user) {
    addIgnoredUser(user);
  });
}

function isValidUsername(username) {
  const USERNAME_REGEX = /^[\w-]+$/;
  return (
    username.length >= 3 &&
    username.length <= 20 &&
    USERNAME_REGEX.test(username) &&
    ignoredUsersList.toString().toLowerCase().indexOf(username.toLowerCase()) <
      0
  );
}

function validateAndAddIgnoredUser() {
  const MAX_IGNORED_USERS_COUNT = 100;
  const $input = $("#ignored-user-input");
  const $msg = $("#ignored-user-msg");
  const username = $input.val();

  // Clear any previous messages
  $msg.empty().attr("class", "help is-danger");
  $input.removeClass("is-danger");

  if (ignoredUsersList.length >= MAX_IGNORED_USERS_COUNT) {
    $input.addClass("is-danger");
    $msg.text(
      "Too many ignored usernames. Remove some of them before trying to add to the list again."
    );
    return;
  }

  if (isValidUsername(username)) {
    // Add to ignored users list and reset input
    addIgnoredUser(username);
    $input.val("");
  } else {
    // Add helper message if failed validation
    $input.addClass("is-danger");
    $msg.text(
      "This is not a valid Reddit username, or it is already in the list."
    );
  }
}

// Validate and add ignored user when enter is pressed
function validateOnEnter(event) {
  if (event.keyCode === 13) {
    event.preventDefault();
    validateAndAddIgnoredUser();
  }
}

function handleCombinedKarmaCheckEvent() {
  const $splitKarmaInputGroup = $("#split-karma-input");
  const $combinedKarmaInputGroup = $("#combined-karma-input");

  let groupToHide;
  let groupToShow;
  if (this.checked) {
    groupToHide = $splitKarmaInputGroup;
    groupToShow = $combinedKarmaInputGroup;
  } else {
    groupToHide = $combinedKarmaInputGroup;
    groupToShow = $splitKarmaInputGroup;
  }

  groupToHide.hide();
  groupToHide.find("input").each(function () {
    $(this).val(this.defaultValue);
  });
  groupToShow.show();
}

document.addEventListener("DOMContentLoaded", () => {
  if ($("#submissions").length > 0) {
    $.ajax({
      dataType: "json",
      url: Endpoint.getSubmissionsForCurrentUser,
      success: buildSubmissionsTable,
    });
  }

  if ($("#submission-url").length > 0) {
    $("#submission-url").focusout(validateUrl);
  }

  $("#combined-karma-checkbox").change(handleCombinedKarmaCheckEvent);
  $("#raffle-form").submit(validateAndSubmitForm);

  // Ignored User section
  setDefaultIgnoredUsers();
  $("#ignored-user-btn").click(validateAndAddIgnoredUser);
  $("#ignored-users").on("click", "a.delete", removeIgnoredUser);
  $("#ignored-user-input").keydown(validateOnEnter);

  ReactDOM.render(
    React.createElement(NewRaffle),
    document.getElementById("new-raffle-root")
  );
});
