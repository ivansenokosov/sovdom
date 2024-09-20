<script setup lang="ts">  
    import { watch } from 'vue'
    import Card from 'primevue/card'
    import Skeleton from 'primevue/skeleton';

    import { useBaseUrl } from '@/stores/baseUrl'
    import { numberWithSpaces } from '@/api/numberWithSpaces';

    const baseUrl = useBaseUrl()
    const props = defineProps(['build', 'loading'])
    var total_rub:string = ''

    watch(() => [props.build], ()=>{
      total_rub = numberWithSpaces(props.build.total_rub.toFixed(0))
    })
</script>

<template>
  <template v-if="loading">
      <div class="flex justify-content-center flex-wrap mt-5">
          <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
            <Skeleton width="350px" height="500px"></Skeleton>
          </div>
          <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
            <Skeleton width="350px" height="500px"></Skeleton>
        </div>
      </div>
  </template>
  
  <template v-else>
    <div class="flex justify-content-center flex-wrap mt-5">
      <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
        <Card style="background-color:lightgray; color:black;  width: 350px; height: 500px; overflow: hidden">
          <template #header>
              <img alt="user header" :src="`${baseUrl.baseUrl}${build.photo}`" width="350" />   
          </template>
          <template #title><h3>{{ build.addr_str }}</h3></template>
          <template #subtitle>{{ build.management_str }}</template>
          <template #content>
              <p class="m-0 font-medium">
                <b>{{ build.year }}</b> год постройки, <b>{{ build.floors }}</b> этажей, <b> {{ build.s_live }}</b> кв.м полезная площадь, <b>{{ build.s_mop }}</b> кв.м площадь МОП, <b>{{ build.s_zem }}</b> кв.м площадь участка
              </p>
          </template>
        </Card>
      </div>
      <div class="flex align-items-center justify-content-center  bg-primary font-bold border-round m-2">
        <Card style="background-color:lightgray; color:black; width: 350px; height: 500px;  overflow: hidden">
          <template #title><h3 class="text-center">Начислено за {{ build.report_number }} лет</h3></template>
          <template #subtitle><h1 class="text-center" style="color: black">{{ total_rub }} руб.</h1></template>
          <template #content>
              <p class="m-0 font-medium">
                Отчёты предоставлены за <b>{{ build.report_rub }}</b> руб., в том числе:
                <ul>
                <li>на <b>{{ build.management_rub }}</b> руб., за управление</li>
                <li>на <b>{{ build.repair_rub }}</b> руб., выполнено текущих ремонтов, согласно отчётам</li>
                <li>на <b>0</b> рублей текущие ремонты подтверждены актами выполненных работ.</li>
                </ul>   
              </p>
          </template>
        </Card>
      </div>
    </div>
  </template>
</template>

<style scoped>
</style>
