<template>
    <div class="container">
        <div class="title">
            环境配置
        </div>
        <!-- 操作系统选择 -->
        <div class="form-group">
            <h3 class="label">操作系统</h3>
            <div class="button-group">
                <button v-for="os in Object.keys(osTree)" :key="os" 
                    :class="['button', selectedOS === os ? 'primary' : 'default']"
                    @click="selectOS(os)">
                    {{ os }}
                </button>
            </div>
        </div>

        <!-- 架构选择 -->
        <div v-if="selectedOS" class="form-group">
            <h3 class="label">架构</h3>
            <div class="button-group">
                <button v-for="arch in Object.keys(osTree[selectedOS])" :key="arch"
                    :class="['button', selectedArchitecture === arch ? 'primary' : 'default']"
                    @click="selectArchitecture(arch)">
                    {{ arch }}
                </button>
            </div>
        </div>

        <!-- 发行方选择 -->
        <div v-if="selectedArchitecture" class="form-group">
            <h3 class="label">发行方</h3>
            <div class="button-group">
                <button v-for="distro in Object.keys(osTree[selectedOS][selectedArchitecture])" :key="distro"
                    :class="['button', selectedDistribution === distro ? 'primary' : 'default']"
                    @click="selectDistribution(distro)">
                    {{ distro }}
                </button>
            </div>
        </div>

        <!-- 版本选择 -->
        <div v-if="selectedDistribution" class="form-group">
            <h3 class="label">版本</h3>
            <div class="button-group">
                <button v-for="version in osTree[selectedOS][selectedArchitecture][selectedDistribution].versions" 
                    :key="version"
                    :class="['button', selectedVersion === version ? 'primary' : 'default']"
                    @click="selectVersion(version)">
                    {{ version }}
                </button>
            </div>
        </div>

        <!-- 安装包类型选择 -->
        <div v-if="selectedVersion" class="form-group">
            <h3 class="label">安装包类型</h3>
            <div class="button-group">
                <button v-for="installer in osTree[selectedOS][selectedArchitecture][selectedDistribution].installerTypes" 
                    :key="installer"
                    :class="['button', selectedInstallerType === installer ? 'primary' : 'default']"
                    @click="selectInstallerType(installer)">
                    {{ installer }}
                </button>
            </div>
        </div>

        <!-- 确认按钮 -->
        <div v-if="selectedInstallerType" class="button-group confirm-group">
            <button type="button" @click="SelectServer" class="button confirm-btn" :disabled="!isComplete">
                确定选择服务器配置
            </button>
        </div>
    </div>
</template>



<script setup>
import { ref, computed } from "vue"; 
import { useGlobalStore } from '@/stores/ConfigStore.js';
import { useRouter } from 'vue-router';

// 初始化 Pinia Store
const globalStore = useGlobalStore();
const router = useRouter();


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
        'aarch64-jetson': {
            Ubuntu: {
                versions: ['20.04'],
                installerTypes: ['deb (local)', 'deb (network)']
            },
        }
    },
    Windows: {
        'x86_64': {
            Microsoft: {
                versions: ['10', '11', 'Server 2022'],
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

// 确认按钮操作
const SelectServer = async () => {
    if (!isComplete.value) {
        console.error("请完成所有配置后再尝试！");
        return;
    }
    try {
        console.log("选择服务器成功:");
        router.push("/uikit/start");
    } catch (error) {
        console.error("选择服务器失败:", error);
    }
};

// 计算是否完成所有配置
const isComplete = computed(() => {
    return (
        selectedOS.value &&
        selectedArchitecture.value &&
        selectedDistribution.value &&
        selectedVersion.value &&
        selectedInstallerType.value
    );
});

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
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
    font-size: 1.8rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
    color: #333;
}

.form-group {
    margin-bottom: 20px;
}

.label {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 10px;
    color: #555;
}

.button-group {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
}

.button {
    font-size: 1rem;
    padding: 10px 15px;
    border-radius: 5px;
    border: 1px solid #ddd;
    background-color: #fff;
    color: #333;
    cursor: pointer;
    transition: all 0.3s ease;
}

.button:hover {
    background-color: #f0f0f0;
    border-color: #ccc;
}

.button.primary {
    background-color: #409eff; /* 选项按钮的主色调 */
    color: #fff;
    border: none;
}

.button.primary:hover {
    background-color: #66b1ff; /* 选项按钮的悬停色 */
}

.button:disabled {
    background-color: #ccc;
    color: #999;
    cursor: not-allowed;
}

.confirm-group {
    margin-top: 20px;
    display: flex;
    justify-content: center;
}

.confirm-btn {
    font-size: 1rem;
    font-weight: bold;
    background-color: #52c41a; /* 确认按钮的主色调 */
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.confirm-btn:hover {
    background-color: #73d13d; /* 确认按钮的悬停色 */
}

.confirm-btn:disabled {
    background-color: #bbb;
    color: #fff;
}
</style>
