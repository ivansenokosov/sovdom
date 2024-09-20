<script setup lang="ts">  
  import Message from 'primevue/message';
  //@ts-ignore
  import MicroData from '@/components/ChartMicro.vue';

  const props = defineProps(['data','years'])



//  ----------------------- загрузка годов для графиков
</script>

<template>
  <div class="card mt-5">
    <Message severity="secondary">
        <h1>Удельные показатели</h1>
        <p class="m-0">Стоимости выполнения видов работ, приведённые к сравнимым величинам по годам, например, 1 кв.м МОП, 1 лифт, 1 узел учёта:
              <ul>
                <li>стоимости работ по ставке платы (при наличии детализированной) на вид работ с разделением на работы и текущий ремонт;</li>
                <li>стоимости работ по отчёту, приведённой к удельному показателю, с разделением на работы и текущий ремонт;</li>
                <li>усреднённое значение;</li>
                <li>минимальное и максимальное значения;</li>
                <li>оптимальное значении по ценовому предложению участников рынка</li>
              </ul>
            </p>                  
    </Message>
  </div>

  <div v-if="data.loading">
    <p>Загружаю</p>
  </div>
  <div v-else>
    <div class="grid  mt-5">
      <div class="col-4 p-1" v-for="(micro, index) in data.microData">
          <MicroData :key="index" :data="micro" :years="years" :ref="index"/>  
      </div> 
    </div>
  </div>
</template>

<style scoped>
</style>
