from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Skill(db.Model):
    name = db.Column(db.String(200), primary_key=True, nullable=False)
    url = db.Column(db.String(500), nullable=True)
    img = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Skill {str(self.name)}>'
