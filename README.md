# redditraffler

redditraffler is a website that facilitates contests or giveaways using Reddit submissions as a platform.

Read more about it at https://redditraffler.com.

## Issues

The issue tracker for this project is on [GitHub](https://github.com/timorthi/redditraffler/issues).

Non-development related questions or issues can be forwarded to me on [Reddit](https://reddit.com/u/xozzo) or via [e-mail](mailto:admin@redditraffler.com).

## Development Requirements

redditraffler is a [Flask](https://github.com/pallets/flask) app with jQuery for DOM manipulation, so you'll need to know Python and/or JavaScript for development. The required tools are:

- Python 3.6+
- pipenv
- Redis
- PostgreSQL 9.4+
- 2 Reddit API keys (one web app, one script app)

## Installation

```
$ git clone git@github.com:timorthi/redditraffler.git
$ cd redditraffler
$ pipenv install --dev
```

## Configuration

For the app to run properly, you'll need to provide configuration values for your database, Redis, and your Reddit app+bot credentials. See [app/config.py](app/config.py) for the required environmental variables.

You can load these environmental variables in manually or you can create a `.env` file in the app root. See [python-dotenv](https://github.com/theskumar/python-dotenv) for more information.

## Database Setup

We use Postgres in production so it'd be a good idea to do the same for development.
Once you have your database set up and app config pointing to it, you'll need to run the database migrations.

```
$ FLASK_APP=runserver.py flask db upgrade
```

## Starting The App

Set `$FLASK_APP`:

```
$ export FLASK_APP=runserver.py
```

To start up the development server:

```
$ pipenv run honcho start -f Procfile.dev
```

This will start up a web server and worker process.

## Testing

Run the app's tests with

```
$ pytest
```
