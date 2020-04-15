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
+ Permissions have been setup to prevent misuse of the API (individually for each view).  Although swagger doesn't properly show the permissions, the API should let you know with a ``403`` status code.
+ **Candidate Registration**: ``POST /api/candidates`` is a valid way of putting a candidate into the system, however ``POST /api/registration`` should be used if you wish to put a candidate into the system and sign them up to an event.  Candidate username/email and password should match if the candidate already exists.  If the candidate already exists, and password is correct, any additional information, such a name and phone number, that is put in the candidate block of the request json will be used to update the candidate information.  If the candidate email doesn't exist, the candidate will be created.
+ **Surveys / Questionnaires**: *Note: surveys are for evaluators to comment on the performance of candidates.  Questionnaires are questions filled out by candidates when signing up.*  Each event is associated with a questionnaire and survey (initially, each event's questionnaire and survey is null.  Questionnaires and surveys must be manually created [look at second bullet below]).  Each questionnaire or survey has multiple questions.  Questions, and surveys / questionnaires are seperate entities.  Associations between surveys / questionnaires and questions are created seperately [look at fourth bullet below]. Note that all endpoints are CRUD, so you may edit / add / delete associations between events, surveys / questionnaires, and questions at any point.

    + Get survey or questionnaire id for an event by ```GET /api/event/``` or ```/api/event/[eventID]/```.
    + Create a new survey or questionnaire for an event by ```POST /api/questionnaire/``` or ```POST /api/survey/```.
    + Post a question (with  5 options) by ```POST /api/question/```.
    + Add questions to a survey / questionnaire by ```POST /api/question/[questionID]/``` 
    + Answer a question by ```POST /api/answer/```.  Evaluator ID should be filled out in ```evaluator``` field if you are answering a survey (conducted by evaluator).  Should be left out for candidate questionnaires.  Also answer is an integer value between 0 and 4 (cooresponding to the 5 MCs).  If a candidate has answered the question in the past POSTing another answer will update the previous answer.  Only one answer per candidate - question is saved.  So if the same questionnaire / survey is used in multiple events, the most recent answer is saved.
+ **Groups**:
    + Can define and list groups using ```/api/group```.
    + For this endpoint you may also GET ```/api/group/?event=<int:eventid>``` to list groups for a specific event.
    + **Do this whenever an evaluator checks into an event:** POST to the endpoint to define a new group for an event.  This is a way of checking into an event as an evaluator (that way you may be assigned a group of candidates as an evaluator).  Be sure to authenticate with token in header and specify the event ID [for which you wish to define the new group for / check into] in the body of the request. e.g.:
    ```
    {
        "event":2
    }
    ```
    + For now, HR will manually commence group division for an event.  This would be commenced after all evaluators have checked into an event. That way candidates could be split into groups evenly depending on the amount of evaluators.  This will arbitrarily assign each candidates a group / evaluator.  A candidate can later be added individually to a group using PATCH ```/api/registered``` if so desired.  In order to commence group division perform GET ```/api/divideGroups/<int:eventID>```.
+ **Text Notify**:
    + Notifies candidate about the interest of the company by sending a text.
    + ```GET /api/smsnotify/<int:candidate_ID>```
    + Add ```TWILIO_CREDS.py``` to ```api``` directory / module.
+ **Resume Ranking**:
    + Request a ranking of all candidates registered in a particular event by ```POST /api/ranking/```.  Specify the job ID and event ID in the request. 
+ **Resume Uploading**:
    + Can upload any kind of file currently
## Additional Notes
+ Local Django uses SQLite as a database, but we will use Postgres on our actual hosted platform. I don't think we'll have to worry about the difference yet, there will just be a different set of data from your local to production (as there should be)

