# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate
from flask import jsonify, request

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake_by_id(id):
    earthquake = Earthquake.query.get(id) #look for earthquake by primary key

    if earthquake:
        response = jsonify(earthquake.to_dict())
        return make_response(response, 200)
    else:
       return make_response(jsonify({"message": f"Earthquake {id} not found."}), 404)

@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_min_magnitude(magnitude):
    # Query earthquakes where magnitude is >= provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Convert each earthquake object to dictionary format
    quake_list = [quake.to_dict() for quake in earthquakes]

    # Build the final response
    response = {
        "count": len(quake_list),
        "quakes": quake_list
    }

    return make_response(jsonify(response), 200)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
