<template>
  <div class="content-display">
    <div class="section" v-for="section in sections" :key="section.name">
      <div class="section-title">{{ section.name }}</div>
      <div class="instances">
        <div
          class="instance"
          v-for="instance in section.instances"
          :key="instance.id"
          @click="navigateToDetails(section.name, instance.id)"
        >
          <div class="instance-header">
            <span class="status-label">{{ instance.status }}</span>
            <span class="date-label">{{ instance.date }}</span>
          </div>
          <img :src="instance.image" alt="Dataset Image" class="instance-image" />
          <div class="instance-details">
            <h3>{{ instance.title }}</h3>
            <p class="authors">{{ instance.authors }}</p>
            <div class="info-box">
              <p class="url"><strong>URL:</strong> <a :href="instance.url" target="_blank" @click.stop>{{ instance.url }}</a> <button @click.stop="copyText(instance.url)">📋</button></p>
              <p class="doi"><strong>DOI:</strong> <a :href="instance.doi" target="_blank" @click.stop>{{ instance.doi }}</a> <button @click.stop="copyText(instance.doi)">📋</button></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import perception1 from '@/assets/MainPage/perception-1.png';
import perception2 from '@/assets/MainPage/perception-2.png';
import perception3 from '@/assets/MainPage/perception-3.png';
import perception4 from '@/assets/MainPage/perception-4.png';
import prediction1 from '@/assets/MainPage/prediction-1.png';
import prediction2 from '@/assets/MainPage/prediction-2.png';
import prediction3 from '@/assets/MainPage/prediction-3.png';
import prediction4 from '@/assets/MainPage/prediction-4.png';
import control1 from '@/assets/MainPage/control-1.png';
import control2 from '@/assets/MainPage/control-2.png';
import control3 from '@/assets/MainPage/control-3.png';
import control4 from '@/assets/MainPage/control-4.png';
import endtoend1 from '@/assets/MainPage/e2e-1.png';
import endtoend2 from '@/assets/MainPage/e2e-2.png';
import endtoend3 from '@/assets/MainPage/e2e-3.png';
import endtoend4 from '@/assets/MainPage/e2e-4.png';
import v2x1 from '@/assets/MainPage/v2x-1.png';
import v2x2 from '@/assets/MainPage/v2x-2.png';
import v2x3 from '@/assets/MainPage/v2x-3.png';
import v2x4 from '@/assets/MainPage/v2x-4.png';
import llm1 from '@/assets/MainPage/llm-1.png';
import llm2 from '@/assets/MainPage/llm-2.png';
import llm3 from '@/assets/MainPage/llm-3.png';
import llm4 from '@/assets/MainPage/llm-4.png';
import nerf1 from '@/assets/MainPage/nerf-1.png';
import nerf2 from '@/assets/MainPage/nerf-2.png';
import nerf3 from '@/assets/MainPage/nerf-3.png';
import nerf4 from '@/assets/MainPage/nerf-4.png';

