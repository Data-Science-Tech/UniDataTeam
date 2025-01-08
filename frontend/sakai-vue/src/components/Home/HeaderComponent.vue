<template>
  <div class="main-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="logo">
        <img src="@/assets/ha.png" alt="EZDP Logo" class="logo-1" />
        <!img src="@/assets/OkHand.svg" alt="EZDP Logo" class="logo-2" />
        <span class="brand">Easy Deploy</span>
      </div>

      <div class="searchbar">
        <SearchBarComponent/>
      </div>

      <ul class="navbar-center">
        <li>首页</li>
        <li>模型</li>
        <li>数据集</li>
        <li>云服务</li>
        <li>使用文档</li>
        <li>社区</li>
        <li>关于我们</li>
      </ul>
      <div class="navbar-right">
        <button class="login-btn" @click="gotoLogin">登录</button>
        <button class="publish-btn" @click="gotoworkbench">工作台</button>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <!-- <div class="hero-section">
      <h1>让AI 开发更高效</h1>
    </div> -->

    


  </div>
</template>

<script>
import SearchBarComponent from '@/components/Home/SearchBarComponent.vue';

export default {
  name: "MainPage",
  components: {
  SearchBarComponent,

  },
  methods: {
    gotoworkbench() {
      console.log("push workbench")
      this.$router.push('/missionManage/mission');
    },
    gotoHome(){
      console.log("push Home")
      this.$router.push('/');
    },
    gotoLogin() {
      console.log("push Home")
      this.$router.push('/auth/login');
    },
    gotoModel() {
      this.$router.push('/model');
    },
    gotoDataset() {
      this.$router.push('/dataset');
    }
  }
};
</script>

<style scoped>
.main-container {
  width: 100%;
  height: 8vh;
  display: flex;
  flex-direction: column;
}

/* 导航栏样式 */
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
    /*padding: 10px 20px;*/
  /*border-bottom: 0.25px solid #ccc;  添加导航栏下方的细线 */
}

.logo {
  display: flex;
  align-items: center;
  margin-left:10%;
}

.logo-1 {
    height: 5vh;
}

.logo-2{
    height:3vh;
}

.brand {
  font-size: 18px;
  font-weight: bolder;
  font-family: 'Microsoft YaHei', sans-serif; 
  margin-left: 1vh;
}

.searchbar{
    padding:0;
}

.navbar-center {
  display: flex;
  list-style:none;
  padding: 0;
  margin: 0;
  font-weight:bold;
  font-family: 'Microsoft YaHei', sans-serif; 
  font-size: 8%;
  color: black;
}

.navbar-center li {
  margin: 0 15px;
  cursor: pointer;
  position: relative;
  font-size: 1vw; /* 增大导航栏字体大小 */
}

.navbar-center li::after {
  content: '';
  display: block;
  width: 0;
  height: 4px;
  background: white;
  transition: height 1s;
  position: absolute;
  bottom: -17px; /* 使下划线位于导航栏细线的上方 */
  left: 0;
}

.navbar-center li:hover::after {
  width: 100%;
}

.navbar-right {
  display: flex;
  margin-right:10%;
}

.login-btn {
  background: none;
  border: 0;
  color: rgb(0, 0, 0);
  padding: 5px 10px;
  cursor: pointer;
  margin-right: 1ch;
  font-weight:bold;
  font-family: 'Microsoft YaHei', sans-serif; 
}

.publish-btn {
  border: 2px whitesmoke;
  background-color: rgb(231, 120, 120);
  color: rgb(255, 255, 255);
  border-radius: 15px;
  padding: 5px 10px;
  font-size: 2vh;
  font-weight:bold;
  font-family: 'Microsoft YaHei', sans-serif; 
}


/* 主内容区域样式 
.hero-section {
  flex: 1;
  display: flex;

  justify-content: center;
  align-items: center;
  margin: 12%;
  margin-top: 2%;
  background-color: rgb(15, 15, 16);
  border-radius: 30px;
  color: white;
}
*/
</style>
