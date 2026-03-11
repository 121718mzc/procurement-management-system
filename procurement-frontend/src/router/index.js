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
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/supplier',
    name: 'Supplier',
    component: Supplier,
    meta: { requiresAuth: true }
  },
  {
    path: '/material',
    name: 'Material',
    component: Material,
    meta: { requiresAuth: true }
  },
  {
    path: '/pricing',
    name: 'Pricing',
    component: Pricing,
    meta: { requiresAuth: true }
  },
  {
    path: '/contract',
    name: 'Contract',
    component: Contract,
    meta: { requiresAuth: true }
  },
  {
    path: '/purchase',
    name: 'Purchase',
    component: Purchase,
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 检查是否有token
    const token = localStorage.getItem('token')
    if (!token) {
      // 没有token，重定向到登录页
      next({ name: 'Login' })
    } else {
      // 有token，继续访问
      next()
    }
  } else {
    // 不需要认证的路由，直接访问
    next()
  }
})

export default router
