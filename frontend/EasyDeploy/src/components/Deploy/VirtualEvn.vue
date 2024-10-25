<template>
  <div class="virtualevn">
    <div class="title">
      虚拟环境搭建
    </div>
    <div class="content-box">
      上传您的yml文件
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.virtualevn {
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
  margin-bottom: 15px;
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

.content-box {
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 20px;
  font-size: 16px;
  color: #a0a0a0;
  text-align: center;
}
</style>