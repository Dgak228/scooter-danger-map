<template>
  <div>
    <h2 style="margin-bottom: 24px;">Добавить ДТП</h2>
    <el-row justify="center">
      <el-col :xs="24" :md="12">
        <el-card shadow="hover">
          <el-form :model="form" label-width="110px" @submit.prevent="onSubmit" :rules="rules" ref="formRef">
            <el-form-item label="Дата" prop="date">
              <el-date-picker v-model="form.date" type="date" placeholder="Выберите дату" style="width: 100%" />
            </el-form-item>
            <el-form-item label="Время" prop="time">
              <el-time-picker v-model="form.time" placeholder="Выберите время" style="width: 100%" />
            </el-form-item>
            <el-form-item label="Адрес" prop="address">
              <el-input v-model="form.address" placeholder="Адрес (например, г. Краснодар, ул. Ленина, 1)" />
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
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { ElNotification } from 'element-plus'

const form = ref({
  date: '',
  time: '',
  address: '',
  injured: false
})
const formRef = ref()
const rules = {
  date: [{ required: true, message: 'Укажите дату', trigger: 'blur' }],
  time: [{ required: true, message: 'Укажите время', trigger: 'blur' }],
  address: [{ required: true, message: 'Укажите адрес', trigger: 'blur' }]
}

const onSubmit = async () => {
  formRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      await axios.post('http://localhost:5000/api/dtp', {
        date: form.value.date,
        time: form.value.time,
        address: form.value.address,
        injured: form.value.injured
      })
      form.value = { date: '', time: '', address: '', injured: false }
      ElNotification({
        title: 'Успех',
        message: 'Инцидент добавлен',
        type: 'success',
        duration: 2500
      })
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
</script> 