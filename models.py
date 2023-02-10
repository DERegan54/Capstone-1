from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


############################################################################
# MODELS:
############################################################################


class User (db.Model):
    """Model that creates instances of users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    family_members_adults = db.Column(db.Integer)
    family_members_children = db.Column(db.Integer)
    other_pets = db.Column(db.String)
    environment = db.Column(db.String)
    experience_level = db.Column(db.String)
    # review_id = db.Column(db.Integer, db.ForeignKey('reviews.id', ondelete='cascade'))

    reviews = db.relationship('Review', single_parent=True, backref='users', cascade='all, delete-orphan')
    # favorites = db.relationship('Favorite', single_parent=True, backref='users', cascade='all, delete-orphan')
    favorites = db.relationship('Breed', secondary="favorites")

    def __repr__(self):
        return f"<User {self.id}, {self.username}, {self.password}"

    @classmethod
    def signup(cls, username, password, email):
        """ Sign up user. Hashes password and adds user to database."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email
        )
        db.session.add(user)
        db.session.commit()
        return user
    
            
    @classmethod
    def authenticate(cls, username, password):
        """Find user with 'username' and 'password'.
        Searches for a user in the database whose password hash matches
        the input password.  If found, it returns the user object.  If not
        found, it returns False. 
        """

        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False


class Breed (db.Model):
    """Model that creates instances of dog breeds."""

    __tablename__ = 'breeds'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    image_link = db.Column(db.String)
    good_with_children = db.Column(db.Integer)
    good_with_other_dogs = db.Column(db.Integer)
    shedding = db.Column(db.Integer)
    coat_length = db.Column(db.Integer)
    trainability = db.Column(db.Integer)
    barking = db.Column(db.Integer)
    min_life_expectancy = db.Column(db.Integer)
    max_life_expectancy = db.Column(db.Integer)
    max_height_male = db.Column(db.Integer)
    max_height_female = db.Column(db.Integer)
    max_weight_male = db.Column(db.Integer)
    max_weight_female = db.Column(db.Integer)
    min_height_male = db.Column(db.Integer)
    min_height_female = db.Column(db.Integer)
    min_weight_male = db.Column(db.Integer)
    min_weight_female = db.Column(db.Integer)
    grooming = db.Column(db.Integer)
    drooling = db.Column(db.Integer)
    good_with_strangers = db.Column(db.Integer)
    playfulness = db.Column(db.Integer)
    protectiveness = db.Column(db.Integer)
    energy = db.Column(db.Integer)
    name = db.Column(db.String, unique=True, nullable=False)    

    reviews = db.relationship('Review', single_parent=True, backref='breeds', cascade='all, delete-orphan')
    favorites = db.relationship('Favorite', single_parent=True, backref='breeds', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"{self.name}"


class Review (db.Model):
    """Model that creates instances of dog breed reviews."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    breed_name = db.Column(db.String)
    maintenance_rating = db.Column(db.Integer, nullable=False)
    behavior_rating = db.Column(db.Integer, nullable=False)
    trainability_rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))


class Favorite (db.Model):
    """Model that creates instances of breeds that the user is considering."""

    __tablename__ = 'favorites'

    
    breeds_name = db.Column(db.Text, db.ForeignKey('breeds.name', ondelete='cascade'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'), primary_key=True)
    
    def __repr__(self):
        return f'<Favorites | User {self.user_id} | Breed {self.breed_id}'

    # @classmethod
    # def add_breed_to_favorites(breed_name, user_id):
    #     """Adds breed to favorites."""
        
    #     user_id = User.id

    #     favorite = Favorite(
    #         breeds_name = breed_name,
    #         user_id = user_id
    #     )
   
    #     db.session.add(favorite)
    #     db.session.commit()
        
    #     return favorite

   