# Qwiz

An open source quiz engine.

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

#### Database: PostgreSQL

TODO

#### Channels: Redis

TODO

#### Heroku CLI

TODO

### Installing

This section includes a step by step guide, with examples, that will explain how to get a development environment up and running for Qwiz.

#### Python Virtual Environment

A Python virtual environment is used to create an isolated Python environment for Python projects. Project dependencies (i.e. Python packages) are then installed within a virtual environment, as opposed to a sytem-wide isntallation.

The standard library distributed with Python 3 includes the `venv` module, for the creation of virtual environments.

It’s a good idea to keep all your virtual environments in one place, for example in `.virtualenvs/` in your home directory. Create one for this project:

```bash
python3 -m venv ~/.virtualenvs/qwiz
```

It can then be activated as follows:

```bash
source ~/.virtualenvs/qwiz/bin/activate
```

N.B. When you have finished with your virtual envornment it can be deactived as follows:

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

TODO

#### Channels: Redis

TODO

#### Heroku CLI

TODO

## Running the tests

Explanation of how manual and automated tests are conducted.

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

Components, OpenSource or otherwise, than gave this project life.

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## Versioning

[SemVer](http://semver.org/) is used for versioning. For the versions available, see the tags on this repository.

### Authors

A list of contributors who participated in this project.

### License

This project is licensed under the MIT License; see the LICENSE.md file for details

### Acknowledgments

Recognition of code and inspiratation received from others that helped shape this project.
