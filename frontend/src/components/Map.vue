<script setup lang="ts">  
    import {ref, shallowRef} from 'vue'
    import { YandexMap, YandexMapDefaultSchemeLayer, YandexMapMarker, YandexMapDefaultFeaturesLayer  } from 'vue-yandex-maps';
    import type { YMap  } from '@yandex/ymaps3-types';
    import type { IMapData } from '@/interfaces';
    import Skeleton from 'primevue/skeleton';
    import { loadMap } from '@/api/loadMapData';

    const props = defineProps(['center'])
    const API_KEY : string = '8cfd01cf-5ac2-4cc0-baa5-ea9e5af226da'
    const map = shallowRef<null | YMap>(null);
    const buildId = defineModel({ required: true })
    const points  = ref<IMapData>({ data: [], error: null, loading: true })   // объекты на карте

    async function loadData() {
      points.value = await loadMap()
    }

    loadData()
</script>

<template>
  <div class="mt-2">
    <div v-if="points.loading">
      <Skeleton width="100%" height="500px"></Skeleton>
    </div>
    <div v-else>
      <div v-if="center">
        <yandex-map :settings="{location: {center: center, zoom: 11, },}" width="100%" height="500px">
        <yandex-map-default-scheme-layer/>
        <yandex-map-default-features-layer/>
            <template v-for="(marker, index) in points.data" :key="index">
                <yandex-map-marker :settings="marker" @click="() => {buildId = marker.buildid}">
                  <div class="marker">{{ marker.title }}</div>
              </yandex-map-marker>
            </template>
      </yandex-map>        

      </div>
    </div>
  </div>
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
