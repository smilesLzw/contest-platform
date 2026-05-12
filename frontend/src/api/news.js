import request from '../utils/request'

export function getNewsList(params) {
  return request.get('/news/', { params })
}

export function getNews(id) {
  return request.get(`/news/${id}`)
}

export function getMyNews(params) {
  return request.get('/news/my', { params })
}

export function getAdminNews(params) {
  return request.get('/news/admin/all', { params })
}

export function createNews(data) {
  return request.post('/news/', data)
}

export function updateNews(id, data) {
  return request.put(`/news/${id}`, data)
}

export function deleteNews(id) {
  return request.delete(`/news/${id}`)
}

export function publishNews(id) {
  return request.put(`/news/${id}/publish`)
}

export function toggleTopNews(id) {
  return request.put(`/news/${id}/top`)
}
