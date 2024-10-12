<template>
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section about">
          <h3>About</h3>
          <ul>
            <li><a href="#">Introduction</a></li>
            <li><a href="#">Influence</a></li>
            <li><a href="#">Chronicle of Events</a></li>
            <li><a href="#">Terms of Service</a></li>
            <li><a href="#">Contact Us</a></li>
          </ul>
        </div>
  
        <div class="footer-section collaborative-construction">
          <h3>Collaborative Construction</h3>
          <ul>
            <li><a href="#">Our Partner</a></li>
            <li><a href="#">Featured Data Community</a></li>
            <li><a href="#">About Data Community</a></li>
          </ul>
        </div>
  
        <div class="footer-section help">
          <h3>Help</h3>
          <ul>
            <li><a href="#">Publishing Processes</a></li>
            <li><a href="#">Data Policy</a></li>
            <li><a href="#">Preferred File Format</a></li>
            <li><a href="#">Open API</a></li>
            <li><a href="#">FAQ</a></li>
          </ul>
        </div>
  
        <div class="footer-section qr-code">
          <img src="https://via.placeholder.com/120" alt="QR Code" class="qr-code-img" />
          <p>Follow the public account</p>
        </div>
      </div>
  
      <div class="footer-bottom">
        <div class="footer-bottom-left">
          <p>Guided by</p>
          <div class="guided-logos">
            <img src="https://via.placeholder.com/100x40" alt="Logo 1" />
            <img src="https://via.placeholder.com/100x40" alt="Logo 2" />
            <img src="https://via.placeholder.com/100x40" alt="Logo 3" />
          </div>
        </div>
        <div class="footer-bottom-right">
          <p>&copy; 2015-2024 Computer Network Information Center, Chinese Academy of Sciences. All Rights Reserved. Beijing ICP NO. 09112257-88</p>
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
  