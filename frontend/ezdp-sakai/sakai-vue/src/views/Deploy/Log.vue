<template>
    <div class="monitoring-page">
      <div class="title">
        日志与性能监测
      </div>
      <div class="card-container">
        <div class="card">
          <div class="card-title">
            日志
          </div>
          <div class="card-content">
            错误记录 分布
          </div>
        </div>
        <div class="card">
          <div class="card-title">
            性能监测
          </div>
          <div class="card-content">
            CPU 内存 网络 使用率
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  .monitoring-page {
    width: 80%;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    background-color: #f8f9fa;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: height 0.3s ease-in-out;
  }
  
  .title {
    font-size: 35px;
    font-weight: bold;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
  }
  
  .title::before {
    content: '';
    display: inline-block;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background-color: #ff6666;
    margin-right: 10px;
  }
  
  .card-container {
    display: flex;
    justify-content: space-between;
  }
  
  .card {
    width: 48%;
    background-color: #f8f8f8;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .card-title {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 10px;
  }
  
  .card-content {
    font-size: 14px;
    color: #a0a0a0;
  }
  </style>
  