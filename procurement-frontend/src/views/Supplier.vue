<template>
  <div class="supplier-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>供应商管理</span>
          <el-button type="primary" @click="handleAdd">添加供应商</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="供应商名称">
          <el-input v-model="searchForm.name" placeholder="请输入供应商名称"></el-input>
        </el-form-item>
        <el-form-item label="联系人">
          <el-input v-model="searchForm.contact_person" placeholder="请输入联系人"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="suppliers" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="name" label="供应商名称" width="200"></el-table-column>
        <el-table-column prop="contact_person" label="联系人" width="120"></el-table-column>
        <el-table-column prop="phone" label="联系电话" width="150"></el-table-column>
        <el-table-column prop="email" label="邮箱" width="200"></el-table-column>
        <el-table-column prop="address" label="地址"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'active' ? 'success' : 'danger'">{{ scope.row.status === 'active' ? '活跃' : '停用' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div class="pagination-container">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[10, 20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </div>
    </el-card>
    
    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
    >
      <el-form :model="supplierForm" :rules="supplierRules" ref="supplierFormRef" label-width="100px">
        <el-form-item label="供应商名称" prop="name">
          <el-input v-model="supplierForm.name" placeholder="请输入供应商名称"></el-input>
        </el-form-item>
        <el-form-item label="联系人" prop="contact_person">
          <el-input v-model="supplierForm.contact_person" placeholder="请输入联系人"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="supplierForm.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="supplierForm.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="supplierForm.address" type="textarea" placeholder="请输入地址"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="supplierForm.status" placeholder="请选择状态">
            <el-option label="活跃" value="active"></el-option>
            <el-option label="停用" value="inactive"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { supplierService } from '../services/supplier'

export default {
  name: 'Supplier',
  setup() {
    const suppliers = ref([])
    const loading = ref(false)
    
    const searchForm = reactive({
      name: '',
      contact_person: ''
    })
    
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加供应商')
    const supplierForm = reactive({
      id: '',
      name: '',
      contact_person: '',
      phone: '',
      email: '',
      address: '',
      status: 'active'
    })
    
    const supplierRules = {
      name: [
        { required: true, message: '请输入供应商名称', trigger: 'blur' },
        { min: 2, max: 100, message: '供应商名称长度应在2-100个字符之间', trigger: 'blur' }
      ],
      contact_person: [
        { required: true, message: '请输入联系人', trigger: 'blur' },
        { min: 2, max: 50, message: '联系人姓名长度应在2-50个字符之间', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入联系电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码格式', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
      ],
      address: [
        { required: true, message: '请输入地址', trigger: 'blur' },
        { min: 5, max: 200, message: '地址长度应在5-200个字符之间', trigger: 'blur' }
      ],
      status: [
        { required: true, message: '请选择状态', trigger: 'change' }
      ]
    }
    
    const supplierFormRef = ref(null)
    
    // 获取供应商列表
    const getSuppliers = async () => {
      loading.value = true
      try {
        const response = await supplierService.getSuppliers(currentPage.value, pageSize.value)
        suppliers.value = response.data.data
        total.value = response.data.total
      } catch (error) {
        ElMessage.error('获取供应商列表失败：' + (error.response?.data?.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    // 初始化数据
    onMounted(() => {
      // 检查是否有token
      const token = localStorage.getItem('token')
      if (token) {
        getSuppliers()
      }
    })
    
    const handleAdd = () => {
      dialogTitle.value = '添加供应商'
      Object.keys(supplierForm).forEach(key => {
        supplierForm[key] = ''
      })
      supplierForm.status = 'active'
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑供应商'
      Object.assign(supplierForm, row)
      dialogVisible.value = true
    }
    
    const handleSubmit = async () => {
      if (!supplierFormRef.value) return
      
      supplierFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            if (supplierForm.id) {
              // 编辑供应商
              await supplierService.updateSupplier(supplierForm.id, supplierForm)
              ElMessage.success('供应商更新成功')
            } else {
              // 添加供应商
              await supplierService.addSupplier(supplierForm)
              ElMessage.success('供应商添加成功')
            }
            dialogVisible.value = false
            getSuppliers() // 重新获取列表
          } catch (error) {
            ElMessage.error('操作失败：' + (error.response?.data?.message || '未知错误'))
          } finally {
            loading.value = false
          }
        }
      })
    }
    
    const handleDelete = async (id) => {
      try {
        await supplierService.deleteSupplier(id)
        ElMessage.success('供应商删除成功')
        getSuppliers() // 重新获取列表
      } catch (error) {
        ElMessage.error('删除失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    const handleSearch = async () => {
      loading.value = true
      try {
        const response = await supplierService.getSuppliers(currentPage.value, pageSize.value)
        let filteredSuppliers = response.data.data
        
        // 根据搜索条件过滤
        if (searchForm.name) {
          filteredSuppliers = filteredSuppliers.filter(supplier => 
            supplier.name.toLowerCase().includes(searchForm.name.toLowerCase())
          )
        }
        
        if (searchForm.contact_person) {
          filteredSuppliers = filteredSuppliers.filter(supplier => 
            supplier.contact_person.toLowerCase().includes(searchForm.contact_person.toLowerCase())
          )
        }
        
        suppliers.value = filteredSuppliers
        total.value = filteredSuppliers.length
      } catch (error) {
        ElMessage.error('搜索失败：' + (error.response?.data?.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    const resetSearch = async () => {
      Object.keys(searchForm).forEach(key => {
        searchForm[key] = ''
      })
      // 重新获取全部供应商列表
      await getSuppliers()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      getSuppliers() // 重新获取列表
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      getSuppliers() // 重新获取列表
    }
    
    return {
      suppliers,
      loading,
      searchForm,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      supplierForm,
      supplierRules,
      supplierFormRef,
      handleAdd,
      handleEdit,
      handleSubmit,
      handleDelete,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.supplier-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
