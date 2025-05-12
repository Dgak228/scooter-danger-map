<template>
  <div>
    <h2 style="margin-bottom: 24px;">ДТП с участием электросамокатов г. Краснодар</h2>
    <el-row style="margin-top: 0;">
      <el-col :span="24">
        <el-card shadow="hover">
          <h3>Список инцидентов</h3>
          <el-table :data="dtpList" style="width: 100%" stripe border empty-text="Нет данных">
            <el-table-column prop="date" label="Дата" width="110" />
            <el-table-column prop="time" label="Время" width="110" />
            <el-table-column prop="address" label="Адрес" />
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const dtpList = ref([])

const fetchDtp = async () => {
  try {
    const res = await axios.get('http://localhost:5000/api/dtp/list')
    dtpList.value = res.data
  } catch (e) {}
}

onMounted(() => {
  fetchDtp()
})
</script> 