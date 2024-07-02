<script setup lang="ts">
    import {ref, computed, defineProps, onMounted} from 'vue'
    import { useRoute, useRouter } from 'vue-router'

    import InputText from 'primevue/inputtext';
    import Card from 'primevue/card';
    import FileUpload from 'primevue/fileupload';
    import Skeleton from 'primevue/skeleton';
    import Button from 'primevue/button';
    import FloatLabel from 'primevue/floatlabel';
    import Select from 'primevue/select';
    import AutoComplete from 'primevue/autocomplete';

    import AxiosInstance from '@/api/axiosInstance';
    import type { IAchievement } from '@/interfaces';
    import axios from 'axios';

    const props = defineProps( {
      id: {
        type: String,
        required: true,
      }}
    )
    const router = useRouter()

    let achievement:IAchievement 
    const loadingAchievement = ref<boolean>(true)

    const submission = () => {
        const url:string = 'achievements/' + props.id
            AxiosInstance.delete(url,{})
        .then((res) => {
            router.push(`/achievements`)
            
        })
    }

    const load_achievement = async () => {
        const url = 'http://localhost:8000/achievements/' + props.id
        const achievementRawData = await AxiosInstance.get(url)
        achievement = achievementRawData.data
        loadingAchievement.value = false
    }

    function get_img_url_before() { return 'http://localhost:8000' + achievement.photo_before }
    function get_img_url_after() { return 'http://localhost:8000' + achievement.photo_after }

    onMounted(async () => {
      await load_achievement()
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
                                    <img :src="get_img_url_before()" width="100%">
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
                                    <img :src="get_img_url_after()" width="100%">
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
                    <router-link to="/achievements" target="_blank" rel="noopener">
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