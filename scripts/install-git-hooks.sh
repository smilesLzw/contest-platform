#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOKS_DIR="$ROOT_DIR/.git/hooks"
SOURCE_DIR="$ROOT_DIR/scripts/git-hooks"

if [ ! -d "$HOOKS_DIR" ]; then
  echo "❌ 未找到 .git/hooks，请在项目 Git 仓库内执行。"
  exit 1
fi

install -m 755 "$SOURCE_DIR/pre-push" "$HOOKS_DIR/pre-push"
install -m 755 "$SOURCE_DIR/post-commit" "$HOOKS_DIR/post-commit"

echo "✅ Git hooks 已安装。commit 只提交；push master 前会构建 dist 并触发服务器更新。"
