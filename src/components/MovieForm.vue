<template>
  <form id="movieForm" @submit.prevent="saveMovie" enctype="multipart/form-data">
    <div class="form-group mb-3">
      <label for="title" class="form-label">Movie Title</label>
      <input v-model="title" type="text" name="title" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="description" class="form-label">Description</label>
      <textarea v-model="description" name="description" class="form-control"></textarea>
    </div>
    <div class="form-group mb-3">
      <label for="poster" class="form-label">Movie Poster</label>
      <input @change="handleFileUpload" type="file" name="poster" class="form-control" />
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
  </form>
</template>

<script setup>
import { ref, onMounted } from "vue";

let title = ref("");
let description = ref("");
let poster = ref(null);
let csrf_token = ref("");

function handleFileUpload(event) {
  poster.value = event.target.files[0];
}

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(res => res.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    });
}

function saveMovie() {
  const formData = new FormData();
  formData.append('title', title.value);
  formData.append('description', description.value);
  formData.append('poster', poster.value);

  fetch("/api/v1/movies", {
    method: "POST",
    body: formData,
    headers: {
      'X-CSRFToken': csrf_token.value
    }
  })
    .then(res => res.json())
    .then(data => {
      console.log(data);
    })
    .catch(err => {
      console.error(err);
    });
}

onMounted(() => {
  getCsrfToken();
});
</script>
