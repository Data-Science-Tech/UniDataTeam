<template>
  <div class="search-container">
    <input
      type="text"
      class="search-input"
      placeholder="输入作者，关键词，标题等检索数据集"
    />
    <button class="search-button">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 24 24"
        class="icon-search"
      >
        <circle cx="11" cy="11" r="7" stroke="white" stroke-width="2" fill="none"/>
        <line x1="16" y1="16" x2="20" y2="20" stroke="white" stroke-width="2"/>
      </svg>
    </button>
  </div>
</template>

<script>
export default {
  name: "SearchBar",
};
</script>

<style scoped>
.search-container {
  display: flex;
  align-items: center;
  width: 66.67%; /* 占网页宽度的2/3 */
  margin: 0 auto; /* 居中对齐 */
  border: 1px solid #000;
  border-radius: 30px;
  overflow: hidden;
}

.search-input {
  flex: 1;
  border: none;
  padding: 15px 20px; /* 增加垂直的内边距 */
  font-size: 16px;
  color: #aaa;
  border-top-left-radius: 30px;
  border-bottom-left-radius: 30px;
  outline: none;
}

.search-button {
  background-color: #000;
  border: none;
  padding: 15px 20px; /* 增加垂直的内边距 */
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-top-right-radius: 30px;
  border-bottom-right-radius: 30px;
}

.icon-search {
  width: 24px; /* 稍微增加图标的尺寸以适应按钮高度 */
  height: 24px;
}

.search-button:focus {
  outline: none;
}
</style>
