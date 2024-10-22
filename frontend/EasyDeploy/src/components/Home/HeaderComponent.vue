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
        <button class="login-btn">登录</button>
        <button class="publish-btn">工作台</button>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <!-- <div class="hero-section">
      <h1>让AI 开发更高效</h1>
    </div> -->

    <div class="container">
    <div class="left-section">
        <img src="@/assets/ha.png" alt="EZDP Logo" class="logo-3" />
        <h1 class="headintro">The AI community building the future.</h1>
        <p class="des">
          The platform where the machine learning community collaborates on models, datasets, and applications.
        </p>
    </div>
    <div class="right-section">
      <h3>Easy Deploy</h3>

        <div class="startbutton">
            Let's deploy!  😀---->
        </div>
    </div>
    </div>


  </div>
</template>

<script>
import SearchBarComponent from '@/components/Home/SearchBarComponent.vue';

export default {
  name: "MainPage",
  components: {
  SearchBarComponent,
  },
};
</script>

<style scoped>
.main-container {
  width: 100%;
  height: 100vh;
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
  color:gray;
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
.container {
  display: flex;
  background-color: white;
  color: #fff;
  border-radius: 25px; /* Smooth border */
  margin: 12%;
  margin-top: 3%;
  margin-bottom: 10%;
  height: 70%;
  
}

.left-section {
  flex: 2;
  margin-top: 2%;
  background-color: #121022;
  border-radius: 25px 0 0 25px; /* Left part with rounded corners */
  padding: 10vh;
  transition: 1s;
}

.headintro{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-weight: bolder;
    font-size: 5vh;
    transition: 1s;
}

.des{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color:grey;
    font-size: 1vw;
    transition: 1s;
}

.right-wrapper {
  flex: 3;
  /* overflow: hidden; Ensure no overflow outside the rounded corners */
  /*border-radius: 50px 25px 50px 50px;  Right part with rounded corners */
}

.right-section {
  background-color: #040219;
  transition: 1s;
  padding: 30px;
  transform: skewX(-5deg); /* Adds slight tilt */
  margin-left: -50px; /* Pulls the section to fill the gap */
  border-radius:5%;
  width: 50%;
}

.right-section h3{
    margin-top: 10%;
    margin-left: 10%;
    font-family:Impact, Haettenschweiler, 'Arial Narrow Bold', sans-serif;
    font-size: 4vw;
    font-weight:lighter;
    color: rgb(18, 213, 148);
}



.logo-3{
    height: 40%;
    transition: 1s;
}

.startbutton{
    margin-top: 40%;
    margin-left: 45%;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 3vh;
    font-weight: bolder;
    padding: 2ch;
    background-color: rgb(243, 207, 24);
    border: 5px white;
    border-radius: 30px;
    transition: 1s;
}
</style>
