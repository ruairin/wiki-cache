
# Application Overview

The application allows the user to enter a search term and presents the text content of the articles matching the search term on www.wikipedia.com. The search results can be cached so that if the same search term is used again, the results can be quickly displayed by loading from the cache.

The main features of the application are as follows:
- The is implemented using the Flask Python framework
- The results cache is implemented using a PostgreSQL database
- The search operation is carried out using the python wikipedia module
- The Bootstrap framework is used for page styline

# Application Organisation

The source code structure is shown below

```
Application
│   app.py
│   db.py
│   README.md
│   requirements.txt
│   Dockerfile
│   wiki.py
│   .env.example
│
├───static
│       style.css
│       Wikipedia-logo.png
│
└───templates
        error.html
        index.html
        search_results.html
```
| File                | Description |
| ---                 | --- |
| app.py              | The main module for the Flask application |
| db.py               | Database queries and updates |
| requirements.txt    | Required packages for the application which can be installed using pip |
| Dockerfile(.dev)    | The Docker files for creating Docker images of the application |
| wiki.py             | Performs wikipedia searches and returns results |
| .env.example        | Sample environment file. This must be renamed to .env and configured before using the app. |
| README.md           | This readme file |
| /static/            | Static files for the web application |
| /templates/         | Jinja templates which are used to display the various pages (search, results etc.) |


# Setup and Configuration
<a id="Host"></a>

## Database Initialisation

The PostgreSQL database must be configured as follows before running the Flask app:
1. Log into the postgres interface: ``($ psql -h <POSTGRES HOST NAME> -U <POSTGRES USERNAME>)``
1. Create a database named wikicache ``(postgres=> CREATE DATABASE wikicache;)``
1. Switch to the wikicache database ``(postgres=> \c wikicache)``
1. Create a table named cache in the database with columns search_string and results ``(wikicache=> CREATE TABLE CACHE (search_string VARCHAR(255) PRIMARY KEY, results TEXT);)``
1. Exit the psql interface ``(wikicache=> exit)``

## Application Setup - Standalone Mode

Setup to run as a standalone application (i.e. not using a Docker container) is described in this section.

The following assumed that a postgres service is available for connection at the location (host, port etc) specified in the configuration file (see steps below)

1. Create a virtual environment (venv) from the source folder: 
``($ py -m venv env)``
1. This creates a env folder in the source folder. Activate the venv: 
``($ ./env/Scripts/activate)``
1. Install all python packages listed in requirements.txt: 
``($ python -m pip install -r .\requirements.txt)``
1. Copy the provided .env.example to .env and set the configuration options for the database connection

The application can be run as follows:
- On the host machine, run Flask application using 
``($ waitress-serve --listen=*:5000 app:app )``


## Application Setup - In a Docker Container

The Flask app can be run in a docker container in either development or production modes. In this section, basic usage of the application using Docker is described. It should be noted that Dockerfiles are not provided for the database but this could be configured if required.

1. Build the Docker image
  - Development Mode: 
  ``($ docker build -f .\Dockerfile.dev -t wikicache-dev .)``
  - Production Mode: 
  ``($ docker build -f .\Dockerfile -t wikicache .)``
1. Copy the provided .env.example to .env and set the configuration options for the database connection
1. Run the image  
``($ docker run -p 5000:5000 --env-file=./.env flask-test)``
Note: the .env is not copied to the docker image, therefore it is required to supply the .env file to the container using the --env-file as shown.


# Usage
- Once the application is running, open a web browser at the address given by Flask (e.g. http://127.0.0.1:5000). This displays the search page.
- Enter the search term and select options for cache and article output. Click search.
- The results of the search are displayed on the results page.

# Deploy to EC2 instance

The following is one possible approach for deploying the application to an EC2 instance

On the local/build machine
1. Build image 
``($ docker build -f .\Dockerfile -t wikicache .)``

1. Tag the image 
`($ docker tag <Image ID> <Docker Hub Username>/<Docker Hub Repository>:<Tag Name>)`

1. Push the image to docker hub 
`($ docker push <Docker Hub Username>/<Docker Hub Repository>)`

On EC2 instance:
1. If required (e.g. to use https or to route traffic to different servers based on domain name), configure an nginx proxy server. See example [here](https://pentacent.medium.com/nginx-and-lets-encrypt-with-docker-in-less-than-5-minutes-b4b8a60d3a71) and [here](https://mindsers.blog/post/https-using-nginx-certbot-docker/).

1. Pull the image 
`($ sudo docker pull <Docker Hub Username>/<Docker Hub Repository>:<Tag Name>)`

1. Create a .env file to configure the environment for the docker container (see sections above and .env.example in the source directory). This should include the host name and access credentials for the RDS instance as applicable.

1. Run the container. 

    `($sudo docker run -d --network nginx-net -h wikicache --name wikicache --env-file ./.env <image_name>)`

    In this command:
    - the container is connected to docker network nginx-net via the --network option. This assumes that an nginx server container is already running and is connected to this network. If nginx is not required, this option can be omitted.
    - the image reads the environment settings in the .env file via the --env-file option.