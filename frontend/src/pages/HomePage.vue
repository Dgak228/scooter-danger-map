<template>
  <div>
    <el-row :gutter="24" class="main-row" align="stretch">
      <el-col :xs="24" :md="16">
        <el-card shadow="hover" class="map-card">
          <LeafletHeatmap :points="heatmapPoints" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="8">
        <el-card shadow="hover" class="info-block">
          <h3>О сервисе</h3>
          <p>
            Этот сервис предназначен для мониторинга и анализа опасных зон для электросамокатов в городе Краснодар.<br><br>
            <b>Возможности:</b>
            <ul>
              <li>Визуализация тепловой карты происшествий с участием электросамокатов.</li>
              <li>Просмотр и поиск зарегистрированных ДТП.</li>
              <li>Добавление новых инцидентов с указанием адреса, даты, времени и наличия пострадавших.</li>
            </ul>
            <b>Назначение:</b>
            <ul>
              <li>Повышение безопасности движения для пользователей электросамокатов.</li>
              <li>Помощь в выявлении наиболее опасных участков города.</li>
              <li>Сбор статистики для анализа и принятия решений.</li>
            </ul>
          </p>
        </el-card>
      </el-col>
    </el-row>
    <el-backtop :right="40" :bottom="40" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import LeafletHeatmap from '../components/LeafletHeatmap.vue'

const heatmapPoints = ref([])

const fetchHeatmapPoints = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/dtp')
    heatmapPoints.value = res.data
  } catch (e) {}
}

onMounted(() => {
  fetchHeatmapPoints()
})
</script>

<style scoped>
.el-row.main-row {
  align-items: stretch;
  min-height: 600px;
}
.map-card,
.info-block {
  height: 100%;
  min-height: 500px;
  display: flex;
  flex-direction: column;
}
.map-card .leaflet-map {
  flex: 1 1 auto;
  height: 100% !important;
  min-height: 400px;
}
.info-block ul {
  margin: 0 0 10px 18px;
  padding: 0;
}
.info-block h3 {
  margin-top: 0;
}
</style> 