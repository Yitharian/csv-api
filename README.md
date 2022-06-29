# Mitigapi 

## First, to the Mitiga team: 
To do this test one consideration was "it will be deployed on kubernetes" but I 
don't have the proper knowledge to write it, I can learn it and just use 
kubernetes instead docker but I can't do it inside the "estimated time"*. So I 
did it in docker just to show it as a "container-like-service" (As well, better 
approach for micro-services). 

But the idea is to use kubernetes.

*Actually I used more time than the estimated 2 hours. 
I spend more time "just for fun".

But, you don't need docker to run this test, you just can run it in "local".
For this way use the "1.2. Using venv" point. Note that in the docker 
example I use postgres as a database, it is just a "better approach" because I separated the 
database from the API in two different services.

## How to use it

### 1. Up the API service

To up the service you have two ways:

#### 1.1. Using docker

Steps:
1. cp available_settings/docker/settings.py mitigapi/mitigapi/settings.py
2. docker-compose up -d mitigapi 
3. docker-compose exec mitigapi python manage.py makemigrations 
4. docker-compose exec mitigapi python manage.py migrate

If you need to see the mitigapi logs then use "docker-compose logs -f mitigapi" too.

#### 1.2. Using venv

Here we will use the "venv" directory, in order to use a python environment.

Steps:
1. cp available_settings/venv/settings.py mitigapi/mitigapi/settings.py
2. python -m venv venv
3. source venv/bin/activate
4. pip install -r requirements.txt
5. cd mitigapi
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py runserver 0.0.0.0:8000

**Now, in both cases, you only need to do requests to the API (it is running in http://localhost:8000)**

### 2. Endpoints

Currently, it has 3 endpoints:
* /cvv/add/
* /cvv/list/
* /cvv/headers/

#### 2.1. /cvv/add/

This endpoint adds a new CVV file to the django database, you need to add
to the "post data" the URL from where the content will be downloaded and 
the associated topic.

If all goes good it responds with cvv file ID (It is IMAHASH).

**Example POST code:**
        
    import requests, json

    data = {
        'url': 'https://someurl/csv/airs.csv',
        'topic': 'test'
    }
    requests.post(
        'http://localhost:8000/csv/add/',
         data=json.dumps(data)
    )

**Example response:**

    {
        'added': 'IMAHASH'
    }

But these endpoint give error codes as well, for example if the topic is
not found on the post data (Actually all endpoints manage the errors):

    {
        'error': 'Parameter "topic" was not found.'
    }

#### 2.2. /cvv/list/

This endpoint lists the cvv files associated to the provided topic.

This is a GET method and the topic should be at the end of the path.

**Example GET code:**

    import requests

    requests.get(
        'http://localhost:8000/csv/list/sometopic/'
    )

**Example response:**

    [
        {"IMAHASH": "https://domaina.tld/cvv/airs.csv"},
        {"IMAHASHTOO": "https://domaina.tld/cvv/afirs.csv"},
        {"IMTHEHASH": "https://domainb.tld/cvv/sairs.csv"}
        . . .
    ]

#### 2.3. /cvv/headers/

This endpoint returns a cvv file with its headers, URL and ID (hashed URL).

Note that it doesn't return the cvv file **content**, just the headers, URL and ID.

**Example GET code:**

    import requests

    requests.get(
        'http://localhost:8000/csv/headers/IMAHASH/'
    )

**Example response:**

    {
        "IMAHASH": {
            "url": "https://domain.tld/csv/Affeurs.csv",
            "headers": ["header", "headertoo", "yepimheader"]
        }
    }

## Considerations

This code is just a "test" and need more changes to be in production.

For example:

 * The secrets are hardcoded here in plaintext, that a really "bad practice", this kind of stuff must be added on the production environment and not "hardcoded".
 * The server needs authentication and run it properly (using gunicorn, for example, and not with the "base" django command "runserver").
 * The server **SHOULD** have the proper loggers.
 * The server responses are just a "json.dumps(stuff)" but these responses must be common classes which give the proper format.
 * Another *VITAL IMPORTANCE* point are the tests. With more time I will code it with the "unittest" library.
 * We have more useful tools for a REST API like "django rest framework", I want to say that the code needs more work time.

As well, I do HTTP requests in some point inside the "add" endpoint, it is a bad practice, 
the server only must do the "server" tasks (take requests and respond responses). 
These work of "I do a request, download content and save it to the database" must
be encapsulated in another service. Here I comment it on the "CVVLoader" class:

    class CVVLoader:
        """
        Acts like the intermediary between the django data and the view doing
        the needed operations on the models.
        
        Actually it is not a good solution: we don't want to do HTTP requests on
        the server, CVVLoader maybe must be another service (just the "add_cvv"). 
        Also, maybe we only need to save in the django model the URI from another 
        database (like s3) as a "content" and do these requests in another service.
        """
        . . .

In this case the "add" endpoint must respond with a 202 HTTP code, the data will not
be added instantly so the server "ACCEPT" it. 
