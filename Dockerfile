# This version should match the Heroku app's runtime
FROM python:3.6.11

WORKDIR /rr

RUN pip install pipenv

COPY Pipfile Pipfile.lock ./

# --ignore-pipfile ignores the pipfile and only depends on Pipfile.lock
# --dev installs dev dependencies
# --system uses the system python to install the packages
RUN pipenv install  --ignore-pipfile --dev --system

COPY . .
