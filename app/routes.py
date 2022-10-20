from flask import Blueprint, jsonify

class Planet():
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description


planet_items = [
    Planet(1, "Mercury", "the smallest planet"),
    Planet(2, "Venus", "the hottest planet"),
    Planet(3, "Earth", "the best planet"),
    Planet(4, "Mars", "the red planet"),
    Planet(5, "Jupiter", "the biggest planet"),
    Planet(6, "Saturn", "the most rings planet"),
    Planet(7, "Uranus", "named after the Greek god of the sky"),
    Planet(8, "Neptune", "the last planet")
]

planet_bp = Blueprint("planets", __name__, url_prefix="/planets")

@planet_bp.route("", methods=["GET"])
def get_all_planet():
    result = []
    for item in planet_items:
        item_dict = {"id": item.id, "name": item.name, "description": item.description}
        result.append(item_dict)
    return jsonify(result), 200