import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  // 主应用布局（所有前台页面）
  {
    path: '/',
    component: () => import('../components/common/AppLayout.vue'),
    children: [
      // 公开路由
      { path: '', name: 'Home', component: () => import('../views/public/HomeView.vue') },
      { path: 'works', name: 'Works', component: () => import('../views/public/WorksView.vue') },
      { path: 'works/:id', name: 'WorkDetail', component: () => import('../views/public/WorkDetailView.vue') },
      { path: 'news', name: 'News', component: () => import('../views/public/NewsView.vue') },
      { path: 'news/:id', name: 'NewsDetail', component: () => import('../views/public/NewsDetailView.vue') },
      { path: 'ai-tools', name: 'AiTools', component: () => import('../views/public/AiToolsView.vue') },
      // 教师中心（需登录）
      { path: 'profile', name: 'Profile', component: () => import('../views/teacher/ProfileView.vue'), meta: { requiresAuth: true } },
      { path: 'my/works', name: 'MyWorks', component: () => import('../views/teacher/MyWorksView.vue'), meta: { requiresAuth: true } },
      { path: 'my/works/create', name: 'WorkCreate', component: () => import('../views/teacher/WorkFormView.vue'), meta: { requiresAuth: true } },
      { path: 'my/works/:id/edit', name: 'WorkEdit', component: () => import('../views/teacher/WorkFormView.vue'), meta: { requiresAuth: true } },
      { path: 'my/news', name: 'MyNews', component: () => import('../views/teacher/MyNewsView.vue'), meta: { requiresAuth: true } },
      { path: 'my/news/create', name: 'NewsCreate', component: () => import('../views/teacher/NewsFormView.vue'), meta: { requiresAuth: true } },
      { path: 'my/news/:id/edit', name: 'NewsEdit', component: () => import('../views/teacher/NewsFormView.vue'), meta: { requiresAuth: true } },
    ],
  },

  // 管理后台登录（独立页面，不嵌套在任何布局内）
  { path: '/admin/login', name: 'AdminLogin', component: () => import('../views/admin/AdminLoginView.vue') },

  // 管理后台（需管理员）
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      { path: '', name: 'AdminDashboard', component: () => import('../views/admin/AdminDashboard.vue') },
      { path: 'works', name: 'AdminWorks', component: () => import('../views/admin/AdminWorksView.vue') },
      { path: 'works/create', name: 'AdminWorkCreate', component: () => import('../views/teacher/WorkFormView.vue') },
      { path: 'works/:id/edit', name: 'AdminWorkEdit', component: () => import('../views/teacher/WorkFormView.vue') },
      { path: 'news', name: 'AdminNews', component: () => import('../views/admin/AdminNewsView.vue') },
      { path: 'news/create', name: 'AdminNewsCreate', component: () => import('../views/teacher/NewsFormView.vue') },
      { path: 'news/:id/edit', name: 'AdminNewsEdit', component: () => import('../views/teacher/NewsFormView.vue') },
      { path: 'ai-tools', name: 'AdminAiTools', component: () => import('../views/admin/AdminAiToolsView.vue') },
      { path: 'users', name: 'AdminUsers', component: () => import('../views/admin/AdminUsersView.vue') },
      { path: 'profile', name: 'AdminProfile', component: () => import('../views/teacher/ProfileView.vue') },
      { path: 'bg-music', name: 'AdminBgMusic', component: () => import('../views/admin/AdminBgMusic.vue') },
      { path: 'logs', name: 'AdminLogs', component: () => import('../views/admin/AdminLogsView.vue') },
      { path: 'majors', name: 'AdminMajors', component: () => import('../views/admin/AdminMajorsView.vue') },
      { path: 'competitions', name: 'AdminCompetitions', component: () => import('../views/admin/AdminCompetitionsView.vue') },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  let userInfo = null
  try {
    userInfo = JSON.parse(localStorage.getItem('userInfo') || 'null')
  } catch {
    userInfo = null
  }

  // 需要登录但未登录 → 跳转管理员登录页
  if (to.meta.requiresAuth && !token) {
    next('/admin/login')
    return
  }

  // 需要管理员但角色不是 admin → 跳转管理员登录页
  if (to.meta.requiresAdmin && userInfo?.role !== 'admin') {
    next('/admin/login')
    return
  }

  next()
})

export default router
