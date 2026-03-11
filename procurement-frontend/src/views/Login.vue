<template>
  <div class="login-container">
    <div class="login-form">
      <h2>采购管理系统登录</h2>
      <el-form :model="loginForm" :rules="loginRules" ref="loginFormRef" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading" style="width: 100%;">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { userService } from '../services/user'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const loginFormRef = ref(null)
    const loading = ref(false)
    
    const loginForm = reactive({
      username: 'buyer',
      password: '123456'
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      loginFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            console.log('Login form:', loginForm)
            const response = await userService.login(loginForm)
            console.log('Login response:', response)
            if (response.data && response.data.token) {
              ElMessage.success('登录成功')
              localStorage.setItem('token', response.data.token)
              console.log('Token stored:', response.data.token)
              // 立即检查token是否存储成功
              const storedToken = localStorage.getItem('token')
              console.log('Token in localStorage after storage:', storedToken)
              router.push('/')
            } else {
              ElMessage.error('登录失败：未返回token')
              console.error('No token in response:', response)
            }
          } catch (error) {
            console.log('Login error:', error)
            ElMessage.error('登录失败：' + (error.response?.data?.message || '未知错误'))
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    return {
      loginForm,
      loginRules,
      loginFormRef,
      handleLogin,
      loading
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f7fa;
}

.login-form {
  width: 400px;
  padding: 30px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.login-form h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #303133;
}
</style>
