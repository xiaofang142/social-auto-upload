import { createRouter, createWebHashHistory } from 'vue-router'
import Dashboard from '../views/Dashboard.vue'
import AccountManagement from '../views/AccountManagement.vue'
import MaterialManagement from '../views/MaterialManagement.vue'
import PublishCenter from '../views/PublishCenter.vue'
import About from '../views/About.vue'
import Joblist from '../views/Joblist.vue'
import Ai from '../views/Ai.vue'
import Listen from '../views/Listen.vue'

const routes = [
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/account-management',
    name: 'AccountManagement',
    component: AccountManagement
  },
  {
    path: '/material-management',
    name: 'MaterialManagement',
    component: MaterialManagement
  },
  {
    path: '/publish-center',
    name: 'PublishCenter',
    component: PublishCenter
  },
  {
    path: '/about',
    name: 'About',
    component: About
  },
  {
    path: '/joblist',
    name: 'joblist',
    component: Joblist
  },
  {
    path: '/ai',
    name: 'ai',
    component: Ai
  },
  {
    path: '/listen',
    name: 'listen',
    component: Listen
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router