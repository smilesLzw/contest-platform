import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as loginApi, getMe } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(JSON.parse(localStorage.getItem('userInfo') || 'null'))

  const isLoggedIn = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  const isTeacher = computed(() => userInfo.value?.role === 'teacher')
  const userName = computed(() => userInfo.value?.name || '')
  const userAvatar = computed(() => userInfo.value?.avatar_url || '')

  async function login(credentials) {
    const res = await loginApi(credentials)
    token.value = res.data.access_token
    userInfo.value = res.data.user
    localStorage.setItem('token', res.data.access_token)
    localStorage.setItem('userInfo', JSON.stringify(res.data.user))
    return res.data
  }

  async function fetchUserInfo() {
    try {
      const res = await getMe()
      userInfo.value = res.data
      localStorage.setItem('userInfo', JSON.stringify(res.data))
    } catch {
      logout()
    }
  }

  function setUserInfo(info) {
    userInfo.value = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  }

  function logout() {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }

  return {
    token, userInfo, isLoggedIn, isAdmin, isTeacher, userName, userAvatar,
    login, fetchUserInfo, setUserInfo, logout,
  }
})
