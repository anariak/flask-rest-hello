from flask_sqlalchemy import SQLAlchemy
import datetime
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(200))
    mail = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    name = db.Column(db.String(20))
    lastname = db.Column(db.String(20))
    rut = db.Column(db.String(15))

    def __repr__(self):
        return '<User %r>' % self.username
    
    def serialize(self):
        return {
            "username": self.username,
            "password": self.password,
            "mail": self.mail,
            "phone": self.phone,
            "name": self.name,
            "lastname": self.lastname,
            "rut": self.rut
        }
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(25))
    creation = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date = db.Column(db.DateTime)
    location = db.Column(db.String(50))
    description = db.Column(db.String(150))
    payment = db.Column(db.Float)
  #  category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    status = db.Column(db.String(10))
    # Outside Columns
  #  category = db.relationship('Category', backref=db.backref('category', lazy=True))
    user = db.relationship('User', backref=db.backref('user', lazy=True))
    def __repr__(self):
        return '<Task %r>' % self.title

    def serialize(self):
        return {
            "user_id": self.user_id,
            "title": self.title,
            "category":self.category_id,
            "creation": self.creation,
            "date": self.date,
            "localtion": self.location,
            "description": self.description,
            "payment": self.payment,
            "status": self.status
        }