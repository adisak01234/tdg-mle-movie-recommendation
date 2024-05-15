from flask import Blueprint, request, jsonify
from .recommendation import get_recommendations, get_features

main = Blueprint('main', __name__)


@main.route('/recommendations')
def recommendations():
    user_id = request.args.get('user_id', type=int)
    return_metadata = request.args.get('returnMetadata', type=bool, default=False)
    return jsonify(get_recommendations(user_id, return_metadata))


@main.route('/features')
def features():
    user_id = request.args.get('user_id', type=int)
    return jsonify(get_features(user_id))