import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../pages/HomePage.vue'
import DtpPage from '../pages/DtpPage.vue'
import AddDtpPage from '../pages/AddDtpPage.vue'

const routes = [
  { path: '/', component: HomePage },
  { path: '/dtp', component: DtpPage },
  { path: '/add', component: AddDtpPage }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 