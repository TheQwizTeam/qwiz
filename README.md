# Qwiz

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/TheQwizTeam/qwiz/blob/master/LICENSE)
[![built with Python3](https://img.shields.io/badge/built%20with-Python3%20%7C%20Angular-red.svg)](https://www.python.org/)
[![Travis](https://img.shields.io/travis/rust-lang/rust.svg)](https://travis-ci.org/TheQwizTeam/qwiz/)

## Getting Started

Instructions to get a copy of Qwiz up and running locally for development and testing purposes.

### Prerequisites

#### Python

Qwiz had a backend powered by Python 3.6.2, the latest Python version. It can be found [here](https://www.python.org/).

This is one of two Python runtimes supported by Heroku. The other, Python 2.7, was released in 2010 and is no longer under active development.

#### Pip

Pip is package management system used to install and manage software packages written in Python.

Pip should be available on your system if you downloaded Python 3.6.2 from python.org.

If it is installed, make sure it is up to date.

##### On Linux or macOS:

```bash
pip install -U pip
```

##### On Windows:

```bash
python -m pip install -U pip
```

If it is not installed, follow [this link](https://pip.pypa.io/en/stable/installing/) to install pip via the `get-pip.py` script. It really does make installation a breeze.


#### Heroku

Heroku is our PaaS of choice for this project; providing the means to create a scalable cloud based application, coupled with continuous integration and delivery, and a suite of useful add-ons.

Heroku takes care of the nitty gritty infrastructure details, and allows the team to focus on the Qwiz application itself. 

The Heroku Command Line Interface (CLI) is a tool for creating and managing Heroku apps from the command line.

The download and installation instructions for the Heroku CLI can be found [here](https://devcenter.heroku.com/articles/heroku-cli).


#### Database: PostgreSQL

The Qwiz Django application utilizes a PostgreSQL object-relational database management system. This is used for persisting rooms, questions, etc.

PostgreSQL download and installation instructions can be found [here](https://www.postgresql.org/download/). Please note that Django does *not* support version 10, please use version 9.4 or 9.6.

##### On Linux
```
$ sudo apt-get install postgresql-9.6 postgresql-server-dev-9.6
$ sudo service postgresql start
```

##### On macOS
Follow [these steps](https://postgresapp.com/) to download, install, and configured the Postgres Mac app.


#### Channels: Redis

The Qwiz Django application requires the ability to handle WebSockets. Channels extends Django to provide this capability, among other benefits.

You can read about Channels in all its gory details [here](http://channels.readthedocs.io/en/stable/).

In a nutshell, Channels separates Django into two process types:

 - Producers: handles HTTP and WebSockets
 - Consumers: runs views, websocket handlers and background tasks

  These processes communicate via a protocol called ASGI, over Channels. The recommended Channels backend is Redis. Download and installation instruction for Redis can be found
  [here](https://redis.io/topics/quickstart).


### Installing

This section includes a step by step guide, with examples, that will explain how to get a development environment up and running for Qwiz.

#### Python Virtual Environment

A Python virtual environment is used to create an isolated Python environment for Python projects. Project dependencies (i.e. Python packages) are then installed within a virtual environment, as
opposed to a sytem-wide isntallation.

The standard library distributed with Python 3 includes the `venv` module, for the creation of virtual environments.

It’s a good idea to keep all your virtual environments in one place, for example in `.virtualenvs/` in your home directory. Create one for this project:

```bash
python3 -m venv ~/.virtualenvs/qwiz
```

It can then be activated as follows:

```bash
source ~/.virtualenvs/qwiz/bin/activate
```

N.B. For the remainder of this guide, and development, you should stay in your virtual environment. When you have finished with your virtual environment it can be deactived as follows:

```bash
deactivate
```

#### Python Dependencies

This repo includes a `requirement.txt` file that lists all the project's Python dependencies, in a format that pip understands.

Install the project's Python dependencies:

```bash
pip install -r requirements.txt
```

See which Python packages are now available in your virtual environment:

```bash
pip freeze
```

**N.B. `pip freeze` is used to generate the requirements file in the first place. Issue `pip freeze > requirements.txt` when the dependencies have changed to update this file.**

#### Database: PostgreSQL

The Django application determines the database URL from an environment variable: `DATABASE_URL`. If this environment variable is not available, Django will default to a locally hosted database called "qwiz".

This databse value is utilized in the Django application's settings module (`filesettings.py`).

Heroku provides an optional PostgreSQL server add-on per application. When this addon has been configured the corresponding `DATABASE_URL` environment variable will be automatically configured within the application's environment, overriding the default value. You can use this URL directly, if you know it, or create the default database on your local PostgreSQL server. The latter is recommended.

Create the database for Qwiz from the PostgreSQL interactive terminal, psql.

```
CREATE DATABASE "qwiz";.
```

Apply the databse migrations.

```
python manage.py migrate
```

Create a superuser account; a user (added to the user table within your new database) that will have all permissions within this Django project.

```bash
python manage.py createsuperuser
```

**N.B. You may wish to give your local database a different name, host it somewhere else, use a different port etc. If you wish to customize your databse in any way don't forget to update your environment variable appropriately. The connection URI is formatted as follows:**

```bash
DATABASE_URL=postgresql://[user[:password]@][netloc][:port][/dbname]
```

#### Channels

Similarly the Django application determines the Redis URL from an environment variable: `REDIS_URL`. If this environment variable is not available, Django will default to a locally hosted redis instance, on port 6379.

Heroku provides an optional Redis server add-on per application. When this addon has been configured the corresponding `REDIS_URL` environment variable will be automatically configured within the application's environment, overriding the default value.

However, for a truly local development environment it is recommended to start an local instance of the Redis server installed in the previous section.

```
redis-server
```

A Redis instance will be running on localhost, at port 6379, by default. You can verify this with some ping pong.

```
redis-cli ping
PONG
```

#### Heroku CLI

Finally, configure Heroku to connect this repository to the the Heroku application.

Simply add the Heroku git remote to unlock the power of the Heroku CLI.

```
git remote add heroku https://git.heroku.com/quiz-monster.git
````

## Local Deployment

Now that all pre-requisites have been acquired, the virtual environment has been activated, and all dependencies are installed and configured, it is time to run Qwiz locally.

```
heroku local
````

Hey presto!!

Navigate to http://localhost:5000/ see the fruits of your labour.

Also, try logging in to http://localhost:5000/admin/ with the superuser username and password you just created. Feel free to explore this automatically generated admin site; primarily used for content management.

## Running the Tests

Currently there is a small Server unittest pack which can be run using Django alone (Heroku and Redis are not required for the tests to run).

To run the test suite, issue the following command:

```
$ python manage.py test quiz
Creating test database for alias 'default'...
..........
----------------------------------------------------------------------
Ran 10 tests in 0.016s

OK
Destroying test database for alias 'default'...
```

Any failures will be listed with a backtrace.


## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available, see the tags on this repository.

### Authors
[Christopher Kane](https://github.com/christopherkane), [Michael Purdy](https://github.com/0mpurdy), 
[Paul Crooks](https://github.com/pgcrooks) and [Scott Hulme](https://github.com/zeroish)

### License

This project is licensed under the MIT License; see the LICENSE.md file for details
