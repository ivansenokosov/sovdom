<script setup lang="ts">
  import {ref, computed, inject, onMounted, shallowRef} from 'vue'

  import Tabs from 'primevue/tabs';
  import TabList from 'primevue/tablist';
  import Tab from 'primevue/tab';
  import Card from 'primevue/card';
  import Skeleton from 'primevue/skeleton';
  import Message from 'primevue/message';
  import SelectButton from 'primevue/selectbutton';

  import { YandexMap, YandexMapDefaultSchemeLayer, YandexMapMarker, YandexMapDefaultFeaturesLayer  } from 'vue-yandex-maps';
  import type { LngLat, YMap  } from '@yandex/ymaps3-types';
  import type { YMapClusterer } from '@yandex/ymaps3-types/packages/clusterer';  
  
  //@ts-ignore
  import MicroData from '../components/ChartMicro.vue';
  //@ts-ignore
  import MacroData from '../components/ChartMacro.vue';

  import AxiosInstance from '@/api/axiosInstance';
  


  const buildId = ref<Number>(0)  // выбранный дом

  // ------------------- города ---------

  interface ICity {
    id: number
    name: string
    ymap: string
    qbuilds: number
  }

  const cities = ref([] as ICity[])   // данные городов
  const selectedCity = ref<string>('1')
  const loadingCities = ref<boolean>(true)

  const error_message = ref<String>('')

  // ------------------- карта-----------

  const API_KEY : string = '8cfd01cf-5ac2-4cc0-baa5-ea9e5af226da'
  const map = shallowRef<null | YMap>(null);
  const clusterer = shallowRef<YMapClusterer | null>(null);

  interface IMarker {
    buildid: number
    coordinates: LngLat
    title: string
    color: string
    draggable: boolean
  }

  let POINTS: IMarker[] = []
  const center  = ref<LngLat>([]

  )
  let mapData = {}  // данные объектов на карте  
  const loadingMapData = ref<boolean>(true)

//  изменение центра карты  
  function setMapCenter(coords:string) {
          const comma : number= coords.indexOf(',', 1)
          const x : number = Number(coords.substr(0,comma))
          const y : number = Number(coords.substr(comma+1,coords.length))
          center.value = [y,x]
  }

//  выбор города и установка центра карты
  const click = () => {
    const coords = cities.value.filter(city => city.id === Number(selectedCity.value))
    setMapCenter(coords[0].ymap)
  };

  const setBuildId = (p_buildId : number) => {
    loadingBuildData.value = true
    loadingMicro.value = true
    loadingMacro.value = true
    buildId.value = p_buildId
    error_message.value = ''
    loadBuildData()
    loadMacroData()    
    loadMicroData()    
  }


// ------------------- данные по дому -----------

  const loadingBuild = ref<boolean>(true)
  let buildData : any = ''   
  const loadingBuildData = ref<boolean>(true)
  const getImg = () => { return "http://localhost:8000/" + buildData.photo }

// ------------------- данные макро ---------------------

  interface IYears {
      text: string
  }

  interface IMacroData {
    color: string
    name: string
    data: number[]
    stack: string
  } 

  const years = ref([] as IYears[])
  const dataMacro = ref<any>([])
  const dataMacroSum = ref<any>([])
  const loadingMacro = ref<boolean>(true)

  const extrawork = ref('Учитывать');
  const extraworkoptions = ref(['Учитывать', 'Не учитывать']);
  const eW = ref<number>(1)

  const getExtraWork = () => {
    eW.value =  (extrawork.value === 'Учитывать'? 1 : 0); 
    loadMacroData()
  }


// ------------------- удельные показатели ---------------------
  
  const dataMicro = ref<any>([])
  const loadingMicro = ref<boolean>(true)

  

// #################################################################################
// ################### загрузка данных #############################################
// #################################################################################

// -----------------------  загрузка данных по городам   
  async function loadCityData() {
    loadingCities.value = true
    const citiesRawData = await AxiosInstance.get('catalogs/cities_ymap')
    cities.value = citiesRawData.data
    loadingCities.value = false
    click() // после загрузки установить центр карты
  }

