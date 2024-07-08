<script setup lang="ts">
    import {ref, defineProps, onMounted} from 'vue'
    import { useRouter } from 'vue-router'
    import Card from 'primevue/card';
    import Skeleton from 'primevue/skeleton';
    import Button from 'primevue/button';
    import AxiosInstance from '@/api/axiosInstance';
    import type { IAchievement } from '@/interfaces';
    import loadAchievement from '@/api/loadAchievement';
    import { useBaseUrl } from '@/stores/baseUrl'


    const props = defineProps( {
      id: {
        type: String,
        required: true,
      }}
    )

    const router = useRouter()
    const baseUrl = useBaseUrl()

    let achievement:IAchievement 
    const loadingAchievement = ref<boolean>(true)

    const submission = () => {
        const url:string = 'achievements/' + props.id
            AxiosInstance.delete(url,{})
        .then((res) => {
            router.push(`/achievements`)
        })
    }

    onMounted(async () => {
        achievement = await loadAchievement(props.id)
        loadingAchievement.value = false
    })    
</script>

<template>
    <div class="content-achievement">
        <Card>                  
            <template #title><h1>Удалить Было/стало?</h1></template>
            <template #content>
                <div v-if="!loadingAchievement" class="mt-3">
                    <h3>Адрес: {{ achievement.address }}</h3>
                    <p class="font-semibold">{{ achievement.name  }}</p>

                    <div class="flex justify-content-center flex-wrap mt-5">
                        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                            <Card style="background-color:lightgray; color:black;  width: 350px; height: 600px; overflow: hidden">
                                <template #header>
                                    <img :src="`${baseUrl.baseUrl}${achievement.photo_before}`" width="100%">
                                </template>
                                <template #title>Было</template>
                                <template #content>
                                    <div class="mt-5">
                                        <div class="field">
                                            <p>Год: {{ achievement.year_before}}</p>
                                        </div>
                                        <div class="field">
                                            <p>Описание: {{ achievement.info_before}}</p>
                                        </div>
                                    </div>                                
                                </template>
                            </Card>
                        </div>

                        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                            <Card style="background-color:lightgray; color:black;  width: 350px; height: 600px; overflow: hidden">
                                <template #header>
                                    <img :src="`${baseUrl.baseUrl}${achievement.photo_after}`" width="100%">
                                </template>
                                <template #title>Стало</template>
                                <template #content>
                                    <div class="mt-5">
                                        <div class="field">
                                            <p>Год: {{ achievement.year_after}} год</p>
                                        </div>
                                        <div class="field">
                                            <p>Описание: {{ achievement.info_after}}</p>
                                        </div>
                                    </div>
                                </template>
                            </Card>
                        </div>
                    </div>
                </div>

                <div v-else>
                    <Skeleton width="100%" height="25px" class="mt-3"></Skeleton>
                    <Skeleton width="100%" height="25px" class="mt-3"></Skeleton>
                    <div class="flex justify-content-center flex-wrap mt-5">
                        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                            <Skeleton width="350px" height="600px"/>
                        </div>

                        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                            <Skeleton width="350px" height="600px"/>
                        </div>
                    </div>
                </div>

            </template>



            <template #footer>
                <div class="flex flex-wrap justify-center gap-4">
                    <router-link to="/achievements" rel="noopener">
                        <Button link label="Отменить" />
                    </router-link>
                    <Button label="Удалить" severity="danger" icon="pi pi-times" iconPos="right" @click="submission"/>
                </div>
            </template>
        </Card>
    </div>
</template>


<style scoped>
    .input { 
        width: 100%;
    }
    .content-achievement { 
        max-width: 1000px; 
        margin: auto;
    }
</style>