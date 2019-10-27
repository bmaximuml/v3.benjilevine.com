from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class About(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(5000), nullable=False)
    priority = db.Column(db.Integer, nullable=False)


class Skill(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable=False)
    url = db.Column(db.String(500), nullable=True)
    img = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Skill {str(self.name)}>'
