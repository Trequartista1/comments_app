<script setup>
import { ref, onMounted, watch } from 'vue'
import CommentItem from './components/CommentItem.vue'
import CommentForm from './components/CommentForm.vue'

const comments = ref([])
const currentPage = ref(1)
const ordering = ref('-created_at')
const totalPages = ref(1)
const replyTo = ref(null)
const lightboxOpen = ref(false)
const lightboxSrc = ref('')

function openLightbox(src) {
  lightboxSrc.value = src
  lightboxOpen.value = true
}

function closeLightbox() {
  lightboxOpen.value = false
}

async function fetchComments() {
  const response = await fetch(
    `https://commentsapp-production-4919.up.railway.app/comments/?page=${currentPage.value}&ordering=${ordering.value}`
  )
  const data = await response.json()
  comments.value = data.results
  totalPages.value = Math.ceil(data.count / 25)
}

onMounted(() => {
  fetchComments()

  const ws = new WebSocket('wss://commentsapp-production-4919.up.railway.app/ws/comments/')

  ws.onmessage = (event) => {
    const newComment = JSON.parse(event.data)
    if (!newComment.parent) {
      comments.value.unshift(newComment)
    } else {
      fetchComments()
    }
  }
})

watch(ordering, () => {
  currentPage.value = 1
  fetchComments()
})

watch(currentPage, () => {
  fetchComments()
})
</script>

<template>
  <div>
    <h1>Comments App</h1>

    <CommentForm
      :parent-id="replyTo"
      @comment-added="fetchComments"
      @cancel-reply="replyTo = null"
    />

    <table border="1" style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th @click="ordering = ordering === 'username' ? '-username' : 'username'" style="cursor:pointer">
            User Name {{ ordering.includes('username') ? (ordering === 'username' ? '↑' : '↓') : '' }}
          </th>
          <th @click="ordering = ordering === 'email' ? '-email' : 'email'" style="cursor:pointer">
            E-mail {{ ordering.includes('email') ? (ordering === 'email' ? '↑' : '↓') : '' }}
          </th>
          <th @click="ordering = ordering === 'created_at' ? '-created_at' : 'created_at'" style="cursor:pointer">
            Дата {{ ordering.includes('created_at') ? (ordering === '-created_at' ? '↓' : '↑') : '' }}
          </th>
          <th>Сообщение</th>
        </tr>
      </thead>
      <tbody>
        <template v-for="comment in comments" :key="comment.id">
          <tr>
            <td>{{ comment.username }}</td>
            <td>{{ comment.email }}</td>
            <td>{{ new Date(comment.created_at).toLocaleString() }}</td>
            <td>
              <span v-html="comment.text"></span>
              <img
                v-if="comment.image"
                :src="comment.image"
                style="max-width:320px; display:block; cursor:pointer;"
                @click="openLightbox(comment.image)"
              />
              <a v-if="comment.text_file" :href="comment.text_file" target="_blank">Download TXT</a>
              <button @click="replyTo = comment.id">Reply</button>
            </td>
          </tr>
          <tr v-if="comment.replies && comment.replies.length" :key="'replies-' + comment.id">
            <td colspan="4" style="padding-left: 40px; background: #f9f9f9;">
              <CommentItem
                v-for="reply in comment.replies"
                :key="reply.id"
                :comment="reply"
                @reply="replyTo = $event"
              />
            </td>
          </tr>
        </template>
      </tbody>
    </table>

    <div class="pagination">
      <button @click="currentPage--" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} / {{ totalPages }}</span>
      <button @click="currentPage++" :disabled="currentPage === totalPages">Next</button>
    </div>

    <!-- Lightbox -->
    <teleport to="body">
      <div
        v-if="lightboxOpen"
        @click="closeLightbox"
        style="
          position: fixed;
          inset: 0;
          background: rgba(0,0,0,0.85);
          display: flex;
          align-items: center;
          justify-content: center;
          z-index: 9999;
          cursor: zoom-out;
          animation: fadeIn 0.2s ease;
        "
      >
        <img
          :src="lightboxSrc"
          style="
            max-width: 90vw;
            max-height: 90vh;
            border-radius: 8px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            animation: scaleIn 0.2s ease;
          "
          @click.stop
        />
      </div>
    </teleport>

  </div>
</template>

<style>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>