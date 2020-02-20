# outreach-backend

## Setup
+ Install Windows Subsystem For Linux 
https://docs.microsoft.com/en-us/windows/wsl/install-win10

+ Install Python 3.5 (should be installed already) but you might have to do `sudo apt-get install python3.5` in the bash shell for WSL

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

+ If you stop work on the project, run `deactivate` to stop the virtual environment


## Additional Notes
+ Local Django uses SQLite as a database, but we will use Postgres on our actual hosted platform. I don't think we'll have to worry about the difference yet, there will just be a different set of data from your local to production (as there should be)

