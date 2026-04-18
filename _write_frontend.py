# -*- coding: utf-8 -*-
import os

FRONTEND = r'C:\Users\HP\.qclaw\workspace\lab-equipment-system\frontend'

def w(path, content):
    full = os.path.join(FRONTEND, path.replace('/', os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {path}')

# main.js
w('src/main.js', '''/* eslint-disable */
import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'
import App from './App.vue'

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(ElementPlus)
app.use(router)
app.mount('#app')
''')

# App.vue
w('src/App.vue', '''<template>
  <div id="app">
    <el-container style="min-height: 100vh">
      <el-aside width="220px" style="background: #001529">
        <div class="logo-title">Lab Equipment System</div>
        <el-menu
          :default-active="$route.path"
          router
          background-color="#001529"
          text-color="rgba(255,255,255,0.65)"
          active-text-color="#fff"
        >
          <el-menu-item index="/equipment">
            <el-icon><Tools /></el-icon>
            <span>Equipment</span>
          </el-menu-item>
          <el-menu-item index="/usage">
            <el-icon><List /></el-icon>
            <span>Usage Records</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid #e8e8e8">
          <span style="font-size: 18px; font-weight: bold; color: #333">Laboratory Equipment System</span>
          <el-tag type="success">Basic v1.0</el-tag>
        </el-header>
        <el-main style="background: #f0f2f5; padding: 20px">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { Tools, List } from '@element-plus/icons-vue'
</script>

<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
#app { height: 100vh; font-family: "Microsoft YaHei", Arial, sans-serif; }
.logo-title {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 15px;
  font-weight: bold;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
</style>
''')

# router/index.js
w('src/router/index.js', '''import { createRouter, createWebHistory } from 'vue-router'
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
''')

# api/equipment.js
w('src/api/equipment.js', '''import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000/api/equipment'

const api = axios.create({ baseURL: BASE_URL, timeout: 10000 })

api.interceptors.response.use(
  resp => resp.data,
  err => { alert('API Error: ' + (err.message || '')); return Promise.reject(err) }
)

export const getEquipmentList = (params) => api.get('/', { params })
export const getEquipmentDetail = (id) => api.get('/' + id)
export const createEquipment = (data) => api.post('/', data)
export const updateEquipment = (id, data) => api.put('/' + id, data)
export const deleteEquipment = (id) => api.delete('/' + id)
''')

# api/usage.js
w('src/api/usage.js', '''import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000/api/usage'

const api = axios.create({ baseURL: BASE_URL, timeout: 10000 })

api.interceptors.response.use(
  resp => resp.data,
  err => { alert('API Error: ' + (err.message || '')); return Promise.reject(err) }
)

export const getUsageList = (params) => api.get('/', { params })
export const getUsageDetail = (id) => api.get('/' + id)
export const createUsage = (data) => api.post('/', data)
export const updateUsage = (id, data) => api.put('/' + id, data)
export const deleteUsage = (id) => api.delete('/' + id)
''')

# views/EquipmentList.vue
w('src/views/EquipmentList.vue', '''<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">Equipment List</span>
          <el-button type="primary" @click="openAdd">+ Add Equipment</el-button>
        </div>
      </template>

      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-input v-model="search" placeholder="Search name/model/serial" clearable @input="loadData">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterStatus" placeholder="Status filter" clearable @change="loadData">
            <el-option label="Normal" value="normal" />
            <el-option label="Maintenance" value="maintenance" />
            <el-option label="Repair" value="repairly" />
            <el-option label="Scrapped" value="scraped" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="loadData">Refresh</el-button>
        </el-col>
      </el-row>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="Name" min-width="140" />
        <el-table-column prop="model" label="Model" min-width="120" />
        <el-table-column prop="manufacturer" label="Manufacturer" min-width="120" />
        <el-table-column prop="serial_number" label="Serial No." min-width="120" />
        <el-table-column prop="location" label="Location" min-width="100" />
        <el-table-column prop="category" label="Category" width="100" />
        <el-table-column label="Status" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Usage" width="80">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.usage_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Actions" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">Edit</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(row)">Del</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          background layout="total, prev, pager, next"
          :total="total" :page-size="pageSize" :current-page="page"
          @current-change="onPageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'Edit Equipment' : 'Add Equipment'" width="580px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="Name" prop="name" :rules="[{ required: true, message: 'Required', trigger: 'blur' }]">
          <el-input v-model="form.name" placeholder="Required" />
        </el-form-item>
        <el-form-item label="Model" prop="model"><el-input v-model="form.model" /></el-form-item>
        <el-form-item label="Manufacturer" prop="manufacturer"><el-input v-model="form.manufacturer" /></el-form-item>
        <el-form-item label="Serial No." prop="serial_number"><el-input v-model="form.serial_number" /></el-form-item>
        <el-form-item label="Location" prop="location"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="Category" prop="category"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="Purchase Date" prop="purchase_date">
          <el-date-picker v-model="form.purchase_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="Status" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="Normal" value="normal" />
            <el-option label="Maintenance" value="maintenance" />
            <el-option label="Repair" value="repairly" />
            <el-option label="Scrapped" value="scraped" />
          </el-select>
        </el-form-item>
        <el-form-item label="Description" prop="description"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import { getEquipmentList, createEquipment, updateEquipment, deleteEquipment } from '../api/equipment.js'

const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const search = ref('')
const filterStatus = ref('')
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const editingId = ref(null)

const form = reactive({
  name: '', model: '', manufacturer: '', serial_number: '',
  location: '', category: '', purchase_date: '', status: 'normal', description: ''
})

const statusMap = { normal: 'Normal', maintenance: 'Maintenance', repairly: 'Repair', scraped: 'Scrapped' }
const typeMap = { normal: 'success', maintenance: 'warning', repairly: 'danger', scraped: 'info' }
const statusText = (s) => statusMap[s] || s
const statusType = (s) => typeMap[s] || 'info'

function resetForm() {
  Object.assign(form, { name: '', model: '', manufacturer: '', serial_number: '',
    location: '', category: '', purchase_date: '', status: 'normal', description: '' })
}

function openAdd() {
  isEdit.value = false; editingId.value = null; resetForm(); dialogVisible.value = true
}
function openEdit(row) {
  isEdit.value = true; editingId.value = row.id
  Object.assign(form, { ...row, purchase_date: row.purchase_date || '' })
  dialogVisible.value = true
}

async function loadData() {
  loading.value = true
  try {
    const res = await getEquipmentList({ page: page.value, page_size: pageSize.value, search: search.value || undefined, status: filterStatus.value || undefined })
    tableData.value = res.items; total.value = res.total
  } catch {}
  finally { loading.value = false }
}

function onPageChange(p) { page.value = p; loadData() }

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateEquipment(editingId.value, form)
      ElMessage.success('Updated')
    } else {
      await createEquipment(form)
      ElMessage.success('Added')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('Error: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('Delete equipment "' + row.name + '"?', 'Confirm', { type: 'warning' })
    await deleteEquipment(row.id)
    ElMessage.success('Deleted')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('Delete failed') }
}

onMounted(loadData)
</script>
''')

# views/UsageList.vue
w('src/views/UsageList.vue', '''<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">Usage Records</span>
          <el-button type="primary" @click="openAdd">+ Add Record</el-button>
        </div>
      </template>

      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-select v-model="filterEquipment" placeholder="Filter by equipment" clearable filterable @change="loadData" style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="loadData">Refresh</el-button>
        </el-col>
      </el-row>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="Equipment" min-width="140">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.equipment_name || 'Equipment #' + row.equipment_id }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user" label="User" min-width="100" />
        <el-table-column prop="purpose" label="Purpose" min-width="160" show-overflow-tooltip />
        <el-table-column prop="start_time" label="Start Time" min-width="160" />
        <el-table-column prop="end_time" label="End Time" min-width="160" />
        <el-table-column prop="notes" label="Notes" min-width="160" show-overflow-tooltip />
        <el-table-column label="Actions" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">Edit</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(row)">Del</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          background layout="total, prev, pager, next"
          :total="total" :page-size="pageSize" :current-page="page"
          @current-change="onPageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? 'Edit Record' : 'Add Usage Record'" width="560px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="Equipment" prop="equipment_id" :rules="[{ required: true, message: 'Required', trigger: 'change' }]">
          <el-select v-model="form.equipment_id" placeholder="Select equipment" filterable style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="User" prop="user" :rules="[{ required: true, message: 'Required', trigger: 'blur' }]">
          <el-input v-model="form.user" />
        </el-form-item>
        <el-form-item label="Purpose" prop="purpose"><el-input v-model="form.purpose" /></el-form-item>
        <el-form-item label="Start Time" prop="start_time" :rules="[{ required: true, message: 'Required', trigger: 'blur' }]">
          <el-date-picker v-model="form.start_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" />
        </el-form-item>
        <el-form-item label="End Time" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" />
        </el-form-item>
        <el-form-item label="Notes" prop="notes"><el-input v-model="form.notes" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">Cancel</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">Save</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsageList, createUsage, updateUsage, deleteUsage } from '../api/usage.js'
import { getEquipmentList } from '../api/equipment.js'

const tableData = ref([])
const loading = ref(false)
const total = ref(0)
const page = ref(1)
const pageSize = ref(20)
const filterEquipment = ref('')
const equipmentOptions = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)
const editingId = ref(null)

const form = reactive({
  equipment_id: null, user: '', purpose: '', start_time: '', end_time: '', notes: ''
})

function resetForm() {
  Object.assign(form, { equipment_id: null, user: '', purpose: '', start_time: '', end_time: '', notes: '' })
}

async function loadEquipmentOptions() {
  try {
    const res = await getEquipmentList({ page: 1, page_size: 1000 })
    equipmentOptions.value = res.items
  } catch {}
}

async function loadData() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filterEquipment.value) params.equipment_id = filterEquipment.value
    const res = await getUsageList(params)
    tableData.value = res.items; total.value = res.total
  } catch {}
  finally { loading.value = false }
}

function openAdd() {
  isEdit.value = false; editingId.value = null; resetForm(); dialogVisible.value = true
}
function openEdit(row) {
  isEdit.value = true; editingId.value = row.id
  Object.assign(form, { ...row, start_time: row.start_time || '', end_time: row.end_time || '' })
  dialogVisible.value = true
}

function onPageChange(p) { page.value = p; loadData() }

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateUsage(editingId.value, form)
      ElMessage.success('Updated')
    } else {
      await createUsage(form)
      ElMessage.success('Added')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('Error: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('Delete this record?', 'Confirm', { type: 'warning' })
    await deleteUsage(row.id)
    ElMessage.success('Deleted')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('Delete failed') }
}

onMounted(() => { loadEquipmentOptions(); loadData() })
</script>
''')

# vite.config.js
w('vite.config.js', '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    open: false,
  },
})
''')

print('\n=== All frontend files written! ===')
