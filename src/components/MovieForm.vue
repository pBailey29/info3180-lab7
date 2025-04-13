<template>
    <form id="movieForm" @submit.prevent="saveMovie">
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
  
      <button class="btn btn-primary" type="submit">Submit</button>
  
      <!-- Success Message -->
      <div v-if="successMessage" class="alert alert-success mt-3">
        {{ successMessage }}
      </div>
  
      <!-- Error Messages -->
      <div v-if="errorMessages.length" class="alert alert-danger mt-3">
        <ul>
          <li v-for="(msg, index) in errorMessages" :key="index">{{ msg }}</li>
        </ul>
      </div>
    </form>
  </template>
  
  <script setup>
  import { ref, onMounted } from "vue";
  
  const title = ref("");
  const description = ref("");
  const poster = ref(null);
  
  const csrf_token = ref("");
  const successMessage = ref("");
  const errorMessages = ref([]);
  
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
  
  onMounted(() => {
    getCsrfToken();
  });
  
  function saveMovie() {
    errorMessages.value = [];
    successMessage.value = "";
  
    const form_data = new FormData();
    form_data.append('title', title.value);
    form_data.append('description', description.value);
    form_data.append('poster', poster.value);
  
    fetch("/api/v1/movies", {
      method: 'POST',
      headers: {
        'X-CSRFToken': csrf_token.value
      },
      body: form_data
    })
      .then(response => response.json())
      .then(data => {
        if (data.errors) {
          errorMessages.value = Object.values(data.errors).flat();
        } else if (data.message) {
          successMessage.value = data.message;
          title.value = "";
          description.value = "";
          poster.value = null;
          document.getElementById("movieForm").reset(); // clears file input
        } else {
          errorMessages.value = ["Something went wrong. Please try again."];
        }
      })
      .catch(error => {
        errorMessages.value = ["An error occurred. Please try again."];
        console.error(error);
      });
  }
  </script>
  