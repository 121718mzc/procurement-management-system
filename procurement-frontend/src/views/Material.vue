<template>
  <div class="material-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>物料管理</span>
          <el-button type="primary" @click="handleAdd">添加物料</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="物料名称">
          <el-input v-model="searchForm.name" placeholder="请输入物料名称"></el-input>
        </el-form-item>
        <el-form-item label="物料编码">
          <el-input v-model="searchForm.code" placeholder="请输入物料编码"></el-input>
        </el-form-item>
        <el-form-item label="物料分类">
          <el-select v-model="searchForm.category_id" placeholder="请选择物料分类">
            <el-option label="生产原料" value="1"></el-option>
            <el-option label="电子元件" value="2"></el-option>
            <el-option label="包装材料" value="3"></el-option>
            <el-option label="办公耗材" value="4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="materials" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="code" label="物料编码" width="150"></el-table-column>
        <el-table-column prop="name" label="物料名称" width="200"></el-table-column>
        <el-table-column prop="specification" label="规格型号" width="200"></el-table-column>
        <el-table-column prop="unit" label="单位" width="80"></el-table-column>
        <el-table-column prop="category_name" label="物料分类" width="120"></el-table-column>
        <el-table-column prop="stock" label="库存" width="80"></el-table-column>
        <el-table-column prop="min_stock" label="最低库存" width="100"></el-table-column>
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
      <el-form :model="materialForm" :rules="materialRules" ref="materialFormRef" label-width="100px">
        <el-form-item label="物料编码" prop="code">
          <el-input v-model="materialForm.code" placeholder="请输入物料编码"></el-input>
        </el-form-item>
        <el-form-item label="物料名称" prop="name">
          <el-input v-model="materialForm.name" placeholder="请输入物料名称"></el-input>
        </el-form-item>
        <el-form-item label="规格型号" prop="specification">
          <el-input v-model="materialForm.specification" placeholder="请输入规格型号"></el-input>
        </el-form-item>
        <el-form-item label="单位" prop="unit">
          <el-input v-model="materialForm.unit" placeholder="请输入单位"></el-input>
        </el-form-item>
        <el-form-item label="物料分类" prop="category_id">
          <el-select v-model="materialForm.category_id" placeholder="请选择物料分类">
            <el-option label="生产原料" value="1"></el-option>
            <el-option label="电子元件" value="2"></el-option>
            <el-option label="包装材料" value="3"></el-option>
            <el-option label="办公耗材" value="4"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="库存" prop="stock">
          <el-input v-model.number="materialForm.stock" placeholder="请输入库存"></el-input>
        </el-form-item>
        <el-form-item label="最低库存" prop="min_stock">
          <el-input v-model.number="materialForm.min_stock" placeholder="请输入最低库存"></el-input>
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
import { materialService } from '../services/material'

