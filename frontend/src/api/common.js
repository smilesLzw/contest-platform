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
