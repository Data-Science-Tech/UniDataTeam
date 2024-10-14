<template>
  <div class="main-container">
    <!-- 导航栏 -->
    <nav class="navbar">
      <div class="navbar-left">
        <img src="@/assets/logo.png" alt="UDB Logo" class="logo" />
        <span class="brand">Uni Data Bank</span>
      </div>
      <ul class="navbar-center">
        <li>首页</li>
        <li>工作台</li>
        <li>浏览数据</li>
        <li>数据社区</li>
        <li>合作伙伴</li>
        <li>帮助中心</li>
        <li>关于我们</li>
      </ul>
      <div class="navbar-right">
        <button class="login-btn">登录</button>
        <button class="publish-btn">发布数据</button>
        <button class="lang-btn">EN</button>
      </div>
    </nav>

    <!-- 主内容区域 -->
    <div class="hero-section">
      <h1>让AI 开发更高效</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainPage",
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
  padding: 10px 20px;
  background-color: #000;
  color: white;
  border-bottom: 0.25px solid #ccc; /* 添加导航栏下方的细线 */
}

.navbar-left {
  display: flex;
  align-items: center;
}

.logo {
  height: 40px;
  margin-right: 10px;
}

.brand {
  font-size: 18px;
  font-weight: bold;
}

.navbar-center {
  display: flex;
  list-style: none;
  padding: 0;
  margin: 0;
}

.navbar-center li {
  margin: 0 15px;
  cursor: pointer;
  position: relative;
  font-size: 20px; /* 增大导航栏字体大小 */
}

.navbar-center li::after {
  content: '';
  display: block;
  width: 0;
  height: 4px;
  background: white;
  transition: width .3s;
  position: absolute;
  bottom: -17px; /* 使下划线位于导航栏细线的上方 */
  left: 0;
}

.navbar-center li:hover::after {
  width: 100%;
}

.navbar-right {
  display: flex;
  align-items: center;
}

.login-btn,
.publish-btn,
.lang-btn {
  background: none;
  border: 1px solid white;
  color: white;
  padding: 5px 10px;
  margin-left: 10px;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.publish-btn {
  background-color: white;
  color: black;
}

.login-btn:hover,
.publish-btn:hover,
.lang-btn:hover {
  background-color: white;
  color: black;
}

/* 主内容区域样式 */
.hero-section {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-image: url('@/assets/background-image.jpg');
  background-size: contain;
  background-position: center;
  color: white;
}

.hero-section h1 {
  font-size: 128px;
  font-weight: bold;
}
</style>