export default {
  name: 'Material',
  setup() {
    const materials = ref([])
    const loading = ref(false)
    
    const searchForm = reactive({
      name: '',
      code: '',
      category_id: ''
    })
    
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加物料')
    const materialForm = reactive({
      id: '',
      code: '',
      name: '',
      specification: '',
      unit: '',
      category_id: '',
      stock: 0,
      min_stock: 0
    })
    
    const materialRules = {
      code: [
        { required: true, message: '请输入物料编码', trigger: 'blur' },
        { min: 3, max: 20, message: '物料编码长度应在3-20个字符之间', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入物料名称', trigger: 'blur' },
        { min: 2, max: 100, message: '物料名称长度应在2-100个字符之间', trigger: 'blur' }
      ],
      specification: [
        { required: true, message: '请输入规格型号', trigger: 'blur' },
        { min: 2, max: 100, message: '规格型号长度应在2-100个字符之间', trigger: 'blur' }
      ],
      unit: [
        { required: true, message: '请输入单位', trigger: 'blur' },
        { min: 1, max: 10, message: '单位长度应在1-10个字符之间', trigger: 'blur' }
      ],
      category_id: [
        { required: true, message: '请选择物料分类', trigger: 'change' }
      ],
      stock: [
        { required: true, message: '请输入库存', trigger: 'blur' },
        { type: 'number', message: '请输入数字', trigger: 'blur' },
        { validator: (rule, value, callback) => {
            if (value < 0) {
              callback(new Error('库存不能为负数'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      min_stock: [
        { required: true, message: '请输入最低库存', trigger: 'blur' },
        { type: 'number', message: '请输入数字', trigger: 'blur' },
        { validator: (rule, value, callback) => {
            if (value < 0) {
              callback(new Error('最低库存不能为负数'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ]
    }
    
    const materialFormRef = ref(null)
    
    // 获取物料列表
    const getMaterials = async () => {
      loading.value = true
      try {
        const response = await materialService.getMaterials(currentPage.value, pageSize.value)
        // 确保stock和min_stock字段是数字类型
        materials.value = response.data.data.map(item => ({
          ...item,
          stock: Number(item.stock),
          min_stock: Number(item.min_stock)
        }))
        total.value = response.data.total
      } catch (error) {
        ElMessage.error('获取物料列表失败：' + (error.response?.data?.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    // 初始化数据
    onMounted(() => {
      getMaterials()
    })
    
    const handleAdd = () => {
      dialogTitle.value = '添加物料'
      Object.keys(materialForm).forEach(key => {
        materialForm[key] = ''
      })
      materialForm.stock = 0
      materialForm.min_stock = 0
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑物料'
      // 确保stock和min_stock字段是数字类型
      Object.assign(materialForm, {
        ...row,
        stock: Number(row.stock),
        min_stock: Number(row.min_stock),
        category_id: String(row.category_id) // 确保category_id字段是字符串类型，与选项的value类型匹配
      })
      dialogVisible.value = true
    }
    
    const handleSubmit = async () => {
      if (!materialFormRef.value) return
      
      materialFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 确保stock和min_stock字段是整数类型
            const formData = {
              ...materialForm,
              stock: parseInt(materialForm.stock),
              min_stock: parseInt(materialForm.min_stock),
              category_id: Number(materialForm.category_id)
            }
            
            if (materialForm.id) {
              // 编辑物料
              await materialService.updateMaterial(materialForm.id, formData)
              ElMessage.success('物料更新成功')
            } else {
              // 添加物料
              await materialService.addMaterial(formData)
              ElMessage.success('物料添加成功')
            }
            dialogVisible.value = false
            getMaterials() // 重新获取列表
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
        await materialService.deleteMaterial(id)
        ElMessage.success('物料删除成功')
        getMaterials() // 重新获取列表
      } catch (error) {
        ElMessage.error('删除失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    const handleSearch = async () => {
      loading.value = true
      try {
        const response = await materialService.getMaterials(currentPage.value, pageSize.value)
        // 确保stock和min_stock字段是数字类型
        let filteredMaterials = response.data.data.map(item => ({
          ...item,
          stock: Number(item.stock),
          min_stock: Number(item.min_stock)
        }))
        
        // 根据搜索条件过滤
        if (searchForm.name) {
          filteredMaterials = filteredMaterials.filter(material => 
            material.name.toLowerCase().includes(searchForm.name.toLowerCase())
          )
        }
        
        if (searchForm.code) {
          filteredMaterials = filteredMaterials.filter(material => 
            material.code.toLowerCase().includes(searchForm.code.toLowerCase())
          )
        }
        
        if (searchForm.category_id) {
          filteredMaterials = filteredMaterials.filter(material => 
            material.category_id == Number(searchForm.category_id)
          )
        }
        
        materials.value = filteredMaterials
        total.value = filteredMaterials.length
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
      // 重新获取全部物料列表
      await getMaterials()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      getMaterials() // 重新获取列表
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      getMaterials() // 重新获取列表
    }
    
    return {
      materials,
      loading,
      searchForm,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      materialForm,
      materialRules,
      materialFormRef,
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
.material-container {
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
