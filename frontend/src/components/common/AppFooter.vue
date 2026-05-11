<template>
  <footer class="app-footer">
    <div class="footer-inner">
      <div class="footer-text">
        <span>院赛作品展示与 AI 工具导航平台</span>
        <span class="footer-divider">|</span>
        <span>© 2024</span>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.app-footer {
  background: var(--bg-secondary);
  padding: 24px 0;
  margin-top: 80px;
}
.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  text-align: center;
}
.footer-text {
  font-size: 12px;
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}
.footer-divider { color: var(--border-subtle); }
</style>
