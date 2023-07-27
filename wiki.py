"""
# @ author: ruairin
# @ about: this code searches information on Wikipedia about a given term and prints the result
# @ usage: python3 wiki.py term
#       e.g., python3 wiki.py "Barack Obama"
"""

import wikipedia
import sys
import json


def search_wikipedia(term):
    """
    Searches wikipedia for the specified term, prints the results
    to stdout as a json string

    :param string term: String to search for on wikipedia
    :return: None, output is written to stdout
    """

    # Get a list of page ids that match the search term
    page_ids = wikipedia.search(term)

    # save the pages corresponding to the page ids in a list
    pages = []
    for pageId in page_ids:
        try:
            page = wikipedia.page(pageId)

            # each page is saved as a dict. a subset of the wikipedia.page object is
            # saved, i.e. title, url, summary, content
            # summary is the article text under the title in wikipedia
            # content is everything under the title, including the summary
            pages.append({"title": page.title,
                          "url": page.url,
                          "summary": format_content(page.summary),
                          "content": format_content(page.content)
                          })
        except:
            sys.stderr.write("Oops: could not parse the page:" + pageId)
            pass

    # Print the pages to stdout as a json string
    return json.dumps({"pages": pages})



def format_content(text):
    """
    Processes the string output from page.summary and page.content to add
    html tags as follows:
        - Wraps each line of text in paragraph tags.
        - Wraps heading lines (identified by '==' or '===') with heading tags

    :param string text: String to be processed
    :return: string output: The string with the tags added
    """
    output = ""
    for line in text.splitlines():
        # Ignore blank lines
        if len(line.strip()) == 0:
            continue

        # Check for heading lines, which are delimited in the string
        # by "===" and "=="
        if '===' in line:
            splitline = line.strip().split('===')
            output += "<h3>" + splitline[1:-1][0].strip() + "</h3>"
        elif '==' in line:
            splitline = line.strip().split('==')
            output += "<h2>" + splitline[1:-1][0].strip() + "</h2>"
        # For non-heading lines, wrap the line in <p></p> tags
        else:
            output += "<p>" + line.strip() + "</p>"
    return output


if __name__ == '__main__':
    arguments = "".join(sys.argv[1:])  # read the arguments (i.e., the search term)
    search_wikipedia(arguments)

