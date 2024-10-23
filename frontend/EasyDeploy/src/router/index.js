import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import DeployMain from '../components/Deploy/DeployMain.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
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
