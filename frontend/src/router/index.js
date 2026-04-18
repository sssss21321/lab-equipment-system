import { createRouter, createWebHistory } from 'vue-router'
import EquipmentList from '../views/EquipmentList.vue'
import UsageList from '../views/UsageList.vue'

const routes = [
  { path: '/', redirect: '/equipment' },
  { path: '/equipment', component: EquipmentList },
  { path: '/usage', component: UsageList },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
