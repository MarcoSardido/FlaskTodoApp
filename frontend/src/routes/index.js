import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: () => import('../views/Home.vue')
    },
    {
        path: '/user',
        name: 'Users',
        component: () => import('../views/UsersView.vue')
    },
    {
        path: '/user/:id',
        name: 'User',
        component: () => import('../views/User.vue')
    },
    {
        path: '/about',
        name: 'About',
        component: () => import('../views/About.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes
  })

export default router