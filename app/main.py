from flask import Flask
from flask import request, jsonify
from app.recommendation import get_recommendations, get_features


app = Flask(__name__)


@app.route('/recommendations')
def recommendations():
    user_id = request.args.get('user_id', type=int)
    return_metadata = request.args.get('returnMetadata', type=bool, default=False)
    return jsonify(get_recommendations(user_id, return_metadata))


@app.route('/features')
def features():
    user_id = request.args.get('user_id', type=int)
    return jsonify(get_features(user_id))


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host="0.0.0.0", debug=True, port=80)