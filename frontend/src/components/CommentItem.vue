<script setup>
import { ref } from 'vue'

defineOptions({
  name: 'CommentItem'
})

defineProps({
  comment: Object
})

const emit = defineEmits(['reply'])

const lightboxOpen = ref(false)
const lightboxSrc = ref('')

function openLightbox(src) {
  lightboxSrc.value = src
  lightboxOpen.value = true
}

function closeLightbox() {
  lightboxOpen.value = false
}
</script>

<template>
  <div class="comment">

    <h3>{{ comment.username }}</h3>

    <p v-html="comment.text"></p>

    <div v-if="comment.image">
      <img
        :src="comment.image"
        alt="uploaded image"
        style="max-width: 320px; cursor: pointer;"
        @click="openLightbox(comment.image)"
      />
    </div>

    <div v-if="comment.text_file">
      <a :href="comment.text_file" target="_blank">Download TXT file</a>
    </div>

    <button @click="emit('reply', comment.id)">Reply</button>

    <div v-if="comment.replies.length" class="replies" style="margin-left: 40px;">
      <CommentItem
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        @reply="emit('reply', $event)"
      />
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

<style scoped>
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes scaleIn {
  from { transform: scale(0.8); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}
</style>