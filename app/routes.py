from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, abort, make_response,request


planet_bp = Blueprint("planets", __name__, url_prefix="/planets")


@planet_bp.route("", methods=["GET"])
def get_all_planets():
    name_query_value = request.args.get("name")
    if name_query_value is not None:
        planets = Planet.query.filter_by(name=name_query_value)
    else:
        planets = Planet.query.all()

    result = [item.to_dict() for item in planets]
    return jsonify(result), 200

# def validate_query(attr):
#     planet_value = request.args.get(attr)
#     all_planets = Planet.query.all()
#     for planet in all_planets:
#         if planet_value in planet.values():

#         if not planet:
#             return abort(make_response({"msg": f"Could not find planet with attribute {attr}"}, 404))
#         else:
#             return planet_value


@planet_bp.route("/<planet_id>", methods=["GET"])
def get_one_planet(planet_id):
    planet = get_class_object_from_id(Planet, planet_id)

    return jsonify(planet.to_dict())


@planet_bp.route("", methods=["POST"])
def create_new_planet():
    request_body = request.get_json()
    new_planet = Planet.from_dict(request_body)

    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Planet {new_planet.name} with id {new_planet.id} successfully created", 201)


@planet_bp.route("/<planet_id>", methods=["DELETE"])
def delete_one_planet(planet_id):
    planet_to_delete = get_class_object_from_id(Planet, planet_id)

    db.session.delete(planet_to_delete)
    db.session.commit()

    return jsonify({"message": f"Successfully deleted planet id {planet_id}"}), 200


@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_one_planet(planet_id):
    planet_to_update = get_class_object_from_id(Planet, planet_id)

    request_body = request.get_json()

    try:
        planet_to_update.name = request_body["name"]
        planet_to_update.description = request_body["description"]
        planet_to_update.solid = request_body["solid"]
    except KeyError:
        return jsonify({"message": f"Missing needed data"}), 400
    
    db.session.commit()
    
    return jsonify({"message": f"Successfully updated planet {planet_id}"}), 200


def get_class_object_from_id(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        return abort(make_response({"message": f"Invalid data type {cls.__name__} with id: {model_id}"}, 400))
    
    chosen_object = cls.query.get(model_id)

    if not chosen_object:
        return abort(make_response({"message": f"Could not find {cls.__name__} with id {model_id}"}, 404))
    
    return chosen_object