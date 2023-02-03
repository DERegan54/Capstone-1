from models import db, User, Breed,  Review, Favorite
from app import app

# Clear any old tables
db.drop_all()
# Create all tables
db.create_all()

db.session.commit()