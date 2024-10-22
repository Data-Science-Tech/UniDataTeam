<template>
  <div class="service-container">
    <div class="header">
        <img src="@/assets/ha.png" alt="EZDP Logo" class="logo-1" />
        <h1>什么是"轻松部署？"</h1>
        <p>
            您只需要准备好您的代码，即可在Easy Deploy提供的云开发平台上一键训练。
        </p>
        <p class="des">
            无需花费大量时间配置环境，无需苦苦寻找预训练模型，无需耗费大量时间转换数据集，无需花费大量金钱配置高性能计算平台
        </p>
    </div>

    <div class="options">
      <div
        class="option"
        :class="{ active: selectedOption === 1 }"
        @click="selectOption(1)"
      >
        <img
          :class="{ invert: selectedOption !== 1 }"
          src="@/assets/user-guidance.png"
          alt="用户指南"
          class="icon"
        />
        <p>选择模型、数据集</p>
      </div>
      <div
        class="option"
        :class="{ active: selectedOption === 2 }"
        @click="selectOption(2)"
      >
        <img
          :class="{ invert: selectedOption === 2 }"
          src="@/assets/community.svg"
          alt="数据社区"
          class="icon"
        />
        <p>选择计算环境</p>
      </div>
      <div
        class="option"
        :class="{ active: selectedOption === 3 }"
        @click="selectOption(3)"
      >
        <img
          :class="{ invert: selectedOption === 3 }"
          src="@/assets/cloud-server.svg"
          alt="云端服务"
          class="icon"
        />
        <p>一键云端部署</p>
      </div>
    </div>

    <!-- <div class="content">
      <div class="features">
        <div class="feature" v-for="(feature, index) in features" :key="index">
          <h2>{{ feature.title }}</h2>
          <p>{{ feature.description }}</p>
        </div>
      </div>
      <div class="about">
        <h3>关于UniDataBank</h3>
        <p>
          UniDataBank是一个开放可信的通用型科学数据存储与发布公共产品，主要面向全球科研人员、团队、科研机构、科研机构及高校等相关主体提供科学数据相关服务（例如，数据获取、数据长期保存、数据发布、数据共享和访问、数据社区建设等）。
        </p>
        <button @click="goToLearnMore">了解更多</button>
      </div>
    </div> -->
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedOption: 1,
      features: [
        {
          title: "01 统一的数据格式",
          description: "标准化数据格式，确保跨平台兼容，轻松集成多源数据。",
        },
        {
          title: "02 数据可视化",
          description: "将数据集直观呈现，帮助您更轻松地分析、理解和探索数据模式。",
        },
        {
          title: "03 数据发布",
          description: "一键发布您的数据，轻松共享、实时更新，确保团队保持同步。",
        },
        {
          title: "04 数据标注",
          description: "精准标注数据细节，提升机器学习模型的训练质量。",
        },
      ],
    };
  },
  methods: {
    selectOption(option) {
      this.selectedOption = option;
    },
    goToLearnMore() {
      console.log("跳转到更多信息页面");
    },
  },
};
</script>

<style scoped>
.logo-1 {
    height: 16vh;
}


.header {
  text-align: center;
  margin: 0;
}

.header h1 {
  font-size: 2vw;
  margin-bottom: 3vw;
}

.header p {
  color: #666;
  font-size: 1.2vw;
}

.options {
  display: flex;
  justify-content: space-between;
  margin: 5vw;
}

.service-container {
  font-family: Arial, sans-serif;
  padding: 20px;
  max-width: 1440px;
  margin: 0 auto;
}

.option {
  background-color: #091447;
  color: white;
  width: 32%;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  cursor: pointer;
  border-radius: 10px;
  transition: background-color 0.3s, box-shadow 0.3s;
}

.option.active {
  background-color: white;
  color: #1f3648;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.option img.icon {
  width: 40px;
  height: 40px;
  margin-bottom: 10px;
}

.option img.invert {
  filter: invert(100%);
}

.option p {
  margin-top: 10px;
  font-size: 24px;
}

.content {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
  width: 95%;
  margin: 0 auto;
}

.features {
  flex: 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: 40px;
  text-align: left;
}

.feature h2 {
  font-size: 28px;
  color: #1f3648;
  margin-bottom: 10px;
}

.feature p {
  font-size: 22px;
  color: #666;
}

.about {
  flex: 1;
  background-color: rgba(91, 120, 143, 0.77);
  padding: 30px;
  border-radius: 8px;
  color: white;
  margin-left: 20px;
  max-width: 450px;
  align-self: flex-start;
}

.about h3 {
  font-size: 24px;
  margin-bottom: 10px;
}

.about p {
  font-size: 20px;
}

.about button {
  background-color: white;
  color: #1f3648;
  border: none;
  padding: 15px 30px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
  width: 100%;
}
</style>
