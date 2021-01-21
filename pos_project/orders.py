from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amann:zaq1@WSX@localhost:5432/pos'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Alias(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ItemID= db.Column(db.Integer)
    Alias = db.Column(db.VARCHAR)
    
@app.route('/')
def index():
    alias = Alias.query.first()
    return 'this is the aliaas table info' + alias.id, alias.ItemID, alias.Alias



#as of Jan 10, 2021, this is not working, the code does not pull the data from Postgres