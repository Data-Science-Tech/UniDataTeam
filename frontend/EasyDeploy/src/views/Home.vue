<template>
  <div>
    <HeaderComponent />
    <PictureComponent />
    <div class="search-bar-container">
      <SearchBarComponent />
    </div>
    <div class="feature-container">
      <FeatureComponent />
    </div>
    <div class="example-container">
      <ExampleComponent />
    </div>
    <div class="statistic-container">
      <StatisticComponent />
    </div>
    <div class="news-container">
      <NewsComponent />
    </div>
    <div class="collaborators-container">
      <CollaboratorsComponent />
    </div>
    <div class="footer-container">
      <FooterComponent />
    </div> 
  </div>
</template>

<script>
import PictureComponent from '@/components/Home/PictureComponent.vue';
import HeaderComponent from '@/components/Home/HeaderComponent.vue';
import SearchBarComponent from '@/components/Home/SearchBarComponent.vue';
import FeatureComponent from '@/components/Home/FeatureComponent.vue';
import ExampleComponent from '@/components/Home/ExampleComponent.vue';
import StatisticComponent from '@/components/Home/StatisticComponent.vue';
import NewsComponent from '@/components/Home/NewsComponent.vue';
import CollaboratorsComponent from '@/components/Home/CollaboratorsComponent.vue';
import FooterComponent from '@/components/Home/FooterComponent.vue';

export default {
  components: {
    PictureComponent,
    HeaderComponent,
    SearchBarComponent,
    FeatureComponent,
    ExampleComponent,
    StatisticComponent,
    NewsComponent,
    CollaboratorsComponent,
    FooterComponent,
  },
};
</script>

<style scoped>
.search-bar-container {
  display: flex;
  justify-content: center;
  scale: 1.6;
}
.feature-container {
  display: flex;
  justify-content: center;
  margin-top: 50px; 
}
.example-container {
  display: flex;
  justify-content: center;
  margin-top: 100px; 
}
.statistic-container {
  display: flex;
  justify-content: center;
  margin-top: 100px; 
}
.news-container {
  display: flex;
  justify-content: center;
  margin-top: 50px; 
}
.collaborators-container {
  display: flex;
  justify-content: center;
  margin-top: 50px; 
}
.footer-container {
  display: flex;
  justify-content: center;
  margin-top: 50px; 
}

</style>
