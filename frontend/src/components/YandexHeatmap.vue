<template>
  <div ref="map" class="yandex-map"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  points: {
    type: Array,
    default: () => []
  }
})

const map = ref(null)
let ymapsInstance = null
let heatmap = null
let mapReady = false

const initMap = () => {
  if (!window.ymaps) return
  window.ymaps.ready(() => {
    ymapsInstance = new window.ymaps.Map(map.value, {
      center: [45.035470, 38.975313], // Краснодар
      zoom: 12,
      controls: ['zoomControl']
    })
    mapReady = true
    addHeatmap()
  })
}

const addHeatmap = () => {
  if (!window.ymaps || !ymapsInstance || !mapReady) return
  if (heatmap) {
    heatmap.setMap(null)
    heatmap = null
  }
  if (!props.points.length) return
  const heatmapData = props.points.map(p => [p.lat, p.lon])
  console.log('Heatmap points:', heatmapData)
  window.ymaps.modules.require(['Heatmap'], function(Heatmap) {
    heatmap = new Heatmap(heatmapData, {
      radius: 60,
      intensityOfMidpoint: 1,
      dissipating: true,
      opacity: 0.8
    })
    heatmap.setMap(ymapsInstance)
  })
}

onMounted(() => {
  initMap()
})

watch(
  () => props.points,
  () => {
    if (mapReady) addHeatmap()
  }
)
</script>

<style scoped>
.yandex-map {
  width: 100%;
  height: 400px;
  border-radius: 8px;
  overflow: hidden;
}
</style> 