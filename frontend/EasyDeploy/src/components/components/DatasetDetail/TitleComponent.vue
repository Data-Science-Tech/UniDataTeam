<template>
  <div class="dataset-detail-header">
    <!-- 顶部按钮 -->
    <div class="header-buttons">
      <button class="open-access-btn">开放获取</button>
      <span class="publish-date">出版时间 2099-12-31</span>
      <span class="last-update">最后更新 9921-1-1</span>
    </div>

    <!-- 中间内容部分 -->
    <div class="main-content">
      <h1 class="title">标题</h1>

      <!-- Web 链接部分 -->
      <div class="web-links">
        <div class="web-link">
          <input type="text" placeholder="Web 1" value="www.web1.com" readonly />
          <button @click="copyToClipboard('www.web1.com')">复制</button>
        </div>
        <div class="web-link">
          <input type="text" placeholder="Web 2" value="www.web2.com" readonly />
          <button @click="copyToClipboard('www.web2.com')">复制</button>
        </div>
        <div class="version-select">
          <select>
            <option>版本: 1</option>
          </select>
        </div>
      </div>

      <!-- 作者部分 -->
      <div class="authors">
        <img src="@/assets/DatasetDetail/man.svg" alt="Author Icon" class="author-icon" />
        作者1；作者2；作者3；
      </div>

      <!-- 摘要部分 -->
      <div class="abstract">
        <h2>摘要</h2>
        <p>This is the description. Write the description here.</p>
      </div>

      <!-- 关键词部分 -->
      <div class="keywords">
        <span>关键词：</span>
        <button>Keyword 1</button>
        <button>Keyword 2</button>
        <button>Keyword 3</button>
      </div>

      <!-- 学科分类部分 -->
      <div class="subject-categories">
        <span>学科分类：</span>
        <button>subject 1</button>
        <button>subject 2</button>
      </div>
    </div>

    <!-- 右侧图标和Logo部分 -->
    <div class="logo-container">
      <div class="social-info">
        <div class="icon-star">★ 15</div>
        <div class="icon-like">👍 500</div>
      </div>
      <div class="logo-box">
        <p>LOGO HERE</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "DatasetDetailHeader",
  methods: {
    copyToClipboard(text) {
      navigator.clipboard.writeText(text).then(
        () => {
          alert('复制成功');
        },
        (err) => {
          console.error('复制失败', err);
        }
      );
    },
  },
};
</script>

<style scoped>
.dataset-detail-header {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(180deg, rgba(25.5, 0, 255, 0.5) 0%, rgba(178.5, 0, 255, 0) 100%);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  color: white;
  box-sizing: border-box;
}

.header-buttons {
  display: flex;
  justify-content: flex-start;
  margin-bottom: 2rem;
}

.header-buttons > * {
  margin-right: 1rem;
}

.open-access-btn {
  background-color: #ffffff;
  color: #000000;
  padding: 0.5rem 1rem;
  border-radius: 31px;
  border: 0.5px solid #000000;
  cursor: pointer;
  font-family: "Microsoft YaHei UI-Regular", Helvetica;
  font-size: 1rem;
  text-align: center;
}

.publish-date,
.last-update {
  font-family: "Arial-Regular", Helvetica;
  font-size: 1rem;
  color: #000000;
  text-align: center;
}

.main-content {
  max-width: 60%;
  margin-top: -2rem;
}

.title {
  font-size: 3rem;
  font-family: "Microsoft YaHei UI-Bold", Helvetica;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #000000;
}

.web-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.web-link {
  display: flex;
  gap: 1rem;
}

.web-link input {
  flex: 1;
  padding: 0.5rem;
  border-radius: 4px;
  border: 1px solid #a6a6a6;
  background-color: #ffffff;
  font-size: 1.25rem; /* 增大字体 */
  max-width: 300px; /* 限制输入框宽度 */
}

.web-link button {
  padding: 0.5rem 1rem;
  border-radius: 4px;
  background-color: #ffffff;
  border: 1px solid #a6a6a6;
  color: black;
  cursor: pointer;
  font-size: 1rem; /* 按钮的字体大小 */
}

.version-select select {
  padding: 0.5rem;
  border-radius: 7px;
  background-color: #ffffff;
  border: 0.7px solid #000000;
  color: black;
}

.authors {
  margin-bottom: 2rem;
  font-family: "Microsoft YaHei UI-Regular", Helvetica;
  font-size: 1.5rem;
  color: #000000;
  display: flex;
  align-items: center;
}

.author-icon {
  display: inline-block;
  width: 2rem;
  margin-right: 1rem;
  margin-top: 10px;
}

.abstract {
  margin-bottom: 2rem;
}

.abstract h2 {
  font-size: 1.75rem;
  font-family: "Microsoft YaHei UI-Bold", Helvetica;
  font-weight: 700;
  color: #000000;
}

.abstract p {
  font-size: 1rem;
  font-family: "Arial-Regular", Helvetica;
  color: #000000;
}

.keywords,
.subject-categories {
  margin-bottom: 2rem;
}

.keywords span,
.subject-categories span {
  font-size: 1.5rem;
  font-family: "Microsoft YaHei UI-Bold", Helvetica;
  font-weight: 700;
  color: #000000;
}

.keywords button,
.subject-categories button {
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 31px;
  border: none;
  background-color: #0077FF;
  color: white;
  cursor: pointer;
}

.logo-container {
  position: absolute;
  top: 20%;
  right: 3%;
}

.social-info {
  background-color: #007aff;
  color: white;
  padding: 1rem 2rem;
  border-radius: 10px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
}

.icon-star,
.icon-like {
  margin-right: 1rem;
  font-size: 1rem;
  font-family: "Arial-Regular", Helvetica;
  color: #ffffff;
}

.logo-box {
  width: 10rem;
  height: 10rem;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  color: black;
  border-radius: 10px;
  font-family: "Arial-Regular", Helvetica;
  font-size: 1rem;
  text-align: center;
}

/* 使用媒体查询 */
@media (max-width: 768px) {
  .main-content {
    max-width: 100%;
    margin-top: 2rem;
  }

  .logo-container {
    position: relative;
    top: 0;
    right: 0;
    margin-top: 2rem;
  }

  .title {
    font-size: 2rem;
  }

  .web-link input,
  .web-link button,
  .version-select select {
    font-size: 0.875rem;
  }
}
</style>
