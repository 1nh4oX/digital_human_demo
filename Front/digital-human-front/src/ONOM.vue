<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

const container = ref(null)

let scene, camera, renderer, controls, model, animationFrameId

const initThree = () => {
  scene = new THREE.Scene()

  camera = new THREE.PerspectiveCamera(
    45,
    container.value.clientWidth / container.value.clientHeight,
    0.1,
    1000
  )
  camera.position.set(0, 1.5, 3)

  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(container.value.clientWidth, container.value.clientHeight)
  container.value.appendChild(renderer.domElement)

  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6)
  scene.add(hemiLight)

  const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.6)
  dirLight1.position.set(5, 10, 7)
  scene.add(dirLight1)

  const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.4)
  dirLight2.position.set(-5, -10, -7)
  scene.add(dirLight2)

  const ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
  scene.add(ambientLight)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true

  const loader = new GLTFLoader()
  loader.load(
    window.location.origin + '/Tracer.glb',
    (gltf) => {
      model = gltf.scene
      model.position.y = -0.8
      scene.add(model)
    },
    undefined,
    (error) => {
      console.error('Fail! Un-fucking-able 2 Load Model:', error)
    }
  )
}

const animate = () => {
  animationFrameId = requestAnimationFrame(animate)
  if (model) {
    model.rotation.y += 0.005
  }
  controls.update()
  renderer.render(scene, camera)
}

const onResize = () => {
  if (!container.value) return
  camera.aspect = container.value.clientWidth / container.value.clientHeight
  camera.updateProjectionMatrix()
  renderer.setSize(container.value.clientWidth, container.value.clientHeight)
}

