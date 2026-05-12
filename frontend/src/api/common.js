import request from '../utils/request'

export function getMajors() {
  return request.get('/majors')
}

export function getStats() {
  return request.get('/stats')
}

export function getLogs(params) {
  return request.get('/logs', { params })
}

export function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/upload/image', formData)
}

export function uploadFile(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/upload/file', formData)
}

export function uploadAudio(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/upload/audio', formData)
}

export function uploadVideo(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/upload/video', formData)
}

export function getBgMusic() {
  return request.get('/bg-music/')
}

export function getAdminBgMusic() {
  return request.get('/bg-music/admin/all')
}

export function createBgMusic(data) {
  return request.post('/bg-music/', data)
}

export function updateBgMusic(id, data) {
  return request.put(`/bg-music/${id}`, data)
}

export function deleteBgMusic(id) {
  return request.delete(`/bg-music/${id}`)
}

export function toggleBgMusic(id) {
  return request.put(`/bg-music/${id}/toggle`)
}
