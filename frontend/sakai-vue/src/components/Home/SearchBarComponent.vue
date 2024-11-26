<template>
    <div class="search-container">
      <input
        type="text"
        v-model="query"
        placeholder="🔍Search models, datasets, users..."
        @input="handleSearch"
      />
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        query: "", // Store the search query here
      };
    },
    methods: {
      handleSearch() {
        // Perform search or emit the query for external use
        console.log(this.query);
      },
    },
  };
  </script>
  
  <style scoped>
  .search-container {
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  input[type="text"] {
    width: 20vw; /* Set the width of the input box */
    padding: 10px 15px;
    border: 1px solid #e4e4e4; /* Border styling */
    border-radius: 15px; /* Rounded edges */
    font-size: 16px;
    /*box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  Light shadow effect */
    outline: none; /* Remove input outline on focus */
    transition: all 0.3s ease-in-out;
  }
  
  input[type="text"]:focus {
    border-color: #8c8c8c; /* Change color on focus */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Increase shadow on focus */
  }
  </style>
  