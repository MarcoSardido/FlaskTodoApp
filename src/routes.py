# from flask import redirect, render_template, request, flash, jsonify, url_for
# import logging
# from src import app, todoCollection
# from .forms import TodoForm
# from datetime import datetime
# from bson import ObjectId



# # ========== Main Page ==========
# @app.route('/')
# def get_todo():
#     todoArray = []
    
#     try:
#         todos = todoCollection.find().sort('date_created', -1)
#     except Exception as ex:
#         logging.error('Error retrieving todoCollection data: ', ex)
        
#     for todo in todos:
#         todoObj = {
#             "_id": str(todo["_id"]),
#             "name": todo["name"],
#             "description": todo["description"],
#             "completed": todo["completed"],
#             "date_created": todo["date_created"].strftime("%b %d %Y %H:%M%S")
#         }
#         todoArray.append(todoObj)

#     return render_template('todo.html', todoArray=todoArray)


# # ========== Add Todo ==========
# # Route
# @app.route('/add_todo', methods=['GET'])
# def view_add_todo():
#     form = TodoForm()
#     return render_template('add_todo.html', form=form)

# # # Create
# @app.route('/add_todo', methods=['POST'])
# def add_todo():
#     form = TodoForm(request.form)
#     todo_name = form.name.data
#     todo_description = form.description.data
#     todo_completed = form.completed.data

#     # Adding data to collection "todo_data"
#     try:
#         result = todoCollection.insert_one({
#             'name': todo_name,
#             'description': todo_description,
#             'completed': todo_completed,
#             'date_created': datetime.utcnow()
#         })
#         print(f'New task was added! {result}')
#         flash('Todo Successfully Added!', 'success')
#         return redirect('/')

#     except Exception as ex:
#         logging.error('Error @add_todo: ', ex)
#         return redirect('/')
    


# # ========== Update Todo ==========
# # Route
# @app.route('/update_todo/<id>', methods=['GET'])
# def view_update_todo(id):
#     form = TodoForm()
#     todo = todoCollection.find_one({"_id": ObjectId(id)})
#     form.name.data = todo.get("name", None)
#     form.description.data = todo.get("description", None)
#     form.completed.data = todo.get("completed", None)

#     return render_template('add_todo.html', form=form)

# # # Update
# @app.route('/update_todo/<id>', methods=['POST'])
# def update_todo(id):
#     form = TodoForm(request.form)
#     todo_name = form.name.data
#     todo_description = form.description.data
#     todo_completed = form.completed.data

#     # Updating data to collection "todo_data"
#     try:
#         todoCollection.find_one_and_update({"_id": ObjectId(id)}, {
#             "$set":{
#                 'name': todo_name,
#                 'description': todo_description,
#                 'completed': todo_completed,
#                 'date_created': datetime.utcnow()
#             }
#         })
#         print(f'Todo ID: {id} was updated!')
#         flash('Todo Successfully Updated!', 'success')
#         return redirect('/')

#     except Exception as ex:
#         logging.error('Error @update_todo: ', ex)
#         return redirect('/')


# # ========== Delete Todo ==========

# @app.route('/delete_todo/<id>')
# def delete_todo(id):
#     try:
#         todoCollection.find_one_and_delete({"_id": ObjectId(id)})
#         flash('Todo Successfully Deleted!', 'success')
#         return redirect('/')
#     except Exception as ex:
#         logging.error('Error @delete_todo: ', ex)

