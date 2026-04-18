# -*- coding: utf-8 -*-
import os

BASE = r'C:\Users\HP\.qclaw\workspace\lab-equipment-system\frontend'
SRC = f'{BASE}\src'

files = {}

# ====== main.js ======
files[f'{BASE}\src\main.js'] = '''/* eslint-disable */
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
'''

# ====== App.vue ======
files[f'{BASE}\src\App.vue'] = '''<template>
  <div id="app">
    <el-container style="min-height: 100vh">
      <el-aside width="220px" style="background: #001529">
        <div class="logo-title">&#128269; 实验室设备管理</div>
        <el-menu
          :default-active="$route.path"
          router
          background-color="#001529"
          text-color="#rgba(255,255,255,0.65)"
          active-text-color="#fff"
        >
          <el-menu-item index="/equipment">
            <el-icon><Tools /></el-icon>
            <span>设备列表</span>
          </el-menu-item>
          <el-menu-item index="/usage">
            <el-icon><List /></el-icon>
            <span>使用记录</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header style="display: flex; align-items: center; justify-content: space-between; background: #fff; border-bottom: 1px solid #e8e8e8">
          <span style="font-size: 18px; font-weight: bold; color: #333">实验室设备管理系统</span>
          <el-tag type="success">基础版 v1.0</el-tag>
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
  font-size: 16px;
  font-weight: bold;
  letter-spacing: 1px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
</style>
'''

# ====== router/index.js ======
files[f'{BASE}\src\router\index.js'] = '''import { createRouter, createWebHistory } from 'vue-router'
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
'''

# ====== api/equipment.js ======
files[f'{BASE}\src\api\equipment.js'] = '''import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000/api/equipment'

const api = axios.create({ baseURL: BASE_URL, timeout: 10000 })

api.interceptors.response.use(
  resp => resp.data,
  err => { alert('API 请求失败: ' + (err.message || '')); return Promise.reject(err) }
)

export const getEquipmentList = (params) => api.get('/', { params })
export const getEquipmentDetail = (id) => api.get('/' + id)
export const createEquipment = (data) => api.post('/', data)
export const updateEquipment = (id, data) => api.put('/' + id, data)
export const deleteEquipment = (id) => api.delete('/' + id)
'''

# ====== api/usage.js ======
files[f'{BASE}\src\api\usage.js'] = '''import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000/api/usage'

const api = axios.create({ baseURL: BASE_URL, timeout: 10000 })

api.interceptors.response.use(
  resp => resp.data,
  err => { alert('API 请求失败: ' + (err.message || '')); return Promise.reject(err) }
)

export const getUsageList = (params) => api.get('/', { params })
export const getUsageDetail = (id) => api.get('/' + id)
export const createUsage = (data) => api.post('/', data)
export const updateUsage = (id, data) => api.put('/' + id, data)
export const deleteUsage = (id) => api.delete('/' + id)
'''

