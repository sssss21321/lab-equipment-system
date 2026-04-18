import axios from 'axios'

const BASE_URL = '/api/equipment'   // 走 Vite 代理，开发和生产环境通用

const api = axios.create({ baseURL: BASE_URL, timeout: 10000 })

api.interceptors.response.use(
  resp => resp.data,
  err => {
    const detail = err.response?.data?.detail
    const msg = (typeof detail === 'string') ? detail
               : (typeof detail === 'object' && detail !== null) ? JSON.stringify(detail)
               : err.message || 'Unknown error'
    console.error('API Error:', err.response?.status, detail, err)
    alert('API Error: ' + msg)
    return Promise.reject(err)
  }
)

function cleanParams(params) {
  const p = {}
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== '') p[k] = v
  }
  return p
}

export const getEquipmentList = (params) => {
  const p = cleanParams(params)
  if (p.page_size > 200) p.page_size = 200
  return api.get('/', { params: p })
}
export const getEquipmentDetail = (id) => api.get('/' + id)
export const createEquipment = (data) => api.post('/', data)
export const updateEquipment = (id, data) => api.put('/' + id, data)
export const deleteEquipment = (id) => api.delete('/' + id)
