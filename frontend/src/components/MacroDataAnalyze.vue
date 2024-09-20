<script setup lang="ts">  
  import {ref, watch} from 'vue'
  import { loadMacroData } from '@/api/loadMacroData';
  import Message from 'primevue/message';
  import SelectButton from 'primevue/selectbutton';
  import Skeleton from 'primevue/skeleton';


  //@ts-ignore
  import MacroData from '@/components/ChartMacro.vue';

  const props = defineProps(['data'])
  const eW = defineModel({ required: true })

  const extraWork = ref('Учитывать');
  const extraworkoptions = ref(['Учитывать', 'Не учитывать']);

  const getExtraWork = () => {
    eW.value =  (extraWork.value === 'Учитывать'? 1 : 0); 
  }

</script>

<template>
  <div class="card mt-5">
        <Message style="background-color: royalblue; color: white">
            <h1>Макропоказатели анализа экономики дома</h1>
            <div class="card flex justify-center">
              <p class="mr-2">Работы, не входящие в минимальный перечень</p>
              <SelectButton v-model="extraWork" :options="extraworkoptions" aria-labelledby="basic" @click="getExtraWork()"/>
            </div>            
        </Message>
      </div>

      <div v-if="data.loading">
          <Skeleton width="100%" height="600px" style="margin: 1em;"></Skeleton>
          <Skeleton width="100%" height="600px" style="margin: 1em;"></Skeleton>
      </div>
      <div v-else>
          <MacroData key="macro"     :data="data.macroData"    :years="data.years" title="Сравнение начислений по применяемой ставке платы, начислений по отчёту, затрат по отчёту по годам" ref="macro"/>  
          <MacroData key="macro_sum" :data="data.macroDataSum" :years="data.years" title="Сравнение начислений по применяемой ставке платы, начислений по отчёту, затрат по отчёту накопительным итогом" ref="macro_sum"/>  
      </div> 
</template>

<style scoped>
</style>
