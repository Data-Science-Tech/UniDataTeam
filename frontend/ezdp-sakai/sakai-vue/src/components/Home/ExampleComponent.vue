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
          name: "感知",
          instances: [
            {
              id: 1,
              title: "Scalability in Perception for Autonomous Driving: Waymo Open Dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "PUBLIC",
              doi: "https://doi.org/10.48550/arXiv.1912.04838",
              url: "https://github.com/waymo-research/waymo-open-dataset",
              image: perception1
            },
            {
              id: 2,
              title: "Vision meets robotics: The KITTI dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "PUBLIC",
              doi: "https://doi.org/10.1177/0278364913491297",
              url: "https://github.com/alexstaravoitau/KITTI-Dataset",
              image: perception2
            },
            {
              id: 3,
              title: "nuScenes: A Multimodal Dataset for Autonomous Driving",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://arxiv.org/abs/1903.11027",
              url: "https://github.com/nutonomy/nuscenes-devkit",
              image: perception3
            },
            {
              id: 4,
              title: "The ApolloScape Dataset for Autonomous Driving",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.1109/TPAMI.2019.2926463",
              url: "https://github.com/ApolloScapeAuto/dataset-api",
              image: perception4
            },
          ]
        },
        {
          name: "预测",
          instances: [
            {
              id: 1,
              title: "Argoverse: 3D Tracking and Forecasting With Rich Maps",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.1911.02620",
              url: "https://github.com/argoverse/argoverse-api",
              image: prediction1
            },
            {
              id: 2,
              title: "INTERACTION Dataset: An INTERnational, Adversarial and Cooperative moTION Dataset in Interactive Driving Scenarios with Semantic Maps",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.1910.03088",
              url: "https://github.com/interaction-dataset/interaction-dataset",
              image: prediction2
            },
            {
              id: 3,
              title: "SIND: A Drone Dataset at Signalized Intersection in China",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2209.02297",
              url: "https://github.com/sotif-avlab/sind",
              image: prediction3
            },
            {
              id: 4,
              title: "CitySim: A Drone-Based Vehicle Trajectory Dataset for Safety Oriented Research and Digital Twins",
              authors: "Author Name",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.1177/03611981231185768",
              url: "https://github.com/UCF-SST-Lab/UCF-SST-CitySim1-Dataset",
              image: prediction4
            }
          ]
        },
        {
          name: "规控",
          instances: [
            {
              id: 1,
              title: "DBNet: A large-scale dataset for driving behavior learning",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "http://www.dbehavior.net/data/egpaper_release.pdf",
              url: "www.dbehavior.net",
              image: control1
            },
            {
              id: 2,
              title: "Udacity Dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://www.udacity.com/self-driving-car",
              url: "https://github.com/udacity/self-driving-car/tree/master/datasets",
              image: control2
            },
            {
              id: 3,
              title: "Toward Driving Scene Understanding: A Dataset for Learning Driver Behavior and Causal Reasoning",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.1811.02307",
              url: "https://usa.honda-ri.com/hdd",
              image: control3
            },
            {
              id: 4,
              title: "A2D2: Audi autonomous driving dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://arxiv.org/abs/2004.06320",
              url: "https://www.a2d2.audi/a2d2/en.html",
              image: control4
            }
          ]
        },
        {
          name: "端到端",
          instances: [
            {
              id: 1,
              title: "DriveCoT: Integrating Chain-of-Thought Reasoning with End-to-End Driving",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://arxiv.org/abs/2403.16996",
              url: "https://drivecot.github.io/",
              image: endtoend1
            },
            {
              id: 2,
              title: "DDD20: end-to-end DAVIS driving dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://ieeexplore.ieee.org/abstract/document/9294515/",
              url: "https://sites.google.com/view/davis-driving-dataset-2020/home",
              image: endtoend2
            },
            {
              id: 3,
              title: "LMDrive: Closed-Loop End-to-End Driving with Large Language Models",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2312.07488",
              url: "https://github.com/opendilab/LMDrive",
              image: endtoend3
            },
            {
              id: 4,
              title: "A Commute in Data: The comma2k19 Dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.1812.05752",
              url: "https://github.com/commaai/comma2k19",
              image: endtoend4
            }
          ]
        },
        {
          name: "V2X",
          instances: [
            {
              id: 1,
              title: "DAIR-V2X Dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2204.05575",
              url: "https://github.com/AIR-THU/DAIR-V2X",
              image: v2x1
            },
            {
              id: 2,
              title: "V2X-Sim: Multi-agent collaborative perception dataset and benchmark for autonomous driving",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://ieeexplore.ieee.org/abstract/document/9835036/",
              url: "https://ai4ce.github.io/V2X-Sim/data.html",
              image: v2x2
            },
            {
              id: 3,
              title: "V2X-Real: a Largs-Scale Dataset for Vehicle-to-Everything Cooperative Perception",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://arxiv.org/pdf/2403.01316.pdf",
              url: "https://tum-traffic-dataset.github.io/tumtraf-v2x/",
              image: v2x3
            },
            {
              id: 4,
              title: "V2X-Seq Dataset",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2305.05938",
              url: "https://thudair.baai.ac.cn/cooplocus",
              image: v2x4
            }
          ]
        },
        {
          name: "LLM",
          instances: [
            {
              id: 1,
              title: "Driving with LLMs: Fusing Object-Level Vector Modality for Explainable Autonomous Driving",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2310.01957",
              url: "https://github.com/waveyai/Driving-with-LLMs",
              image: llm1
            },
            {
              id: 2,
              title: "Learning to Copy for Automatic Post-Editing",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.1911.03627",
              url: "https://github.com/talk2car/Talk2Car",
              image: llm2
            },
            {
              id: 3,
              title: "DriveLM: Driving with Graph Visual Question Answering",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2312.14150",
              url: "https://github.com/OpenDriveLab/DriveLM",
              image: llm3
            },
            {
              id: 4,
              title: "Automated Evaluation of Large Vision-Language Models on Self-driving Corner Cases",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2404.10595",
              url: "https://github.com/DLUT-LYZ/CODA-LM",
              image: llm4
            }
          ]
        },
        {
          name: "NeRF",
          instances: [
            {
              id: 1,
              title: "DriveEnv-NeRF: Exploration of A NeRF-Based Autonomous Driving Environment for Real-World Performance Validation",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2403.15791",
              url: "https://github.com/muyishen2040/DriveEnvNeRF",
              image: nerf1
            },
            {
              id: 2,
              title: "NeuroNCAP: Photorealistic Closed-loop Safety Testing for Autonomous Driving",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2404.07762",
              url: "https://github.com/atonderski/neuro-ncap",
              image: nerf2
            },
            {
              id: 3,
              title: "LiDAR4D: Dynamic Neural Fields for Novel Space-time View LiDAR Synthesis",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2404.02742",
              url: "https://github.com/ispc-lab/LiDAR4D",
              image: nerf3
            },
            {
              id: 4,
              title: "Learning to Copy for Automatic Post-Editing",
              authors: "Unknown Authors",
              date: "2024-08-16",
              status: "RESTRICTED",
              doi: "https://doi.org/10.48550/arXiv.2403.05907",
              url: "https://github.com/VISION-SJTU/Lightning-NeRF",
              image: nerf4
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
  width: 30%;
  background-color: #f2f2f2;
  text-align: center;
  font-size: 24px;
  padding: 15px;
  border-radius: 8px;
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
