<template>
    <div class="globe-container">
      <div class="globe">
        <img src="@/assets/ha.png" alt="EZDP Logo" class="logo-1" />
      </div>
      <div class="data-display">
        <div class="data-row">
          <div class="data-item" v-for="(item, index) in dataItems" :key="index">
            <h2>{{ item.value }}</h2>
            <p>{{ item.label }}</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        dataItems: [
          { value: '5,000', label: '部署项目' },
          { value: '12,300', label: '模型数据集' },
          { value: '8,750', label: '算法使用量' },
        ],
      };
    },
  };
  </script>
  
  <style scoped>
  .globe-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(to right, #d7acd0, #e6dba1);
    height: 500px; /* 设置组件的高度 */
    width: 100vw; /* 设置宽度为视口宽度 */
    margin: 0; /* 取消外边距 */
  }
  
  .globe {
    width: 65%; /* 占据65%的宽度 */
    height: 100%; /* 占据父容器的高度 */
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  
  .data-display {
    width: 35%; 

    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .data-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr); 
    grid-gap: 20px; 
  }
  
  .data-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  
  .data-item h2 {
    font-size: 3rem;
    margin: 0;
  }
  
  .data-item p {
    margin: 0;
    font-size: 2rem;
  }
  </style>
