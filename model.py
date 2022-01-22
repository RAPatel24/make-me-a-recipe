from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    '''users table'''
    __tablename__ = "users"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User user_id={self.id} name = {self.fname}  email={self.email}>"

class UserPreference(db.Model):
    '''users table'''
    __tablename__ = "user_preferences"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    preference_id = db.Column(db.Integer, db.ForeignKey('preferences.id'))

    user = db.relationship("User", backref="user_preferences")
    preference = db.relationship("Preference", backref="user_preferences")

    def __repr__(self):
        return f"<UserPreference user_id={self.user_id} preference={self.preference_id}>"

class Preference(db.Model):
    '''users table'''
    __tablename__ = "preferences"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String, nullable=False)
    value = db.Column(db.String, nullable=False)

    user = db.relationship("User", backref="preferences")

    def __repr__(self):
        return f"<Preference user_id={self.user_id} name={self.name} value={self.value}>"

class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    recipe_id = db.Column(db.Integer, nullable = False)

    user = db.relationship("User", backref="recipes")

    def __repr__(self):
        return f"<Recipe user_id={self.user_id} recipe_id={self.recipe_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///make_me_a_recipe_db", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)