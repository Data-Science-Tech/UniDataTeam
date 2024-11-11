import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import DeployMain from '../components/Deploy/DeployMain.vue';
import SaveConfig from '@/components/TrainConfig/SaveConfig.vue';

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home
  // },
  {
    path: '/',
    name: 'SaveConfig',
    component: SaveConfig
  },
  {
    path: '/DeployMain',
    name: 'DeployMain',
    component: DeployMain
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
