import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import 'leaflet.heat'

let leafletMap = null
let heatLayer = null
let mapContainer = null

export function getOrCreateMap(container) {
  if (!leafletMap) {
    leafletMap = L.map(container).setView([45.035470, 38.975313], 12)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: ''
    }).addTo(leafletMap)
    leafletMap.attributionControl.setPrefix('')
    leafletMap.attributionControl.remove()
    mapContainer = container
  } else if (container !== mapContainer) {
    // Очищаем новый контейнер перед вставкой карты
    while (container.firstChild) {
      container.removeChild(container.firstChild)
    }
    // Перемещаем DOM-элемент карты в новый контейнер
    container.appendChild(leafletMap.getContainer())
    leafletMap.invalidateSize()
    mapContainer = container
  }
  return leafletMap
}

export function setHeatmap(points) {
  if (!leafletMap) return
  if (heatLayer) {
    leafletMap.removeLayer(heatLayer)
    heatLayer = null
  }
  if (!points.length) return
  const heatmapData = points.map(p => [p.lat, p.lon, 1.2])
  heatLayer = L.heatLayer(heatmapData, {
    radius: 50,
    blur: 8,
    maxZoom: 17,
    gradient: {
      0.2: '#ff0000',
      0.5: '#b20000',
      1.0: '#800000'
    }
  }).addTo(leafletMap)
} 