# redditraffler
redditraffler is a website that facilitates contests or giveaways using Reddit submissions as a platform.

Read more about it at https://redditraffler.com.

# Issues
The issue tracker for this project is on [GitHub](https://github.com/timorthi/redditraffler/issues).

Non-development related questions or issues can be forwarded to me on [Reddit](https://reddit.com/u/xozzo) or via [e-mail](mailto:admin@redditraffler.com).

# Development
## Requirements
* Python 3.6+
* pip
* Redis
* Reddit API keys (one web app, one script app)
* PostgreSQL is recommended but SQLite will work

## Installation
```
$ git clone git@github.com:timorthi/redditraffler.git
$ cd redditraffler
$ virtualenv -p python3 venv  # (optional)
$ source venv/bin/activate  # (optional)
$ pip install -r requirements.txt
```

## Configuration
For the app to run properly, you'll need to provide configuration values for your database, Redis, and your Reddit app+bot credentials. See [app/config.py](app/config.py) for the required environmental variables.

You can load these environmental variables in manually or you can create a `.env` file in the app root. See [python-dotenv](https://github.com/theskumar/python-dotenv) for more information.

## Database Setup
We use Postgres in production so it'd be a good idea to do the same for development.
Once you have your database and app configuration set up, you'll need to run the database migrations.
```
$ FLASK_APP=runserver.py flask db upgrade
```

## Starting The App
Set `FLASK_APP`:
```
$ export FLASK_APP=runserver.py
```
To start the Flask development server:
```
$ FLASK_DEBUG=1 flask run
```
To start a worker process:
```
$ flask rq worker
```

## Testing
Run the app's tests with
```
$ pytest
```