export default {
  data() {
    return {
      sections: [
        {
          name: "模型",
          instances: [
            {
              id: 1,
              title: "BERT: Bidirectional Encoder Representations from Transformers",
              authors: "Jacob Devlin 等",
              date: "2019-10-11",
              status: "PUBLIC",
              doi: "https://doi.org/10.48550/arXiv.1810.04805",
              url: "https://github.com/google-research/bert",
              image: 'model1' // 请确保已导入相应图片
            },
            {
              id: 2,
              title: "GPT-4: Generative Pre-trained Transformer 4",
              authors: "OpenAI",
              date: "2023-03-14",
              status: "PUBLIC",
              doi: "https://doi.org/10.48550/arXiv.2005.14165",
              url: "https://github.com/openai/gpt-4",
              image: 'model2' // 请确保已导入相应图片
            }
          ]
        },
        {
          name: "数据集",
          instances: [
            {
              id: 1,
              title: "ImageNet",
              authors: "ImageNet 团队",
              date: "2009-08-16",
              status: "PUBLIC",
              doi: "https://doi.org/10.1007/s11263-015-0816-y",
              url: "http://www.image-net.org/",
              image: 'dataset1' // 请确保已导入相应图片
            },
            {
              id: 2,
              title: "COCO: Common Objects in Context",
              authors: "Tobias Müller 等",
              date: "2014-08-16",
              status: "PUBLIC",
              doi: "https://doi.org/10.48550/arXiv.1405.0312",
              url: "https://cocodataset.org/",
              image: 'dataset2' // 请确保已导入相应图片
            }
          ]
        },
        {
          name: "算法",
          instances: [
            {
              id: 1,
              title: "梯度下降法 (Gradient Descent)",
              authors: "多位学者",
              date: "1858-03-01",
              status: "PUBLIC",
              doi: "https://doi.org/10.1002/cpa.3160390204",
              url: "https://en.wikipedia.org/wiki/Gradient_descent",
              image: 'algorithm1' // 请确保已导入相应图片
            },
            {
              id: 2,
              title: "随机森林 (Random Forest)",
              authors: "Leo Breiman 等",
              date: "2001-01-01",
              status: "PUBLIC",
              doi: "https://doi.org/10.1023/A:1010933404324",
              url: "https://github.com/scikit-learn/scikit-learn/tree/main/sklearn/ensemble",
              image: 'algorithm2' // 请确保已导入相应图片
            }
          ]
        },
        {
          name: "云服务",
          instances: [
            {
              id: 1,
              title: "AWS EC2",
              authors: "Amazon Web Services",
              date: "2006-08-25",
              status: "PUBLIC",
              doi: "https://aws.amazon.com/ec2/",
              url: "https://aws.amazon.com/ec2/",
              image: 'cloud1' // 请确保已导入相应图片
            },
            {
              id: 2,
              title: "Google Cloud Storage",
              authors: "Google Cloud",
              date: "2010-04-07",
              status: "PUBLIC",
              doi: "https://cloud.google.com/storage",
              url: "https://cloud.google.com/storage",
              image: 'cloud2' // 请确保已导入相应图片
            }
          ]
        }
      ]
    };
  },
  methods: {
    copyText(text) {
      navigator.clipboard.writeText(text).then(() => {
        alert("复制成功!");
      });
    },
    navigateToDetails(sectionName, instanceId) {
    // 这里使用 sectionName 和 instanceId 组合来跳转到详情页
    console.log(`Navigating to details page for section: ${sectionName}, dataset with id: ${instanceId}`);

    // 示例：构建一个基于 sectionName 和 instanceId 的唯一 URL
    const sectionSlug = sectionName.toLowerCase().replace(/\s+/g, '-');
    window.location.href = `/dataset-details/${sectionSlug}/${instanceId}`;
    
    // 或者使用 Vue Router 进行导航
    // this.$router.push({ name: 'DatasetDetails', params: { section: sectionSlug, id: instanceId } });
  },
  }
};
</script>

<style scoped>
.content-display {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.section {
  margin-bottom: 100px;
  width: 100%;
}

.section-title {
  width: 10vw;
  background-color: #f1f1a9;
  text-align: center;
  font-size: 24px;
  padding: 10px;
  border-radius: 20px;
  margin: 0 auto 20px auto; /* 设置左右 margin 为 auto, 确保居中 */
  font-weight: bold;
}

.instances {
  display: flex;
  max-height: 8000px; /* 设置图标的最大高度 */
  justify-content: flex-start;
  overflow-x: auto;
  white-space: nowrap;
}

.instance {
  display: inline-block;
  width: 300px;
  margin: 0 10px;
  text-align: left;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: #fff;
  box-sizing: border-box;
  position: relative;
  cursor: pointer;
  transition: transform 0.2s;
}

.instance:hover {
  transform: scale(1.0011);
}

.instance-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.status-label {
  background-color: #e0e0e0;
  border-radius: 12px;
  padding: 5px 10px;
  font-size: 12px;
  color: #333;
}

.date-label {
  font-size: 12px;
  color: #888;
}

.instance img {
  width: 100%;
  height: 180px; /* 固定高度 */
  border-radius: 8px;
  object-fit: cover; /* 确保图片拉伸时不失真 */
  margin-bottom: 10px;
}

.instance-details h3,
.instance-details .authors,
.info-box p a {
  font-size: 16px;
  margin-bottom: 0px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.authors {
  margin-bottom: 15px; /* 增加作者与链接之间的间距 */
}

.info-box {
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 8px;
  background-color: #f9f9f9;
  margin-top: 15px; /* 将链接框整体下移 */
}

.info-box p {
  margin: 5px 0;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.info-box a {
  color: #007bff;
  text-decoration: none;
  word-break: break-all;
  flex-grow: 1; /* 使链接在按钮之前占据最大空间 */
}

.info-box a:hover {
  text-decoration: underline;
}

button {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #555;
  margin-left: 10px; /* 确保按钮与链接之间有间距 */
}

button:hover {
  color: #007bff;
}
</style>
