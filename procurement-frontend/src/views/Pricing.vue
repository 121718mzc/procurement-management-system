<template>
  <div class="pricing-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>价格管理</span>
          <el-button type="primary" @click="handleAdd">添加价格</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="物料名称">
          <el-select v-model="searchForm.material_id" placeholder="请选择物料">
            <el-option
              v-for="material in materials"
              :key="material.id"
              :label="material.name"
              :value="String(material.id)">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="searchForm.supplier_id" placeholder="请选择供应商">
            <el-option
              v-for="supplier in suppliers"
              :key="supplier.id"
              :label="supplier.name"
              :value="String(supplier.id)">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="pricings" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="material_name" label="物料名称" width="150"></el-table-column>
        <el-table-column prop="supplier_name" label="供应商" width="150"></el-table-column>
        <el-table-column prop="price" label="价格" width="100"></el-table-column>
        <el-table-column prop="effective_date" label="生效日期" width="180"></el-table-column>
        <el-table-column prop="expiry_date" label="过期日期" width="180"></el-table-column>
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
      <el-form :model="pricingForm" :rules="pricingRules" ref="pricingFormRef" label-width="100px">
        <el-form-item label="物料" prop="material_id">
          <el-select v-model="pricingForm.material_id" placeholder="请选择物料">
            <el-option
              v-for="material in materials"
              :key="material.id"
              :label="material.name"
              :value="String(material.id)">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商" prop="supplier_id">
          <el-select v-model="pricingForm.supplier_id" placeholder="请选择供应商">
            <el-option
              v-for="supplier in suppliers"
              :key="supplier.id"
              :label="supplier.name"
              :value="String(supplier.id)">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input v-model.number="pricingForm.price" placeholder="请输入价格"></el-input>
        </el-form-item>
        <el-form-item label="生效日期" prop="effective_date">
          <el-date-picker v-model="pricingForm.effective_date" type="date" placeholder="请选择生效日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="过期日期" prop="expiry_date">
          <el-date-picker v-model="pricingForm.expiry_date" type="date" placeholder="请选择过期日期"></el-date-picker>
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
import { pricingService } from '../services/pricing'
import { formatDate, toNumber, toString } from '../utils'

export default {
  name: 'Pricing',
  setup() {
    const pricings = ref([])
    const loading = ref(false)
    const materials = ref([])
    const suppliers = ref([])
    
    const searchForm = reactive({
      material_id: '',
      supplier_id: ''
    })
    
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加价格')
    const pricingForm = reactive({
      id: '',
      material_id: '',
      supplier_id: '',
      price: 0,
      effective_date: '',
      expiry_date: ''
    })
    
    const pricingRules = {
      material_id: [
        { required: true, message: '请选择物料', trigger: 'blur' }
      ],
      supplier_id: [
        { required: true, message: '请选择供应商', trigger: 'blur' }
      ],
      price: [
        { required: true, message: '请输入价格', trigger: 'blur' },
        { type: 'number', message: '请输入数字', trigger: 'blur' },
        { validator: (rule, value, callback) => {
            if (value < 0) {
              callback(new Error('价格不能为负数'))
            } else {
              callback()
            }
          },
          trigger: 'blur'
        }
      ],
      effective_date: [
        { required: true, message: '请选择生效日期', trigger: 'blur' }
      ]
    }
    
    const pricingFormRef = ref(null)

    // 获取基础数据（物料和供应商列表）
    const getBaseData = async () => {
      try {
        const materialsRes = await pricingService.getMaterials()
        const suppliersRes = await pricingService.getSuppliers()
        materials.value = materialsRes.data.data || materialsRes.data || []
        suppliers.value = suppliersRes.data.data || suppliersRes.data || []
      } catch (error) {
        ElMessage.error('获取基础数据失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    // 获取价格列表
    const getPricings = async () => {
      loading.value = true
      try {
        const response = await pricingService.getPricings(currentPage.value, pageSize.value)
        pricings.value = response.data.data.map(item => ({
          ...item,
          material_name: materials.value.find(m => m.id === item.material_id)?.name || '未知物料',
          supplier_name: suppliers.value.find(s => s.id === item.supplier_id)?.name || '未知供应商'
        }))
        total.value = response.data.total
      } catch (error) {
        ElMessage.error('获取价格列表失败：' + (error.response?.data?.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    // 初始化数据
    onMounted(async () => {
      // 检查是否有token
      const token = localStorage.getItem('token')
      if (token) {
        await getBaseData()
        await getPricings()
      }
    })
    
    const handleAdd = () => {
      dialogTitle.value = '添加价格'
      Object.keys(pricingForm).forEach(key => {
        pricingForm[key] = ''
      })
      pricingForm.price = 0
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑价格'
      // 确保物料和供应商显示的是对应的ID，以便在下拉框中正确选择
      Object.assign(pricingForm, {
        ...row,
        material_id: String(row.material_id),
        supplier_id: String(row.supplier_id)
      })
      dialogVisible.value = true
    }
    
    const handleSubmit = async () => {
      if (!pricingFormRef.value) return
      
      pricingFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 日期格式化已在工具函数中实现
            
            const formData = {
              ...pricingForm,
              material_id: Number(pricingForm.material_id),
              supplier_id: Number(pricingForm.supplier_id),
              price: Number(pricingForm.price),
              effective_date: formatDate(pricingForm.effective_date),
              expiry_date: formatDate(pricingForm.expiry_date)
            }
            
            if (pricingForm.id) {
              // 编辑价格
              await pricingService.updatePricing(pricingForm.id, formData)
              ElMessage.success('价格更新成功')
            } else {
              // 添加价格
              await pricingService.addPricing(formData)
              ElMessage.success('价格添加成功')
            }
            dialogVisible.value = false
            getPricings() // 重新获取列表
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
        await pricingService.deletePricing(id)
        ElMessage.success('价格删除成功')
        getPricings() // 重新获取列表
      } catch (error) {
        ElMessage.error('删除失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    const handleSearch = async () => {
      loading.value = true
      try {
        const response = await pricingService.getPricings(currentPage.value, pageSize.value)
        let filteredPricings = response.data.data.map(item => ({
          ...item,
          material_name: materials.value.find(m => m.id === item.material_id)?.name || '未知物料',
          supplier_name: suppliers.value.find(s => s.id === item.supplier_id)?.name || '未知供应商'
        }))
        
        // 根据搜索条件过滤
        if (searchForm.material_id) {
          filteredPricings = filteredPricings.filter(pricing => 
            pricing.material_id == Number(searchForm.material_id)
          )
        }
        
        if (searchForm.supplier_id) {
          filteredPricings = filteredPricings.filter(pricing => 
            pricing.supplier_id == Number(searchForm.supplier_id)
          )
        }
        
        pricings.value = filteredPricings
        total.value = filteredPricings.length
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
      // 重新获取全部价格列表
      await getPricings()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      getPricings() // 重新获取列表
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      getPricings() // 重新获取列表
    }
    
    return {
      pricings,
      loading,
      materials,
      suppliers,
      searchForm,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      pricingForm,
      pricingRules,
      pricingFormRef,
      getBaseData,
      getPricings,
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
.pricing-container {
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
