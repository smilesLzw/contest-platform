import request from '../utils/request'

export function getWorks(params) {
  return request.get('/works/', { params })
}

export function getWork(id) {
  return request.get(`/works/${id}`)
}

export function getMyWorks(params) {
  return request.get('/works/my', { params })
}

export function getAdminWorks(params) {
  return request.get('/works/admin/all', { params })
}

export function createWork(data) {
  return request.post('/works/', data)
}

export function publishWork(id) {
  return request.put(`/works/${id}/publish`)
}

export function archiveWork(id) {
  return request.put(`/works/${id}/archive`)
}

export function updateWork(id, data) {
  return request.put(`/works/${id}`, data)
}

export function deleteWork(id) {
  return request.delete(`/works/${id}`)
}
