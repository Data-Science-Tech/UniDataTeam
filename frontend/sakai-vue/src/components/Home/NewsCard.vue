<template>
  <div class="news-card" @click="navigate">
    <div class="news-image">
      <img :src="imageSrc" alt="News Image" />
    </div>
    <div class="news-date">{{ date }}</div>
    <div class="news-title">{{ title }}</div>
    <div class="news-body">{{ body }}</div>
    <div class="news-link">
      <a href="#" @click.stop="navigate">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 7l5 5m0 0l-5 5m5-5H6" />
        </svg>
      </a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NewsCard',
  props: {
    imageSrc: {
      type: String,
      required: true
    },
    date: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    body: {
      type: String,
      required: true
    },
    link: {
      type: String,
      required: true
    }
  },
  methods: {
    navigate() {
      window.location.href = this.link;
    }
  }
};
</script>

<style scoped>
.news-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  max-width: 100%; /* 确保卡片宽度适应容器 */
  font-family: Arial, sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer; /* 增加鼠标悬停时的指针效果 */
  transition: transform 0.2s; /* 增加点击时的视觉反馈 */
}

.news-card:hover {
  transform: scale(1.02); /* 鼠标悬停时放大效果 */
}

.news-image img {
  width: 100%; /* 图片宽度适应卡片宽度 */
  height: auto; /* 保持图片的宽高比 */
  aspect-ratio: 16 / 9; /* 强制图片为16:9比例 */
  object-fit: cover; /* 确保图片覆盖整个区域，并保持比例 */
  border-radius: 10px; /* 圆角图片 */
}

.news-date {
  color: #9e9e9e;
  font-size: 0.9rem;
  margin-top: 10px;
}

.news-title {
  font-weight: bold;
  font-size: 1.2rem;
  margin-top: 10px;
}

.news-body {
  font-size: 0.95rem;
  margin-top: 10px;
  color: #333;
}

.news-link {
  display: flex;
  justify-content: flex-end;
  margin-top: 15px;
}

.news-link a {
  color: #000;
  text-decoration: none;
}

.news-link a:hover {
  color: #007bff;
}
</style>
