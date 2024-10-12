<template>
  <div class="news-section">
    <div class="news-header">
      <h1>UniDataBank的最新动态</h1>
      <p>新闻、博客和评论</p>
    </div>
    <div class="news-container">
      <NewsCard
        v-for="(news, index) in newsItems"
        :key="index"
        :imageSrc="news.imageSrc"
        :date="news.date"
        :title="news.title"
        :body="news.body"
        :link="news.link"
      />
    </div>
  </div>
</template>

<script>
import NewsCard from '@/components/Home/NewsCard.vue';

export default {
  components: {
    NewsCard
  },
  data() {
    return {
      newsItems: [
        {
          imageSrc: "https://via.placeholder.com/350",
          date: "2024-06-19",
          title: "新功能速递：欢迎集成您的徽章组件！",
          body: "近日，ScienceDB上线了徽章（Badge）组件功能，徽章组件为您提供了一种便捷且简单的方式...",
          link: "#"
        },
        {
          imageSrc: "https://via.placeholder.com/350",
          date: "2024-05-20",
          title: "平台访问量突破7亿次！",
          body: "感谢大家的支持，ScienceDB平台访问量已突破7亿次，我们将继续为科研工作者提供更优质的服务...",
          link: "#"
        },
        {
          imageSrc: "https://via.placeholder.com/350",
          date: "2024-04-15",
          title: "数据共享的未来：ScienceDB发布新功能",
          body: "ScienceDB最近发布了数据共享的新功能，帮助科研人员更好地管理和共享他们的数据资源...",
          link: "#"
        },
      ]
    };
  }
};
</script>

<style scoped>
.news-section {
  text-align: center;
  margin: 40px auto;
  width: 100%;
  max-width: 1200px;
}

.news-header {
  margin-bottom: 40px;
}

.news-header h1 {
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.news-header p {
  font-size: 1rem;
  color: #666;
  margin-bottom: 10px;
}

.news-container {
  display: flex;
  justify-content: space-between;
  flex-wrap: nowrap; /* 禁止换行 */
}

.news-container > * {
  width: calc((100% - 40px) / 3); /* 保证每行三个卡片，减去间距 */
  aspect-ratio: 16 / 9; /* 保持固定的宽高比 */
  margin-right: 20px; /* 卡片之间的间距 */
}

.news-container > *:last-child {
  margin-right: 0; /* 去除最后一个卡片的右边距 */
}

.news-card {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  cursor: pointer;
  transition: transform 0.2s;
}

.news-card:hover {
  transform: scale(1.02);
}

.news-image img {
  width: 100%;
  height: auto;
  object-fit: cover;
  border-radius: 10px;
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