onMounted(() => {
  initThree()
  animate()
  window.addEventListener('resize', onResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  cancelAnimationFrame(animationFrameId)
  renderer.dispose()
  controls.dispose()
})

const isMuted = ref(false)
const isStopped = ref(false)

const inputText = ref('')
const messages = ref([])

const isGenerating = ref(false)
const isThinking = ref(false)
const stopRequested = ref(false)

import { CozeAPI } from '@coze/api'

const apiClient = new CozeAPI({
  token: 'cztei_qGn8N6FphI9OT3GbKrU02N4JCf1jH0oj8tlFOrPJtF7jaiP9oGbZ0XwpEEXug96Xh',
  baseURL: 'https://api.coze.cn',
})

const askCozeStream = async (userMessage, pushToken) => {
  try {
    const stream = await apiClient.chat.stream({
      bot_id: '7527898944106823690',
      user_id: 'Mono',
      additional_messages: [
        {
          content: userMessage,
          content_type: "text",
          role: "user",
          type: "question"
        }
      ]
    });

    let reply = '';
    for await (const event of stream) {
      if (event.event === 'conversation.message.delta') {
        const delta = event.data?.content || event.data?.message?.content;
        if (delta) {
          if (isThinking.value) isThinking.value = false; // 👈 加这行
          reply += delta;
          //console.log('当前累积回复:', reply);
          pushToken(reply);
        }
      }
    }
  } catch (err) {
    console.error('❌ Coze 连接失败：', err);
    pushToken('❌ 无法连接 Coze API');
  }
};

const sendMessage = async () => {
  if (!inputText.value.trim() || isGenerating.value) return

  const userMessage = inputText.value.trim()
  messages.value.push({ role: 'user', text: userMessage })
  inputText.value = ''

  isThinking.value = true
  isGenerating.value = true
  stopRequested.value = false

  let currentReply = ''
  messages.value.push({ role: 'ai', text: currentReply })

  const updateReply = (newText) => {
    currentReply = newText
    //console.log('更新内容:', currentReply)
    const lastIndex = messages.value.length - 1
    messages.value.splice(lastIndex, 1, { ...messages.value[lastIndex], text: currentReply })
  }

  await askCozeStream(userMessage, updateReply)

  isThinking.value = false
  isGenerating.value = false

  setTimeout(() => {
    const record = document.querySelector('.record')
    if (record) record.scrollTop = record.scrollHeight
  }, 100)
}

const stopGenerating = () => {
  stopRequested.value = true
  isThinking.value = false
  isGenerating.value = false
}
</script>

<template>
  <div class="Main">
    <div class="Dig_appearance">
      <div class="appearance" ref="container"></div>

      <div class="controls">
        <button class="mute" :class="{ active: isMuted }" @click="isMuted = !isMuted">🎤Mute</button>
        <button class="still" :class="{ active: isStopped }" @click="isStopped = !isStopped">🛑Stop</button>
      </div>
    </div>

    <div class="interact">
      <div class="record">
        <div v-for="(msg, index) in messages" :key="index" :class="['message', msg.role]">
          {{ msg.text }}
        </div>
      </div>
      <div class="input_box">
        <textarea
          class="question"
          placeholder="Type your question here..."
          v-model="inputText"
          @keyup.enter="sendMessage"
        ></textarea>
        <div class="send_button" @click="isGenerating ? stopGenerating() : sendMessage">
          {{ isGenerating ? 'Stop' : 'Send' }}
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.Main {
  width: 1560px;
  height:960px;
  min-width: 600px;
  min-height: 400px;
  background-color: white;
  border-radius: 20px;
  box-shadow: -10px 10px 30px rgba(0, 0, 0, 0.2);
  margin: 40px 0;
  padding: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4%;
  position: relative;
  margin-left: -150px; /* 距离左侧 100px */
}
.Dig_appearance,
.interact {
  width: 47%;
  height: 100%;
  box-sizing: border-box;
  background-color: honeydew;
  border: 1px solid #000;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}
.interact {
  gap: 20px;
}
.controls {
  position: absolute;
  bottom: 10px;
  left: 10px;
  display: flex;
  gap: 10px;
}
.controls button {
  background-color: #eee;
  border: none;
  border-radius: 8px;
  padding: 5px 10px;
  font-size: 12px;
  transition: background-color 0.2s ease;
}

.controls button.active {
  background-color: #50e3c2; /* 青绿色，表示开启 */
  color: white;
}
.appearance {
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.record {
  width: 95%;
  height: 70%;
  min-height: 350px;
  background-color: azure;
  border: 1px solid #000;
  border-radius: 12px;
  box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  position: relative;
  overflow-y: auto;
  overflow-x: hidden;
  margin-top: 10px;
  flex-shrink: 0;
}

.input_box {
  width: 80%;
  height: 20%;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  flex-shrink: 0;
}

.question {
  width: 100%;
  min-height: 40px;
  max-height: 72px;
  resize: none;
  overflow-y: auto;
  padding: 8px;
  font-size: 14px;
  border-radius: 6px;
  border: 1px solid #ccc;
  line-height: 1.4;
  box-sizing: border-box;
   font-size: 20px;
  line-height: 1.5;
  font-weight: 400; /* 稍微加粗 */
}

.send_button {
  width: 36px;
  height: 36px;
  position: absolute;
  right: 8px;
  bottom: 8px;
  background-color: #50e3c2;
  color: white;
  text-align: center;
  line-height: 36px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 14px;
}
</style>

<style>
html, body {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;      /* 垂直居中 */
}
body {
  margin: 0;
  padding: 0;
  background-color: azure;
  /* background: linear-gradient(
    to right,
    rgba(155, 47, 238, 0.8),
    rgba(100, 61, 255, 0.8)
  ); */
  font-family: sans-serif;
}
</style>

<style scoped>
.message {
  max-width: 80%;
  padding: 10px 14px;
  margin: 6px 0;
  font-size: 18px;
  line-height: 1.5;
  word-break: break-word;
  border-radius: 12px;
  position: relative;
  font-weight: 500;
}

.message.user {
  align-self: flex-end;
  background-color: #dcf8c6;
  color: #333;
  border-bottom-right-radius: 0;
}

.message.ai {
  align-self: flex-start;
  background-color: #f1f0f0;
  color: #0a529c;
  border-bottom-left-radius: 0;
}
.thinking .dots {
  font-size: 20px;
  color: #888;
  animation: breathing 1.5s ease-in-out infinite;
}

@keyframes breathing {
  0% { color: #333; }
  50% { color: #aaa; }
  100% { color: #333; }
}
</style>