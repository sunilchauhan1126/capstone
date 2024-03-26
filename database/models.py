import os
from sqlalchemy import Column, Integer, String, Date
from flask_sqlalchemy import SQLAlchemy


database_path = os.environ['DATABASE_URL']
if database_path.startswith("postgres://"):
    database_path = database_path.replace("postgres://", "postgresql://", 1)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    with app.app_context():
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    age = Column(Integer)
    gender = Column(String(6))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def __repr__(self):
        return f"<Actor {self.id}: {self.name}>"

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def patch(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def __repr__(self):
        return f"<Movie {self.id}: {self.title}>"

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def patch(self, title, release_date):
        self.title = title
        self.release_date = release_date
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
