from flask import redirect, render_template, request, url_for, flash
from src import app, db
from .forms import TodoForm
from datetime import datetime


@app.route('/')
def index():
    return render_template('todo.html')

@app.route('/add_todo', methods=['GET', 'POST'])
def add_todo():
    if request.method == 'POST':
        form = TodoForm(request.form)
        todo_name = form.name.data
        todo_description = form.description.data
        todo_completed = form.completed.data

        # Adding data to collection "todo_flask"
        db.todos.insert_one({
            'name': todo_name,
            'description': todo_description,
            'completed': todo_completed,
            'date_completed': datetime.utcnow()
        })
        flash('Todo Successfully Added!', 'success')
        return redirect('/')
    
    else:
        form = TodoForm()
        
    return render_template('add_todo.html', form=form)



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
