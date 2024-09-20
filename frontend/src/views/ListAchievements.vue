<script setup lang="ts">    
    import {ref, onMounted} from 'vue'
    import Card from 'primevue/card';
    import Button from 'primevue/button';
    import InputText from 'primevue/inputtext';
    import type { IDocument, IAchievement } from '@/interfaces';
    import { useBaseUrl } from '@/stores/baseUrl'
    import AchievementCard from '@/components/AchievementCard.vue';
    import { useFetch } from '@/api/useFetch'

    const baseUrl = useBaseUrl()
    const achievements = ref<IDocument<IAchievement>>({data:[], error: null, loading: true})
    const achievementsDisplay = ref<IAchievement[]>([])
    const loading = ref<boolean>(true)
    const searchText = ref<string>('')

    const search = () => {
        if (searchText.value.length > 0) {
            const searchAchievements = achievements.value.data.filter(item => item.address.toLowerCase().includes(searchText.value.toLowerCase()) || item.name.toLowerCase().includes(searchText.value.toLowerCase())   );
            achievementsDisplay.value =  searchAchievements
        } else {
            achievementsDisplay.value =  achievements.value.data
        }
    }

    async function loadData() {
        achievements.value = await useFetch('achievements')
        achievementsDisplay.value = achievements.value.data
        loading.value = false
    }

    onMounted(() => {
        loadData()
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
                </template>
                <template #content>

                    <AchievementCard :achievement="achievement" width="160" height="300" :key="index"/>

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