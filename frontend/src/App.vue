<template>
  <router-view />
</template>

<style>
/* ====== Apple Design System ====== */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f5f5f7;
  --bg-card: #ffffff;
  --bg-card-hover: #fafafa;
  --border-subtle: #d2d2d7;
  --border-hover: #86868b;
  --text-primary: #1d1d1f;
  --text-secondary: #86868b;
  --text-tertiary: #aeaeb2;
  --accent: #0071e3;
  --accent-hover: #0077ed;
  --link: #0066cc;
  --green: #34c759;
  --amber: #ff9500;
  --red: #ff3b30;
  --shadow-sm: rgba(0,0,0,0.06);
  --shadow-md: rgba(0,0,0,0.08);
  --shadow-lg: rgba(0,0,0,0.1);
  --input-bg: #ffffff;
  --header-bg: rgba(255, 255, 255, 0.8);
  --radius-sm: 8px;
  --radius-md: 18px;
  --radius-lg: 24px;
  --radius-pill: 980px;
  --font-display: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
  --font-body: "PingFang SC", "Helvetica Neue", Arial, sans-serif;
}

/* Dark theme */
[data-theme="dark"] {
  --bg-primary: #1d1d1f;
  --bg-secondary: #2d2d2f;
  --bg-card: #2d2d2f;
  --bg-card-hover: #3a3a3c;
  --border-subtle: #424245;
  --border-hover: #6e6e73;
  --text-primary: #f5f5f7;
  --text-secondary: #a1a1a6;
  --text-tertiary: #6e6e73;
  --accent: #2997ff;
  --accent-hover: #40a9ff;
  --link: #40a9ff;
  --green: #30d158;
  --amber: #ff9f0a;
  --red: #ff453a;
  --shadow-sm: rgba(0,0,0,0.2);
  --shadow-md: rgba(0,0,0,0.3);
  --shadow-lg: rgba(0,0,0,0.4);
  --input-bg: #3a3a3c;
  --header-bg: rgba(29, 29, 31, 0.8);
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  line-height: 1.6;
  font-size: 16px;
  transition: background 0.3s ease, color 0.3s ease;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(128,128,128,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(128,128,128,0.5); }

/* ====== Element Plus Global Overrides ====== */

/* Button */
.el-button--primary {
  --el-button-bg-color: var(--accent);
  --el-button-border-color: var(--accent);
  --el-button-hover-bg-color: var(--accent-hover);
  --el-button-hover-border-color: var(--accent-hover);
  --el-button-active-bg-color: var(--accent);
  --el-button-active-border-color: var(--accent);
  --el-button-text-color: #ffffff;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: -0.01em;
  border-radius: var(--radius-pill);
  padding: 8px 20px;
  transition: all 0.3s ease;
}
.el-button--default {
  border-radius: var(--radius-pill);
  font-weight: 500;
  font-size: 14px;
  padding: 8px 20px;
  transition: all 0.3s ease;
}

/* Card */
.el-card {
  background: var(--bg-card) !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  box-shadow: 0 2px 12px var(--shadow-sm) !important;
  color: var(--text-primary) !important;
}
.el-card__header {
  border-bottom: 1px solid var(--border-subtle) !important;
  color: var(--text-primary) !important;
}

/* Table */
.el-table {
  --el-table-bg-color: var(--bg-card);
  --el-table-tr-bg-color: var(--bg-card);
  --el-table-header-bg-color: var(--bg-secondary);
  --el-table-border-color: var(--border-subtle);
  --el-table-text-color: var(--text-primary);
  --el-table-header-text-color: var(--text-secondary);
  --el-table-row-hover-bg-color: var(--bg-card-hover);
}

/* Input */
.el-input__wrapper {
  background: var(--input-bg) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  box-shadow: none !important;
  transition: border-color 0.3s ease !important;
}
.el-input__inner { color: var(--text-primary) !important; }
.el-input__wrapper:hover { border-color: var(--border-hover) !important; }
.el-input__wrapper.is-focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(0,113,227,0.15) !important; }

/* Select */
.el-select .el-input__wrapper { background: var(--input-bg) !important; }
.el-select-dropdown { background: var(--bg-card) !important; border: 1px solid var(--border-subtle) !important; }
.el-select-dropdown__item { color: var(--text-primary) !important; }
.el-select-dropdown__item.hover, .el-select-dropdown__item:hover { background: var(--bg-card-hover) !important; }
.el-select-dropdown__item.selected { color: var(--accent) !important; }
.el-popper.is-light {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px var(--shadow-lg) !important;
}

/* Dialog */
.el-dialog {
  background: var(--bg-card) !important;
  border-radius: 20px !important;
  box-shadow: 0 20px 60px var(--shadow-lg) !important;
}
.el-dialog__header { border-bottom: 1px solid var(--border-subtle) !important; }
.el-dialog__title { color: var(--text-primary) !important; font-weight: 600 !important; }

/* Tabs */
.el-tabs__item {
  color: var(--text-secondary) !important;
  font-weight: 500;
}
.el-tabs__item.is-active { color: var(--accent) !important; }
.el-tabs__active-bar { background-color: var(--accent) !important; height: 2px !important; }
.el-tabs__nav-wrap::after { background-color: var(--border-subtle) !important; height: 1px !important; }

/* Pagination */
.el-pagination .el-pager li {
  color: var(--text-secondary) !important;
  background: transparent !important;
  border-radius: 8px !important;
}
.el-pagination .el-pager li.is-active {
  background: var(--accent) !important;
  color: #ffffff !important;
}
.el-pagination button {
  color: var(--text-secondary) !important;
  background: transparent !important;
}

/* Dropdown */
.el-dropdown-menu {
  background: var(--bg-card) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px var(--shadow-lg) !important;
  border: 1px solid var(--border-subtle) !important;
}
.el-dropdown-menu__item { color: var(--text-primary) !important; }
.el-dropdown-menu__item:hover { background: var(--bg-card-hover) !important; }

/* Empty */
.el-empty__description p { color: var(--text-tertiary) !important; }

/* Message */
.el-message {
  background: var(--bg-card) !important;
  border: 1px solid var(--border-subtle) !important;
  border-radius: 12px !important;
  box-shadow: 0 8px 32px var(--shadow-lg) !important;
}

/* Image error */
.el-image__error { background: var(--bg-secondary) !important; }

/* Switch */
.el-switch.is-checked .el-switch__core { background: var(--accent) !important; border-color: var(--accent) !important; }

/* Radio button */
.el-radio-button__inner {
  border-radius: var(--radius-pill) !important;
  background: var(--bg-card) !important;
  color: var(--text-secondary) !important;
  border-color: var(--border-subtle) !important;
}
.el-radio-button__original-radio:checked + .el-radio-button__inner {
  background: var(--accent) !important;
  color: #ffffff !important;
  border-color: var(--accent) !important;
}

/* Loading mask */
.el-loading-mask { background-color: var(--bg-primary) !important; opacity: 0.7; }
</style>
