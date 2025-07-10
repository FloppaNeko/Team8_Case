from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)  # e.g., Student, UniversityRep, Admin

    applications = db.relationship('Application', back_populates='student')
    feedbacks = db.relationship('Feedback', back_populates='author')


class University(db.Model):
    __tablename__ = 'universities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    contact_info = db.Column(db.String)

    exchange_programs = db.relationship('ExchangeProgram', back_populates='university')


class ExchangeProgram(db.Model):
    __tablename__ = 'exchange_programs'
    id = db.Column(db.Integer, primary_key=True)
    university_id = db.Column(db.Integer, db.ForeignKey('universities.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    duration = db.Column(db.String)
    requirements = db.Column(db.Text)

    university = db.relationship('University', back_populates='exchange_programs')
    courses = db.relationship('Course', back_populates='program')
    applications = db.relationship('Application', back_populates='program')
    feedbacks = db.relationship('Feedback', back_populates='program')


class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('exchange_programs.id'), nullable=False)
    code = db.Column(db.String)
    name = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer)
    semester = db.Column(db.String)
    competencies = db.Column(db.Text)
    annotation = db.Column(db.Text)

    program = db.relationship('ExchangeProgram', back_populates='courses')


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('exchange_programs.id'), nullable=False)
    status = db.Column(db.String)
    submission_date = db.Column(db.DateTime, default=datetime.utcnow)
    feedback = db.Column(db.Text)

    student = db.relationship('User', back_populates='applications')
    program = db.relationship('ExchangeProgram', back_populates='applications')
    feedbacks = db.relationship('Feedback', back_populates='application')


class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('exchange_programs.id'), nullable=False)
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    application = db.relationship('Application', back_populates='feedbacks')
    program = db.relationship('ExchangeProgram', back_populates='feedbacks')
    author = db.relationship('User', back_populates='feedbacks')  # Assuming only students leave feedbacks
