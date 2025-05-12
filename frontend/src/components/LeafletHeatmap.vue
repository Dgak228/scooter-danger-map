<template>
  <div ref="map" class="leaflet-map" :style="{height: '100%'}"></div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

const props = defineProps({
  points: {
    type: Array,
    default: () => []
  }
})

const map = ref(null)
let leafletMap = null
let heatLayer = null

const initMap = () => {
  leafletMap = L.map(map.value).setView([45.035470, 38.975313], 12)
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: ''
  }).addTo(leafletMap)
  leafletMap.attributionControl.setPrefix('')
  leafletMap.attributionControl.remove()
  addHeatmap()
}

const addHeatmap = () => {
  if (!leafletMap) return
  if (heatLayer) {
    leafletMap.removeLayer(heatLayer)
    heatLayer = null
  }
  if (!props.points.length) return
  const heatmapData = props.points.map(p => [p.lat, p.lon, 1.2]) // чуть выше интенсивность
  heatLayer = L.heatLayer(heatmapData, {
    radius: 50,
    blur: 8,
    maxZoom: 17,
    gradient: {
      0.2: '#ff0000',   // красный
      0.5: '#b20000',   // тёмно-красный
      1.0: '#800000'    // бордовый
    }
  }).addTo(leafletMap)
}

onMounted(() => {
  initMap()
})

watch(() => props.points, () => {
  addHeatmap()
})
</script>

<style scoped>
.leaflet-map {
  width: 100%;
  height: 100% !important;
  min-height: 400px;
  border-radius: 8px;
  overflow: hidden;
  flex: 1 1 auto;
  display: flex;
}

.leaflet-control-attribution,
.leaflet-control-logo {
  display: none !important;
}
</style> 