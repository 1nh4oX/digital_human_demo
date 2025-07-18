<script setup>

import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

///////////////////////模型导入
// 关键对象--container
const container = ref(null)

let scene, camera, renderer, controls, model, animationFrameId

// 初始化元素，比如场景，模型，摄像头...
  // 同时包含加载模型
const initThree = () => {
  scene = new THREE.Scene()

  camera = new THREE.PerspectiveCamera(
    45,
    container.value.clientWidth / container.value.clientHeight,
    0.1,
    1000
  )
  camera.position.set(0, 1.5, 3)
  
  // 创建渲染器############
  renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true })
  renderer.setSize(container.value.clientWidth, container.value.clientHeight)
  container.value.appendChild(renderer.domElement)

  // 加灯光
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 0.6)
  scene.add(hemiLight)

  const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.6)
  dirLight1.position.set(5, 10, 7)
  scene.add(dirLight1)

  const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.4)
  dirLight2.position.set(-5, -10, -7)
  scene.add(dirLight2)

  // 环境灯
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.3)
  scene.add(ambientLight)

  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = true

  // 上传模型
  const loader = new GLTFLoader()
  loader.load(
    window.location.origin + '/Tracer.glb',
    (gltf) => {
      model = gltf.scene
      model.position.y = -0.8
      scene.add(model)

      // console.log("GLTF 内容:", gltf)
      // console.log("骨架结构:", gltf.scene.children)
    },
    undefined,
    (error) => {
      console.error('Fail! Un-fucking-able 2 Load Model:', error)
    }
  )
}

// set movements
const animate = () => {
  animationFrameId = requestAnimationFrame(animate)
  if (model) {
    model.rotation.y += 0.005 // 转圈->为了展示模型（后期改为具体动作）
  }
  controls.update()
  renderer.render(scene, camera)
}


// 保持等比适应变化
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

///////////////////页面设置
// 设置两个控制模型的按钮状态
const isMuted = ref(false)
const isStopped = ref(false)

// 新增对话内容及输入框响应式变量
const inputText = ref('')
const messages = ref([])

const sendMessage = async () => {
  if (!inputText.value.trim()) return

  const userMessage = inputText.value.trim()
  messages.value.push({ role: 'user', text: userMessage })
  inputText.value = ''

  try {
    const res = await fetch('http://127.0.0.1:5200/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: userMessage })
    })

    if (!res.ok) throw new Error('服务器响应异常')

    const data = await res.json()
    messages.value.push({ role: 'ai', text: data.reply })
  } catch (err) {
    messages.value.push({ role: 'ai', text: '❌ 后端未响应，请检查 Flask 是否启动' })
  }

  setTimeout(() => {
    const record = document.querySelector('.record')
    if (record) record.scrollTop = record.scrollHeight
  }, 100)
}
</script>

<template>
  <div class="Main">
    <div class="Dig_appearance">
      <div 
        class="appearance" 
        ref="container">
      </div>
      
      <div class="controls">
        <button 
          class="mute"
          :class="{ active:isMuted }"
          @click="isMuted=!isMuted"
        >
          🎤Mute
        </button>
        <button 
          class="still"
          :class="{ active:isStopped}"
          @click="isStopped=!isStopped"
          >
          🛑Stop
        </button>

      </div>
    </div>

    <div class="interact">
      <div class="record">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.role]"
        >
          {{ msg.role === 'user' ? 'User: ' : 'ONOM: ' }}{{ msg.text }}
        </div>
      </div>
      <div class="input_box">
        <textarea
          class="question"
          placeholder="Type your question here..."
          v-model="inputText"
          @keyup.enter="sendMessage"
        ></textarea>
        <div class="send_button" @click="sendMessage">Send</div>
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
  width: 90%;
  margin: 6px 0;
  font-size: 25px;
  line-height: 1.5;
  word-break: break-word;
  font-weight: 600; /* 稍微加粗 */
}
.message.user {
  text-align: right;
  color: #333;
}
.message.ai {
  text-align: left;
  color: #0a529c;
}
</style>