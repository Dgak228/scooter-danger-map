<template>
  <div class="route-builder">
    <div class="input-group">
      <el-input
        v-model="startAddress"
        placeholder="Начальный адрес (например: Краснодар, ул. Красная, 1)"
        class="address-input"
      />
      <el-input
        v-model="endAddress"
        placeholder="Конечный адрес (например: Краснодар, ул. Офицерская, 1)"
        class="address-input"
      />
      <el-button type="primary" @click="buildRoute" :loading="loading">
        Построить маршрут
      </el-button>
    </div>
    <div class="map-container" ref="mapContainer"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import axios from 'axios'
import { ElMessage } from 'element-plus'

export default {
  name: 'RouteBuilder',
  setup() {
    const mapContainer = ref(null)
    const map = ref(null)
    const startAddress = ref('')
    const endAddress = ref('')
    const loading = ref(false)
    const routeLayer = ref(null)
    const markersLayer = ref(null)

    const formatAddress = (address) => {
      // Добавляем "Краснодар" в начало адреса, если его нет
      if (!address.toLowerCase().includes('краснодар')) {
        address = `Краснодар, ${address}`
      }
      
      // Заменяем "ул." на "улица" для лучшего распознавания
      address = address.replace(/ул\./g, 'улица')
      
      // Убираем лишние пробелы
      address = address.replace(/\s+/g, ' ').trim()
      
      console.log('Formatted address:', address)
      return address
    }

    const initMap = () => {
      map.value = L.map(mapContainer.value).setView([45.0448, 38.9760], 13)
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
      }).addTo(map.value)
      
      routeLayer.value = L.layerGroup().addTo(map.value)
      markersLayer.value = L.layerGroup().addTo(map.value)
    }

    const buildRoute = async () => {
      if (!startAddress.value || !endAddress.value) {
        ElMessage.warning('Пожалуйста, введите начальный и конечный адреса')
        return
      }

      loading.value = true
      try {
        const response = await axios.post('http://localhost:5000/api/route', {
          start: formatAddress(startAddress.value),
          end: formatAddress(endAddress.value)
        })

        // Очищаем предыдущий маршрут
        routeLayer.value.clearLayers()
        markersLayer.value.clearLayers()

        // Отображаем точки ДТП
        response.data.dtp_points.forEach(point => {
          L.circleMarker([point.lat, point.lon], {
            radius: 8,
            color: 'red',
            fillColor: '#f03',
            fillOpacity: 0.5
          }).addTo(markersLayer.value)
        })

        // Отображаем маршрут
        const route = response.data.route.routes[0]
        const path = route.polyline.encodedPolyline
        const points = decodePolyline(path)
        
        L.polyline(points, {
          color: 'blue',
          weight: 5,
          opacity: 0.7
        }).addTo(routeLayer.value)

        // Устанавливаем границы карты по маршруту
        map.value.fitBounds(routeLayer.value.getBounds())
      } catch (error) {
        console.error('Route building error:', error)
        ElMessage.error('Ошибка при построении маршрута: ' + (error.response?.data?.error || error.message))
      } finally {
        loading.value = false
      }
    }

    // Функция для декодирования полилинии
    const decodePolyline = (encoded) => {
      const points = []
      let index = 0
      let lat = 0
      let lng = 0

      while (index < encoded.length) {
        let shift = 0
        let result = 0

        do {
          let b = encoded.charCodeAt(index++) - 63
          result |= (b & 0x1f) << shift
          shift += 5
        } while (result >= 0x20)

        let dlat = ((result & 1) ? ~(result >> 1) : (result >> 1))
        lat += dlat

        shift = 0
        result = 0

        do {
          let b = encoded.charCodeAt(index++) - 63
          result |= (b & 0x1f) << shift
          shift += 5
        } while (result >= 0x20)

        let dlng = ((result & 1) ? ~(result >> 1) : (result >> 1))
        lng += dlng

        points.push([lat * 1e-5, lng * 1e-5])
      }

      return points
    }

    onMounted(() => {
      initMap()
    })

    return {
      mapContainer,
      startAddress,
      endAddress,
      loading,
      buildRoute
    }
  }
}
</script>

<style scoped>
.route-builder {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem;
  height: 100%;
}

.input-group {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.address-input {
  flex: 1;
}

.map-container {
  flex: 1;
  min-height: 400px;
  border-radius: 8px;
  overflow: hidden;
}
</style> 