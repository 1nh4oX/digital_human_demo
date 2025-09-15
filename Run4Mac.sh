#!/bin/bash
# -------------------------------
# 一键启动 Vue + Three.js 项目（Mac）
# -------------------------------

# 1️⃣ 忽略虚拟环境对 PATH 的影响，确保系统 Node 在 PATH
export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH

# 2️⃣ 动态查找 Node 和 npx
NODE_PATH=$(which node || echo "")
NPX_PATH=$(which npx || echo "")

if [ -z "$NODE_PATH" ] || [ -z "$NPX_PATH" ]; then
  echo "❌ Node.js 或 npx 未找到，请先安装 Node.js"
  exit 1
fi

echo "✅ Node: $NODE_PATH"
echo "✅ npx:  $NPX_PATH"

# 3️⃣ 项目目录
PROJECT_DIR="$(cd "$(dirname "$0")/Front/digital-human-front" && pwd)"
cd "$PROJECT_DIR" || { echo "❌ 项目目录不存在: $PROJECT_DIR"; exit 1; }

# 4️⃣ 选择端口
PORT=8080
if lsof -i tcp:$PORT &> /dev/null; then
  echo "⚠️ 端口 $PORT 已被占用，使用临时端口 3000"
  PORT=3000
fi

# 5️⃣ 启动 http-server（使用绝对路径 npx）
$NPX_PATH http-server dist -p $PORT &

# 6️⃣ 延迟 2 秒确保服务器启动完成
sleep 2

# 7️⃣ 打开默认浏览器访问项目
open http://127.0.0.1:$PORT

echo "-------------------------------"
echo "✅ 项目已启动，请在浏览器查看效果"
echo "-------------------------------"