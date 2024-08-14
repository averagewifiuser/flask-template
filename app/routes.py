from apiflask import APIBlueprint
from flask import jsonify


main = APIBlueprint('main', __name__)

#routes
@main.get("/")
def lhome():
    return jsonify({'message': 'Hello from the other...'})
