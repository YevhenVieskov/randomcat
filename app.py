from flask import Flask, render_template
import random

app = Flask(__name__)

# list of cat images
images = [
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-13/anigif_sub-buzz-11282-1502314385-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-10/anigif_sub-buzz-8427-1502313524-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-02/anigif_sub-buzz-22626-1502313674-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-02/anigif_sub-buzz-22707-1502313740-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-06/anigif_sub-buzz-8222-1502313939-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-14/anigif_sub-buzz-24014-1502314003-8.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-01/anigif_sub-buzz-20568-1502314071-7.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-05/anigif_sub-buzz-30975-1502314180-1.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/17/asset/buzzfeed-prod-web-01/anigif_sub-buzz-20634-1502314251-8.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/19/asset/buzzfeed-prod-web-08/anigif_sub-buzz-21012-1502319766-12.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/19/asset/buzzfeed-prod-web-08/anigif_sub-buzz-21438-1502320104-2.gif",
"https://img.buzzfeed.com/buzzfeed-static/static/2017-08/9/19/asset/buzzfeed-prod-web-04/anigif_sub-buzz-3679-1502320218-1.gif"
    
]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0")




