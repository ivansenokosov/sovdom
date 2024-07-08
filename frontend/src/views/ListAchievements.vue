<script setup lang="ts">    
    import {ref, onMounted} from 'vue'
    import Card from 'primevue/card';
    import Button from 'primevue/button';
    import InputText from 'primevue/inputtext';
    import AxiosInstance from '@/api/axiosInstance';
    import type { IAchievement } from '@/interfaces';
    import { useBaseUrl } from '@/stores/baseUrl'

    const baseUrl = useBaseUrl()
    const achievements = ref<IAchievement[]>([])
    const achievementsDisplay = ref<IAchievement[]>([])
    const loading = ref<boolean>(true)
    const searchText = ref<string>('')

    const search = () => {
        if (searchText.value.length > 0) {
            const searchAchievements = achievements.value.filter(item => item.address.toLowerCase().includes(searchText.value.toLowerCase()) || item.name.toLowerCase().includes(searchText.value.toLowerCase())   );
            achievementsDisplay.value =  searchAchievements
        } else {
            achievementsDisplay.value =  achievements.value
        }
    }

    const load_achievements = async <T extends IAchievement> ():Promise<T[]> => {
        loading.value = true
        const url = baseUrl.baseUrl + 'achievements'
        const achievementsRawData = await AxiosInstance.get(url)
        let items : Array<T> = achievementsRawData.data
        return items
    }

    onMounted(async () => {
      const listAchievements : Array<IAchievement> = await load_achievements()
      achievements.value = [...listAchievements]
      achievementsDisplay.value = achievements.value
      loading.value = false
    })    

</script>

<template>
    <div v-if="loading">
        загружаю
    </div>
    <div v-else>
        <h1>Спиок достижений</h1>

        <router-link to="/add_achievement" rel="noopener">
            <Button label="Создать" severity="info"></Button>
        </router-link>
        
        <div class="field mt-5">
            <InputText class="input" v-model="searchText" type="text" size="large" placeholder="Поиск..." @input="search"></InputText>
        </div>

        
        <div class="grid mt-5">
            <Card class="col-4 m-1" style="background-color: #e5e5e5; width: 410px" v-for="(achievement, index) in achievementsDisplay">
                <template #title>
                    <h3>{{ achievement.address }}</h3>
                    <p  class="text-sm">{{ achievement.name }}</p>
                <!-- </template>
                <template #content> -->

                    <div class="flex justify-content-center flex-wrap mt-5">
                        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-1">


                        <Card style=" color:black;  width: 160px; height: 300px; overflow: hidden">
                            <template #header>
                                <img v-if="achievement.photo_before" :src="`${baseUrl.baseUrl}${achievement.photo_before}`" width="160">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" width="160"/>
                            </template>
                            <template #title>{{ achievement.year_before }} год</template>
                            <template #content>
                                <div class="field text-sm m-1 font-light">
                                    {{ achievement.info_before }}
                                </div>
                            </template>
                        </Card>
                    </div>

                    <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-1">
                        <Card style="color:black;  width: 160px; height: 300px; overflow: hidden">
                            <template #header>
                                <img v-if="achievement.photo_after" :src="`${baseUrl.baseUrl}${achievement.photo_after}`" width="160">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" width="160"/>
                            </template>
                            <template #title>{{ achievement.year_after }} год</template>
                            <template #content>
                                <div class="field text-sm m-1 font-light">
                                    {{ achievement.info_after }}
                                </div>
                            </template>
                        </Card>
                    </div>
                </div>

                </template>
                <template #footer>
                    <router-link :to="`/delete_achievement/${achievement.id}`" rel="noopener">
                        <Button icon="pi pi-times" severity="danger"></Button>
                    </router-link>
                    <router-link :to="`/edit_achievement/${achievement.id}`" rel="noopener">
                        <Button icon="pi pi-pencil" class="ml-2"></Button>
                    </router-link>
                </template>
                </Card>
            </div>
    </div>

</template>

<style scoped>
    .p-card-body {margin:0}
    .input {width: 100%}
</style>