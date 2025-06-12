import { http } from '@/utils/request'

// 素材管理API
export const materialApi = {
  // 获取所有素材
  getAllMaterials: (params) => {
    return http.get('/material/list',params)
  },
  
  // 上传素材
  uploadMaterial: (formData) => {
    // 使用http.upload方法，它已经配置了正确的Content-Type
    return http.upload('/material/upload', formData)
  },
  
  // 删除素材
  deleteMaterial: (id) => {
    return http.get(`/material/deleted?id=${id}`)
  },
  
  // 获取素材预览URL
  getMaterialPreviewUrl: (filename) => {
    return `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:5409'}/material/preview?filename=${filename}`
  }
}