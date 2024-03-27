# Project Capstone FSND
Udacity Full-Stack Web Developer Nanodegree Program Capstone Project

## Project Motivation
The Capstone Employee Project models a company that is responsible for maintaining Employee and departments to those employees. You are an HR Admin within the company and are creating a employee management to simplify and streamline your process. 

This project is simply a workspace for practicing and showcasing different set of skills related with web development. These include data modelling, API design, authentication and authorization and cloud deployment.

## Getting Started

The project adheres to the PEP 8 style guide and follows common best practices, including:

* Variable and function names are clear.
* Endpoints are logically named.
* Code is commented appropriately.
* Secrets are stored as environment variables.

## Tools needed
    - VS Code
    - Postman

#### Python 3.11

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your environment setup and running, install dependencies by naviging to the `capstone` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Key Dependencies & Platforms

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

- [Auth0](https://auth0.com/docs/) is the authentication and authorization system we'll use to handle users with different roles with more secure and easy ways

- [PostgreSQL](https://www.postgresql.org/) this project is integrated with a popular relational database PostgreSQL, though other relational databases can be used with a little effort.

- [Heroku](https://www.heroku.com/what) is the cloud platform used for deployment

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Models

Create 3 models
   - Employee model with id, name and designation attribute
   - Department model with id and name attribute
   - Joining model with id, employee_id, department_id and joining_date attributes

There are three models:
* Employee
	* name
	* designstion
* department
	* name
* joining
	* employee_id
	* department_id
   * joining_date

This application uses below endpoints
----------------------------
- GET /employee
- GET /department
- GET /joining
- GET /employee/id
- GET /department/id

- POST /employee
- POST /department
- POST /joining

- PATCH /employee/id
- PATCH /department/id

- DELETE /employee/id
- DELETE /department/id

----------------------------

### Running Locally

#### Installing Dependencies

##### Python 3.11

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

#### Database Setup
With Postgres running, restore a database using the `setup.sql` file provided. In terminal run:

```bash
dropdb capstone
createdb capstone
psql capstone < employee_table.psql
psql capstone < department_table.psql
psql capstone < joining_table.psql
```

#### Running Tests
To run the tests, run
```bash
dropdb capstone_test
createdb capstone_test
psql capstone < employee_table.psql
psql capstone < department_table.psql
psql capstone < joining_table.psql
python test_capstone.py
```

#### Auth0 Setup

1. You need to setup an Auth0 account.

2. Select a unique tenant domain

3. Create a new, single page web application

4. Create a new API "capstone"
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token

5. Create new API permissions
-----------------------------------------
   - `get:employee`
   - `post:employee`
   - `patch:employee`
   - `delete:employee`
----------------------------------------
   - `get:department`
   - `post:department`
   - `patch:department`
   - `delete:department`
----------------------------------------
   - `get:joining`
   - `post:joining`
----------------------------------------

6. Create new roles for:
- Employee Users
   -  `get:employee`
   -  `get:department`
   -  `get:joining`

- Manager Leads
   -  `get:employee`
   -  `get:joining`
   -  `post:employee`
   -  `patch:employee`
   -  `delete:employee`

- HR Administrator
   -  `get:employee`
   -  `get:department`
   -  `get:joining`
   -  `post:employee`
   -  `post:department`
   -  `post:joining`
   -  `patch:employee`
   -  `patch:department`
   -  `patch:joining`
   -  `delete:employee`
   -  `delete:department`
   - can perform all actions

7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users
      - Assign User Role to one user
      - Assign Manager Leads Role to Another User
      - Assign HR Administrator Role to one more user
   - Sign into each account and make note of the JWT.

   - Import the postman collection `Capstone.postman_collection.json`

   - Right-clicking the collection folder for Employee User, Manager Leads, HR Administratorr, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   
   - Run the collection and correct any errors.
   
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

##### Set JWT Tokens in `setup.sh`

Use the following link to create users and sign them in. This way, you can generate 

```
https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
```
Environment variables needed: (setup.sh)

   ```bash
   export AUTH0_DOMAIN="xxxxxxxxxx.auth0.com" # Choose your tenant domain
   export ALGORITHMS="RS256"
   export API_AUDIENCE="capstone" # Create an API in Auth0

   ```

#### Launching The App

1. Initialize and activate a virtualenv:

   ```bash
   virtualenv --no-site-packages env_capstone
   source env_capstone/bin/activate
   ```

2. Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```
3. Configure database path to connect local postgres database in `models.py`

    ```python
    database_path = "postgres://{}/{}".format('localhost:5432', 'capstone')
    ```
**Note:** For default postgres installation, default user name is `postgres` with no password. Thus, no need to speficify them in database path. You can also omit host and post (localhost:5432). But if you need, you can use this template:

## Application Login URL
    [Employee Admin Login]
   https://dev-44rtmev4pptlyduw.us.auth0.com/authorize?audience=coffee&response_type=token&client_id=uRTeAazrQmdXUc78TJC3IPKC06wb3O0m&redirect_uri=https://127.0.0.1:8080/login-results

## Render Steps

    - Connect your repository with Render Dashboard
    - Create a Web service and deploy in in the repository connect by adding DATABASE_URL

## Deployment Link for the Application 

https://capstone-project-xpxs.onrender.com

## TEST and PostMan Collection

Attach the casting api file 
- Update the Postman token and run the collections

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Resource Not Found
- 422: Not Processable 
- 500: Internal Server Error
