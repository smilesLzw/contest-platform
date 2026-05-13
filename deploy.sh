#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SERVER_USER="${SERVER_USER:-admin}"
SERVER_IP="${SERVER_IP:-47.108.139.130}"
PROJECT_DIR="${PROJECT_DIR:-/home/$SERVER_USER/project/contest-platform}"
BRANCH="${BRANCH:-$(git -C "$ROOT_DIR" rev-parse --abbrev-ref HEAD)}"
REMOTE="${REMOTE:-origin}"
TARGET_SHA="$(git -C "$ROOT_DIR" rev-parse HEAD)"

echo "🚀 开始本地构建前端..."
cd "$ROOT_DIR/frontend"
npm run build
echo "✅ 前端构建完成！"

echo "☁️ 正在将前端打包文件同步到服务器..."
rsync -avz --delete "$ROOT_DIR/frontend/dist/" "$SERVER_USER@$SERVER_IP:$PROJECT_DIR/frontend/dist/"

echo "⬆️ 正在推送代码到 GitHub..."
DEPLOY_SKIP_PRE_PUSH=1 git -C "$ROOT_DIR" push "$REMOTE" "$BRANCH"

echo "🔄 触发服务器执行 git pull、迁移与重启..."
"$ROOT_DIR/scripts/remote_update_after_push.sh" "$BRANCH" "$TARGET_SHA"

echo "🎉 全部部署完成！"
