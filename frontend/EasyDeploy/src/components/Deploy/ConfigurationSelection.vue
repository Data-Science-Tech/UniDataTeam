<template>
    <div>
      <!-- 操作系统选择 -->
      <h3>操作系统</h3>
      <div>
        <el-button
          v-for="os in Object.keys(osTree)"
          :key="os"
          :type="selectedOS === os ? 'primary' : 'default'"
          @click="selectOS(os)"
        >
          {{ os }}
        </el-button>
      </div>
  
      <!-- 架构选择 -->
      <div v-if="selectedOS">
        <h3>架构</h3>
        <div>
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
      <div v-if="selectedArchitecture">
        <h3>发行方</h3>
        <div>
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
      <div v-if="selectedDistribution">
        <h3>版本</h3>
        <div>
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
      <div v-if="selectedVersion">
        <h3>安装包类型</h3>
        <div>
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
    <div v-if="selectedInstallerType">
      <h3>Hello World！</h3>
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
  