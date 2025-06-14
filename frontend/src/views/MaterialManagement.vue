<template>
  <div class="material-management">
    <div class="page-header">
      <h1>素材管理</h1>
    </div>
    
    <div class="material-list-container">
      <div class="material-search">
        <el-input
          v-model="searchKeyword"
          placeholder="输入文件名搜索"
          prefix-icon="Search"
          clearable
          @clear="handleSearch"
          @input="handleSearch"
        />
        <el-select style="width: 200px;" clearable @clear="handleSearch"  @input="handleSearch" v-model="searchCategoryId" placeholder="输入分类搜索">
            <el-option style="width: 200px;"
              v-for="item in categorys"
              :key="item.id"
              :label="item.name"
              :value="item.id"
            />
        </el-select>
        <div class="action-buttons">
          <el-button type="primary" @click="handleUploadMaterial">上传素材</el-button>
          <el-button type="danger" @click="handleCategoty">添加分类</el-button>
          <el-button type="info" @click="fetchMaterials" :loading="false">
            <el-icon :class="{ 'is-loading': isRefreshing }"><Refresh /></el-icon>
            <span v-if="isRefreshing">刷新中</span>
          </el-button>
        </div>
      </div>
      
      <div v-if="filteredMaterials.length > 0" class="material-list">
        <el-table :data="filteredMaterials" style="width: 100%">
          <el-table-column prop="filename" label="文件名" width="300" />
          <el-table-column prop="filesize" label="文件分类" width="180">
            <template #default="scope">
              {{ getCategoryType(scope.row.category_id) }}
            </template>
          </el-table-column>
          <el-table-column prop="filesize" label="文件大小" width="120">
            <template #default="scope">
              {{ scope.row.filesize }} MB
            </template>
          </el-table-column>
          <el-table-column prop="create_time" label="上传时间" width="180" />
          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" @click="handlePreview(scope.row)">预览</el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
      
      <div v-else class="empty-data">
        <el-empty description="暂无素材数据" />
      </div>
    </div>
    
    <!-- 上传对话框 -->
    <el-dialog
      v-model="uploadDialogVisible"
      title="上传素材"
      width="40%"
      @close="handleUploadDialogClose"
    >
      <div class="upload-form">
        <el-form label-width="80px">
          <el-form-item label="文件名称:">
            <el-input
              v-model="customFilename"
              placeholder="选填"
              clearable
            />
          </el-form-item>
          <el-form-item label="文件分类:">
            <el-select v-model="categoryId">
              <el-option
                v-for="item in categorys"
                :key="item.id"
                :label="item.name"
                :value="item.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="选择文件">
            <el-upload
              class="upload-demo"
              drag
              :auto-upload="false"
              :on-change="handleFileChange"
              :file-list="fileList"
              :limit="1"
            >
              <el-icon class="el-icon--upload"><Upload /></el-icon>
              <div class="el-upload__text">
                将文件拖到此处，或<em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持视频、图片等格式文件，只能上传一个文件
                </div>
              </template>
            </el-upload>
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="uploadDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitUpload" :loading="isUploading">
            {{ isUploading ? '上传中' : '确认上传' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
    
    <!-- 预览对话框 -->
    <el-dialog
      v-model="previewDialogVisible"
      title="素材预览"
      width="50%"
      :top="'10vh'"
    >
      <div class="preview-container" v-if="currentMaterial">
        <div v-if="isVideoFile(currentMaterial.filename)" class="video-preview">
          <video controls style="max-width: 100%; max-height: 60vh;">
            <source :src="getPreviewUrl(currentMaterial.filepath)" type="video/mp4">
            您的浏览器不支持视频播放
          </video>
        </div>
        <div v-else-if="isImageFile(currentMaterial.filename)" class="image-preview">
          <img :src="getPreviewUrl(currentMaterial.filepath)" style="max-width: 100%; max-height: 60vh;" />
        </div>
        <div v-else class="file-info">
          <p>文件名: {{ currentMaterial.filename }}</p>
          <p>文件大小: {{ currentMaterial.filesize }} MB</p>
          <p>上传时间: {{ currentMaterial.upload_time }}</p>
          <el-button type="primary" @click="downloadFile(currentMaterial)">下载文件</el-button>
        </div>
      </div>
    </el-dialog>

    <!-- 添加分类 -->
    <el-dialog
      v-model="categoryDialogVisible"
      title="添加分类"
      width="40%"
      @close="handleCategoryDialogClose"
    >
      <div class="upload-form">
        <el-form label-width="80px">
          <el-form-item label="文件名称:">
            <el-input
              v-model="categoryName"
              placeholder="请输入分类名称"
              clearable
            />
          </el-form-item>
        </el-form>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="categoryDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="submitCategory" :loading="isUploading">
            {{ isUploading ? '添加中' : '确认添加' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Refresh, Upload } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { materialApi } from '@/api/material'
import { useAppStore } from '@/stores/app'
import { categoryApi } from '@/api/category'

// 获取应用状态管理
const appStore = useAppStore()

// 搜索和状态控制
const searchKeyword = ref('')
const searchCategoryId = ref('')
const isRefreshing = ref(false)
const isUploading = ref(false)

// 对话框控制
const uploadDialogVisible = ref(false)
const previewDialogVisible = ref(false)
const currentMaterial = ref(null)
const categoryDialogVisible = ref(false)
// 文件上传
const fileList = ref([])
const customFilename = ref('')
const categoryName = ref('')
const categoryId = ref('')

// 获取素材列表
const fetchMaterials = async () => {
  isRefreshing.value = true
  try {
    const response = await materialApi.getAllMaterials()
    
    if (response.code === 200) {
      appStore.setMaterials(response.data)
      ElMessage.success('刷新成功')
    } else {
      ElMessage.error('获取素材列表失败')
    }
  } catch (error) {
    console.error('获取素材列表出错:', error)
    ElMessage.error('获取素材列表失败')
  } finally {
    isRefreshing.value = false
  }
}

// 过滤素材
const filteredMaterials = computed(() => {
  if (!searchKeyword.value && !searchCategoryId.value) return appStore.materials

  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    return appStore.materials.filter(material => 
      material.filename.toLowerCase().includes(keyword)
    )
  }
  if (searchCategoryId.value) {
    const categoryid = searchCategoryId.value
    return appStore.materials.filter(material => 
      material.category_id == categoryid
    )
  }
})
// 
const categorys = computed(() => {
  return appStore.categorys
})

// 搜索处理
const handleSearch = () => {
  // 搜索逻辑已通过计算属性实现
}

// 上传素材
const handleUploadMaterial = () => {
  // 清空变量
  fileList.value = []
  customFilename.value = ''
  uploadDialogVisible.value = true
}

// 关闭上传对话框时清空变量
const handleUploadDialogClose = () => {
  fileList.value = []
  customFilename.value = ''
}

// 文件选择变更
const handleFileChange = (file, uploadFileList) => {
  // 只保留最新选择的文件
  console.log('选择的文件:', file)
  if (file.raw) {
    // 确保获取到原始文件对象
    fileList.value = [file]
  }
}

// 提交上传
const submitUpload = async () => {
  if (fileList.value.length === 0) {
     ElMessage.error('请选择要上传的文件')
    return
  }
  if (!categoryId.value) {
    ElMessage.error('请选择文件分类')
    return
  }
  // 确保文件对象存在
  const fileObj = fileList.value[0]
  if (!fileObj || !fileObj.raw) {
    ElMessage.error('文件对象无效，请重新选择文件')
    return
  }
  
  isUploading.value = true
  
  try {
    // 使用FormData进行表单提交
    const formData = new FormData()
    
    // 添加文件，确保使用正确的文件对象
    formData.append('file', fileObj.raw)
    formData.append('category_id', categoryId.value)
    
    // 如果用户输入了自定义文件名，则添加到表单中
    if (customFilename.value.trim()) {
      formData.append('filename', customFilename.value.trim())
    }
    
    const response = await materialApi.uploadMaterial(formData)
    
    if (response.code === 200) {
      ElMessage.success('上传成功')
      uploadDialogVisible.value = false
      // 上传成功后直接刷新素材列表
      await fetchMaterials()
    } else {
      ElMessage.error(response.msg || '上传失败')
    }
  } catch (error) {
    console.error('上传素材出错:', error)
    ElMessage.error('上传失败: ' + (error.msg || '未知错误'))
  } finally {
    isUploading.value = false
  }
}

// 预览素材
const handlePreview = async (material) => {
  currentMaterial.value = null
  previewDialogVisible.value = true
  ElMessage.info('加载中...')
  try {
    // 等待一小段时间以确保对话框已打开
    await new Promise(resolve => setTimeout(resolve, 100))
    currentMaterial.value = material
  } catch (error) {
    console.error('预览素材出错:', error)
    ElMessage.error('预览加载失败')
    previewDialogVisible.value = false
  }
}

// 删除素材
const handleDelete = (material) => {
  ElMessageBox.confirm(
    `确定要删除素材 ${material.filename} 吗？`,
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
    .then(async () => {
      try {
        const response = await materialApi.deleteMaterial(material.id)
        
        if (response.code === 200) {
          appStore.removeMaterial(material.id)
          ElMessage.success('删除成功')
        } else {
          ElMessage.error(response.msg || '删除失败')
        }
      } catch (error) {
        console.error('删除素材出错:', error)
        ElMessage.error('删除失败')
      }
    })
    .catch(() => {
      // 取消删除
    })
}

// 获取预览URL
const getPreviewUrl = (filePath) => {
  const filename = filePath.split('/').pop()
  return materialApi.getMaterialPreviewUrl(filename)
}

// 下载文件
const downloadFile = (material) => {
  const url = materialApi.downloadMaterial(material.filepath)
  window.open(url, '_blank')
}

// 判断文件类型
const isVideoFile = (filename) => {
  const videoExtensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']
  return videoExtensions.some(ext => filename.toLowerCase().endsWith(ext))
}

const isImageFile = (filename) => {
  const imageExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
  return imageExtensions.some(ext => filename.toLowerCase().endsWith(ext))
}

// 添加分类
const handleCategoty = () => {
  // 清空变量
  categoryName.value = ''
  categoryId.value = ''
  categoryDialogVisible.value = true
}
// 关闭添加分类
const handleCategoryDialogClose = () => {
  categoryName.value = ''
  categoryId.value = 0
}
// 提交上传
const submitCategory = async () => {
  if (!categoryName) {
    ElMessage.warning('请输入分类名称')
    return
  }
  isUploading.value = true
  
  try {
    const formData = {name: categoryName.value}
    const response = await categoryApi.addOneCategory(formData)
    if (response.code !== 200) {
       ElMessage.error(response.msg || '上传失败')
    }
    ElMessage.success('添加成功')
    categoryDialogVisible.value = false
    fetchCategory()
  } catch (error) {
    ElMessage.error('添加失败: ' + (error.msg || '未知错误'))
  } finally {
    isUploading.value = false
  }
}
// 获取素材列表
const fetchCategory = async () => {
  isRefreshing.value = true
  try {
    const response = await categoryApi.getAllCategory()
    
    if (response.code === 200) {
      console.log(response.data)
      appStore.setCategorys(response.data)
      ElMessage.success('刷新成功')
    } else {
      ElMessage.error('获取素材列表失败')
    }
  } catch (error) {
    ElMessage.error('获取素材列表失败')
  } finally {
    isRefreshing.value = false
  }
}

// 根据平台获取标签类型
const getCategoryType = (category_id) => {
  let type = 'name'
  appStore.categorys.forEach(item => {
    if (item.id === category_id) {
      type = item.name
    }
  })
  return type
}

// 组件挂载时获取素材列表
onMounted(() => {
  // 只有store中没有数据时才获取
  fetchCategory()
  if (appStore.materials.length === 0) {
    fetchMaterials()
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.material-management {
  
  .page-header {
    margin-bottom: 20px;
    
    h1 {
      font-size: 24px;
      font-weight: 500;
      color: $text-primary;
      margin: 0;
    }
  }
  
  .material-list-container {
    background-color: #fff;
    border-radius: 4px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    padding: 20px;
    
    .material-search {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      
      .el-input {
        width: 300px;
      }
      
      .action-buttons {
        display: flex;
        gap: 10px;
        
        .is-loading {
          animation: rotate 1s linear infinite;
        }
      }
    }
    
    .material-list {
      margin-top: 20px;
    }
    
    .empty-data {
      padding: 40px 0;
    }
  }
  
  .material-upload {
    width: 100%;
  }
  
  .preview-container {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    padding: 0 20px;
    
    .file-info {
      text-align: center;
      margin-top: 20px;
    }
  }
}

.upload-form {
  padding: 0 20px;
  
  .form-tip {
    font-size: 12px;
    color: #909399;
    margin-top: 5px;
  }
  
  .upload-demo {
    width: 100%;
  }
}

.dialog-footer {
  padding: 0 20px;
  display: flex;
  justify-content: flex-end;
}

/* 覆盖Element Plus对话框样式 */
:deep(.el-dialog__body) {
  padding: 20px 0;
}

:deep(.el-dialog__header) {
  padding-left: 20px;
  padding-right: 20px;
  margin-right: 0;
}

:deep(.el-dialog__footer) {
  padding-top: 10px;
  padding-bottom: 15px;
}
</style>