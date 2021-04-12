# Teacher Directory App

[![Python Version](https://img.shields.io/badge/Python-3.9.1-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/Django-3.2-brightgreen.svg)](https://djangoproject.com)

A teacher directory app containing all the Teachers in a given school.

Each teacher should have the following information

- First Name
- Last Name
- Profile picture
- Email Address
- Phone Number
- Room Number
- Subjects taught

## Implementation

The backend is implemented using [Django][django] in [Python][python].

### Built with

#### Backend:

- Python: 3.9.1
- Django: 3.2

### Frontend

- Bootstrap 4

## Development

### Requirements

- Python 3.9 (3.8 may also work)
- Virtualenv (or pipenv)
- python-venv

### Installing Requirements

- If Python 3.9 is the default Python for the system, then create and activate
  the virtual environment:

      $ virtualenv venv
      $ ./venv/bin/activate

  OR

  If Python 3.8 is not the default Python for the system, then specify it's
  path when creating the virtual environment. For example, if Python 3.9
  binary is located at `/usr/bin/python3.9`, then run following commands
  instead of above:

      $ virtualenv -p /usr/bin/python3.9 venv
      $ ./venv/bin/activate

  _If you prefer using pipenv instead of virtualenv, then replace respective
  commands with pipenv equevalents._

- Clone this repository and cd to it:

      (venv) $ git clone https://github.com/santoshpy/TeacherDirectoryApp.git
      (venv) $ cd TeacherDirectoryApp

- Install Python dependencies:

      (venv) $ pip install -r requirements.txt

- Configure environment variable:

NOTE: Rename .env.example to .env

      (venv) $ mv .env.example .env

- Create the database:

      (venv) $ python manage.py makemigrations
      (venv) $ python manage.py migrate

### Running Servers

- Start the Django development server:

      (venv) $ python manage.py runserver

- Create admin user:

      (venv) $ python manage.py createsuperuser

  Enter your desired username and password to create admin user.

Now you can visit 127.0.0.1:8000 in your browser

To import CSV file have to log in using username and password created above.

NOTE: Bulk Import Teacher:
This csv importer will import the following fields in given orders:

`first_name,last_name,profile_picture,email_address,phone_number,room_number,subjects`
