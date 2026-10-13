from extensions import db

class UserStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)