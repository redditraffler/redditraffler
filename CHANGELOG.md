# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## Unreleased

### Fixed

- Fixed an issue where some raffles in the Recent Raffles list did not have accompanying emojis.

## 2020.5 (2020-09-01)

### Added

- Added some vanity metrics to the home page.
- Added a list of recent raffles to the home page.

### Changed

- Removed the 'Raffles' page.
- The "Getting Started" and "How It Works" sections have been moved to the About page.

## 2020.4 (2020-08-15)

### Changed

- Refactored a bunch of internal code to set the project up for quicker iterations

### Security

- Added some HTTP security headers to improve overall security of the site.

## 2020.3 (2020-05-11)

### Fixed

- Fixed an issue where the selected winners would be mostly the same across multiple raffle runs.

## 2020.2 (2020-04-02)

### Fixed

- Fixed an issue where users could not create a raffle for a submission that has an existing unverified raffle

## 2020.1 (2020-03-10)

### Security

- Users' Reddit auth tokens are now stored in a more secure manner.

### Fixed

- Resolved an issue during raffle creation where combined karma checks would erroneously fail when the minimum combined karma is 0.
- Resolved an issue with raffle parameter displaying minimum combined karma incorrectly.

## 2019.3 (2019-05-15)

### Added

- Winners can now be selected by minimum combined karma (link karma + comment karma)

### Changed

- Specific error messages will now be shown to the user when a raffle fails to create.

## 2019.2 (2019-04-22)

### Changed

- Dropped legacy database table (ignored_users)
- Improved logging around Raffle creation to be able to resolve issues better

### Fixed

- Fixed an issue where threads with long titles would error out and fail to save

## 2019.1 (2019-04-10)

### Changed

- Updated Flask to v1.X
- Ignored users are now managed better on the database level

## 2018.7 (2018-10-21)

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
