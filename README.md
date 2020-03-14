# Outreach-Backend

This repo contains the API for the Outreach django application (2020 capstone project).

## Setup
+ Install Windows Subsystem For Linux (if needed).
https://docs.microsoft.com/en-us/windows/wsl/install-win10

+ Install Python 3.5 (`apt-get install python3.5` in the bash shell).

+ Install Pip (to check, do `pip3 --version`). If you don't have it, `sudo apt-get install python3-pip`

+ Install `virtualenv` by running `pip3 install virtualenv`

+ Clone the repo, and `cd` into the outer directory (with `requirements.txt`)

+ Run `python3 -m virtualenv ./env` to create the virtual environment

+ Run `source env/bin/activate` to start the virtual environment

+ Run `pip3 install -r requirements.txt` to install Django and all other dependencies

+ `cd` into the `outreach` directory, and run `python3 manage.py runserver` to run the backend server locally

+ If you stop work on the project, run `deactivate` to stop the virtual environment

## Running
+ Run `source env/bin/activate` to start the virtual environment

+ Run `pip3 install -r requirements.txt` to install Django and all other dependencies

+ `cd` into the `outreach` directory and run `python3 manage.py makemigrations` and `python3 manage.py migrate` to update your database schema with any changes that were made

+ `python3 manage.py runserver <hostname>:<port>` to run server. Hostname and port optional.

+ If you stop work on the project, run `deactivate` to stop the virtual environment

## API Documentation

+ **Most** of the api is viewable from `/api/docs`.  This section simply highlights things that the swagger documentation doesn't show.
+ **Authentication**:
    + ``/api/login/`` : Takes in ``username`` (email of the user), and ``password``.  Returns the ``id`` of the person and ``token``.  The ``token`` needs to be sent in the authentication header of any request that requires authentication.
    + Example of Authentication header: 
    ```
    Authentication : Token 5fe98b5200ee113083e0242835b54a6d22a6a162 
    ```
+ Permissions have been set up to prevent misuse of the API.  Although swagger doesn't properly show the permission the API should let you know with a ``403`` status code.
+ **Candidate Registration**: ``POST /api/candidates`` is a valid way of putting a candidate into the system, however ``POST /api/registration`` should be used if you wish to put a candidate into the system and sign them up to an event.  Candidate username/email and password should match if the candidate already exists.  If the candidate already exists, and password is correct, any additional information, such a name and phone number, that is put in the candidate block of the request json will be used to update the candidate information.  If the candidate email doesn't exist, the candidate will be created.

## Additional Notes
+ Local Django uses SQLite as a database, but we will use Postgres on our actual hosted platform. I don't think we'll have to worry about the difference yet, there will just be a different set of data from your local to production (as there should be)

