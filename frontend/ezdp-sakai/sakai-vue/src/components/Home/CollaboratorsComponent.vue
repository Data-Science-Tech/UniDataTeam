<template>
    <div class="collaborators-section">
      <h2 class="collaborators-title">Our Global Collaborators</h2>
      <div class="collaborators-logos">
        <div v-for="(logo, index) in logos" :key="index" class="logo-container">
          <img :src="logo.src" :alt="logo.alt" class="logo" />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        logos: [
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 1" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 2" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 3" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 4" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 5" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 6" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 7" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 8" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 9" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 10" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 11" },
          { src: "https://via.placeholder.com/200x100", alt: "Collaborator 12" },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .collaborators-section {
    text-align: center;
    padding: 40px 0;
  }
  
  .collaborators-title {
    font-size: 32px;
    margin-bottom: 20px;
    font-weight: bold;
  }
  
  .collaborators-logos {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
  }
  
  .logo-container {
    border-radius: 8px;
    padding: 15px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  }
  
  .logo {
    max-width: 100%;
    max-height: 100px;
    object-fit: contain;
  }
  </style>
  