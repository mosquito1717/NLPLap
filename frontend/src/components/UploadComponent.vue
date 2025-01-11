<template>
  <div>
    <h2>Upload File</h2>
    <input type="file" @change="handleFileUpload">
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null
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
    }
  }
}
</script>

<style scoped>
input, button {
  margin: 5px;
}
</style>
