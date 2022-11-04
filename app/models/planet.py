from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    name = db.Column(db.String)
    solid = db.Column(db.Boolean)
    description = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "solid": self.solid
        }

    @classmethod
    def from_dict(cls, planet_dict):
        return cls(
            name=planet_dict["name"],
            solid=planet_dict["solid"],
            description=planet_dict["description"]
        )