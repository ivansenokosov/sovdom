<script setup lang="ts">
    import { useUserStore } from '@/stores/user';
    import { ref, computed } from 'vue'   
    import type { ComputedRef } from 'vue'

    const userStore = useUserStore()

    interface IMenuItem {
        label: string
        url: string
        icon: string
        show: ComputedRef<boolean>
    }

    const items = ref<IMenuItem[]>([
        {
            label: 'Главная',
            url: '/',
            icon: '',
            show: computed((): boolean => !userStore.userId)
        },
        {
            label: 'Добились',
            url: '/achievements',
            icon: '/',
            show: computed((): boolean => !userStore.userId)
        },

    ])



</script>

<template>
    <app-menubar :model="items" class="menu" style="border: 0">
        <template #start>
            <RouterLink to="/">
                <img src="../assets/sovdom_logo_red64.png" width="64">
            </RouterLink>    
    </template>
            <template #item="{ item, props }">
            <template v-if="item.show">
                <RouterLink :to="item.url" class="flex items-center cursor-pointer px-4 py-2 overflow-hidden relative font-semibold text-lg uppercase" v-bind="props.action">
                    <span class="ml-2"> {{ item.label }} </span>
                </RouterLink>
            </template>
        </template>
        
        <template #end>
            <span v-if="userStore.userId" @click="userStore.userId=''">
                <span class="flex align-items-center menu-exit">
                    <RouterLink to="/" class="flex align-items-center">
                        <span class="pi pi-sign-out p-menuitem-icon"></span>
                        <span class="ml-2">Выход</span>
                    </RouterLink>
                </span>
            </span>
            <span v-else>
                <span class="flex align-items-center menu-exit">
                    <RouterLink to="/auth" class="flex align-items-center">
                        <span class="pi pi-sign-in p-menuitem-icon"></span>
                        <span class="ml-2"> Вход </span>
                    </RouterLink>
                </span>
            </span>
        </template>

    </app-menubar>
</template>

<style scoped>
    .menu {
        margin: 30px 0;
    }
    .menu-exit {
        cursor: pointer;
    }
</style>
