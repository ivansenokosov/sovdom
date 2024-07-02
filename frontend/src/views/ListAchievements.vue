<script setup lang="ts">    
    import {ref, onMounted} from 'vue'
    import Card from 'primevue/card';
    import Button from 'primevue/button';
    import InputText from 'primevue/inputtext';

    import AxiosInstance from '@/api/axiosInstance';


    import type { IAchievement } from '@/interfaces';

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

    const get_photo_url = (path:string) => {
        return 'http://localhost:8000' + path
    }
     

    const load_achievements = async () => {
        loading.value = true
        const url = 'http://localhost:8000/achievements'
        const achievementsRawData = await AxiosInstance.get(url)
        achievements.value = achievementsRawData.data
        achievementsDisplay.value = achievementsRawData.data
        loading.value = false
    }

    const get_router_path = (id:number) => { return '/edit_achievement/' + id }
    const get_router_path_delete = (id:number) => { return '/delete_achievement/' + id }

    onMounted(async () => {
      await load_achievements()
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
                            <template #header><img :src="get_photo_url(achievement.photo_before)" width="160"></template>
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
                            <template #header><img :src="get_photo_url(achievement.photo_after)" width="160"></template>
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
                    <router-link :to="get_router_path_delete(achievement.id)" rel="noopener">
                        <Button icon="pi pi-times" severity="danger"></Button>
                    </router-link>
                    <router-link :to="get_router_path(achievement.id)" rel="noopener">
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