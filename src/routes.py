from flask import redirect, render_template, request, url_for, flash, jsonify
import logging
from src import app, todoCollection
from .forms import TodoForm
from datetime import datetime


@app.route('/')
def get_todo():
    todoArray = []

    try:
        todos = todoCollection.find().sort('date_created', -1)

        for todo in todos:
            todoObj = {
                "_id": str(todo["_id"]),
                "name": todo["name"],
                "description": todo["description"],
                "completed": todo["completed"],
                "date_created": todo["date_created"].strftime("%b %d %Y %H:%M%S")
            }
            todoArray.append(todoObj)

            return render_template('todo.html', todoArray=todoArray)
    except Exception as ex:
        logging.error('Error: ', ex)
        return render_template('todo.html', todoArray=todoArray)

    

    


@app.route('/view_add_todo', methods=['GET'])
def view_add_todo():
    form = TodoForm()
    return render_template('add_todo.html', form=form)


@app.route('/add_todo', methods=['GET', 'POST'])
def add_todo():
    form = TodoForm(request.form)
    todo_name = form.name.data
    todo_description = form.description.data
    todo_completed = form.completed.data

    # Adding data to collection "todo_flask"
    try:
        result = todoCollection.insert_one({
            'name': todo_name,
            'description': todo_description,
            'completed': todo_completed,
            'date_created': datetime.utcnow()
        })
        print(f'New task was added! {result}')
        flash('Todo Successfully Added!', 'success')
        return redirect('/')

    except Exception as ex:
        logging.error('Error: ', ex)
        return redirect('/')
    







# @app.route('/add_todo', methods=['POST'])
# def add_todo():
#     form = TodoForm(request.form)
#     todo_name = form.name.data
#     todo_description = form.description.data
#     todo_completed = form.completed.data

#     # Adding data to collection "todo_flask"
#     db.todos.insert_one({
#         'name': todo_name,
#         'description': todo_description,
#         'completed': todo_completed,
#         'date_completed': datetime.utcnow()
#     })
#     flash('Todo Successfully Added!', 'success')
#     return redirect('/')


# @app.route('/get_todos', methods=['GET'])
# def get_todos():
#     form = TodoForm()
#     return render_template('add_todo.html', form=form)


# === Old Todo route codes ===

# @app.route('/add_todo', methods=['POST'])
# def add_todo():
#     todo = request.form['todo']
#     todos.append({'task': todo, 'done': False})
#     return redirect(url_for('todo_page'))


# @app.route('/edit_todo/<int:index>', methods=['GET', 'POST'])
# def edit_todo(index):
#     todo = todos[index]
#     if (request.method == 'POST'):
#         todo['task'] == request.form['todo']
#         return redirect(url_for('todo_page'))
#     else:
#         return render_template('edit.html', todo=todo, index=index)


# @app.route('/check_todo/<int:index>')
# def check_todo(index):
#     todos[index]['done'] = not todos[index]['done']
#     return redirect(url_for('todo_page'))


# @app.route('/delete_todo/<int:index>')
# def delete_todo(index):
#     del todos[index]
#     return redirect(url_for('todo_page'))
