<template>
    <HeaderComponent/>
    <TitleComponent/>
</template>

<script>
import HeaderComponent from '@/components/DatasetDetail/HeaderComponent.vue';
import TitleComponent from '@/components/DatasetDetail/TitleComponent.vue';

export default {
  components: {
    HeaderComponent,
    TitleComponent,
  },
};
</script>

<style scoped>
.header-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  z-index: 1;
}
</style>