<template>
  <div class="route-map-container">
    <div class="route-controls">
      <input v-model="startAddress" type="text" placeholder="Начальный адрес" :disabled="loading">
      <input v-model="endAddress" type="text" placeholder="Конечный адрес" :disabled="loading">
      <button @click="buildRoute" :disabled="loading">
        {{ loading ? 'Строится маршрут...' : 'Построить маршрут' }}
      </button>
    </div>
    <div id="route-map" ref="mapContainer"></div>
  </div>
</template>

<script>
export default {
  name: 'RouteMap',
  data() {
    return {
      map: null,
      startAddress: '',
      endAddress: '',
      loading: false
    }
  },
  mounted() {
    // Инициализация карты после загрузки API
    ymaps.ready(() => {
      this.initMap();
    });
  },
  methods: {
    normalizeAddress(addr) {
      let address = addr.trim();
      // Если нет 'краснодар' — добавляем в начало
      if (!address.toLowerCase().includes('краснодар')) {
        address = 'Краснодар, ' + address;
      }
      // Разбиваем на город и остальное
      let parts = address.split(',');
      if (parts.length === 1) {
        // Нет запятой, значит только улица и дом
        address = 'Краснодар, улица ' + address.replace(/^ул\.?\s*/i, '');
      } else if (parts.length >= 2) {
        // parts[0] — город, parts[1] — улица и дом
        let city = parts[0].trim();
        let street = parts.slice(1).join(',').trim();
        if (!street.toLowerCase().includes('улица') && !street.toLowerCase().includes('ул.')) {
          street = 'улица ' + street.replace(/^ул\.?\s*/i, '');
        }
        address = city + ', ' + street;
      }
      return address;
    },
    initMap() {
      try {
        // Создаем карту
        this.map = new ymaps.Map(this.$refs.mapContainer, {
          center: [45.0448, 38.9760], // Краснодар
          zoom: 12,
          controls: ['zoomControl', 'fullscreenControl']
        });

        // Добавляем поиск
        this.map.controls.add(new ymaps.control.SearchControl({
          options: {
            provider: 'yandex#search'
          }
        }));
      } catch (error) {
        console.error('Error initializing map:', error);
        alert('Ошибка при инициализации карты');
      }
    },
    async buildRoute() {
      if (!this.startAddress || !this.endAddress) {
        alert('Пожалуйста, введите начальный и конечный адреса');
        return;
      }

      this.loading = true;

      try {
        // Очищаем карту
        this.map.geoObjects.removeAll();

        const normStart = this.normalizeAddress(this.startAddress);
        const normEnd = this.normalizeAddress(this.endAddress);
        console.log('Sending request with addresses:', { start: normStart, end: normEnd });

        // Запрашиваем маршрут
        const response = await fetch('/api/route', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            start: normStart,
            end: normEnd
          })
        });

        const data = await response.json();
        console.log('Received response:', data);

        if (!response.ok) {
          throw new Error(data.error || 'Ошибка при получении маршрута');
        }

        if (data.error) {
          throw new Error(data.error);
        }

        if (!data.start || !data.end || !Array.isArray(data.start) || !Array.isArray(data.end) || data.start.length < 2 || data.end.length < 2) {
          alert('Ошибка: не удалось получить координаты для построения маршрута');
          this.loading = false;
          return;
        }

        // Создаем маршрут
        const multiRoute = new ymaps.multiRouter.MultiRoute({
          referencePoints: [
            `${data.start[0]},${data.start[1]}`,
            `${data.end[0]},${data.end[1]}`
          ],
          params: {
            routingMode: 'bicycle'
          }
        }, {
          boundsAutoApply: true
        });

        // Добавляем маршрут на карту
        this.map.geoObjects.add(multiRoute);

        // Добавляем точки ДТП
        if (data.dtp_points && data.dtp_points.length > 0) {
          console.log('Adding DTP points:', data.dtp_points);
          data.dtp_points.forEach(point => {
            const placemark = new ymaps.Placemark([point.lat, point.lon], {}, {
              preset: 'islands#redDotIcon'
            });
            this.map.geoObjects.add(placemark);
          });
        }

      } catch (error) {
        console.error('Error:', error);
        alert(error.message || 'Произошла ошибка при построении маршрута');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.route-map-container {
  position: relative;
  width: 100%;
  height: 100vh;
}

#route-map {
  width: 100%;
  height: 100%;
}

.route-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 1000;
  background: white;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.route-controls input {
  width: 250px;
  padding: 8px;
  margin: 5px 0;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.route-controls input:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.route-controls button {
  width: 100%;
  padding: 8px;
  margin-top: 10px;
  background-color: #004494;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.route-controls button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.route-controls button:hover:not(:disabled) {
  background-color: #005fa3;
}
</style> 