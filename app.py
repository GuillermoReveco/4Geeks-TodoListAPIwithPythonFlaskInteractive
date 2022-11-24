import os
from flask import Flask, request
from flask import jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

BASEDIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(BASEDIR, 'app.db')

Migrate(app, db)
db.init_app(app)
CORS(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    done = db.Column(db.Boolean, default=False, nullable=False)
    label = db.Column(db.Text, nullable = False, unique=True)

    def __repr__(self) -> str:
        return "<Todo %r>" % self.done

    def serialize(self):
        return{
            "id": self.id,
            "done": self.done,
            "label": self.label,
        }

@app.route('/todos', methods = ['GET'])
def get_todos():
    todos = db.session.query(Todo).all()
    response = []
    for todo in todos:
        print(todo)
        print(todo.done)
        print(todo.label)
        response.append({"done": todo.done, "label": todo.label})
    print(todos)
    if response is not None:
        return jsonify(response), 200
    else:
        return jsonify({"msg":"todos not found"}), 404

@app.route('/todos', methods = ['POST'])
def create_todo():
    try:
        todo = Todo()
        todo.done = request.json.get("done")
        todo.label = request.json.get("label")
        print(todo)
        db.session().add(todo)
        db.session().commit()
        return jsonify({"message":"create todo"}), 201
    except Exception as e:
        return jsonify({"message":e}), 500

@app.route('/todos/<int:id>', methods = ['DELETE'])
def delete_todo(id):
    todo = db.session.query(Todo).get(id)
    if todo is not None:
        db.session.delete(todo)
        db.session.commit()
        todos = db.session.query(Todo).all()
        response = []
        for todo in todos:
            print(todo)
            print(todo.done)
            print(todo.label)
            response.append({"done": todo.done, "label": todo.label})
        print(todos)
        if response is not None:
            return jsonify(response), 200
        else:
            return jsonify({"msg":"todos empty"}), 203
    else:
        return jsonify({"msg":"todo not found"}), 404
