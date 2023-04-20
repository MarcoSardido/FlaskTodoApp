<script setup>
import { reactive, ref, toRefs } from 'vue';
import axios from 'axios'
import Todo from './components/Todo.vue'

const todoTitle = ref('')
const todoDescription = ref('')
const todoStatus = ref(false)

const state = reactive({
  todos: [],
  todoContent: {}
})

const clearInput = () => {
  todoTitle.value = ''
  todoDescription.value = ''
  todoStatus.value = false
}

// Api
const path = "http://localhost:4123"
const getTodoList = async () => {
  if (state.todos.length > 0) state.todos.length = 0
  try {
    const res = await axios.get(path)
    for (const [index, value] of Object.entries(res.data)) {
      state.todos.push({
        id: value._id.$oid,
        completed: /^true$/i.test(value.completed),
        title: value.title,
        description: value.description,
        date_created: value.date_created,
      })
    }
  } catch (error) {
    console.error(`Error @getTodoList: ${error.message}`)
  }
}

const addTodo = async () => {
  try {
    await axios.post(`${path}/todo`, {
      title: todoTitle.value,
      description: todoDescription.value,
      completed: todoStatus.value
    })
    clearInput()
    generateAlert('Success', 'Todo successfully added!', 'success')
    getTodoList()
  } catch (error) {
    generateAlert('Oops...', 'Something went wrong!', 'error')
    console.error(`Error @addTodo: ${error.message}`)
  }
}

const getTodo = async (id) => {
  try {
    const res = await axios.get(`${path}/todo/${id}`)
    for (const [index, value] of Object.entries(res.data.data)) {
      state.todoContent[index] = value
    }
  } catch (error) {
    console.error(`Error @getTodo: ${error.message}`)
  }
}

const updateTodo = async (id) => {
  try {
    await axios.post(`${path}/todo/${id}`, {
      title: state.todoContent.title,
      description: state.todoContent.description,
      completed: state.todoContent.completed
    })
    generateAlert('Success', 'Todo successfully updated!', 'success')
    getTodoList()
  } catch (error) {
    generateAlert('Oops...', 'Something went wrong!', 'error')
    console.error(`Error @addTodo: ${error.message}`)
  }
}

const deleteTodo = async (id) => {
  try {
    const alertStatus = await Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    })
    if (alertStatus.isConfirmed) {
      await axios.post(`${path}/todo/${id}/delete`)
      generateAlert('Deleted!', 'Todo successfully deleted!', 'success')
      getTodoList()
    }
  } catch (error) {
    generateAlert('Oops...', 'Something went wrong!', 'error')
    console.error(`Error @addTodo: ${error.message}`)
  }
}

const generateAlert = (title, text, icon) => {
  Swal.fire({
    title: title,
    text: text,
    icon: icon,
    showConfirmButton: false,
    timer: 1500
  })
}

// Destructure reactive. instead of using 'state.todos'
const { todos, todoContent } = toRefs(state)

// Render todo list
getTodoList()
</script>

<template>
  <div class="container-fluid">
    <header>
      <h4>Todo List</h4>
      <button type="button" class="btn btn-outline-primary" data-bs-toggle="modal" data-bs-target="#addTodoModal">
        Add new todo
      </button>
    </header>

    <div>
      <div v-if="todos.length > 0" v-for="todo in todos" :key="todo.id">
        <Todo :data=todo :getTodo=getTodo :deleteTodo=deleteTodo v-bind="42" />
      </div>
      <div v-else class="empty-text">
        <p class="font-monospace text-center">You have no todos... 🎉</p>
        <p class="font-monospace text-center">Try adding one!</p>
      </div>
    </div>
  </div>

  <!-- Add Modal -->
  <div class="modal fade" id="addTodoModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title lead" id="exampleModalLabel">CREATE A TODO</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="addTodo()">
          <div class="modal-body">
            <div class="mb-3">
              <label for="todoTitle" class="form-label">What's on your todo list?</label>
              <input type="text" required v-model="todoTitle" class="form-control" id="todoTitle"
                placeholder="e.g. do homework">
            </div>
            <div class="mb-3">
              <label for="todoDescription" class="form-label">Todo description</label>
              <textarea class="form-control" v-model="todoDescription" required id="todoDescription" rows="3"
                placeholder="e.g. finish math and science homework" style="resize: none;"></textarea>
            </div>
            <div class="mb-3">
              <label for="todoStatus" class="form-label">Todo status</label>
              <select class="form-select" id="todoStatus" v-model="todoStatus">
                <option value="false">Pending</option>
                <option value="true">Done</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>

  <!-- Update Modal -->
  <div class="modal fade" id="updateTodoModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title lead" id="exampleModalLabel">UPDATE TODO</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>
        <form @submit.prevent="updateTodo(todoContent.id.$oid)">
          <div class="modal-body">
            <div class="mb-3">
              <label for="todoTitle" class="form-label">What's on your todo list?</label>
              <input type="text" required v-model="todoContent.title" class="form-control" id="todoTitle"
                placeholder="e.g. do homework">
            </div>
            <div class="mb-3">
              <label for="todoDescription" class="form-label">Todo description</label>
              <textarea class="form-control" v-model="todoContent.description" required id="todoDescription" rows="3"
                placeholder="e.g. finish math and science homework" style="resize: none;"></textarea>
            </div>
            <div class="mb-3">
              <label for="todoStatus" class="form-label">Todo status</label>
              <select class="form-select" id="todoStatus" v-model="todoContent.completed">
                <option value="false">Pending</option>
                <option value="true">Done</option>
              </select>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="submit" class="btn btn-primary" data-bs-dismiss="modal">Save changes</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>