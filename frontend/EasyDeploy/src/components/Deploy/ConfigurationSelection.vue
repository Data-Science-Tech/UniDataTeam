<template>
    <div class="container">
      <!-- 操作系统选择 -->
      <div class="form-group">
        <h3 class="label">操作系统</h3>
        <div class="button-group">
          <el-button
            v-for="os in Object.keys(osTree)"
            :key="os"
            :type="selectedOS === os ? 'primary' : 'default'"
            @click="selectOS(os)"
          >
            {{ os }}
          </el-button>
        </div>
      </div>
  
      <!-- 架构选择 -->
      <div v-if="selectedOS" class="form-group">
        <h3 class="label">架构</h3>
        <div class="button-group">
          <el-button
            v-for="arch in Object.keys(osTree[selectedOS])"
            :key="arch"
            :type="selectedArchitecture === arch ? 'primary' : 'default'"
            @click="selectArchitecture(arch)"
          >
            {{ arch }}
          </el-button>
        </div>
      </div>
  
      <!-- 发行方选择 -->
      <div v-if="selectedArchitecture" class="form-group">
        <h3 class="label">发行方</h3>
        <div class="button-group">
          <el-button
            v-for="distro in Object.keys(osTree[selectedOS][selectedArchitecture])"
            :key="distro"
            :type="selectedDistribution === distro ? 'primary' : 'default'"
            @click="selectDistribution(distro)"
          >
            {{ distro }}
          </el-button>
        </div>
      </div>
  
      <!-- 版本选择 -->
      <div v-if="selectedDistribution" class="form-group">
        <h3 class="label">版本</h3>
        <div class="button-group">
          <el-button
            v-for="version in osTree[selectedOS][selectedArchitecture][selectedDistribution].versions"
            :key="version"
            :type="selectedVersion === version ? 'primary' : 'default'"
            @click="selectVersion(version)"
          >
            {{ version }}
          </el-button>
        </div>
      </div>
  
      <!-- 安装包类型选择 -->
      <div v-if="selectedVersion" class="form-group">
        <h3 class="label">安装包类型</h3>
        <div class="button-group">
          <el-button
            v-for="installer in osTree[selectedOS][selectedArchitecture][selectedDistribution].installerTypes"
            :key="installer"
            :type="selectedInstallerType === installer ? 'primary' : 'default'"
            @click="selectInstallerType(installer)"
          >
            {{ installer }}
          </el-button>
        </div>
      </div>
  
      <!-- 显示其他信息 -->
      <div v-if="selectedInstallerType" class="form-group">
        <h3 class="label">Hello World！</h3>
      </div>
    </div>
  </template>
  

  <script setup>
  import { ref } from 'vue';

  
  // 树形结构数据，存储操作系统、架构、发行版、版本、安装包类型
  const osTree = {
    Linux: {
      'x86_64': {
        'Amazon-Linux': {
          versions: ['2023'],
          installerTypes: ['rpm (local)', 'rpm (network)']
        },
        'Amure-Linux': {
          versions: ['2'],
          installerTypes: ['rpm (local)', 'rpm (network)']
        },
        Debian: {
          versions: ['11', '12'],
          installerTypes: ['deb (local)', 'deb (network)', 'runfile (local)']
        },
        Fedora: {
          versions: ['39'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        KylinOS: {
          versions: ['10'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        OpenSUSE: {
          versions: ['15'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        RHEL: {
          versions: ['8', '9'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        Rocky: {
          versions: ['8', '9'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        SLES: {
          versions: ['15'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        Ubuntu: {
          versions: ['20.04', '22.04', '24.04'],
          installerTypes: ['deb (local)', 'deb (network)', 'runfile (local)']
        },
        'WSL-Ubuntu': {
          versions: ['2.0'],
          installerTypes: ['deb (local)', 'deb (network)', 'runfile (local)']
        },
        
      },
      'arm64-sbsa': {
        KylinOS: {
          versions: ['10'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        RHEL: {
          versions: ['8', '9'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        SLES: {
          versions: ['15'],
          installerTypes: ['rpm (local)', 'rpm (network)', 'runfile (local)']
        },
        Ubuntu: {
          versions: ['20.04', '22.04', '24.04'],
          installerTypes: ['deb (local)', 'deb (network)', 'runfile (local)']
        },
      },
      'aarch64-jetson':{
        Ubuntu: {
          versions: ['20.04'],
          installerTypes: ['deb (local)', 'deb (network)']
        },
      }
    },
    Windows: {
      'x86_64': {
        Microsoft: {
            versions: ['10', '11','Server 2022'],
            installerTypes: ['exe (local)', 'exe (network)']
        }
          
      }
    }
  };
  
  // 选择的操作系统、架构、发行版、版本、安装包类型
  const selectedOS = ref('');
  const selectedArchitecture = ref('');
  const selectedDistribution = ref('');
  const selectedVersion = ref('');
  const selectedInstallerType = ref('');
  
  // 选择操作系统
  const selectOS = (os) => {
    selectedOS.value = os;
    selectedArchitecture.value = '';
    selectedDistribution.value = '';
    selectedVersion.value = '';
    selectedInstallerType.value = '';
  };
  
  // 选择架构
  const selectArchitecture = (arch) => {
    selectedArchitecture.value = arch;
    selectedDistribution.value = '';
    selectedVersion.value = '';
    selectedInstallerType.value = '';
  };
  
  // 选择发行版
  const selectDistribution = (distro) => {
    selectedDistribution.value = distro;
    selectedVersion.value = '';
    selectedInstallerType.value = '';
  };
  
  // 选择版本
  const selectVersion = (version) => {
    selectedVersion.value = version;
    selectedInstallerType.value = '';
  };
  
  // 选择安装包类型
  const selectInstallerType = (installer) => {
    selectedInstallerType.value = installer;

  // 打印用户选择的所有值
  console.log(`Selected Configuration:
  OS: ${selectedOS.value}
  Architecture: ${selectedArchitecture.value}
  Distribution: ${selectedDistribution.value}
  Version: ${selectedVersion.value}
  Installer Type: ${selectedInstallerType.value}`);
  };
</script>
  

<style scoped>
.container {
  width: 80%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  background-color: #f8f9fa;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: height 0.3s ease-in-out;
}

/* 操作系统、架构、发行方等选择按钮的样式 */
.el-button {
  border-radius: 5px;
  padding: 10px 20px;
  margin: 10px;
  font-size: 16px;
  border: 1px solid #ced4da;
  color: #333;
  background-color: #fff;
  transition: background-color 0.3s, color 0.3s;
}

.el-button:hover {
  background-color: #e9ecef;
}

.el-button.primary {
  background-color: #0d6efd;
  color: #fff;
  border-color: #0d6efd;
}

.el-button.primary:hover {
  background-color: #0b5ed7;
  border-color: #0b5ed7;
}

/* 提示词和对应右侧按钮位置关系调整 */
.form-group {
  display: flex;
  align-items: center; /* 垂直居中对齐 */
  margin-bottom: 16px; /* 提高行之间的间隔 */
}

.form-group label {
  flex: 1; /* 左侧占据剩余空间 */
  margin-right: 16px; /* 右侧间距 */
  font-weight: bold; /* 提示词加粗 */
}

.button-group {
  display: flex; /* 使按钮水平排列 */
  flex-wrap: wrap; /* 允许按钮换行 */
  min-width: 200px; /* 设置一个最小宽度以保持一致性 */
}

.button-group .el-button {
  margin-right: 8px; /* 按钮之间的间隔 */
  margin-bottom: 8px; /* 按钮换行时的底部间隔 */
}


div {
  margin: 20px 0;
  text-align: center;
}

.label {
  font-size: 28px;
  font-weight: bold;
  color: #212529;
  margin-bottom: 20px;
  flex-basis: 30%;
  text-align: left;
  min-width: 30%;
}

/* 每个模块的外边距 */
.el-button-group {
  margin: 30px auto;
  text-align: center;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .row {
    flex-direction: column;
    align-items: flex-start;
  }

  .label {
    margin-bottom: 10px;
  }

  .button-group {
    justify-content: flex-start;
  }
}
</style>