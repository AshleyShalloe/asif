from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from get_story import retrieve_and_normalise_story, get_story_image_by_url
from asif import retrieve_and_write_updated_json

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET', 'POST'])
def returnMainHtml():
    return render_template("index.html")

@app.route('/get_story_by_url')
def getStoryByUrl():
    url = request.args.get('url')

    story = retrieve_and_normalise_story(url)
    
    return jsonify(story)

@app.route('/update_feed')
def updateFeed():
    try:
        retrieve_and_write_updated_json()
        return jsonify({"Status": "Success"})
    except:
        return jsonify({"Status": "Didn't work mate"})

@app.route('/get_story_image')
def getStoryImage():
    try:
        url = request.args.get("url")
        image = get_story_image_by_url(url)
        return jsonify({"image_url": image})
    except:
        return jsonify({"image_url": None})