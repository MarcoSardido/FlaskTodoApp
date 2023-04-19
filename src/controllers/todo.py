from src import app
from flask import redirect, render_template, request, flash, jsonify
from bson.json_util import dumps
import logging

# Forms
from src.forms import TodoForm

# Models
from src.models.todo import Todo

@app.route('/')
def get_todo():
    todo_array = []
    todos = Todo.getList()
    for todo in todos:
        todo['date_created'] = todo["created"].strftime("%d/%m/%Y, %H:%M:%S")
        todo_array.append(todo)
    return dumps(todo_array), 200

@app.route('/todo', methods=['GET'])
def view_add_todo():
    form = TodoForm()
    return render_template('add_todo.html', form=form)

@app.route('/todo', methods=['POST'])
def add_todo():
    data = request.get_json()
    title, description, completed = data.values()
    try:
        Todo.create({
        "title": title,
        "description": description,
        "completed": completed
        })
        return jsonify({'message': 'Todo Successfully Added!', 'status': 200})
    except ValueError as ex:
        logging.error('%s invalid value passed', ex)
    except Exception as ex:
        logging.error('error creating todo')
        return jsonify({'error': ex.message})
    
@app.route('/todo/<id>', methods=['GET'])
def view_update_todo(id):
    todo = Todo.get(id)
    if todo is None:
        logging.error('Todo does not exist')
        return jsonify({'error': 'Todo does not exist'})
    try:
        content = {
            "id": todo._id,
            "title": todo.title,
            "description": todo.description,
            "completed": todo.completed
        }
        return dumps({'data': content, 'status': 200})
    except ValueError as ex:
        logging.error('%s invalid value passed', ex)
    except Exception as ex:
        logging.error('error updating todo')
        return jsonify({'error': ex})

@app.route('/todo/<id>', methods=['POST'])
def update_todo(id):
    data = request.get_json()
    title, description, completed = data.values()
    todo = Todo.get(id)
    try:
        todo.update({
            "title": title,
            "description": description,
            "completed": completed
        })
        return jsonify({"message": 'Todo Successfully Updated!', 'status': 200})
    except ValueError as ex:
        logging.error('%s invalid value passed', ex)
    except Exception as ex:
        logging.error('error creating todo')
        return jsonify({'error': ex.message})
 
@app.route('/todo/<id>/delete', methods=['POST'])
def delete_todo(id):
    todo = Todo.get(id)
    if todo is None:
        logging.error('Todo does not exist')
        return jsonify({'error': 'Todo does not exist', 'status': 404})
    try:
        todo.delete()
        return jsonify({'message': 'Todo Successfully Deleted!', 'status': 200})
    except Exception as ex:
        logging.error('error deleting todo')
        return jsonify({'error': ex.message})
