<script setup>
import { ref, onMounted, computed } from 'vue'

const props = defineProps({
  parentId: Number
})

const emit = defineEmits(['comment-added', 'cancel-reply'])

const username = ref('')
const email = ref('')
const homepage = ref('')
const text = ref('')
const captcha = ref('')
const image = ref(null)
const textFile = ref(null)
const captchaUrl = ref('')
const captchaToken = ref('')
const textArea = ref(null)

async function loadCaptcha() {
  const response = await fetch('https://commentsapp-production-4919.up.railway.app/captcha/', { credentials: 'include' })
  captchaToken.value = response.headers.get('X-Captcha-Token')
  console.log('captcha token:', captchaToken.value)
  const blob = await response.blob()
  captchaUrl.value = URL.createObjectURL(blob)
}

onMounted(() => loadCaptcha())

function handleImageUpload(event) { image.value = event.target.files[0] }
function handleTextUpload(event) { textFile.value = event.target.files[0] }

function insertTag(openTag, closeTag) {
  const el = textArea.value
  const start = el.selectionStart
  const end = el.selectionEnd
  const selected = text.value.substring(start, end)
  text.value = text.value.substring(0, start) + openTag + selected + closeTag + text.value.substring(end)
}

function insertLink() {
  const href = prompt('URL:')
  const title = prompt('Title:')
  if (href) insertTag(`<a href="${href}" title="${title || ''}">`, '</a>')
}

const preview = computed(() => text.value
  .replace(/<strong>(.*?)<\/strong>/g, '<strong>$1</strong>')
  .replace(/<i>(.*?)<\/i>/g, '<i>$1</i>')
  .replace(/<code>(.*?)<\/code>/g, '<code>$1</code>')
  .replace(/<a href="(.*?)".*?>(.*?)<\/a>/g, '<a href="$1">$2</a>')
)

async function submitComment() {
  if (!username.value || !email.value || !text.value || !captcha.value) {
    alert('Please fill in all required fields')
    return
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email.value)) {
    alert('Invalid email format')
    return
  }
  if (homepage.value && !/^https?:\/\/.+/.test(homepage.value)) {
    alert('Homepage must be a valid URL (http:// or https://)')
    return
  }
  const usernameRegex = /^[a-zA-Z0-9]+$/
  if (!usernameRegex.test(username.value)) {
    alert('Username must contain only letters and digits')
    return
  }

  const formData = new FormData()
  formData.append('username', username.value)
  formData.append('email', email.value)
  formData.append('homepage', homepage.value)
  formData.append('text', text.value)
  formData.append('captcha', captcha.value)
  formData.append('captcha_token', captchaToken.value)
  if (image.value) formData.append('image', image.value)
  if (textFile.value) formData.append('text_file', textFile.value)
  if (props.parentId) formData.append('parent', props.parentId)

  const response = await fetch('https://commentsapp-production-4919.up.railway.app/comments/', {
    method: 'POST',
    body: formData,
    credentials: 'include'
  })

  const data = await response.json()

  if (response.ok) {
    username.value = ''
    email.value = ''
    homepage.value = ''
    text.value = ''
    captcha.value = ''
    image.value = null
    textFile.value = null
    loadCaptcha()
    emit('comment-added')
    emit('cancel-reply')
  } else {
    alert(data.detail || 'Error submitting comment')
    loadCaptcha()
  }
}
</script>

<template>
  <div class="comment-form">

    <div v-if="props.parentId" class="reply-indicator">
      <span>Replying to comment #{{ props.parentId }}</span>
      <button @click="emit('cancel-reply')">Cancel</button>
    </div>

    <h2>Add Comment</h2>

    <div class="form-row">
      <input v-model="username" placeholder="Username *" />
      <input v-model="email" placeholder="Email *" />
      <input v-model="homepage" placeholder="Homepage" />
    </div>

    <div class="toolbar">
      <button type="button" @click="insertTag('<strong>', '</strong>')">B</button>
      <button type="button" @click="insertTag('<i>', '</i>')">i</button>
      <button type="button" @click="insertTag('<code>', '</code>')">code</button>
      <button type="button" @click="insertLink()">link</button>
    </div>

    <textarea v-model="text" ref="textArea" placeholder="Comment text *"></textarea>

    <div v-if="text" class="preview">
      <strong>Preview</strong>
      <div v-html="preview"></div>
    </div>

    <div class="file-row">
      <input type="file" accept="image/*" @change="handleImageUpload" />
      <input type="file" accept=".txt" @change="handleTextUpload" />
    </div>

    <div class="captcha-row">
      <img v-if="captchaUrl" :src="captchaUrl" alt="captcha" />
      <input v-model="captcha" placeholder="Captcha *" />
    </div>

    <button class="submit" @click="submitComment">Submit</button>

  </div>
</template>