<script setup lang="ts">
    import Card from 'primevue/card'
    import { useBaseUrl } from '@/stores/baseUrl'
    const baseUrl = useBaseUrl()
    const props = defineProps(['achievement','width','height'])
</script>

<template>
    <div class="flex justify-content-center flex-wrap mt-5">
        <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-1">

                        <Card :style="`color:black; width: ${width}px; height: ${height}px; overflow: hidden`">
                            <template #header>
                                <img v-if="achievement.photo_before" :src="`${baseUrl.baseUrl}${achievement.photo_before}`" :width="width">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" :width="width"/>
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
                        <Card :style="`color:black;  width: ${width}px; height: ${height}px; overflow: hidden`">
                            <template #header>
                                <img v-if="achievement.photo_after" :src="`${baseUrl.baseUrl}${achievement.photo_after}`" :width="width">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" :width="width"/>
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

<style scoped>
</style>
