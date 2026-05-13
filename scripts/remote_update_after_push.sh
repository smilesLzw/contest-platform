#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SERVER_USER="${SERVER_USER:-admin}"
SERVER_IP="${SERVER_IP:-47.108.139.130}"
PROJECT_DIR="${PROJECT_DIR:-/home/$SERVER_USER/project/contest-platform}"
BACKEND_SERVICE="${BACKEND_SERVICE:-contest-platform-backend}"
BRANCH="${1:-master}"
TARGET_SHA="${2:-$(git -C "$ROOT_DIR" rev-parse HEAD)}"
REMOTE="${REMOTE:-origin}"

echo "⏳ 等待 GitHub 上的 $BRANCH 更新到 $TARGET_SHA ..."
for _ in $(seq 1 60); do
  remote_sha="$(git -C "$ROOT_DIR" ls-remote "$REMOTE" "refs/heads/$BRANCH" | awk '{print $1}')"
  if [ "$remote_sha" = "$TARGET_SHA" ]; then
    break
  fi
  sleep 2
done

remote_sha="$(git -C "$ROOT_DIR" ls-remote "$REMOTE" "refs/heads/$BRANCH" | awk '{print $1}')"
if [ "$remote_sha" != "$TARGET_SHA" ]; then
  echo "❌ GitHub 分支 $BRANCH 未在超时时间内更新到目标提交，跳过服务器更新。"
  exit 1
fi

ssh "$SERVER_USER@$SERVER_IP" \
  "PROJECT_DIR='$PROJECT_DIR' BRANCH='$BRANCH' BACKEND_SERVICE='$BACKEND_SERVICE' bash -s" <<'REMOTE'
set -Eeuo pipefail

echo "📦 进入服务器项目目录：$PROJECT_DIR"
cd "$PROJECT_DIR"

echo "⬇️ 拉取最新代码..."
OLD_SHA="$(git rev-parse HEAD)"
git fetch origin "$BRANCH"
git checkout "$BRANCH"
git pull --ff-only origin "$BRANCH"
NEW_SHA="$(git rev-parse HEAD)"

if [ "$OLD_SHA" != "$NEW_SHA" ] && [ -n "$(git diff --name-only "$OLD_SHA" "$NEW_SHA" -- backend/alembic/versions)" ]; then
  echo "🧱 检测到数据库迁移文件变更，执行数据库迁移..."
  cd "$PROJECT_DIR/backend"
  if [ -x "venv/bin/alembic" ]; then
    venv/bin/alembic upgrade head
  else
    alembic upgrade head
  fi
  cd "$PROJECT_DIR"
else
  echo "💡 本次没有数据库迁移文件变更，跳过 alembic upgrade。"
fi

echo "🔁 尝试重启后端服务..."
if [ -n "$BACKEND_SERVICE" ] && command -v systemctl >/dev/null 2>&1; then
  if systemctl list-unit-files "$BACKEND_SERVICE.service" --no-legend >/dev/null 2>&1; then
    sudo -n systemctl restart "$BACKEND_SERVICE" || echo "⚠️ 后端服务重启失败，请手动检查 sudo 权限或服务名：$BACKEND_SERVICE"
  else
    echo "⚠️ 未找到 systemd 服务：$BACKEND_SERVICE，已跳过后端重启。"
  fi
fi

echo "🌐 尝试重载 Nginx..."
if command -v systemctl >/dev/null 2>&1 && systemctl list-unit-files nginx.service --no-legend >/dev/null 2>&1; then
  sudo -n systemctl reload nginx || echo "⚠️ Nginx 重载失败，请手动检查。"
fi

echo "✅ 服务器更新完成。"
REMOTE
