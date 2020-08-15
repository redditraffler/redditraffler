# redditraffler

[![Maintainability](https://api.codeclimate.com/v1/badges/2a36d1fc5ba2728cc9f9/maintainability)](https://codeclimate.com/github/timorthi/redditraffler/maintainability)

redditraffler is a website that facilitates contests or giveaways using Reddit submissions as a platform.

Read more about it at https://redditraffler.com.

## Issues

The issue tracker for this project is on [GitHub](https://github.com/timorthi/redditraffler/issues).

Non-development related questions or issues can be forwarded to me on [Reddit](https://reddit.com/u/xozzo) or via [e-mail](mailto:admin@redditraffler.com).

## Development Requirements

redditraffler is a [Flask](https://github.com/pallets/flask) app with jQuery for DOM manipulation, so you'll need to know Python and/or JavaScript for development. The required tools are:

- Python 3.6+
- pipenv
- Docker and Docker Compose (for Redis and PostgreSQL)
- 2 Reddit API keys (one web app, one script app)
- Yarn 1.x

## Installation

```sh
$ git clone git@github.com:timorthi/redditraffler.git
$ cd redditraffler
$ pipenv install --dev # install python dependencies
$ yarn install --dev # install node dependencies
```

## Configuration

For the app to run properly, you'll need to provide configuration values via a `.env` file at the app's root directory. Use [`.env.example`](./.env.example) as a template for your `.env` file.

For the full list of environment variables used by the app, see [`app/config.py`](app/config.py).

## Starting The App

Spin up the Docker containers for Postgres and Redis:

```sh
$ docker-compose up
```

To start up the development server:

```sh
$ bin/start
```

This will run migrations to keep the database schema up to date, then start up the Flask web server and a worker process.

## Testing

Run the app's tests with

```sh
$ pipenv run test
```
