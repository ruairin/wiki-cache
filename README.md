
# Application Overview

The application allows the user to enter a search term and presents the text content of the articles matching the 
search term on www.wikipedia.com. The main features of the application are as follows:
- The application runs as a Flask application
- A results cache is implemented using a PostgreSQL database
- The search operation is carried out using the python wikipedia module

# Application Organisation

The source code structure is shown below

```
Application
│   config.py
│   config.yml
│   db.py
│   main.py
│   README.md
│   requirements.txt
│   wiki.py
│
├───static
│       style.css
│       Wikipedia-logo.png
│       Wikipedia20_background.jpg
│
└───templates
        error.html
        index.html
        search_results.html

```

# Setup and Configuration
<a id="Host"></a>

The following assumed that a postgres service is available for connection at the location (host, port etc)
specified in the configuration file (see steps below)

1. Create a virtual environment (venv) from the source folder: py -m venv env
1. This creates a env folder in the source folder. Activate the venv: ./env/Scripts/activate
1. Install all python packages listed in requirements.txt: python -m pip install -r .\requirements.txt
1. Copy the provided config.yml.example to config.yml and set the configuration options for the database connection

# Usage

Once the configuration has been completed, the application can be run as follows:
- On the host machine, run Flask application (main.py) from PyCharm
- Open a web browser at the address given by Flask (http://127.0.0.1:5000). This displays the search page.
- Enter the search term and select options for cache and article output. Click search.
- The results of the search are displayed on the results page.
