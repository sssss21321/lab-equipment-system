<template>
  <div>
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span style="font-size:16px;font-weight:bold">使用记录</span>
          <el-button type="primary" @click="openAdd">+ 添加记录</el-button>
        </div>
      </template>

      <el-row :gutter="12" style="margin-bottom: 16px">
        <el-col :span="8">
          <el-select v-model="filterEquipment" placeholder="按设备筛选" clearable filterable @change="loadData" style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-button @click="loadData">刷新</el-button>
        </el-col>
      </el-row>

      <el-table :data="tableData" v-loading="loading" stripe border>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="设备" min-width="140">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.equipment_name || '设备 #' + row.equipment_id }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user" label="使用者" min-width="100" />
        <el-table-column prop="purpose" label="用途" min-width="160" show-overflow-tooltip />
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

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑记录' : '添加使用记录'" width="560px" :close-on-click-modal="false">
      <el-form :model="form" label-width="100px" ref="formRef">
        <el-form-item label="设备" prop="equipment_id" :rules="[{ required: true, message: '必填', trigger: 'change' }]">
          <el-select v-model="form.equipment_id" placeholder="选择设备" filterable style="width:100%">
            <el-option v-for="eq in equipmentOptions" :key="eq.id" :label="eq.name" :value="eq.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="使用者" prop="user" :rules="[{ required: true, message: '必填', trigger: 'blur' }]">
          <el-input v-model="form.user" />
        </el-form-item>
        <el-form-item label="用途" prop="purpose"><el-input v-model="form.purpose" /></el-form-item>
        <el-form-item label="开始时间" prop="start_time" :rules="[{ required: true, message: '必填', trigger: 'blur' }]">
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
      ElMessage.success('更新成功')
    } else {
      await createUsage(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadData()
  } catch (e) { ElMessage.error('操作失败: ' + (e.message || '')) }
  finally { submitting.value = false }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm('删除此记录？', '确认删除', { type: 'warning' })
    await deleteUsage(row.id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) { if (e !== 'cancel') ElMessage.error('删除失败') }
}

onMounted(() => { loadEquipmentOptions(); loadData() })
</script>
