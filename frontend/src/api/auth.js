import request from '../utils/request'

export function login(data) {
  return request.post('/auth/login', data)
}

export function getMe() {
  return request.get('/auth/me')
}

export function updateProfile(data) {
  return request.put('/auth/me', data)
}

export function changePassword(data) {
  return request.put('/auth/me/password', data)
}
