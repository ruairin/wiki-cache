"""
# @ author: ruairin
# @ about: Main flask file for CT5169 Assignment 01
# @ usage: 1. Consult readme.md for setup instructions
#          2. Run this main.py file
#          3. Load the app in a web browser (default is 127.0.0.1:5000
#             if the flask server is running on the local machine)
"""

from flask import Flask, render_template, request
import json
import db
import wiki

# Set flask configuration
# set app name to main
app = Flask(__name__)
app.config['ENV'] = "Development"
app.config['DEBUG'] = True


# Route to the default page for the application
@app.route('/')
def default():
    return render_template('index.html')


# The route for displaying the search results
@app.route('/submit_search')
def submit_search():
    # get the search term entered by the user
    search_string = request.args.get('search_text')

    # redirect to the error page if no search term was entered
    if search_string.strip() == '':
        return render_template('error.html', message="You didn't enter anything")

    # Get the cache option selected by the user.
    # If enabled, the app tries to read the existing results from the database cache
    # otherwise it uses the search script and adds the results to the database
    # If not enabled, the app uses the search script and updates the database even if the record already exists
    cache_option = request.args.get('cache_option')
    use_db = False
    if cache_option == 'yes':
        use_db = True

    # get the summary option
    # if 'summary' is selected, only the text under the title in wikipedia is displayed
    # otherwise, the entire article content is displayed
    summary = True if request.args.get('summary') == "summary" else False

    # Check DB if search string exists
    cached_result = db.search(search_string)

    # The search term is already in the database, and the user has selected use cached data
    if cached_result and use_db:
        article_data = json.loads(cached_result)
        article_source = 'Cache'
    else:
        result = wiki.search_wikipedia(search_string)

        # Note: the script output (in 'result' variable) is the output of json.dumps() in the wiki.py script
        # (i.e.a string). Use json.loads() to convert the json string to a dict
        # Note article_data is in this format:
        # { 'pages': [
        #      {'title': 'Page 1 Title', 'url':'Page 1 URL', 'summary':'Page 1 summary', 'content': 'Page 1 content'},
        #      {'title': 'Page 2 Title', 'url':'Page 2 URL', 'summary':'Page 2 summary', 'content': 'Page 2 content'},
        #       ....
        #      ]
        # }
        article_data = json.loads(result)

        # Set a flag for displaying article source on the results page
        article_source = 'New Search'

        # Insert/update the cache database if a result was found
        if len(article_data['pages']) > 0:
            db.insert(search_string, json.dumps(article_data))

    # Display the results page
    return render_template('search_results.html', search_string=search_string, article_data=article_data,
                           summary=summary, article_source=article_source)


if __name__ == '__main__':
    app.run()
