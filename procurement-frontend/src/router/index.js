// 路由配置
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import Supplier from '../views/Supplier.vue'
import Material from '../views/Material.vue'
import Pricing from '../views/Pricing.vue'
import Contract from '../views/Contract.vue'
import Purchase from '../views/Purchase.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/supplier',
    name: 'Supplier',
    component: Supplier
  },
  {
    path: '/material',
    name: 'Material',
    component: Material
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: Pricing
  },
  {
    path: '/contract',
    name: 'Contract',
    component: Contract
  },
  {
    path: '/purchase',
    name: 'Purchase',
    component: Purchase
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
