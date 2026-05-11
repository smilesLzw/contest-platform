import request from '../utils/request'

export function getCategories() {
  return request.get('/ai-tools/categories')
}

export function createCategory(data) {
  return request.post('/ai-tools/categories', data)
}

export function updateCategory(id, data) {
  return request.put(`/ai-tools/categories/${id}`, data)
}

export function deleteCategory(id) {
  return request.delete(`/ai-tools/categories/${id}`)
}

export function getTools(params) {
  return request.get('/ai-tools/', { params })
}

export function createTool(data) {
  return request.post('/ai-tools/', data)
}

export function updateTool(id, data) {
  return request.put(`/ai-tools/${id}`, data)
}

export function deleteTool(id) {
  return request.delete(`/ai-tools/${id}`)
}
