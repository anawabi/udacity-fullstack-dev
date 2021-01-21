from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import BYTEA

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amann:zaq1@WSX@localhost:5432/pos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# class Person(db.Model):
#     __tablename__ = 'persons'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(), nullable=False)

#     def __repr__(self):
#         return f'<Person Id: {self.id}, Name: {self.name} >'

class Category(db.Model):
    __tablename__ = 'Category'
    hqid = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer)
    DepartmentID = db.Column(db.Integer)
    Name = db.Column(db.String(30))
    Code = db.Column(db.String(17))
    # DBTimeStamp = db.Column(db.BYTEA)

    def __repr__(self):
        return f'<Person Id: {self.id}, Name: {self.Name} >'


@app.route('/')
def index():
   return render_template('index.html', data=Category.query.all())

