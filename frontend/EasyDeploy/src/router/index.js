import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import ConfigurationSelection from '../components/Deploy/ConfigurationSelection.vue';

const routes = [
  // {
  //   path: '/',
  //   name: 'Home',
  //   component: Home
  // },
  {
    path: '/',
    name: 'ConfigurationSelection',
    component: ConfigurationSelection
  },
  
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
