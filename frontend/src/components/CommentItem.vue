<script setup>

defineOptions({
  name: 'CommentItem'
})

defineProps({
  comment: Object
})

const emit = defineEmits([
  'reply'
])

</script>


<template>

  <div class="comment">

    <h3>
      {{ comment.username }}
    </h3>

    <p v-html="comment.text"></p>

    <div v-if="comment.image">

    <img
      :src="comment.image"
      alt="uploaded image"
      style="max-width: 320px;"
    />

    </div>


    <div v-if="comment.text_file">

    <a
      :href="comment.text_file"
      target="_blank"
    >
      Download TXT file
    </a>

    </div>
    <button
       @click="emit('reply', comment.id)"
    >
       Reply
    </button>

    <div
      v-if="comment.replies.length"
      class="replies"
      style="margin-left: 40px;"
    >

    <CommentItem
      v-for="reply in comment.replies"
      :key="reply.id"
      :comment="reply"
      @reply="emit('reply', $event)"
    />

    </div>

  </div>

</template>