# ====== views/EquipmentList.vue ======
files[f'{BASE}\src\views\EquipmentList.vue'] = r'''<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">设备列表</span>
          <el-button type="primary" @click="openAdd">+ 添加设备</el-button>
        </div>
      </template>

      <!-- 搜索栏 -->
      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-input v-model="search" placeholder="搜索设备名称/型号/序列号" clearable @input="loadData">
            <template #prefix><el-icon><Search /></el-icon></template>
          </el-input>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterStatus" placeholder="状态筛选" clearable @change="loadData">
            <el-option label="正常" value="normal" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="维修中" value="repairly" />
            <el-option label="已报废" value="scraped" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="loadData">刷新</el-button>
        </el-col>
      </el-row>

      <!-- 表格 -->
      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="设备名称" min-width="140" />
        <el-table-column prop="model" label="型号" min-width="120" />
        <el-table-column prop="manufacturer" label="制造商" min-width="120" />
        <el-table-column prop="serial_number" label="序列号" min-width="120" />
        <el-table-column prop="location" label="存放位置" min-width="100" />
        <el-table-column prop="category" label="类别" width="100" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="使用次数" width="90">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.usage_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          background layout="total, prev, pager, next"
          :total="total" :page-size="pageSize" :current-page="page"
          @current-change="onPageChange"
        />
      </div>
    </el-card>

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '添加设备'" width="580px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="设备名称" prop="name" :rules="[{ required: true, message: '请输入设备名称', trigger: 'blur' }]">
          <el-input v-model="form.name" placeholder="必填" />
        </el-form-item>
        <el-form-item label="型号" prop="model"><el-input v-model="form.model" /></el-form-item>
        <el-form-item label="制造商" prop="manufacturer"><el-input v-model="form.manufacturer" /></el-form-item>
        <el-form-item label="序列号" prop="serial_number"><el-input v-model="form.serial_number" /></el-form-item>
        <el-form-item label="存放位置" prop="location"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="设备类别" prop="category"><el-input v-model="form.category" /></el-form-item>
        <el-form-item label="购置日期" prop="purchase_date">
          <el-date-picker v-model="form.purchase_date" type="date" value-format="YYYY-MM-DD" style="width:100%" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width:100%">
            <el-option label="正常" value="normal" />
            <el-option label="维护中" value="maintenance" />
            <el-option label="维修中" value="repairly" />
            <el-option label="已报废" value="scraped" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
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

const statusMap = { normal: '正常', maintenance: '维护中', repairly: '维修中', scraped: '已报废' }
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
  } catch { /* ignore */ }
  finally { loading.value = false }
}

function onPageChange(p) { page.value = p; loadData() }

async function handleSubmit() {
  await formRef.value.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateEquipment(editingId.value, form)
      ElMessage.success('更新成功')
    } else {
      await createEquipment(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('保存失败: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除设备「${row.name}」？`, '删除确认', { type: 'warning' })
    await deleteEquipment(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(loadData)
</script>
'''

# ====== views/UsageList.vue ======
files[f'{BASE}\src\views\UsageList.vue'] = r'''<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">使用记录</span>
          <el-button type="primary" @click="openAdd">+ 添记录</el-button>
        </div>
      </template>

      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-select v-model="filterEquipment" placeholder="筛选设备" clearable filterable @change="loadData" style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="loadData">刷新</el-button>
        </el-col>
      </el-row>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="设备名称" min-width="140">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.equipment_name || '设备#'+row.equipment_id }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user" label="使用者" min-width="100" />
        <el-table-column prop="purpose" label="使用目的" min-width="160" show-overflow-tooltip />
        <el-table-column prop="start_time" label="开始时间" min-width="160" />
        <el-table-column prop="end_time" label="结束时间" min-width="160" />
        <el-table-column prop="notes" label="备注" min-width="160" show-overflow-tooltip />
        <el-table-column label="操作" width="160" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" plain @click="handleDelete(row)">删除</el-button>
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

    <!-- 添加/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑记录' : '添加使用记录'" width="560px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="设备" prop="equipment_id" :rules="[{ required: true, message: '请选择设备', trigger: 'change' }]">
          <el-select v-model="form.equipment_id" placeholder="请选择设备" filterable style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="使用者" prop="user" :rules="[{ required: true, message: '请输入使用者', trigger: 'blur' }]">
          <el-input v-model="form.user" />
        </el-form-item>
        <el-form-item label="使用目的" prop="purpose"><el-input v-model="form.purpose" /></el-form-item>
        <el-form-item label="开始时间" prop="start_time" :rules="[{ required: true, message: '请输入开始时间', trigger: 'blur' }]">
          <el-date-picker v-model="form.start_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" value-format="YYYY-MM-DD HH:mm:ss" style="width:100%" />
        </el-form-item>
        <el-form-item label="备注" prop="notes"><el-input v-model="form.notes" type="textarea" :rows="3" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">保存</el-button>
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
  } catch { /* ignore */ }
}

async function loadData() {
  loading.value = true
  try {
    const params = { page: page.value, page_size: pageSize.value }
    if (filterEquipment.value) params.equipment_id = filterEquipment.value
    const res = await getUsageList(params)
    tableData.value = res.items; total.value = res.total
  } catch { /* ignore */ }
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
      ElMessage.success('更新成功')
    } else {
      await createUsage(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('保存失败: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(`确认删除此记录？`, '删除确认', { type: 'warning' })
    await deleteUsage(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(() => { loadEquipmentOptions(); loadData() })
</script>
'''

# ====== vite.config.js ======
files[f'{BASE}\vite.config.js'] = '''import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    open: true,
  },
})
'''

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'OK: {os.path.relpath(filepath, BASE)}')

print('\n=== All frontend files created! ===')
