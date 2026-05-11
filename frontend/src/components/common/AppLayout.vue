<template>
  <el-container direction="vertical">
    <AppHeader />
    <el-main class="main-content">
      <router-view />
    </el-main>
    <AppFooter />
  </el-container>
</template>

<script setup>
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'
</script>

<style scoped>
.main-content {
  min-height: calc(100vh - 112px);
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 24px;
  overflow: visible;
}
</style>
