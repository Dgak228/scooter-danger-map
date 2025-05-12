<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import LeafletHeatmap from './components/LeafletHeatmap.vue'
import { ElNotification } from 'element-plus'

const form = ref({
  date: '',
  time: '',
  street: '',
  house: '',
  injured: false
})
const formRef = ref()
const rules = {
  date: [{ required: true, message: 'Укажите дату', trigger: 'blur' }],
  time: [{ required: true, message: 'Укажите время', trigger: 'blur' }],
  street: [{ required: true, message: 'Укажите улицу', trigger: 'blur' }],
  house: [{ required: true, message: 'Укажите дом', trigger: 'blur' }]
}

const dtpList = ref([])
const heatmapPoints = ref([])

const fetchDtp = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/dtp/list')
    dtpList.value = res.data
  } catch (e) {
    ElNotification({
      title: 'Ошибка',
      message: 'Не удалось загрузить данные',
      type: 'error',
      duration: 2500
    })
  }
}

const fetchHeatmapPoints = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/dtp')
    heatmapPoints.value = res.data
  } catch (e) {
    // не показываем уведомление, чтобы не мешать работе таблицы
  }
}

const onSubmit = async () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      await axios.post('http://localhost:5000/api/dtp', {
        date: form.value.date,
        time: form.value.time,
        street: form.value.street,
        house: form.value.house,
        injured: form.value.injured
      })
      form.value = { date: '', time: '', street: '', house: '', injured: false }
      ElNotification({
        title: 'Успех',
        message: 'Инцидент добавлен',
        type: 'success',
        duration: 2500
      })
      fetchDtp()
      fetchHeatmapPoints()
    } catch (e) {
      ElNotification({
        title: 'Ошибка',
        message: 'Не удалось добавить инцидент',
        type: 'error',
        duration: 2500
      })
    }
  })
}

onMounted(() => {
  fetchDtp()
  fetchHeatmapPoints()
})
</script>

<template>
  <div>
    <header class="main-header">
      <h2 class="site-title">Карта опасных зон — Электросамокаты Краснодар</h2>
      <nav class="main-nav">
        <router-link to="/" class="nav-link" active-class="active" exact>Главная</router-link>
        <router-link to="/dtp" class="nav-link" active-class="active">ДТП</router-link>
        <router-link to="/add" class="nav-link" active-class="active">Добавить ДТП</router-link>
      </nav>
    </header>
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<style>
body {
  background: #f0f2f5;
}
.main-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 64px;
  background: #fff;
  box-shadow: 0 2px 8px #f0f1f2;
  z-index: 100;
  display: flex;
  align-items: center;
  padding: 0 32px;
  justify-content: space-between;
}
.site-title {
  margin: 0;
  font-weight: 700;
  font-size: 1.35rem;
  color: #222;
  letter-spacing: 0.01em;
  line-height: 64px;
}
.main-nav {
  display: flex;
  gap: 24px;
}
.nav-link {
  color: #222;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.1rem;
  padding: 6px 18px;
  border-radius: 6px;
  transition: background 0.2s, color 0.2s;
}
.nav-link.active, .nav-link.router-link-exact-active {
  background: #409eff;
  color: #fff;
}
.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 80px;
  padding-bottom: 40px;
  min-height: 100vh;
}
.main-row {
  margin-left: 0 !important;
  margin-right: 0 !important;
}
.map-placeholder {
  height: 400px;
  background: linear-gradient(135deg, #e0e7ef 0%, #f5f7fa 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #bbb;
  font-size: 1.2rem;
  border-radius: 8px;
  border: 1px dashed #d3dce6;
  margin-bottom: 8px;
}
.el-card {
  border-radius: 10px;
}
@media (max-width: 600px) {
  .main-header {
    height: 48px;
    padding: 0 8px;
  }
  .site-title {
    font-size: 1rem;
    line-height: 48px;
  }
  .main-content {
    padding-top: 56px;
  }
  .main-nav {
    gap: 8px;
  }
  .nav-link {
    font-size: 0.95rem;
    padding: 4px 10px;
  }
}
</style>
