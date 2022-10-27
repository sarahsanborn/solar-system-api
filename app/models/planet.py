from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key= True, autoincrement=True)
    name = db.Column(db.String)
    solid = db.Column(db.Boolean)
    description = db.Column(db.String)