<template>
  <div class="dashboard">
    <div class="dashboard-content">
      <div class="recent-tasks">
        
        <el-table :data="recentTasks" style="width: 100%">
          <el-table-column prop="title" label="任务名称" width="250" />
          <el-table-column prop="platform" label="平台" width="120">
            <template #default="scope">
              <el-tag
                :type="getPlatformTagType(scope.row.platform)"
                effect="plain"
              >
                {{ scope.row.platform }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="account" label="账号" width="150" />
          <el-table-column prop="createTime" label="创建时间" width="180" />
          <el-table-column prop="createTime" label="计划执行时间" width="180" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag
                :type="getStatusTagType(scope.row.status)"
                effect="plain"
              >
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="viewTaskDetail(scope.row)">查看</el-button>
              <el-button 
                size="small" 
                type="primary" 
                v-if="scope.row.status === '待执行'"
                @click="executeTask(scope.row)"
              >
                执行
              </el-button>
              <el-button 
                size="small" 
                type="danger" 
                v-if="scope.row.status !== '已完成' && scope.row.status !== '已失败'"
                @click="cancelTask(scope.row)"
              >
                取消
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { 
  User, UserFilled, Platform, List, Document, 
  Upload, Timer, DataAnalysis 
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

// 账号统计数据
const accountStats = reactive({
  total: 12,
  normal: 10,
  abnormal: 2
})

// 平台统计数据
const platformStats = reactive({
  total: 4,
  kuaishou: 3,
  douyin: 4,
  channels: 2,
  xiaohongshu: 3
})

// 任务统计数据
const taskStats = reactive({
  total: 24,
  completed: 18,
  inProgress: 5,
  failed: 1
})

// 内容统计数据
const contentStats = reactive({
  total: 36,
  published: 30,
  draft: 6
})

// 最近任务数据
const recentTasks = ref([
  {
    id: 1,
    title: '快手视频自动发布',
    platform: '快手',
    account: '快手账号1',
    createTime: '2024-05-01 10:30:00',
    status: '已完成'
  },
  {
    id: 2,
    title: '抖音视频定时发布',
    platform: '抖音',
    account: '抖音账号1',
    createTime: '2024-05-01 11:15:00',
    status: '进行中'
  },
  {
    id: 3,
    title: '视频号内容上传',
    platform: '视频号',
    account: '视频号账号1',
    createTime: '2024-05-01 14:20:00',
    status: '待执行'
  },
  {
    id: 4,
    title: '小红书图文发布',
    platform: '小红书',
    account: '小红书账号1',
    createTime: '2024-05-01 16:45:00',
    status: '已失败'
  },
  {
    id: 5,
    title: '快手短视频批量上传',
    platform: '快手',
    account: '快手账号2',
    createTime: '2024-05-02 09:10:00',
    status: '待执行'
  }
])

// 根据平台获取标签类型
const getPlatformTagType = (platform) => {
  const typeMap = {
    '快手': 'success',
    '抖音': 'danger',
    '视频号': 'warning',
    '小红书': 'info'
  }
  return typeMap[platform] || 'info'
}

// 根据状态获取标签类型
const getStatusTagType = (status) => {
  const typeMap = {
    '已完成': 'success',
    '进行中': 'warning',
    '待执行': 'info',
    '已失败': 'danger'
  }
  return typeMap[status] || 'info'
}

// 导航到指定路由
const navigateTo = (path) => {
  router.push(path)
}

// 查看任务详情
const viewTaskDetail = (task) => {
  ElMessage.info(`查看任务: ${task.title}`)
  // 实际应用中应该跳转到任务详情页面
}

// 执行任务
const executeTask = (task) => {
  ElMessageBox.confirm(
    `确定要执行任务 ${task.title} 吗？`,
    '提示',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'info',
    }
  )
    .then(() => {
      // 更新任务状态
      const index = recentTasks.value.findIndex(t => t.id === task.id)
      if (index !== -1) {
        recentTasks.value[index].status = '进行中'
      }
      ElMessage({
        type: 'success',
        message: '任务已开始执行',
      })
    })
    .catch(() => {
      // 取消执行
    })
}

// 取消任务
const cancelTask = (task) => {
  ElMessageBox.confirm(
    `确定要取消任务 ${task.title} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(() => {
      // 更新任务状态
      const index = recentTasks.value.findIndex(t => t.id === task.id)
      if (index !== -1) {
        recentTasks.value[index].status = '已取消'
      }
      ElMessage({
        type: 'success',
        message: '任务已取消',
      })
    })
    .catch(() => {
      // 取消操作
    })
}
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.dashboard {
  .page-header {
    margin-bottom: 20px;
    
    h1 {
      font-size: 24px;
      color: $text-primary;
      margin: 0;
    }
  }
  
  .dashboard-content {
    .stat-card {
      height: 140px;
      margin-bottom: 20px;
      
      .stat-card-content {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
        
        .stat-icon {
          width: 60px;
          height: 60px;
          border-radius: 50%;
          background-color: rgba($primary-color, 0.1);
          display: flex;
          justify-content: center;
          align-items: center;
          margin-right: 15px;
          
          .el-icon {
            font-size: 30px;
            color: $primary-color;
          }
          
          &.platform-icon {
            background-color: rgba($success-color, 0.1);
            
            .el-icon {
              color: $success-color;
            }
          }
          
          &.task-icon {
            background-color: rgba($warning-color, 0.1);
            
            .el-icon {
              color: $warning-color;
            }
          }
          
          &.content-icon {
            background-color: rgba($info-color, 0.1);
            
            .el-icon {
              color: $info-color;
            }
          }
        }
        
        .stat-info {
          .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: $text-primary;
            line-height: 1.2;
          }
          
          .stat-label {
            font-size: 14px;
            color: $text-secondary;
          }
        }
      }
      
      .stat-footer {
        border-top: 1px solid $border-lighter;
        padding-top: 10px;
        
        .stat-detail {
          display: flex;
          justify-content: space-between;
          color: $text-secondary;
          font-size: 13px;
          
          .el-tag {
            margin-right: 5px;
          }
        }
      }
    }
    
    .quick-actions {
      margin: 20px 0 30px;
      
      h2 {
        font-size: 18px;
        margin-bottom: 15px;
        color: $text-primary;
      }
      
      .action-card {
        height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.3s;
        
        &:hover {
          transform: translateY(-5px);
          box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .action-icon {
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background-color: rgba($primary-color, 0.1);
          display: flex;
          justify-content: center;
          align-items: center;
          margin-bottom: 15px;
          
          .el-icon {
            font-size: 24px;
            color: $primary-color;
          }
        }
        
        .action-title {
          font-size: 16px;
          font-weight: bold;
          color: $text-primary;
          margin-bottom: 5px;
        }
        
        .action-desc {
          font-size: 13px;
          color: $text-secondary;
          text-align: center;
        }
      }
    }
    
    .recent-tasks {
      margin-top: 30px;
      
      .section-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        
        h2 {
          font-size: 18px;
          color: $text-primary;
          margin: 0;
        }
      }
    }
  }
}
</style>