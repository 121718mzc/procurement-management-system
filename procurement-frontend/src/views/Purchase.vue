<template>
  <div class="purchase-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>采购订单管理</span>
          <el-button type="primary" @click="handleAdd">添加采购订单</el-button>
        </div>
      </template>
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="订单编号">
          <el-input v-model="searchForm.order_number" placeholder="请输入订单编号"></el-input>
        </el-form-item>
        <el-form-item label="供应商">
          <el-select v-model="searchForm.supplier_id" placeholder="请选择供应商">
            <el-option v-for="supplier in suppliers" :key="supplier.id" :label="supplier.name" :value="supplier.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft"></el-option>
            <el-option label="已发送" value="sent"></el-option>
            <el-option label="已接收" value="received"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="待处理" value="pending"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">搜索</el-button>
          <el-button @click="resetSearch">重置</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="purchaseOrders" style="width: 100%;">
        <el-table-column prop="id" label="ID" width="80"></el-table-column>
        <el-table-column prop="order_number" label="订单编号" width="180"></el-table-column>
        <el-table-column prop="supplier_id" label="供应商" width="150">
          <template #default="scope">
            {{ getSupplierName(scope.row.supplier_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getTagType(scope.row.status)">{{ getStatusText(scope.row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180"></el-table-column>
        <el-table-column label="操作" width="200">
          <template #default="scope">
            <el-button type="primary" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="success" size="small" @click="handleView(scope.row)">查看详情</el-button>
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
      <el-form :model="purchaseForm" :rules="purchaseRules" ref="purchaseFormRef" label-width="100px">
        <el-form-item label="订单编号" prop="order_number">
          <el-input v-model="purchaseForm.order_number" placeholder="请输入订单编号"></el-input>
        </el-form-item>
        <el-form-item label="合同" prop="contract_id">
          <el-select v-model="purchaseForm.contract_id" placeholder="请选择合同">
            <el-option v-for="contract in contracts" :key="contract.id" :label="contract.contract_number" :value="contract.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="供应商" prop="supplier_id">
          <el-select v-model="purchaseForm.supplier_id" placeholder="请选择供应商">
            <el-option v-for="supplier in suppliers" :key="supplier.id" :label="supplier.name" :value="supplier.id"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="订单日期" prop="order_date">
          <el-date-picker
            v-model="purchaseForm.order_date"
            type="date"
            placeholder="选择订单日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="交付日期" prop="delivery_date">
          <el-date-picker
            v-model="purchaseForm.delivery_date"
            type="date"
            placeholder="选择交付日期"
            style="width: 100%"
          ></el-date-picker>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="purchaseForm.status" placeholder="请选择状态">
            <el-option label="草稿" value="draft"></el-option>
            <el-option label="已发送" value="sent"></el-option>
            <el-option label="已接收" value="received"></el-option>
            <el-option label="已完成" value="completed"></el-option>
            <el-option label="已取消" value="cancelled"></el-option>
            <el-option label="待处理" value="pending"></el-option>
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
import { purchaseService } from '../services/purchase';
import { supplierService } from '../services/supplier';
import { contractService } from '../services/contract';
import { formatDate, parseDate, toNumber, toString, debounce } from '../utils';

export default {
  name: 'Purchase',
  data() {
    return {
      purchaseOrders: [],
      suppliers: [],
      contracts: [],
      searchForm: {
        order_number: '',
        supplier_id: '',
        status: ''
      },
      currentPage: 1,
      pageSize: 10,
      total: 0,
      dialogVisible: false,
      dialogTitle: '添加采购订单',
      purchaseForm: {
        id: '',
        order_number: '',
        contract_id: '',
        supplier_id: '',
        order_date: '',
        delivery_date: '',
        status: 'pending'
      },
      purchaseRules: {
        order_number: [
          { required: true, message: '请输入订单编号', trigger: 'blur' }
        ],
        contract_id: [
          { required: true, message: '请选择合同', trigger: 'blur' }
        ],
        supplier_id: [
          { required: true, message: '请选择供应商', trigger: 'blur' }
        ],
        order_date: [
          { required: true, message: '请选择订单日期', trigger: 'blur' }
        ],
        delivery_date: [
          { required: true, message: '请选择交付日期', trigger: 'blur' }
        ]
      },
      loading: false
    }
  },
  mounted() {
    // 检查是否有token
    const token = localStorage.getItem('token');
    if (token) {
      this.getPurchaseOrders();
      this.getSuppliers();
      this.getContracts();
    }
  },
  methods: {
    // debounce函数已在工具函数中实现,
    getTagType(status) {
      switch (status) {
        case 'completed': return 'success'
        case 'sent': return 'warning'
        case 'received': return 'info'
        case 'cancelled': return 'danger'
        case 'pending': return 'warning'
        default: return 'info'
      }
    },
    getStatusText(status) {
      switch (status) {
        case 'draft': return '草稿'
        case 'sent': return '已发送'
        case 'received': return '已接收'
        case 'completed': return '已完成'
        case 'cancelled': return '已取消'
        case 'pending': return '待处理'
        default: return status
      }
    },
    getSupplierName(supplierId) {
      if (!supplierId) return '';
      const supplier = this.suppliers.find(s => s.id === supplierId);
      return supplier ? supplier.name : supplierId;
    },
    getPurchaseOrders() {
      if (this.loading) return;
      this.loading = true;
      
      const params = {
        page: this.currentPage,
        per_page: this.pageSize
      };
      if (this.searchForm.order_number) {
        params.order_number = this.searchForm.order_number;
      }
      if (this.searchForm.supplier_id) {
        params.supplier_id = this.searchForm.supplier_id;
      }
      if (this.searchForm.status) {
        params.status = this.searchForm.status;
      }
      
      purchaseService.getPurchaseOrders(params)
        .then(response => {
          console.log('采购订单API响应:', response);
          if (response && response.data) {
            if (response.data.error) {
              this.$message.error(response.data.error);
              return;
            }
            this.purchaseOrders = response.data.data;
            this.total = response.data.total;
            console.log('采购订单数据:', this.purchaseOrders);
          } else {
            this.purchaseOrders = [];
            this.total = 0;
            console.log('无采购订单数据');
          }
        })
        .catch(error => {
          console.error('获取采购订单失败:', error);
          this.$message.error('获取采购订单失败');
          this.purchaseOrders = [];
          this.total = 0;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    getSuppliers() {
      supplierService.getSuppliers()
        .then(response => {
          if (response && response.data && response.data.data) {
            this.suppliers = response.data.data;
          }
        })
        .catch(error => {
          console.error('获取供应商失败:', error);
        });
    },
    getContracts() {
      contractService.getContracts()
        .then(response => {
          if (response && response.data && response.data.data) {
            this.contracts = response.data.data;
          }
        })
        .catch(error => {
          console.error('获取合同失败:', error);
        });
    },
    handleAdd() {
      this.dialogTitle = '添加采购订单'
      this.purchaseForm = {
        id: '',
        order_number: '',
        contract_id: '',
        supplier_id: '',
        order_date: '',
        delivery_date: '',
        status: 'pending'
      }
      this.dialogVisible = true
    },
    handleEdit(row) {
      if (!row) return;
      this.dialogTitle = '编辑采购订单'
      this.purchaseForm = { ...row }
      // 转换日期格式
      if (row.order_date) {
        this.purchaseForm.order_date = parseDate(row.order_date);
      }
      if (row.delivery_date) {
        this.purchaseForm.delivery_date = parseDate(row.delivery_date);
      }
      this.dialogVisible = true
    },
    handleSubmit() {
      if (!this.$refs.purchaseFormRef) return;
      this.$refs.purchaseFormRef.validate((valid) => {
        if (valid) {
          const formData = { ...this.purchaseForm };
          // 转换日期格式
          if (formData.order_date) {
            formData.order_date = formatDate(formData.order_date);
          }
          if (formData.delivery_date) {
            formData.delivery_date = formatDate(formData.delivery_date);
          }
          
          if (formData.id) {
            // 更新采购订单
            purchaseService.updatePurchaseOrder(formData.id, formData)
              .then(response => {
                this.$message.success('更新成功');
                this.dialogVisible = false;
                this.getPurchaseOrders();
              })
              .catch(error => {
                console.error('更新采购订单失败:', error);
                this.$message.error('更新采购订单失败');
              });
          } else {
            // 添加采购订单
            purchaseService.addPurchaseOrder(formData)
              .then(response => {
                this.$message.success('添加成功');
                this.dialogVisible = false;
                this.getPurchaseOrders();
              })
              .catch(error => {
                console.error('添加采购订单失败:', error);
                this.$message.error('添加采购订单失败');
              });
          }
        }
      });
    },
    handleDelete(id) {
      if (!id) return;
      this.$confirm('确定要删除这个采购订单吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        purchaseService.deletePurchaseOrder(id)
          .then(response => {
            this.$message.success('删除成功');
            this.getPurchaseOrders();
          })
          .catch(error => {
            console.error('删除采购订单失败:', error);
            this.$message.error('删除采购订单失败');
          });
      }).catch(() => {
        // 取消删除
      });
    },
    handleView(row) {
      // 查看详情
      this.$message.info('查看详情功能开发中');
    },
    handleSearch() {
      // 搜索功能
      if (this.loading) return;
      this.loading = true;
      
      const params = {
        page: this.currentPage,
        per_page: this.pageSize
      };
      if (this.searchForm.order_number) {
        params.order_number = this.searchForm.order_number;
      }
      if (this.searchForm.supplier_id) {
        params.supplier_id = this.searchForm.supplier_id;
      }
      if (this.searchForm.status) {
        params.status = this.searchForm.status;
      }
      
      purchaseService.getPurchaseOrders(params)
        .then(response => {
          if (response && response.data) {
            if (response.data.error) {
              this.$message.error(response.data.error);
              return;
            }
            this.purchaseOrders = response.data.data;
            this.total = response.data.total;
          } else {
            this.$message.error('搜索结果为空');
            this.purchaseOrders = [];
            this.total = 0;
          }
        })
        .catch(error => {
          console.error('搜索采购订单失败:', error);
          this.$message.error('搜索采购订单失败');
          this.purchaseOrders = [];
          this.total = 0;
        })
        .finally(() => {
          this.loading = false;
        });
    },
    resetSearch() {
      this.searchForm = {
        order_number: '',
        supplier_id: '',
        status: ''
      }
      this.getPurchaseOrders()
    },
    handleSizeChange(size) {
      this.pageSize = size
    },
    handleCurrentChange(current) {
      this.currentPage = current
    }
  }
}
</script>

<style scoped>
.purchase-container {
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