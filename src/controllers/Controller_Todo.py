from src import app
from flask import redirect, render_template, request, flash

# Forms
from src.forms import TodoForm

# Models
from src.models.Model_Todo import Todo


# ========== Main Page ==========
@app.route('/')
def get_todo():
    todo = Todo()

    todoArray = []
    todos = todo.find({})

    for todo in todos:
      todoObj = {
        "_id": str(todo["_id"]),
        "name": todo["title"],
        "description": todo["description"],
        "completed": todo["completed"],
        "date_created": todo["created"].strftime("%b %d %Y %H:%M%S")
      }
      todoArray.append(todoObj)

    # // Not Working
    return render_template('todo.html', todoArray=todoArray)


# ========== Add Page ==========
# Route
@app.route('/add_todo', methods=['GET'])
def view_add_todo():
    form = TodoForm()
    return render_template('add_todo.html', form=form)

# Create
@app.route('/add_todo', methods=['POST'])
def add_todo():
    todo = Todo()

    form = TodoForm(request.form)
    todo_name = form.name.data
    todo_description = form.description.data
    todo_completed = form.completed.data

    todo.create({
        "title": todo_name,
        "description": todo_description,
        "completed": todo_completed
    })

    flash('Todo Successfully Added!', 'success')
    return redirect('/')


# ========== Update Todo ==========
# Route
@app.route('/update_todo/<id>', methods=['GET'])
def view_update_todo(id):
    todo = Todo()
    result = todo.find_by_id(id)
    
    form = TodoForm()
    form.name.data = result['title']
    form.description.data = result['description']
    form.completed.data = result['completed']

    return render_template('add_todo.html', form=form)

# Update
@app.route('/update_todo/<id>', methods=['POST'])
def update_todo(id):
    todo = Todo()

    form = TodoForm(request.form)
    todo_name = form.name.data
    todo_description = form.description.data
    todo_completed = form.completed.data

    todo.update(id, {
        "title": todo_name,
        "description": todo_description,
        "completed": todo_completed
    })
    
    flash('Todo Successfully Updated!', 'success')
    return redirect('/')


# ========== Delete Todo ==========
@app.route('/delete_todo/<id>')
def delete_todo(id):
    todo = Todo()
    todo.delete(id)

    flash('Todo Successfully Deleted!', 'success')
    return redirect('/')