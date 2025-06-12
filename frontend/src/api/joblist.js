import { http } from '@/utils/request'

// 任务相关API
export const joblistApi = {
  // 最近任务
  getRecentJoblist() {
    return http.get(`getRecentJoblist`)
  },

}