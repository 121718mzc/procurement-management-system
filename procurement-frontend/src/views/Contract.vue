<template>
  <div class="contract-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>合同管理</span>
          <el-button type="primary" @click="handleAdd">添加合同</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="合同编号">
          <el-input v-model="searchForm.contract_number" placeholder="请输入合同编号"></el-input>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="searchForm.supplier_id" placeholder="请选择供应商">
            <el-option label="供应商A" value="1"></el-option>
            <el-option label="供应商B" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="合同类型">
          <el-select v-model="searchForm.type_id" placeholder="请选择合同类型">
            <el-option label="NDA保密协议" value="1"></el-option>
            <el-option label="多物品采购合同" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="contracts" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="contract_number" label="合同编号" width="180"></el-table-column>
        <el-table-column prop="title" label="合同标题" width="200"></el-table-column>
        <el-table-column prop="supplier_name" label="供应商" width="150"></el-table-column>
        <el-table-column prop="type_name" label="合同类型" width="120"></el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="150"></el-table-column>
        <el-table-column prop="end_date" label="结束日期" width="150"></el-table-column>
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'signed' ? 'success' : scope.row.status === 'draft' ? 'warning' : 'danger'">
              {{ scope.row.status === 'signed' ? '已签署' : scope.row.status === 'draft' ? '草稿' : '已过期' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleExport(scope.row.id)">导出PDF</el-button>
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
      width="600px"
    >
      <el-form :model="contractForm" :rules="contractRules" ref="contractFormRef" label-width="100px">
        <el-form-item label="合同编号" prop="contract_number">
          <el-input v-model="contractForm.contract_number" placeholder="请输入合同编号"></el-input>
        </el-form-item>
        <el-form-item label="合同标题">
          <el-input v-model="contractForm.title" placeholder="请输入合同标题"></el-input>
        </el-form-item>
        <el-form-item label="合同类型" prop="type_id">
          <el-select v-model="contractForm.type_id" placeholder="请选择合同类型">
            <el-option label="NDA保密协议" value="1"></el-option>
            <el-option label="多物品采购合同" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商" prop="supplier_id">
          <el-select v-model="contractForm.supplier_id" placeholder="请选择供应商">
            <el-option label="供应商A" value="1"></el-option>
            <el-option label="供应商B" value="2"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="contractForm.start_date" type="date" placeholder="请选择开始日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="contractForm.end_date" type="date" placeholder="请选择结束日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="合同内容">
          <el-input v-model="contractForm.content" type="textarea" placeholder="请输入合同内容" :rows="5"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="contractForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft"></el-option>
            <el-option label="已签署" value="signed"></el-option>
            <el-option label="已过期" value="expired"></el-option>
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
import { contractService } from '../services/contract'

export default {
  name: 'Contract',
  setup() {
    const contracts = ref([])
    const loading = ref(false)
    
    const searchForm = reactive({
      contract_number: '',
      supplier_id: '',
      type_id: ''
    })
    
    const currentPage = ref(1)
    const pageSize = ref(10)
    const total = ref(0)
    
    const dialogVisible = ref(false)
    const dialogTitle = ref('添加合同')
    const contractForm = reactive({
      id: '',
      contract_number: '',
      title: '',
      type_id: '',
      supplier_id: '',
      content: '',
      start_date: '',
      end_date: '',
      status: 'draft'
    })
    
    const contractRules = {
      contract_number: [
        { required: true, message: '请输入合同编号', trigger: 'blur' }
      ],
      type_id: [
        { required: true, message: '请选择合同类型', trigger: 'blur' }
      ],
      supplier_id: [
        { required: true, message: '请选择供应商', trigger: 'blur' }
      ],
      start_date: [
        { required: true, message: '请选择开始日期', trigger: 'blur' }
      ]
    }
    
    const contractFormRef = ref(null)
    
    // 获取合同列表
    const getContracts = async () => {
      loading.value = true
      try {
        const response = await contractService.getContracts(currentPage.value, pageSize.value)
        // 模拟供应商和合同类型名称
        const supplierMap = {
          1: '供应商A',
          2: '供应商B'
        }
        const typeMap = {
          'NDA': 'NDA保密协议',
          'Purchase': '多物品采购合同'
        }
        // 转换合同类型格式
        const transformedContracts = response.data.data.map(contract => {
          // 转换合同类型
          let type_id = 1
          let type_name = 'NDA保密协议'
          if (contract.contract_type === 'Purchase') {
            type_id = 2
            type_name = '多物品采购合同'
          }
          
          return {
            ...contract,
            title: contract.title || contract.contract_number, // 使用合同标题，如果没有则使用合同编号
            type_id: type_id,
            type_name: type_name,
            supplier_name: supplierMap[contract.supplier_id] || '未知供应商',
            content: contract.content || '合同内容...' // 使用合同内容，如果没有则使用默认值
          }
        })
        contracts.value = transformedContracts
        total.value = response.data.total
      } catch (error) {
        ElMessage.error('获取合同列表失败：' + (error.response?.data?.message || '未知错误'))
      } finally {
        loading.value = false
      }
    }
    
    // 初始化数据
    onMounted(() => {
      getContracts()
    })
    
    const handleAdd = () => {
      dialogTitle.value = '添加合同'
      Object.keys(contractForm).forEach(key => {
        contractForm[key] = ''
      })
      contractForm.status = 'Active'
      dialogVisible.value = true
    }
    
    const handleEdit = (row) => {
      dialogTitle.value = '编辑合同'
      // 确保类型和供应商ID是字符串，以便在下拉框中正确显示
      Object.assign(contractForm, {
        ...row,
        type_id: String(row.type_id),
        supplier_id: String(row.supplier_id)
      })
      dialogVisible.value = true
    }
    
    const handleSubmit = async () => {
      if (!contractFormRef.value) return
      
      contractFormRef.value.validate(async (valid) => {
        if (valid) {
          loading.value = true
          try {
            // 格式化日期为YYYY-MM-DD格式
            const formatDate = (date) => {
              if (!date) return date
              const d = new Date(date)
              return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
            }
            
            // 转换合同类型
            let contract_type = 'NDA'
            if (contractForm.type_id === '2') {
              contract_type = 'Purchase'
            }
            
            const formData = {
              supplier_id: Number(contractForm.supplier_id),
              contract_number: contractForm.contract_number,
              contract_type: contract_type,
              start_date: formatDate(contractForm.start_date),
              end_date: formatDate(contractForm.end_date),
              status: contractForm.status,
              title: contractForm.title,
              content: contractForm.content
            }
            console.log('提交的合同数据:', formData)
            
            if (contractForm.id) {
              // 编辑合同
              await contractService.updateContract(contractForm.id, formData)
              ElMessage.success('合同更新成功')
            } else {
              // 添加合同
              await contractService.addContract(formData)
              ElMessage.success('合同添加成功')
            }
            dialogVisible.value = false
            getContracts() // 重新获取列表
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
        await contractService.deleteContract(id)
        ElMessage.success('合同删除成功')
        getContracts() // 重新获取列表
      } catch (error) {
        ElMessage.error('删除失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    const handleExport = async (id) => {
      try {
        const response = await contractService.exportContract(id)
        // 创建下载链接
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `contract_${id}.pdf`)
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        ElMessage.success('PDF导出成功')
      } catch (error) {
        ElMessage.error('导出失败：' + (error.response?.data?.message || '未知错误'))
      }
    }
    
    const handleSearch = async () => {
      loading.value = true
      try {
        const response = await contractService.getContracts(currentPage.value, pageSize.value)
        // 模拟供应商和合同类型名称
        const supplierMap = {
          1: '供应商A',
          2: '供应商B'
        }
        const typeMap = {
          'NDA': 'NDA保密协议',
          'Purchase': '多物品采购合同'
        }
        // 转换合同类型格式
        let filteredContracts = response.data.data.map(contract => {
          // 转换合同类型
          let type_id = 1
          let type_name = 'NDA保密协议'
          if (contract.contract_type === 'Purchase') {
            type_id = 2
            type_name = '多物品采购合同'
          }
          
          return {
            ...contract,
            title: contract.title || contract.contract_number, // 使用合同标题，如果没有则使用合同编号
            type_id: type_id,
            type_name: type_name,
            supplier_name: supplierMap[contract.supplier_id] || '未知供应商',
            content: contract.content || '合同内容...' // 使用合同内容，如果没有则使用默认值
          }
        })
        
        // 根据搜索条件过滤
        if (searchForm.contract_number) {
          filteredContracts = filteredContracts.filter(contract => 
            contract.contract_number.toLowerCase().includes(searchForm.contract_number.toLowerCase())
          )
        }
        
        if (searchForm.supplier_id) {
          filteredContracts = filteredContracts.filter(contract => 
            contract.supplier_id == Number(searchForm.supplier_id)
          )
        }
        
        if (searchForm.type_id) {
          filteredContracts = filteredContracts.filter(contract => 
            contract.type_id == Number(searchForm.type_id)
          )
        }
        
        contracts.value = filteredContracts
        total.value = filteredContracts.length
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
      // 重新获取全部合同列表
      await getContracts()
    }
    
    const handleSizeChange = (size) => {
      pageSize.value = size
      getContracts() // 重新获取列表
    }
    
    const handleCurrentChange = (current) => {
      currentPage.value = current
      getContracts() // 重新获取列表
    }
    
    return {
      contracts,
      loading,
      searchForm,
      currentPage,
      pageSize,
      total,
      dialogVisible,
      dialogTitle,
      contractForm,
      contractRules,
      contractFormRef,
      getContracts,
      handleAdd,
      handleEdit,
      handleSubmit,
      handleDelete,
      handleExport,
      handleSearch,
      resetSearch,
      handleSizeChange,
      handleCurrentChange
    }
  }
}
</script>

<style scoped>
.contract-container {
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