<template>
  <div>
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
      searchQuery: '',
      results: []
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
    }
  }
}
</script>

<style scoped>
input, button {
  margin: 5px;
}
</style>