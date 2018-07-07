# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## Unreleased
### Changed
- Replaced the raffle list in the user page with DataTables (the same kind of table as in the raffle index page).
- Site usage information has been moved to a FAQ page.

## 2018.6 (2018-05-28)
### Security
- Submission titles are now sanitized before saving to the database instead of relying on the templating engine to escape the string.

## 2018.5 (2018-05-24)
### Added
- Added a confirmation popup for raffle parameters on form submit.
- Added a "show more" button on user profile pages to prevent showing too many raffles at once.
- Existing unverified raffles can now be overwritten by verified raffles. Logged-in users should be able to select their submission when creating a new raffle; unverified raffles will be removed automatically upon successful creation of the verified one.

### Changed
- Use simpler versioning scheme (increment with each release) instead of SemVer.

## 2018.4 (2018-04-06)
### Changed
- Revised phrasing for the unverified raffle warning message in raffle results page

## 2018.3 (2018-03-30)
### Added
- Redirect HTTP requests to HTTPS in production

## 2018.2 (2018-03-30)
### Changed
- Heroku Procfile now defines gunicorn and worker processes on a single dyno

## 2018.1 (2018-03-30)
- Initial release! :tada:
