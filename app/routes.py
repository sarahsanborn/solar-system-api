from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response,request


# class Planet():
#     def __init__(self, id, name, description):
#         self.id = id
#         self.name = name
#         self.description = description


# planet_items = [
#     Planet(1, "Mercury", "the smallest planet"),
#     Planet(2, "Venus", "the hottest planet"),
#     Planet(3, "Earth", "the best planet"),
#     Planet(4, "Mars", "the red planet"),
#     Planet(5, "Jupiter", "the biggest planet"),
#     Planet(6, "Saturn", "the most rings planet"),
#     Planet(7, "Uranus", "named after the Greek god of the sky"),
#     Planet(8, "Neptune", "the last planet")
# ]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")


@planet_bp.route("", methods=["GET"])
def get_all_planets():
    all_planets = Planet.query.all()
    result = [item.to_dict() for item in all_planets]
    return jsonify(result), 200


@planet_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = get_planet_from_id(planet_id)

    return jsonify(planet.to_dict())


@planet_bp.route("", methods=["POST"])
def create_new_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                    solid=request_body["solid"],
                    description=request_body["description"])

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)


@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    planet_to_delete = get_planet_from_id(planet_id)

    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted planet id {planet_id}"}), 200


@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_one_planet(planet_id):
    planet_to_update = get_planet_from_id(planet_id)

    request_body = request.get_json()

    try:
        planet_to_update.name = request_body["name"]
        planet_to_update.description = request_body["description"]
        planet_to_update.solid = request_body["solid"]
    except KeyError:
        return jsonify({"message": f"Missing needed data"}), 400
    
    db.session.commit()
    
    return jsonify({"message": f"Successfully updated planet {planet_id}"}), 200


def get_planet_from_id(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        return abort(make_response({"message": f"Invalid data type: {planet_id}"}, 400))
    
    chosen_planet = Planet.query.get(planet_id)

    if not chosen_planet:
        return abort(make_response({"message": f"Could not find planet with id {planet_id}"}, 404))
    
    return chosen_planet