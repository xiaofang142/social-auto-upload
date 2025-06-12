<template>
  <div class="dashboard">
    <div class="dashboard-content">
      <el-row :gutter="20">
        <!-- 账号统计卡片 -->
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-card-content">
              <div class="stat-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ getCount(accountList) }}</div>
                <div class="stat-label">账号总数</div>
              </div>
            </div>
            <div class="stat-footer">
              <div class="stat-detail" >
                <span v-for="item in accountList.value" :key="item">{{ getStatusText(item.status) }}: {{item.count}}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 平台统计卡片 -->
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-card-content">
              <div class="stat-icon platform-icon">
                <el-icon><Platform /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ getCount(paltformList) }}</div>
                <div class="stat-label">平台总数</div>
              </div>
            </div>
            <div class="stat-footer">
              <div class="stat-detail">
                  <div v-for="item in paltformList.value" :key="item">
                    <el-tooltip  :content="getPlatformTagText(item.type)" >
                      <el-tag size="small" :type="getPlatformTagLabel(item.type)">{{ item.count }}</el-tag>
                    </el-tooltip>
                  </div>
    
              </div>
            </div>
          </el-card>
        </el-col>
        
        <!-- 任务统计卡片 -->
        <el-col :span="8">
          <el-card class="stat-card">
            <div class="stat-card-content">
              <div class="stat-icon task-icon">
                <el-icon><List /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-value">{{ getCount(joblist) }}</div>
                <div class="stat-label">任务总数</div>
              </div>
            </div>
            <div class="stat-footer">
              <div class="stat-detail">
                <span  v-for="item in joblist.value" :key="item">{{ getJobStatusText(item.status) }}: {{ item.count }}</span>
              </div>
            </div>
          </el-card>
        </el-col>
        
      </el-row>
      
      
      <!-- 最近任务列表 -->
      <div class="recent-tasks">
        <div class="section-header">
          <h2>最近任务</h2>
          <el-button @click="navigateTo('/joblist')" text>查看全部</el-button>
        </div>
        
        <el-table :data="recentTasks" style="width: 100%">
          <el-table-column prop="title" label="任务名称" width="250" />
          <el-table-column prop="platform" label="平台" width="120">
            <template #default="scope">
              <el-tag
                :type="getPlatformTagLabel(scope.row.type)"
                effect="plain"
              >
                {{ getPlatformTagText(scope.row.type) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="220" />
          <el-table-column prop="scheduleTime" label="计划执行时间" width="220" />
          <el-table-column prop="publishTime" label="创建时间" width="220" />
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag
                :type="getJobStatusLabel(scope.row.status)"
                effect="plain"
              >
                {{ getJobStatusText(scope.row.status) }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive,onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { accountApi } from '@/api/account'

const router = useRouter()

// 账号统计数据
const accountList = reactive([])

// 平台统计数据
const paltformList = reactive([])

// 任务统计数据
const joblist = reactive([])



// 最近任务数据
const recentTasks = ref([])

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

// 根据平台获取标签类型
const getPlatformTagText = (platform) => {
  const typeMap = {
    '1': '快手',
    '2': '抖音',
    '3': '视频号',
    '4': '小红书'
  }
  return typeMap[platform] || 'info'
}
const getPlatformTagLabel = (platform) => {
  const typeMap = {
    '1': 'success',
    '2': 'danger',
    '3': 'warning',
    '4': 'info'
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
  return typeMap[status] || '位置'
}

const getJobStatusText = (status) => {
  const typeMap = {
    '0': '待执行',
    '5': '进行中',
    '15': '已失败',
    '20': '已完成'
  }
  return typeMap[status] || '未知'
}
const getJobStatusLabel = (status) => {
  const typeMap = {
    '0': 'success',
    '5': 'warning',
    '15': 'info',
    '20': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusText = (status) => {
    const map = {
    1: '正常',
    0: '异常',
  }
  return map[status] || '正常'
}

const getCount = (list) => {
  let total = 0;
  let new_list = list.value
  if(new_list  && new_list.length > 0){
    new_list.forEach(item => {
      total += item.count
    })
  }
  return total
}

// 导航到指定路由
const navigateTo = (path) => {
  router.push(path)
}

// 页面加载时获取账号数据
onMounted(() => {
  fetchStatistics()
})
// 统计数据
const fetchStatistics = async () => {
  try {
    const res = await accountApi.getAccountsStatistics()
    console.log('账号数据:', res.data)
    if (res.code === 200 && res.data) {
      accountList.value = res.data.status_list || []
      recentTasks.value = res.data.job_list || []
      paltformList.value = res.data.paltform_list || []
      joblist.value = res.data.job || []
      console.log('账号数据:', paltformList.value)
      ElMessage.success('账号数据获取成功')
    } else {
      ElMessage.error('获取账号数据失败1')
    }
  } catch (error) {
    console.error('获取账号数据失败:', error)
    ElMessage.error('获取账号数据失败2')
  }
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