from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

##########################################################

class User (db.Model):
    """Model that creates instances of users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    profile_photo = db.Column(db.String)
    email = db.Column(db.String, nullable=False)
    family_members_adults = db.Column(db.Integer)
    family_members_kids = db.Column(db.Integer)
    other_pets = db.Column(db.String)
    environment = db.Column(db.String)
    experience_level = db.Column(db.String)

    def __repr__(self):
        return f"<User {self.id}: {self.username}, {self.password}"

    @classmethod
    def signup(cls, username, password, email):
        """ Sign up user.
            Hashes password and adds user to database.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email
        )
        db.session.add(user)
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
    breed_name = db.Column(db.String, unique=True, nullable=False)    
    image_url= db.Column(db.String)



class Characteristic (db.Model):
    """Model that creates instances of dog characteristics."""

    __tablename__ = 'characteristics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    good_with_children= db.Column(db.Integer)
    good_with_other_dogs = db.Column(db.Integer)
    shedding = db.column(db.Integer)
    drooling = db.column(db.Integer)
    grooming = db.column(db.Integer)
    protectiveness = db.column(db.Integer)
    trainability = db.column(db.Integer)
    energy = db.column(db.Integer)
    barking = db.column(db.Integer)
    max_life_expectancy = db.column(db.Integer)
    max_height_male = db.column(db.Integer)
    max_height_female = db.column(db.Integer)
    max_weight_male = db.column(db.Integer)
    max_weight_female = db.column(db.Integer)



class Review (db.Model):
    """Model that creates instances of dog breed reviews."""

    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    maintenance_rating = db.Column(db.Integer, nullable=False)
    behavior_rating = db.Column(db.Integer, nullable=False)
    trainability_rating = db.Column(db.Integer, nullable=False)
    comments = db.Column(db.String)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id', ondelete='cascade'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    users = db.relationship('User', backref='reviews')
    breeds = db.relationship('Breed', single_parent=True, backref='reviews', cascade='all, delete-orphan')


class Favorite_breed (db.Model):
    """Model that creates instances of breeds that the user is considering."""

    __tablename__ = 'favorite_breeds'

    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    breeds = db.relationship('Breed', single_parent=True, backref='favorite_breeds', cascade='all, delete-orphan')
    users = db.relationship('User', single_parent=True, backref='favorite_breeds', cascade='all, delete-orphan')



class Breed_characteristic (db.Model):
    """Model to create instances of characteristics on a dog breed."""

    __tablename__ = 'breed_characteristics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    breed_id = db.Column(db.Integer, db.ForeignKey('breeds.id', ondelete='cascade'))
    characteristic_id = db.Column(db.Integer,db.ForeignKey('characteristics.id'))

    breeds = db.relationship('Breed', single_parent=True, backref='breed_characteristics', cascade='all, delete-orphan')
    characteristics = db.relationship('Characteristic', single_parent=True, backref='breed_characteristics', cascade='all, delete-orphan') 
    

# class User_valued_characteristic (db.Model):
#     """Model to create instances of breed characteristics that the user values."""

#     __tablename__= 'user_valued_characteristics'

#     id = db.Column(db.Integer, autoincrement=True, nullable=False)
#     value_rating = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, ForeignKey=('users'), ondelete='CASCADE')
#     characteristc_id = db.Column(db.Integer, ForeignKey=('breed_characteristics'))

#     users = db.relationship('User', backref='user_valued_characteristics', cascade='all, delete-orphan')

# class Dog_in_home (db.Model): 
#     """Model that creates instances of dogs already in user's home."""

#     __tablename__ = 'dogs_in_home'

#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
#     photo = db.Column(db.String)
#     breed_id = db.Column(db.Integer, db.ForeignKey('breeds'))
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    
#     breeds = db.relationship('Breed', backref='dogs_in_home', cascade='all, delete-orphan')
#     users = db.relationship('User', backref='dogs_in_home', cascade='all, delete-orphan')