// ----------------------- загрузка данных карты
  async function loadMapData() {
    loadingMapData.value = true 
    const mapRawData = await AxiosInstance.get('map_json')
    let newmapdata =  []
    newmapdata = JSON.parse(mapRawData.data)
    mapData = newmapdata
    mapData.map((item) => {
    POINTS.push({buildid: item.id, 
                    coordinates:[item.geometry.coordinates[1], item.geometry.coordinates[0]], 
                    title:item.properties.iconContent,
                    color: '#343d44',
                    draggable: false,
                  })
    })
    loadingMapData.value = false
  }

//  ----------------------- загрузка данных по дому
  async function loadBuildData() {
    loadingBuild.value = true
    const url = 'builds/' + buildId.value
    try {
      const buildRawData = await AxiosInstance.get(url)
      buildData = buildRawData.data
      loadingBuild.value = false
    } catch(error) {
      error_message.value="Нет данных по дому"
    }
  }    

//  ----------------------- загрузка данных удельных показателей
  async function loadMicroData() {
    loadingMicro.value = true
    const url = 'http://127.0.0.1:8000/micro_details_json?build_id=' + buildId.value
    try {
      const microRawData = await AxiosInstance.get(url)
      dataMicro.value = JSON.parse(microRawData.data)
      loadingMicro.value = false
      dataMicro.value = JSON.parse(microRawData.data)
      loadingMicro.value = false
    } catch(error) {
      error_message.value="Нет данных по дому"
    }
  }

  async function loadMacroData()  {
      loadingMacro.value = true
      const url = 'http://localhost:8000/json?build_id=186066&extra_work=' + String(eW.value)
      try {
        const macroRawData = await AxiosInstance.get(url)
        let newdata =  []
        newdata = JSON.parse(macroRawData.data)
        years.value = newdata[0].categories
        dataMacro.value = newdata[1].macro
        dataMacroSum.value = newdata[2].macro_sum
        loadingMacro.value = false      
      } catch (error) {
        error_message.value="Нет данных по дому"
      }
  }

   onMounted(async () => {
      await loadCityData()
      await loadMapData()
  })


</script>





<template>


<!---------------------------------- Выбор города ------------------------------->


  <div v-if="loadingCities">
    <Skeleton width="100%" height="50px"></Skeleton>
  </div>
  <div v-else>
        <Tabs scrollable v-model:value="selectedCity">
            <TabList>
                <Tab v-for="(city, index) in cities" :key="index" :value="city.id.toString()" @click="click()">
                    {{ city.name }} ({{ city.qbuilds }})
                </Tab>                
            </TabList>
        </Tabs>
      </div>

<!---------------------------------- Карта ------------------------------->
<div class="mt-2">
  <div v-if="loadingMapData">
    <Skeleton width="100%" height="500px"></Skeleton>
  </div>
  <div v-else>
    <yandex-map :settings="{location: {center: center, zoom: 11, },}" width="100%" height="500px">
            <yandex-map-default-scheme-layer/>
            <yandex-map-default-features-layer/>
                <template v-for="(marker, index) in POINTS" :key="index">
                    <yandex-map-marker :settings="marker" @click="setBuildId(marker.buildid)">
                      <div class="marker">{{ marker.title }}</div>
                  </yandex-map-marker>
                </template>
        </yandex-map>       
  </div>
</div>


<!---------------------------------- Блок анализа экономики ------------------------------->

<div v-if="buildId === 0" class="pt-5">
  <div class="card">
    <Message severity="contrast">
        <h1>Дом не выбран</h1>
        <p>Выберите дом не карте</p>
    </Message>
  </div>
</div>
<div v-else class="pt-5">


  <div v-if="error_message" class="card">
    <Message severity="warn">
        <h1>Нет данных</h1>
        <p>{{ error_message }}</p>
    </Message>
  </div>

