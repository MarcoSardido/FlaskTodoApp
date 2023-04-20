<script setup>
const props = defineProps(['data', 'getTodo', 'deleteTodo', 'test'])

// allows for easier access to the properties within the component's template and methods.
const { id, title, description, date_created, completed } = props.data

const getTodo = async () => props.getTodo(id)
const deleteTodo = () => props.deleteTodo(id)
</script>

<template>
    <div class="todo">
        <div class="card my-2">
            <div class="card-header">
                <span>{{ date_created }}</span>
                <span class="badge rounded-pill bg-success" v-if="completed">Done</span>
                <span class="badge rounded-pill bg-warning" v-else>Pending</span>
            </div>
            <div class="card-body">
                <h5 class="card-title" v-if="completed" style="text-decoration: line-through;"><del>{{ title }}</del></h5>
                <h5 class="card-title" v-else>{{ title }}</h5>
                <p class="card-text">{{ description }}</p>
                <button @click="getTodo" type="button" class="btn btn-warning me-2" data-bs-toggle="modal"
                    data-bs-target="#updateTodoModal">Update</button>
                <button @click="deleteTodo" type="button" class="btn btn-danger">Delete</button>
            </div>
        </div>
    </div>
</template>