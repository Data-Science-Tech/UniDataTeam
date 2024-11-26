<template>
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section about">
          <h3>关于</h3>
          <ul>
            <li><a href="#">简介</a></li>
            <li><a href="#">影响力</a></li>
            <li><a href="#">事件纪事</a></li>
            <li><a href="#">服务条款</a></li>
            <li><a href="#">联系我们</a></li>
          </ul>
        </div>

        <div class="footer-section collaborative-construction">
          <h3>协同构建</h3>
          <ul>
            <li><a href="#">我们的合作伙伴</a></li>
            <li><a href="#">精选 Easy Deploy</a></li>
            <li><a href="#">关于 Easy Deploy</a></li>
          </ul>
        </div>

        <div class="footer-section help">
          <h3>帮助</h3>
          <ul>
            <li><a href="#">发布流程</a></li>
            <li><a href="#">数据政策</a></li>
            <li><a href="#">首选文件格式</a></li>
            <li><a href="#">开放 API</a></li>
            <li><a href="#">常见问题</a></li>
          </ul>
        </div>

        <div class="footer-section qr-code">
          <img src="https://via.placeholder.com/120" alt="二维码" class="qr-code-img" />
          <p>关注公众号</p>
        </div>
      </div>

      <div class="footer-bottom">
        <div class="footer-bottom-left">
          <p>指导由</p>
          <div class="guided-logos">
            <img src="https://via.placeholder.com/100x40" alt="Logo 1" />
            <img src="https://via.placeholder.com/100x40" alt="Logo 2" />
            <img src="https://via.placeholder.com/100x40" alt="Logo 3" />
          </div>
        </div>
        <div class="footer-bottom-right">
          <p>&copy; 2015-2024 中国科学院计算机网络信息中心。保留所有权利。北京 ICP NO. 09112257-88</p>
        </div>
      </div>
    </footer>
  </template>

  <script>
  export default {
    name: "FooterComponent",
  };
  </script>

  <style scoped>
  .footer {
    width: 100%; /* 设置页脚宽度为页面宽度 */
    background-color: #1f3648;
    color: #fff;
    padding: 40px 0; /* 移除左右 padding，确保与页面宽度一致 */
    box-sizing: border-box; /* 包含 padding 在内计算宽度 */
  }

  .footer-content {
    width: 90%; /* 内容区域宽度稍微缩进 */
    margin: 0 auto; /* 居中内容 */
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
  }

  .footer-section {
    flex: 1;
    min-width: 200px;
    margin-bottom: 20px;
  }

  .footer-section h3 {
    font-size: 18px;
    margin-bottom: 15px;
  }

  .footer-section ul {
    list-style: none;
    padding: 0;
  }

  .footer-section ul li {
    margin-bottom: 10px;
  }

  .footer-section ul li a {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
  }

  .footer-section ul li a:hover {
    color: #00b4ff;
  }

  .qr-code-img {
    width: 120px;
    height: auto;
    margin-bottom: 10px;
  }

  .footer-bottom {
    width: 90%; /* 底部区域与内容区域一致 */
    margin: 20px auto 0; /* 居中内容 */
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    padding-top: 20px;
    border-top: 1px solid #3a4f63;
  }

  .footer-bottom-left {
    display: flex;
    align-items: center;
  }

  .footer-bottom-left p {
    margin-right: 20px;
    font-size: 14px;
  }

  .guided-logos img {
    height: 40px;
    margin-right: 10px;
  }

  .footer-bottom-right p {
    font-size: 12px;
    text-align: right;
  }
  </style>
