<template>
    <div class="globe-container">
      <div class="globe">
        <img src="https://cdn-icons-png.flaticon.com/512/4985/4985578.png" alt="Earth Icon" />
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
          { value: '10,286,019', label: '公开数据集' },
          { value: '738,392,908', label: '平台访问量' },
          { value: '592,763', label: '数据体量 +GB' },
          { value: '27,472,550', label: '文件下载量' },
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
    background: linear-gradient(to right, #3b8beb, #3d4efb);
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
  
  .globe img {
    width: 50%; /* 适当缩小地球图标的宽度 */
    height: auto;
  }
  
  .data-display {
    width: 35%; /* 占据35%的宽度 */
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .data-row {
    display: grid;
    grid-template-columns: repeat(2, 1fr); /* 两列布局 */
    grid-gap: 20px; /* 增加行间距和列间距 */
  }
  
  .data-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
  }
  
  .data-item h2 {
    font-size: 2rem;
    margin: 0;
  }
  
  .data-item p {
    margin: 0;
    font-size: 1.2rem;
  }
  </style>
  