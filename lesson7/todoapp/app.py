from flask import Flask, render_template, request, redirect, url_for, jsonify
import sys
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://amann:zaq1@WSX@localhost:5432/example'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed =db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f'<Todo {self.description}>'

# db.create_all()

@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body ={}
    id = request.get_json()['id']
    description = request.get_json()['description']
    # todo = Todo(description=description)
    try:
        todo = Todo(id=id, description=description)
        db.session.add(todo)
        db.session.commit()
        body['id'] = todo.id
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    if not error:
        return jsonify(body)


@app.route('/')
def index():
   return render_template('index.html', data=Todo.query.all())