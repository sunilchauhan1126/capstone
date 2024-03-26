# Casting Agency

## Final Project

Getting Started

## Tools needed
    - VS Code
    - Postman

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


#### PIP Dependencies

Once you have your environment setup and running, install dependencies by naviging to the `casting` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

Overview of the Project:

The Application is for Casting agency to organise Actors and Movies.

## Models

Create 2 models
   - Actors model with name, age and gender attribute
   - Movies model with title and release_date attribute

This application uses below endpoints
----------------------------
- GET /movies
- GET /actors
- GET /movies/id
- GET /actors/id

- POST /movies
- POST /actors

- PATCH /movies/id
- PATCH /actors/id

- DELETE /movies/id
- DELETE /actors/id

----------------------------


### Setup Auth0

1. Create a new Auth0 Account

2. Select a unique tenant domain

3. Create a new, single page web application

4. Create a new API "casting"
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token

5. Create new API permissions
-----------------------------------------
   - `get:movies`
   - `post:movies`
   - `patch:movies`
   - `delete:movies`
----------------------------------------
   - `get:actors`
   - `post:actors`
   - `patch:actors`
   - `delete:actors`
----------------------------------------

6. Create new roles for:
   - Casting Assistant
        -  `get:movies`
        -  `get:actors`

   - Casting Director
        -  `get:movies`
        -  `get:actors`
        -  `post:actors`
        -  `patch:actors`
        -  `delete:movies`
        -  `patch:movies`

    - Executive Director
        -  `get:movies`
        -  `get:actors`
        -  `post:actors`
        -  `patch:movies`
        -  `patch:actors`
        -  `patch:movies`
        -  `delete:movies`
        -  `delete:actors`
        - can perform all actions

7. Test your endpoints with [Postman](https://getpostman.com).
   - Register 3 users
        - Assign Casting Assitant Role to one user
        - Assign Casting Director Role to Another User
        - Assign Executive Director Role to one more user
   - Sign into each account and make note of the JWT.

   - Import the postman collection `Casting.postman_collection.json`

   - Right-clicking the collection folder for casting assistant, casting director and executive producer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
   
   - Run the collection and correct any errors.
   
   - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## Application Login URL
    [casting agency login]
    https://kavyasrik.us.auth0.com/authorize?audience=casting&response_type=token&client_id=QwwLST9BrD7VoeyhM773l2sT7o1v4Ljg&redirect_uri=https://127.0.0.1:8080/Casting 

## Render Steps

    - Connect your repository with Render Dashboard
    - Create a Web service and deploy in in the repository connect by adding DATABASE_URL

## Deployment Link for the Application 

https://casting-2tvr.onrender.com

## TEST and PostMan Collection

Attach the casting api file 
- Update the Postman token and run the collections
