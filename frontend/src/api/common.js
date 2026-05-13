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

function appendUploadMeta(formData, meta = {}) {
  if (meta.title) formData.append('title', meta.title)
  if (meta.academic_year) formData.append('academic_year', meta.academic_year)
  if (meta.semester) formData.append('semester', meta.semester)
  if (meta.suffix) formData.append('suffix', meta.suffix)
}

export function uploadImage(file, meta) {
  const formData = new FormData()
  formData.append('file', file)
  appendUploadMeta(formData, meta)
  return request.post('/upload/image', formData)
}

export function uploadFile(file, meta) {
  const formData = new FormData()
  formData.append('file', file)
  appendUploadMeta(formData, meta)
  return request.post('/upload/file', formData)
}

export function uploadAudio(file, meta) {
  const formData = new FormData()
  formData.append('file', file)
  appendUploadMeta(formData, meta)
  return request.post('/upload/audio', formData)
}

export function uploadVideo(file, meta) {
  const formData = new FormData()
  formData.append('file', file)
  appendUploadMeta(formData, meta)
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

// 专业管理（管理员）
export function getAdminMajors() {
  return request.get('/admin/majors')
}
export function createMajor(data) {
  return request.post('/admin/majors', data)
}
export function updateMajor(id, data) {
  return request.put(`/admin/majors/${id}`, data)
}
export function deleteMajor(id) {
  return request.delete(`/admin/majors/${id}`)
}

// 赛事管理
export function getCompetitions() {
  return request.get('/competitions')
}
export function getAdminCompetitions() {
  return request.get('/admin/competitions')
}
export function createCompetition(data) {
  return request.post('/admin/competitions', data)
}
export function updateCompetition(id, data) {
  return request.put(`/admin/competitions/${id}`, data)
}
export function deleteCompetition(id) {
  return request.delete(`/admin/competitions/${id}`)
}
export function toggleCompetition(id) {
  return request.put(`/admin/competitions/${id}/toggle`)
}

// 教师下拉列表
export function getTeachers() {
  return request.get('/users/teachers')
}
