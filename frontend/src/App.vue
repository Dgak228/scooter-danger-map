<script setup>
import { ref, onMounted, reactive } from 'vue'
import axios from 'axios'

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

const notification = reactive({
  visible: false,
  title: '',
  message: '',
  type: 'success'
})

const fetchDtp = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/dtp/list')
    dtpList.value = res.data
  } catch (e) {
    notification.visible = true
    notification.title = 'Ошибка'
    notification.message = 'Не удалось загрузить данные'
    notification.type = 'error'
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
      notification.visible = true
      notification.title = 'Успех'
      notification.message = 'Инцидент добавлен'
      notification.type = 'success'
      fetchDtp()
    } catch (e) {
      notification.visible = true
      notification.title = 'Ошибка'
      notification.message = 'Не удалось добавить инцидент'
      notification.type = 'error'
    }
  })
}

onMounted(() => {
  fetchDtp()
})
</script>

<template>
  <div>
    <header class="main-header">
      <h2 class="site-title">Карта опасных зон — Электросамокаты Краснодар</h2>
    </header>
    <div class="main-content">
      <el-row :gutter="24" class="main-row">
        <el-col :xs="24" :md="16">
          <el-card shadow="hover">
            <h3>Карта происшествий</h3>
            <div class="map-placeholder">
              [Карта будет здесь]
            </div>
          </el-card>
        </el-col>
        <el-col :xs="24" :md="8">
          <el-card shadow="hover">
            <h3>Добавить инцидент</h3>
            <el-form :model="form" label-width="110px" @submit.prevent="onSubmit" :rules="rules" ref="formRef">
              <el-form-item label="Дата" prop="date">
                <el-date-picker v-model="form.date" type="date" placeholder="Выберите дату" style="width: 100%" />
              </el-form-item>
              <el-form-item label="Время" prop="time">
                <el-time-picker v-model="form.time" placeholder="Выберите время" style="width: 100%" />
              </el-form-item>
              <el-form-item label="Улица" prop="street">
                <el-input v-model="form.street" placeholder="Улица" />
              </el-form-item>
              <el-form-item label="Дом" prop="house">
                <el-input v-model="form.house" placeholder="Дом" />
              </el-form-item>
              <el-form-item>
                <el-checkbox v-model="form.injured">Есть пострадавшие</el-checkbox>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="onSubmit" style="width: 100%">Добавить</el-button>
              </el-form-item>
            </el-form>
          </el-card>
        </el-col>
      </el-row>
      <el-row style="margin-top: 32px;">
        <el-col :span="24">
          <el-card shadow="hover">
            <h3>Список инцидентов</h3>
            <el-table :data="dtpList" style="width: 100%" stripe border empty-text="Нет данных">
              <el-table-column prop="date" label="Дата" width="110" />
              <el-table-column prop="time" label="Время" width="110" />
              <el-table-column prop="street" label="Улица" />
              <el-table-column prop="house" label="Дом" width="90" />
              <el-table-column prop="injured" label="Пострадавшие" width="140">
                <template #default="scope">
                  <el-tag :type="scope.row.injured ? 'danger' : 'success'" effect="dark">
                    {{ scope.row.injured ? 'Да' : 'Нет' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </el-card>
        </el-col>
      </el-row>
      <el-backtop :right="40" :bottom="40" />
    </div>
    <el-notification v-if="notification.visible" :title="notification.title" :type="notification.type" :message="notification.message" :duration="2500" @close="notification.visible = false" />
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
}
.site-title {
  margin: 0;
  font-weight: 700;
  font-size: 1.35rem;
  color: #222;
  letter-spacing: 0.01em;
  line-height: 64px;
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
}
</style>
