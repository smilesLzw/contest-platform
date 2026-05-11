<template>
  <header class="app-header" :class="{ scrolled: isScrolled }">
    <div class="header-inner">
      <div class="logo" @click="$router.push('/')">
        <span class="logo-mark">◆</span>
        <span class="logo-text">院赛作品平台</span>
      </div>
      <nav class="nav-links">
        <router-link to="/" :class="{ active: isActive('/') }">首页</router-link>
        <router-link to="/works" :class="{ active: isActive('/works') }">作品展示</router-link>
        <router-link to="/ai-tools" :class="{ active: isActive('/ai-tools') }">AI 工具</router-link>
        <router-link to="/news" :class="{ active: isActive('/news') }">资讯中心</router-link>
      </nav>
      <div class="header-right">
        <button class="theme-toggle" @click="toggleTheme" :title="isDark ? '切换到日间模式' : '切换到夜间模式'">
          <el-icon :size="18"><Sunny v-if="!isDark" /><Moon v-else /></el-icon>
        </button>
        <template v-if="authStore.isLoggedIn">
          <el-dropdown trigger="click">
            <span class="user-avatar">
              <el-avatar :size="32" :src="authStore.userAvatar || ''">
                {{ authStore.userName?.charAt(0) }}
              </el-avatar>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item v-if="authStore.isAdmin" @click="$router.push('/admin')">管理后台</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { Sunny, Moon } from '@element-plus/icons-vue'

const route = useRoute()
const authStore = useAuthStore()
const isScrolled = ref(false)
const isDark = ref(false)

const THEME_KEY = 'app-theme'

function applyTheme(dark) {
  isDark.value = dark
  document.documentElement.setAttribute('data-theme', dark ? 'dark' : 'light')
}

function toggleTheme() {
  const next = !isDark.value
  applyTheme(next)
  localStorage.setItem(THEME_KEY, next ? 'dark' : 'light')
}

function getAutoTheme() {
  const hour = new Date().getHours()
  return hour < 6 || hour >= 19 ? 'dark' : 'light'
}

onMounted(() => {
  const saved = localStorage.getItem(THEME_KEY)
  const theme = saved || getAutoTheme()
  applyTheme(theme === 'dark')

  // Listen for time changes (every minute) if no manual preference
  if (!saved) {
    setInterval(() => {
      applyTheme(getAutoTheme() === 'dark')
    }, 60000)
  }
})

if (typeof window !== 'undefined') {
  window.addEventListener('scroll', () => {
    isScrolled.value = window.scrollY > 0
  }, { passive: true })
}

function isActive(base) {
  const path = route.path
  if (base === '/') return path === '/'
  return path.startsWith(base)
}

function handleLogout() {
  authStore.logout()
  window.location.href = '/'
}
</script>

<style scoped>
.app-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 48px;
  background: var(--header-bg);
  backdrop-filter: saturate(180%) blur(20px);
  -webkit-backdrop-filter: saturate(180%) blur(20px);
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}
.app-header.scrolled {
  border-bottom-color: var(--border-subtle);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  align-items: center;
  padding: 0 24px;
}

/* Logo */
.logo {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  user-select: none;
  margin-right: 40px;
}
.logo-mark { font-size: 16px; color: var(--accent); }
.logo-text {
  font-family: var(--font-display);
  font-size: 16px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Nav */
.nav-links {
  flex: 1;
  display: flex;
  gap: 4px;
}
.nav-links a {
  display: inline-flex;
  align-items: center;
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
}
.nav-links a:hover { color: var(--text-primary); }
.nav-links a.active { color: var(--text-primary); }

/* Right */
.header-right {
  display: flex;
  align-items: center;
  margin-left: 16px;
}
.user-avatar {
  cursor: pointer;
  display: flex;
  align-items: center;
}

/* Theme toggle */
.theme-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border: none;
  border-radius: 50%;
  background: transparent;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.3s ease;
  margin-right: 8px;
}
.theme-toggle:hover {
  background: var(--bg-card-hover);
  color: var(--text-primary);
}
</style>
