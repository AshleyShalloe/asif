from flask import Flask, request, jsonify
from flask_cors import CORS
from get_story import retrieve_and_normalise_story
from asif import retrieve_and_write_updated_json

app = Flask(__name__)
CORS(app)

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
