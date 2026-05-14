<template>
  <div class="admin-layout">
    <!-- Sidebar -->
    <aside class="sidebar">
      <div class="sidebar-brand" @click="$router.push('/')">
        <span class="brand-mark">◆</span>
        <span class="brand-text">管理后台</span>
      </div>

      <nav class="sidebar-nav">
        <section v-for="group in navGroups" :key="group.label" class="nav-group">
          <div class="nav-group-title">{{ group.label }}</div>
          <router-link
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            :class="['nav-item', { active: isActive(item.path) }]"
          >
            <el-icon :size="16"><component :is="item.icon" /></el-icon>
            <span>{{ item.label }}</span>
          </router-link>
        </section>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <el-avatar :size="28">{{ authStore.userName?.charAt(0) }}</el-avatar>
          <span class="user-name">{{ authStore.userName }}</span>
        </div>
        <button class="back-btn" @click="handleBack">返回前台</button>
      </div>
    </aside>

    <!-- Main -->
    <div class="main-area">
      <header class="topbar">
        <h2 class="page-title">{{ currentTitle }}</h2>
      </header>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { DataAnalysis, Collection, Reading, Tools, User, Document, Headset, School, Trophy, UserFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const navSections = [
  {
    label: '工作台',
    items: [
      { path: '/admin', label: '仪表盘', icon: DataAnalysis },
    ],
  },
  {
    label: '内容管理',
    items: [
      { path: '/admin/works', label: '作品管理', icon: Collection },
      { path: '/admin/news', label: '新闻管理', icon: Reading },
      { path: '/admin/bg-music', label: '背景音乐', icon: Headset },
    ],
  },
  {
    label: '平台配置',
    items: [
      { path: '/admin/ai-tools', label: 'AI 工具管理', icon: Tools },
      { path: '/admin/majors', label: '专业管理', icon: School },
      { path: '/admin/competitions', label: '赛事管理', icon: Trophy, adminOnly: true },
    ],
  },
  {
    label: '系统管理',
    items: [
      { path: '/admin/logs', label: '操作日志', icon: Document },
      { path: '/admin/users', label: '用户管理', icon: User, adminOnly: true },
    ],
  },
  {
    label: '个人中心',
    items: [
      { path: '/admin/profile', label: '个人资料', icon: UserFilled },
    ],
  },
]

const navGroups = computed(() => navSections
  .map(section => ({
    ...section,
    items: section.items.filter(item => !item.adminOnly || authStore.isAdmin),
  }))
  .filter(section => section.items.length > 0)
)

const navItems = computed(() => navGroups.value.flatMap(group => group.items))

function isActive(path) {
  if (path === '/admin') return route.path === '/admin'
  return route.path.startsWith(path)
}

const routeTitles = {
  '/admin': '仪表盘',
  '/admin/works': '作品管理',
  '/admin/news': '新闻管理',
  '/admin/ai-tools': 'AI 工具管理',
  '/admin/users': '用户管理',
  '/admin/profile': '个人资料',
  '/admin/bg-music': '背景音乐',
  '/admin/logs': '操作日志',
  '/admin/majors': '专业管理',
  '/admin/competitions': '赛事管理',
}
const currentTitle = computed(() => {
  const matchedPath = Object.keys(routeTitles)
    .filter(path => path === '/admin' ? route.path === path : route.path.startsWith(path))
    .sort((a, b) => b.length - a.length)[0]
  return routeTitles[matchedPath] || '管理后台'
})

function handleBack() {
  router.push('/')
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-subtle);
  display: flex;
  flex-direction: column;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 100;
  transition: background 0.3s ease;
}

.sidebar-brand {
  height: 52px;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 0 20px;
  cursor: pointer;
  border-bottom: 1px solid var(--border-subtle);
}
.brand-mark { font-size: 16px; color: var(--accent); }
.brand-text {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  padding: 12px 10px 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
  overflow-y: auto;
}
.nav-group {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.nav-group-title {
  padding: 0 12px 4px;
  font-size: 10px;
  font-weight: 600;
  line-height: 1.4;
  color: var(--text-tertiary);
  letter-spacing: 0;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.2s ease;
}
.nav-item:hover { color: var(--text-primary); background: var(--bg-card-hover); }
.nav-item.active {
  color: var(--accent);
  background: rgba(0, 113, 227, 0.06);
}

/* Footer */
.sidebar-footer {
  padding: 12px 14px;
  border-top: 1px solid var(--border-subtle);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}
.user-name {
  font-size: 12px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.back-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: none;
  background: var(--bg-card);
  color: var(--text-tertiary);
  font-size: 11px;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
}
.back-btn:hover { color: var(--text-primary); background: var(--bg-card-hover); }

/* ── Main Area ── */
.main-area {
  flex: 1;
  margin-left: 220px;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.topbar {
  height: 52px;
  display: flex;
  align-items: center;
  padding: 0 28px;
  border-bottom: 1px solid var(--border-subtle);
  background: var(--bg-primary);
  position: sticky;
  top: 0;
  z-index: 50;
  transition: background 0.3s ease;
}

.page-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.content {
  flex: 1;
  padding: 28px;
  background: var(--bg-primary);
  transition: background 0.3s ease;
}
</style>
