# Hubstaff Bot

This is a bot which fetches user activities across projects for given day. By default, it displays yesterday's data. You can download data as json or csv and also can send the data as email.

# Setup and Run

Follow the following steps to run the program

## Setting up virtualenv

Create a virtualenv using python3

```virtualenv venv -p python3```

Activate the venv

```source venv/bin/activate```

Install the requirements

```pip3 install -r requirements.txt```

## Run test cases

To run pytest test cases with code coverage execute

```pytest ./tests/ --cov=./ --cov-report term-missing```

## Run flask app

To run the flask app execute either

```gunicorn --worker-class=gevent --workers=$((2)) -b 0.0.0.0:5000 --access-logfile - --error-logfile - "main:create_app('config.DevelopmentConfig')"```

Or

```python3 main.py```

## View Dashboard

Please view the dashboard at <http://localhost:5000> after running the app
