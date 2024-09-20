<script setup lang="ts">
    import {ref, defineProps, onMounted} from 'vue'
    import { useRouter } from 'vue-router'
    import Card from 'primevue/card';
    import Skeleton from 'primevue/skeleton';
    import Button from 'primevue/button';
    import type { IDocument, IAchievement } from '@/interfaces';
    import AxiosInstance from '@/api/axiosInstance';
    import { useFetch } from '@/api/useFetch';
    import { deleteData } from '@/api/dataActions'
    import { useBaseUrl } from '@/stores/baseUrl'
    import AchievementCard from '@/components/AchievementCard.vue';

    const props = defineProps( {
      id: {
        type: String,
        required: true,
      }}
    )

    const router = useRouter()
    const achievement = ref<IDocument<IAchievement>>({data:[], error: null, loading: true})
    let  error = ref<any>()

    const submission = () => {
        const url:string = 'achievements/' + props.id + '/'
        deleteData(url).then(() => {router.push(`/achievements`)})
    }


    onMounted(async () => {
        achievement.value = await useFetch('achievements/' + props.id, {});
    })    
</script>

<template>
    <div class="content-achievement">
        <Card>                  
            <template #title><h1>Удалить Было/стало?</h1></template>
            <template #content>
                <div v-if="!achievement.loading" class="mt-3">
                    <h3>Адрес: {{ achievement.data[0].address }}</h3>
                    <p class="font-semibold">{{ achievement.data[0].name  }}</p>

                    <AchievementCard :achievement="achievement.data[0]" width="350" height="600"/>

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