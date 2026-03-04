<template>
  <div class="home-container">
    <el-card shadow="hover">
      <template #header>
        <div class="card-header">
          <span>系统概览</span>
        </div>
      </template>
      <div class="dashboard">
        <el-row :gutter="20">
          <el-col :span="6">
            <el-card class="dashboard-card">
              <div class="dashboard-item">
                <el-icon class="dashboard-icon"><UserFilled /></el-icon>
                <div class="dashboard-content">
                  <div class="dashboard-title">供应商数量</div>
                  <div class="dashboard-value">10</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="dashboard-card">
              <div class="dashboard-item">
                <el-icon class="dashboard-icon"><Goods /></el-icon>
                <div class="dashboard-content">
                  <div class="dashboard-title">物料数量</div>
                  <div class="dashboard-value">50</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="dashboard-card">
              <div class="dashboard-item">
                <el-icon class="dashboard-icon"><Document /></el-icon>
                <div class="dashboard-content">
                  <div class="dashboard-title">合同数量</div>
                  <div class="dashboard-value">5</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :span="6">
            <el-card class="dashboard-card">
              <div class="dashboard-item">
                <el-icon class="dashboard-icon"><ShoppingCart /></el-icon>
                <div class="dashboard-content">
                  <div class="dashboard-title">采购订单</div>
                  <div class="dashboard-value">15</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </el-card>
    
    <el-card shadow="hover" style="margin-top: 20px;">
      <template #header>
        <div class="card-header">
          <span>最近活动</span>
        </div>
      </template>
      <el-table :data="recentActivities" style="width: 100%;">
        <el-table-column prop="time" label="时间" width="180"></el-table-column>
        <el-table-column prop="activity" label="活动" width="400"></el-table-column>
        <el-table-column prop="user" label="操作人" width="120"></el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === '成功' ? 'success' : 'warning'">{{ scope.row.status }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { UserFilled, Goods, Document, ShoppingCart } from '@element-plus/icons-vue'

export default {
  name: 'Home',
  components: {
    UserFilled,
    Goods,
    Document,
    ShoppingCart
  },
  setup() {
    const recentActivities = ref([
      {
        time: '2026-03-03 14:00',
        activity: '创建了采购合同',
        user: '采购员',
        status: '成功'
      },
      {
        time: '2026-03-03 13:30',
        activity: '更新了物料价格',
        user: '采购员',
        status: '成功'
      },
      {
        time: '2026-03-03 12:45',
        activity: '添加了新供应商',
        user: '采购员',
        status: '成功'
      },
      {
        time: '2026-03-03 11:20',
        activity: '创建了采购订单',
        user: '采购员',
        status: '成功'
      },
      {
        time: '2026-03-03 10:15',
        activity: '修改了物料信息',
        user: '采购员',
        status: '成功'
      }
    ])
    
    return {
      recentActivities
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dashboard {
  margin-top: 20px;
}

.dashboard-card {
  height: 120px;
}

.dashboard-item {
  display: flex;
  align-items: center;
  height: 100%;
}

.dashboard-icon {
  font-size: 32px;
  color: #409EFF;
  margin-right: 20px;
}

.dashboard-content {
  flex: 1;
}

.dashboard-title {
  font-size: 14px;
  color: #606266;
  margin-bottom: 10px;
}

.dashboard-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}
</style>
