<template>
  <div id="app">
    <template v-if="$route.name !== 'Login'">
      <el-container style="height: 100vh;">
        <el-header height="60px" style="background-color: #333; color: white; display: flex; align-items: center; padding: 0 20px;">
          <h1 style="margin: 0; font-size: 20px;">采购管理系统</h1>
          <div style="flex: 1;"></div>
          <el-button type="primary" @click="logout">退出登录</el-button>
        </el-header>
        <el-container>
          <el-aside width="200px" style="background-color: #f0f2f5;">
            <el-menu :default-active="activeMenu" class="el-menu-vertical-demo" @select="handleMenuSelect">
              <el-menu-item index="/">
                <el-icon><House /></el-icon>
                <span>首页</span>
              </el-menu-item>
              <el-menu-item index="/supplier">
                <el-icon><UserFilled /></el-icon>
                <span>供应商管理</span>
              </el-menu-item>
              <el-menu-item index="/material">
                <el-icon><Goods /></el-icon>
                <span>物料管理</span>
              </el-menu-item>
              <el-menu-item index="/pricing">
                <el-icon><Money /></el-icon>
                <span>价格管理</span>
              </el-menu-item>
              <el-menu-item index="/contract">
                <el-icon><Document /></el-icon>
                <span>合同管理</span>
              </el-menu-item>
              <el-menu-item index="/purchase">
                <el-icon><ShoppingCart /></el-icon>
                <span>采购订单</span>
              </el-menu-item>
            </el-menu>
          </el-aside>
          <el-main>
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </template>
    <template v-else>
      <router-view />
    </template>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { House, UserFilled, Goods, Money, Document, ShoppingCart } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    House,
    UserFilled,
    Goods,
    Money,
    Document,
    ShoppingCart
  },
  setup() {
    const router = useRouter()
    const activeMenu = ref('/')

    const handleMenuSelect = (key, keyPath) => {
      router.push(key)
    }

    const logout = () => {
      // 清除登录状态
      localStorage.removeItem('token')
      router.push('/login')
    }

    onMounted(() => {
      // 检查登录状态
      const token = localStorage.getItem('token')
      if (!token && router.currentRoute.value.name !== 'Login') {
        router.push('/login')
      }
    })

    return {
      activeMenu,
      handleMenuSelect,
      logout
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
}

.el-aside {
  position: fixed;
  left: 0;
  top: 60px;
  bottom: 0;
  z-index: 99;
}

.el-main {
  margin-left: 200px;
  margin-top: 60px;
  min-height: calc(100vh - 60px);
  padding: 20px;
}
</style>
