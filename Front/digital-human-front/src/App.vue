<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import { ref } from 'vue'

const question = ref('')

function sendQuestion() {
  // placeholder for send button click event
}
</script>

<template>
  <div class="Main">

    <div class="Dig_appearance">

      <div class="appearance"></div>
      <div class="mute"></div>
      <div class="still"></div>

    </div>

    <div class="interact">

      <div class="input_box">
        <input type="text" class="question" v-model="question" placeholder="Type your question here..." />
        <div class="send_button" @click="sendQuestion"></div>
      </div>

      <div class="record"></div>
      
    </div>
  </div>
</template>

<style scoped>
.Main {
  width: 800px;
  height: 600px;
  background-color: white;
  border-radius: 20px;
  box-shadow: -10px 10px 30px rgba(0, 0, 0, 0.2);
  margin: 40px 0;
  padding: 20px;
}

.Main {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4%;
}

.Dig_appearance,
.interact {
  width: 47%;
  height: 100%;
  background-color: #f0f0f0;
  border: 1px solid #000;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
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
  background: linear-gradient(
    to right,
    rgba(155, 47, 238, 0.8),
    rgba(100, 61, 255, 0.8)
  );
  font-family: sans-serif;
}
</style>
