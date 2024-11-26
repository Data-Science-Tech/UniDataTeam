<script setup>
import { useLayout } from '@/layout/composables/layout';
import AppConfigurator from './AppConfigurator.vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const { onMenuToggle, toggleDarkMode, isDarkTheme, gotoHome } = useLayout();

const gotoModel = () => {
    router.push('/model');
};

const gotoDataset = () => {
    router.push('/dataset');
};
</script>

<style scoped>
.searchbar {
    margin-left: 5vw;
}

.navbar-center {
  display: flex;
  list-style:none;
  padding: 0;
  margin: 0;
  margin-left: 5vw;
  font-weight: 600;
  font-family: 'Microsoft YaHei', sans-serif; 
  font-size: 8%;
  color: rgb(131, 131, 131);
}

.navbar-center li {
  margin: 0 15px;
  cursor: pointer;
  position: relative;
  font-size: 1vw; /* 增大导航栏字体大小 */
}


.navbar-center li:hover::after {
  width: 100%;
}

.navbar-right {
  display: flex;
  margin-right:10%;
}
</style>

<template>
    <div class="layout-topbar">
        <div class="layout-topbar-logo-container">
            <button class="layout-menu-button layout-topbar-action" @click="onMenuToggle">
                <i class="pi pi-bars"></i>
            </button>
            <router-link to="/" class="layout-topbar-logo">
                <img src="/src/assets/ha.png" alt="logo" style="height: 2.5rem; margin-left: 0.5rem;"/>
                <span>Easy Deploy</span>
                <span>工作台</span>
            </router-link>
        </div>
    <div class="searchbar">
        <SearchBarComponent/>
    </div>

      <ul class="navbar-center">
        <li @click="gotoHome">首页</li>
        <li @click="gotoModel">模型</li>
        <li @click="gotoDataset">数据集</li>
        <li>云服务</li>
        <li>使用文档</li>
        <li>社区</li>
        <li>关于我们</li>
      </ul>

        <div class="layout-topbar-actions">
            <div class="layout-config-menu">
                <button type="button" class="layout-topbar-action" @click="toggleDarkMode">
                    <i :class="['pi', { 'pi-moon': isDarkTheme, 'pi-sun': !isDarkTheme }]"></i>
                </button>
                <div class="relative">
                    <button
                        v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'animate-scalein', leaveToClass: 'hidden', leaveActiveClass: 'animate-fadeout', hideOnOutsideClick: true }"
                        type="button"
                        class="layout-topbar-action layout-topbar-action-highlight"
                    >
                        <i class="pi pi-palette"></i>
                    </button>
                    <AppConfigurator />
                </div>
            </div>

            <button
                class="layout-topbar-menu-button layout-topbar-action"
                v-styleclass="{ selector: '@next', enterFromClass: 'hidden', enterActiveClass: 'animate-scalein', leaveToClass: 'hidden', leaveActiveClass: 'animate-fadeout', hideOnOutsideClick: true }"
            >
                <i class="pi pi-ellipsis-v"></i>
            </button>

            <div class="layout-topbar-menu hidden lg:block">
                <div class="layout-topbar-menu-content">
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-calendar"></i>
                        <span>Calendar</span>
                    </button>
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-inbox"></i>
                        <span>Messages</span>
                    </button>
                    <button type="button" class="layout-topbar-action">
                        <i class="pi pi-user"></i>
                        <span>Profile</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
