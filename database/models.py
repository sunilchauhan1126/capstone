import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
from settings import DB_NAME, DB_PASSWORD, DB_USER, DB_CONN_STRING

database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_CONN_STRING, DB_NAME)

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Joining(db.Model):
    __tablename__ = 'joining'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    joining_date = Column(DateTime, nullable=False)
    
class Employee(db.Model):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    designation = Column(String(50))
    empployee_dept = relationship('Department', secondary=Joining.__tablename__, backref=db.backref('employee', lazy=True))

    def __init__(self, name, designation):
        self.name = name
        self.designation = designation

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}>"

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'designation': self.designation
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def patch(self, name, designation):
        self.name = name
        self.designation = designation
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Department(db.Model):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Department {self.id}: {self.name}>"

    def format(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def patch(self, name):
        self.name = name
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
