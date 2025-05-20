<template>
  <div class="route-page">
    <h1>Построение маршрута</h1>
    <RouteBuilder />
  </div>
</template>

<script>
import RouteBuilder from '../components/RouteBuilder.vue'

export default {
  name: 'RoutePage',
  components: {
    RouteBuilder
  }
}
</script>

<style scoped>
.route-page {
  padding: 1rem;
  height: 100%;
}

h1 {
  margin-bottom: 1rem;
}
</style> 