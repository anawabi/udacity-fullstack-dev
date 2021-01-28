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
    list_id = db.Column (db.Integer, db.ForeignKey('todolists.id'), nullable = False)

    def __repr__(self):
        return f'<Todo {self.description}>'

class TodList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column (db.String, nullable = False)
    todos = db.relationship('Todo', backref='list', lazy = True)

# db.create_all()

# This function gets the todo item completed status along wiht the todo item ID and updates the todo status in DB, the completed value would be either True or False coming for the fron end.
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
   
    try:
        completed =request.get_json()['completed']
        todo=Todo.query.get(todo_id)
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
        error = True
        print(sys.exc_info)
    finally:
        db.session.close()
    return redirect(url_for('index'))

@app.route('/todos/<todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
  try:
    Todo.query.filter_by(id=todo_id).delete()
    db.session.commit()
  except:
    db.session.rollback()
  finally:
    db.session.close()
#   return jsonify({ 'success': True })
  return redirect(url_for('index'))



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
        body['description'] = todo.description
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
   return render_template('index.html', data=Todo.query.order_by('id').all())