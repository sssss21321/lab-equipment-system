<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">设备列表</span>
          <el-button type="primary" @click="openAdd">+ 添加设备</el-button>
        </div>
      </template>

      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-input v-model="search" placeholder="搜索名称/型号/编号" clearable @input="loadData">
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

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="名称" min-width="140" />
        <el-table-column prop="model" label="型号" min-width="120" />
        <el-table-column prop="manufacturer" label="厂商" min-width="120" />
        <el-table-column prop="serial_number" label="序列号" min-width="120" />
        <el-table-column prop="location" label="存放位置" min-width="100" />
        <el-table-column prop="category" label="类别" width="100" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="使用次数" width="80">
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

      <div style="margin-top: 16px; display: flex; justify-content: flex-end">
        <el-pagination
          background layout="total, prev, pager, next"
          :total="total" :page-size="pageSize" :current-page="page"
          @current-change="onPageChange"
        />
      </div>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑设备' : '添加设备'" width="580px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="名称" prop="name" :rules="[{ required: true, message: '必填', trigger: 'blur' }]">
          <el-input v-model="form.name" placeholder="必填" />
        </el-form-item>
        <el-form-item label="型号" prop="model"><el-input v-model="form.model" /></el-form-item>
        <el-form-item label="厂商" prop="manufacturer"><el-input v-model="form.manufacturer" /></el-form-item>
        <el-form-item label="序列号" prop="serial_number"><el-input v-model="form.serial_number" /></el-form-item>
        <el-form-item label="存放位置" prop="location"><el-input v-model="form.location" /></el-form-item>
        <el-form-item label="类别" prop="category"><el-input v-model="form.category" /></el-form-item>
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
        <el-form-item label="备注" prop="description"><el-input v-model="form.description" type="textarea" :rows="3" /></el-form-item>
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
      ElMessage.success('更新成功')
    } else {
      await createEquipment(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('操作失败: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('删除设备 "' + row.name + '"？', '确认删除', { type: 'warning' })
    await deleteEquipment(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(loadData)
</script>
