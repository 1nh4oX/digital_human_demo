<script setup>
import { ref } from 'vue'
import { CozeAPI } from '@coze/api'

import { nextTick } from 'vue'

const scrollToBottom = () => {
  nextTick(() => {
    const record = document.querySelector('.record')
    if (record) {
      record.scrollTop = record.scrollHeight
    }
  })
}

// ------------------------
// Coze API 部分
// ------------------------
const COZE_TOKEN = ref('')
let apiClient = null

fetch('./config.json')
  .then(res => res.json())
  .then(data => {
    COZE_TOKEN.value = data.COZE_TOKEN
    apiClient = new CozeAPI({
      token: COZE_TOKEN.value,
      baseURL: 'https://api.coze.cn'
    })
  })
  .catch(err => console.error('读取 config.json 出错:', err))

const inputText = ref('')
const messages = ref([
  { role: 'ai', text: '你好！我是南特金融科技学院的智能招生助手。有什么关于学院招生的问题，我可以帮你解答？' }
])
const isGenerating = ref(false)
const isThinking = ref(false)
const stopRequested = ref(false)

const askCozeStream = async (userMessage, pushToken) => {
  if (!apiClient) {
    console.error('❌ Coze API 尚未初始化')
    pushToken('❌ Coze API 未初始化')
    return
  }
  try {
    const stream = await apiClient.chat.stream({
      bot_id: '7527930097362911232',
      user_id: 'Mono',
      additional_messages: [
        { content: userMessage, content_type: "text", role: "user", type: "question" }
      ]
    })
    let reply = ''
    for await (const event of stream) {
      if (event.event === 'conversation.message.delta') {
        const delta = event.data?.content || event.data?.message?.content
        if (delta) {
          if (isThinking.value) isThinking.value = false
          reply += delta
          pushToken(reply)
        }
      }
    }
  } catch (err) {
    console.error('❌ Coze 连接失败：', err)
    pushToken('❌ 无法连接 Coze API')
  }
}

const sendMessage = async () => {
  if (!inputText.value.trim() || isGenerating.value) return

  const userMessage = inputText.value.trim()
  messages.value.push({ role: 'user', text: userMessage })
  inputText.value = ''

  isThinking.value = true
  isGenerating.value = true
  stopRequested.value = false

  let currentReply = '...'
  const aiMsgIndex = messages.value.push({ role: 'ai', text: currentReply }) - 1

  const updateReply = (newText) => {
    currentReply = newText
    messages.value.splice(aiMsgIndex, 1, { role: 'ai', text: currentReply })
    scrollToBottom()
  }

  await askCozeStream(userMessage, updateReply)

  isThinking.value = false
  isGenerating.value = false
}

const stopGenerating = () => {
  stopRequested.value = true
  isThinking.value = false
  isGenerating.value = false
}

const insertQuestion = (q) => {
  inputText.value = q
}
</script>

<template>
  <div class="app">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-left">
        <img src="/Logo.jpg" alt="logo" class="logo">
        <div>
          <h1>南特金融科技学院</h1>
          <p>招生咨询智能助手</p>
        </div>
      </div>
      <div class="navbar-right">
        <a href="https://www.720yun.com/t/d8vktwr9sfy?scene_id=72926475">校园一览</a>
        <a href="https://mp.weixin.qq.com/s/w57Haz68cE7JRb7foSXK7w">招生宣传片</a>
        <a href="https://safti.szu.edu.cn/">学院官网</a>
      </div>
    </nav>

    <!-- 主内容区 -->
    <main class="main">
      <!-- 左侧信息 -->
      <aside class="sidebar">
        <h2><i class="fa fa-info-circle"></i> 学院简介</h2>
        <p>
          南特金融科技学院是深圳大学与法国南特高等商学院合作举办，
          是全国首个聚焦金融科技领域开展中外合作办学的非独立法人机构。
        </p>

        <h2><i class="fa fa-graduation-cap"></i> 热门咨询问题</h2>
        <ul>
          <li @click="insertQuestion('学院的招生专业有哪些？')">学院的招生专业有哪些？</li>
          <li @click="insertQuestion('双学位项目的具体要求是什么？')">双学位项目的具体要求是什么？</li>
          <li @click="insertQuestion('学院的师资力量如何？')">学院的师资力量如何？</li>
          <li @click="insertQuestion('毕业生的就业方向有哪些？')">毕业生的就业方向有哪些？</li>
        </ul>
      </aside>

      <!-- 聊天面板 -->
      <section class="chat">
        <header class="chat-header">
          <img src="/Profile.png" alt="机器人头像" class="avatar">
          <div>
            <h3>智能招生助手</h3>
            <p>我可以回答你关于学院招生的问题</p>
          </div>
        </header>

        <div class="chat-body record">
          <div v-for="(msg, index) in messages" :key="index" :class="['msg', msg.role]">
            <p>{{ msg.text }}</p>
          </div>
          <div v-if="isThinking" class="typing">思考中...</div>
        </div>

        <footer class="chat-footer">
          <input v-model="inputText" @keyup.enter="sendMessage" type="text" placeholder="请输入你的问题...">
          <button @click="isGenerating ? stopGenerating() : sendMessage">
            <i class="fa fa-paper-plane"></i>发送
          </button>
        </footer>
        <p class="hint">输入 "菜单" 查看常见问题，或输入 "转人工" 联系招生办老师</p>
      </section>
    </main>

    <!-- 联系方式 -->
    <div class="contact">
      <h2><i class="fa fa-phone"></i> 联系方式</h2>
      <div class="info">
        <span><i class="fa fa-envelope-o"></i> 邮箱：safti-admission@szu.edu.cn</span>
        <span><i class="fa fa-phone"></i> 电话：0755-26531523</span>
        <span><i class="fa fa-map-marker"></i> 地址：广东省深圳市南山区南海大道3688号</span>
      </div>
    </div>

    <!-- 页脚 -->
    <footer class="footer">
      <p>© 2025 南特金融科技学院. 保留所有权利.</p>
      <div>
        <i class="fa fa-weixin"></i>
        <i class="fa fa-weibo"></i>
        <i class="fa fa-linkedin"></i>
      </div>
    </footer>
  </div>
