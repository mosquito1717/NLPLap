<template>
    <nav>
      <router-link to="/">Home</router-link> |
      <router-link to="/upload">Upload</router-link> |
      <router-link to="/search">Search</router-link>
    </nav>
  </template>
  
  <style scoped>
  nav a {
    margin: 0 10px;
    text-decoration: none;
    color: #42b983;
  }
  nav a.router-link-active {
    font-weight: bold;
  }
  </style>
  