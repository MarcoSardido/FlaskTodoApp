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
    return render_template('todo.html', todo_array=todo_array)

@app.route('/todo', methods=['GET'])
def view_add_todo():
    form = TodoForm()
    return render_template('add_todo.html', form=form)

@app.route('/todo', methods=['POST'])
def add_todo():
    form = TodoForm(request.form)
    todo_name = form.name.data
    todo_description = form.description.data
    todo_completed = form.completed.data
    try:
        Todo.create({
        "title": todo_name,
        "description": todo_description,
        "completed": todo_completed
        })
        flash('Todo Successfully Added!', 'success')
        return redirect('/')
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
        form = TodoForm()
        form.name.data = todo['title']
        form.description.data = todo['description']
        form.completed.data = todo['completed']
        return render_template('add_todo.html', form=form)
    except ValueError as ex:
        logging.error('%s invalid value passed', ex)
    except Exception as ex:
        logging.error('error updating todo')
        return jsonify({'error': ex.message})

@app.route('/todo/<id>', methods=['POST'])
def update_todo(id):
    todo = Todo.get(id)
    form = TodoForm(request.form)
    todo_name = form.name.data
    todo_description = form.description.data
    todo_completed = form.completed.data
    try:
        todo.update({
            "title": todo_name,
            "description": todo_description,
            "completed": todo_completed
        })
        flash('Todo Successfully Updated!', 'success')
        return redirect('/')
    except ValueError as ex:
        logging.error('%s invalid value passed', ex)
    except Exception as ex:
        logging.error('error creating todo')
        return jsonify({'error': ex.message})
 
@app.route('/todo/<id>/delete',  methods=['POST'])
def delete_todo(id):
    todo = Todo.get(id)
    if todo is None:
        logging.error('Todo does not exist')
        return jsonify({'error': 'Todo does not exist'})
    try:
        todo.delete()
        flash('Todo Successfully Deleted!', 'success')
        return redirect('/')
    except Exception as ex:
        logging.error('error deleting todo')
        return jsonify({'error': ex.message})
