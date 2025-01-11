<template>
  <div id="app">
    <h1>File Upload and Search</h1>

    <h2>Upload File</h2>
    <input type="file" @change="handleFileUpload">
    <button @click="uploadFile">Upload</button>

    <h2>Search Data</h2>
    <input type="text" v-model="searchQuery" placeholder="Enter search query">
    <button @click="searchData">Search</button>

    <h2>Results</h2>
    <div v-if="results.length">
      <div v-for="(result, index) in results" :key="index">
        <p>{{ result.content }}</p>
        <hr>
      </div>
    </div>
    <div v-else>
      <p>No results found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      searchQuery: '',
      results: []
    };
  },
  methods: {
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0];
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert('Please select a file first.');
        return;
      }
      const formData = new FormData();
      formData.append('file', this.selectedFile);
      try {
        const response = await axios.post('/upload', formData);
        alert(response.data.message);
      } catch (error) {
        alert('File upload failed.');
      }
    },
    async searchData() {
      if (!this.searchQuery) {
        alert('Please enter a search query.');
        return;
      }
      try {
        const response = await axios.post('/search', { query: this.searchQuery });
        this.results = response.data.results || [];
      } catch (error) {
        alert('Search failed.');
      }
    }
  }
}
</script>

<style>
#app {
  text-align: center;
  margin-top: 30px;
}
input, button {
  margin: 5px;
}
</style>