</template>

<style scoped>
/* 全局 */
.app {
  font-family: 'Inter', sans-serif;
  background: #fff;
  color: #1D2129;
  min-height: 100vh;
  width: 100%;          /* ✅ 用百分比而不是 vw */
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  display: flex;
  gap: 20px;
  padding: 20px;
  width: 100%;          /* ✅ 占满屏幕 */
  max-width: none;      /* ✅ 禁止收窄 */
  min-height: 0;   /* 🚀 保证内部滚动，而不是撑开外部 */
  margin: 0;            /* ✅ 禁止居中 */
  box-sizing: border-box;
}
/* 导航栏 */
.navbar {
  background: #fff;
  box-shadow: 0 2px 6px rgba(0,0,0,0.05);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  position: sticky;
  top: 0;
  z-index: 50;
}
.navbar-left {
  display: flex;
  align-items: center;
  gap: 10px;
}
.logo {
  width: 40px;
  height: 40px;
  border-radius: 8px;
}
.navbar-left h1 {
  font-size: 18px;
  font-weight: bold;
  color: #0055A5;
}
.navbar-left p {
  font-size: 12px;
  color: #666;
}
.navbar-right a {
  margin-left: 20px;
  font-size: 14px;
  color: #555;
  text-decoration: none;
}
.navbar-right a:hover {
  color: #0055A5;
}

/* 主内容区 */

.sidebar {
  width: 30%;
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
.sidebar h2 {
  font-size: 16px;
  font-weight: bold;
  color: #0055A5;
  margin: 16px 0 8px;
}
.sidebar p {
  font-size: 14px;
  color: #444;
  line-height: 1.6;
}
.sidebar ul {
  list-style: none;
  padding: 0;
}
.sidebar li {
  padding: 8px;
  background: #F5F7FA;
  border-radius: 6px;
  margin-bottom: 6px;
  cursor: pointer;
  transition: background 0.2s;
}
.sidebar li:hover {
  background: #EAF3FF;
}

.sidebar {
  flex: 0 0 30%;   /* ✅ 固定 30% 宽 */
  max-width: 30%;
}

.chat {
  flex: 1;         /* ✅ 自动填满剩余空间 */
  min-width: 0;    /* ✅ 防止撑破 */
}

/* 聊天 */
.chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: 100%;      /* 🚀 确保它不会被内容撑高 */
  min-height: 0;     /* 🚀 防止 flex 子元素溢出 */
}
.chat-header {
  display: flex;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}
.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 12px;
}
.chat-header h3 {
  font-weight: bold;
  color: #0055A5;
}
.chat-header p {
  font-size: 12px;
  color: #666;
}
.chat-body {
  flex: 1;
  min-height: 0;      /* 🚀 防止撑开父级 */
  padding: 12px;
  overflow-y: auto;
  overflow-x: hidden;
  word-wrap: break-word;
  word-break: break-word;
}
.msg {
  margin-bottom: 10px;
  max-width: 70%;   /* ✅ 不超过聊天区的 70% */
  padding: 10px;
  border-radius: 8px;
  word-wrap: break-word;
  word-break: break-word;
}
.msg.user {
  margin-left: auto;
  background: #0055A5;
  color: white;
  border-bottom-right-radius: 0;
}
.msg.ai {
  margin-right: auto;
  background: #F5F7FA;
  color: #333;
  border-bottom-left-radius: 0;
}
.typing {
  font-style: italic;
  color: #888;
  animation: blink 1.5s infinite;
}
@keyframes blink {
  0%, 100% { opacity: 0; }
  50% { opacity: 1; }
}
.chat-footer {
  display: flex;
  align-items: center;
  padding: 12px;
  border-top: 1px solid #eee;
}
.chat-footer input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
}
.chat-footer button {
  margin-left: 8px;
  padding: 8px 12px;
  border: none;
  border-radius: 50%;
  background: #0055A5;
  color: white;
  cursor: pointer;
}
.hint {
  font-size: 12px;
  text-align: center;
  color: #666;
  margin: 8px 0;
}

/* 联系方式 */
.contact {
  background: #F5F7FA;
  padding: 20px;
  border-top: 1px solid #ddd;
}
.contact h2 {
  color: #0055A5;
  font-size: 16px;
  margin-bottom: 12px;
}
.contact .info {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  font-size: 14px;
}

/* 页脚 */
.footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fff;
  border-top: 1px solid #eee;
  padding: 12px 20px;
  font-size: 14px;
  color: #555;
}
.footer i {
  margin-left: 10px;
  cursor: pointer;
  transition: color 0.2s;
}
.footer i:hover {
  color: #0055A5;
}
</style>


<style>
html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background: #fff;   /* 防止出现黑边 */
}

#app {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.app {
  flex: 1;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.main {
  flex: 1;
  display: flex;
  width: 100%;       /* ✅ 铺满 */
  height: 100%;      /* ✅ 铺满 */
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}
</style>