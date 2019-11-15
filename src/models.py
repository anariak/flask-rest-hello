from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    mail = db.Column(db.String(20))
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
            "name": self.name,
            "lastname": self.lastname,
            "rut": self.rut
        }