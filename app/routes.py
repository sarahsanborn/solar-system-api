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
def get_all_planet():
    result = []
    all_planets = Planet.query.all()
    for item in all_planets:
        item_dict = {"id": item.id, "name": item.name, "solid": item.solid, "description": item.description}
        result.append(item_dict)
    return jsonify(result), 200


@planet_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = valid_planet(planet_id)

    return jsonify({
        "id": planet.id,
        "name": planet.name,
        "description": planet.description
    })


def valid_planet(planet_id):
    try:
        planet_id = int(planet_id)
    except ValueError:
        abort(make_response({"message": f"Planet {planet_id} is invalid"}, 400))

    for planet in planet_items:
        if planet.id == planet_id:
            return planet

    abort(make_response({"message": f"Planet {planet_id} not found."}, 404))



@planet_bp.route("", methods=["POST"])
def create_new_planet():
    request_body = request.get_json()
    new_planet = Planet(name=request_body["name"],
                      solid=request_body["solid"],
                      description=request_body["description"])

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} successfully created", 201)