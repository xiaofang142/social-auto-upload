import { http } from '@/utils/request'

export const categoryApi = {
  getAllCategory: () => {
    return http.get('/category/list')
  },
  

  addOneCategory: (formData) => {
    return http.post('/category/add', formData)
  },
  
  deleteOneCategory: (id) => {
    return http.get(`/category/deleted?id=${id}`)
  },
  

}