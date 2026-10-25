from flask import app
from extensions import db
from models import *

"""
Test seed file
"""

def seed_db(app):
    db.init_app(app)

    with app.app_context():
        db.drop_all()
        db.create_all()
        if Part.query.count() == 0:
            for i in range(0,10):
                db.session.add(Part(name=f"Part id {i}"))
        if Category.query.count() == 0:
            db.session.add(Category(name="Connectors"))
            db.session.add(Category(name="Sensors"))
            db.session.add(Category(name="Power"))
            db.session.add(Category(name="Protection"))
            db.session.add(Category(name="ICs"))
            db.session.add(Category(name="Diodes"))
            db.session.add(Category(name="Resistors"))
            db.session.commit()   
        
        db.session.commit()   