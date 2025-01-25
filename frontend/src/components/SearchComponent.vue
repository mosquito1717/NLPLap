<template>
  <div>
    <h2>Search Data</h2>
    <input type="text" v-model="searchQuery" placeholder="Enter search query">
    <button @click="searchData">Search</button>

    <h2>Results</h2>
    <p v-if="results.length">Total Results: {{ results.length }}</p>
    <div v-if="results.length" class="results-container">
      <div v-for="(result, index) in results" :key="index">
        <p @click="viewDetail(result)" class="clickable">{{ result.content }}</p>
        <hr>
      </div>
    </div>
    <div v-else>
      <p>No results found.</p>
    </div>

    <div v-if="selectedResult" class="modal">
      <div class="modal-content">
        <h3>Document Details</h3>
        <p>{{ selectedResult.content }}</p>
        <button @click="closeDetail">Close</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      searchQuery: '',
      results: [],
      selectedResult: null
    };
  },
  methods: {
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
    },
    viewDetail(result) {
      this.selectedResult = result;
    },
    closeDetail() {
      this.selectedResult = null;
    }
  }
}
</script>

<style scoped>
input, button {
  margin: 5px;
}
.clickable {
  cursor: pointer;
  color: blue;
  text-decoration: underline;
}
.results-container {
  max-height: 400px; /* 결과 목록의 최대 높이 */
  overflow-y: auto;  /* 세로 스크롤 가능 */
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 5px;
  background: #f9f9f9;
}
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}
</style>