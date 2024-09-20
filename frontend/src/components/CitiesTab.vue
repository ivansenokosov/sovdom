<script setup lang="ts">  
    import { ref } from 'vue';
    import Tabs from 'primevue/tabs';
    import TabList from 'primevue/tablist';
    import Tab from 'primevue/tab';
    import Skeleton from 'primevue/skeleton';
    import type {IDocument, ICity} from '@/interfaces'

    import { useBaseUrl } from '@/stores/baseUrl'
    import { useFetch } from '@/api/useFetch';
    const baseUrl = useBaseUrl()
    const props = defineProps(['cities', 'loading'])
    const center = defineModel({ required: true })

    const cities = ref<IDocument<ICity>>({data:[], error: null, loading: true})   // данные городов
    const selectedCity = ref<string>('1')  // выбранный город

//  изменение центра карты  
    function setMapCenter(coords:string) {
      const comma : number= coords.indexOf(',', 1)
      const x : number = Number(coords.substr(0, comma))
      const y : number = Number(coords.substr(comma+1, coords.length))
      center.value = [y,x]
    }

  //  выбор города и установка центра карты
    const click = () => {
      const coords = cities.value.data.filter((city:ICity) => city.id === Number(selectedCity.value))
      setMapCenter(coords[0].ymap)
    };

    async function loadData() {
      cities.value = await useFetch('catalogs/cities_ymap', {});
      click() // после загрузки установить центр карты
    }

    loadData()

</script>

<template>
  <div v-if="cities.loading">
    <Skeleton width="100%" height="50px"></Skeleton>  
  </div>
  <div v-else>

    <Tabs scrollable v-model:value="selectedCity">
        <TabList>
            <Tab v-for="(city, index) in cities.data" :key="index" :value="city.id.toString()" @click="click()">
                {{ city.name }} ({{ city.qbuilds }})
            </Tab>                
        </TabList>
    </Tabs> 
  </div>

</template>

<style scoped>
</style>
