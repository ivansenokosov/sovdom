<script setup lang="ts">
  import {ref, watch } from 'vue'

  import Message from 'primevue/message';
  import CitiesTab from '@/components/CitiesTab.vue';
  import Map from '@/components/Map.vue';
  import BuildAnalizeCard from '@/components/BuildAnalizeCard.vue';
  import MacroDataAnalyze from '@/components/MacroDataAnalyze.vue';
  import MicroDataAnalyze from '@/components/MicroDataAnalyze.vue';

  import type { LngLat } from '@yandex/ymaps3-types';
  import type { IMacroData, IMicroContainer, IDocument, IBuild, IBuildCard } from '@/interfaces';

  import { useFetch } from '@/api/useFetch';
  import { loadMacroData } from '@/api/loadMacroData';
  import { loadMicroData } from '@/api/loadMIcroData ';

  const buildId       = ref<number>(0)    // выбранный дом
  const error_message = ref<string>('')
  const macroData     = ref<IMacroData>({years: [], macroData: [], macroDataSum: [], error: null, loading: true})  // данные макропоказателей
  const microData     = ref<IDocument<IMicroContainer>>({data: [], error: null, loading: true}) // удельные показатели
  const extraWork     = ref<number>(1)  // учитывать дополнительные работы не из минимального перечня
  const center        = ref<LngLat>()     // центр карты


// ------------------- данные по дому -----------

  const buildData = ref<IDocument<IBuildCard>>({data:[], error: null, loading:true})   

  watch ([buildId, extraWork], async () => {
    if (Number(buildId.value) > 0) {
      // buildData.value.data = []
      error_message.value='' 
      buildData.value = await useFetch('builds/' + buildId.value.toString(), {}) 
      if (buildData.value.error) { 
        error_message.value='Нет данных' 
      } else {
        macroData.value.loading = true
        macroData.value = await loadMacroData(Number(buildId.value), extraWork.value)
        microData.value = await loadMicroData(Number(buildId.value))
      }
    }
  })

</script>


<template>
  <CitiesTab v-model="center"/>
  <Map :center="center" v-model="buildId"/>  

  <div v-if="buildId === 0" class="pt-5">
    <div class="card">
      <Message severity="contrast">
          <h1>Дом не выбран</h1>
          <p>Выберите дом не карте</p>
      </Message>
    </div>
  </div>

  <div v-else class="pt-5">


    <div class="card" v-if="!error_message">
      <Message severity="contrast">
          <h1>Предварительный анализ экономики дома</h1>
          <h4>Содержание жилого помещения и текущий ремонт</h4>
      </Message>
    </div>
    <div v-else class="card">
      <Message severity="warn">
          <h1>Нет данных</h1>
          <p>{{ error_message }}</p>
      </Message>
    </div>
    <BuildAnalizeCard :build="buildData.data[0]" :loading="buildData.loading" v-if="!buildData.loading && !error_message"/>

    <template v-if="buildData && !buildData.loading && !error_message">
      <MacroDataAnalyze :data="macroData" v-model="extraWork"/>
      <MicroDataAnalyze :data="microData.data" :years="macroData.years"/>
    </template>
  </div>
  
</template>