<!---------------------------------- Карточки дома ------------------------------->
    <template v-if="loadingBuild">
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


      
      <div class="card">
        <Message severity="contrast">
            <h1>Предварительный анализ экономики дома</h1>
            <h4>Содержание жилого помещения и текущий ремонт</h4>
        </Message>
      </div>
                  




                  <div class="flex justify-content-center flex-wrap mt-5">
                    <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                      <Card style="background-color:lightgray; color:black;  width: 350px; height: 500px; overflow: hidden">
                        <template #header>
                            <img alt="user header" :src="getImg()" width="350" />   
                        </template>
                        <template #title><h2>{{ buildData.addr_str }}</h2></template>
                        <template #subtitle>{{ buildData.management_str }}</template>
                        <template #content>
                            <p class="m-0">
                              <b>{{ buildData.year }}</b> год постройки, <b>{{ buildData.floors }}</b> этажей, <b> {{ buildData.s_live }}</b> кв.м полезная площадь, <b>{{ buildData.s_mop }}</b> кв.м площадь МОП, <b>{{ buildData.s_zem }}</b> кв.м площадь участка
                            </p>
                        </template>
                      </Card>
                    </div>
                    <div class="flex align-items-center justify-content-center  bg-primary font-bold border-round m-2">
                      <Card style="background-color:lightgray; color:black; width: 350px; height: 500px;  overflow: hidden">
                        <template #title>Начислено за {{ buildData.report_number }} лет</template>
                        <template #subtitle><h1>{{ buildData.total_rub }} руб.</h1></template>
                        <template #content>
                            <p class="m-0">
                              Отчёты предоставлены за {{ buildData.report_rub }} руб., в том числе:
                              <ul>
                              <li>на {{ buildData.management_rub }} руб.,<br/>за управление</li>
                              <li>на {{ buildData.repair_rub }} руб.,<br/>выполнено текущих ремонтов, согласно отчётам</li>
                              <li>на <span className="bg-warning">0</span> рублей,<br/>текущие ремонты подтверждены актами выполненных работ.</li>
                              </ul>   
                            </p>
                        </template>
                      </Card>
                    </div>
                  </div>


<!-- Макропоказатели экономики -->

      <div class="card mt-5">
        <Message style="background-color: royalblue; color: white">
            <h1>Макропоказатели анализа экономики дома</h1>
            <div class="card flex justify-center">
              <p class="mr-2">Работы, не входящие в минимальный перечень</p>
              <SelectButton v-model="extrawork" :options="extraworkoptions" aria-labelledby="basic" @click="getExtraWork()"/>
            </div>            
        </Message>
      </div>

          <div v-if="loadingMacro">
              <Skeleton width="100%" height="600px" style="margin: 1em;"></Skeleton>
              <Skeleton width="100%" height="600px" style="margin: 1em;"></Skeleton>
          </div>
          <div v-else>
              <MacroData key="macro"     :data="dataMacro"    :years="years" title="Сравнение начислений по применяемой ставке платы, начислений по отчёту, затрат по отчёту по годам" ref="macro"/>  
              <MacroData key="macro_sum" :data="dataMacroSum" :years="years" title="Сравнение начислений по применяемой ставке платы, начислений по отчёту, затрат по отчёту накопительным итогом" ref="macro_sum"/>  
          </div> 


<!-- Удельные показатели -->

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

          <div v-if="loadingMicro">
            <p>Загружаю</p>
          </div>
          <div v-else>
            <div class="grid  mt-5">
              <div class="col-4 p-1" v-for="(micro, index) in dataMicro">
                 <MicroData :key="index" :data="micro" :years="years" :ref="index"/>  
              </div> 
            </div>
          </div>
    </template>
  </div>



  <!--  -->

</template>

<style scoped>
.bounds {
  user-select: all;
}
.marker {
    position: relative;
    background: #ffffff;
    border: 2px solid #c0c0c0;
    text-align: center;
    color: #000000;
    font-weight: bold;
    font-size: 8px;
    line-height: 10px;
  }
  .cluster {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  height: 50px;
  background: green;
  color: #fff;
  border-radius: 100%;
  cursor: pointer;
  border: 2px solid limegreen;
  outline: 2px solid green;
}
.fade-in {
  animation: fadeIn 0.3s;
}
@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
</style>
