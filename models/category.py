from extensions import db

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    parts = db.relationship("Part", back_populates="category", cascade="all, delete-orphan")
