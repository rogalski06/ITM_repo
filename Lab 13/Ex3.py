# Create a simple Flask application to retrieve memes from https://meme-api.com/gimme/wholesomememes.  To get the memes you will need to issue a requests.request("GET", url) command.

# a. Present the meme and the meme source (subreddit) to the user. Refresh the meme every 10 seconds.  You can accomplish this by including the following <meta> tags in the <head> of your HTML page.
# <head>
   # <title>Memes'R'Us</title>
   # <meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=0.8">
   # <meta http-equiv="refresh" content="10; url=http://127.0.0.1:5000" />
# </head>

from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

@app.route('/')
def home():
    url = "https://meme-api.com/gimme/wholesomememes"
    response = requests.request("GET", url)
    meme_data = response.json()
    meme_url = meme_data['url']
    subreddit = meme_data['subreddit']
    return render_template('meme.html', meme_url=meme_url, subreddit=subreddit)

if __name__ == '__main__':
    app.run(debug=True)