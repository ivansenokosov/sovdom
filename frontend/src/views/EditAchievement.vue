<script setup lang="ts">
    import {ref, computed, defineProps, onMounted} from 'vue'
    import InputText from 'primevue/inputtext';
    import Card from 'primevue/card';
    import FileUpload from 'primevue/fileupload';
    import Skeleton from 'primevue/skeleton';
    import Button from 'primevue/button';
    import FloatLabel from 'primevue/floatlabel';
    import InputNumber from 'primevue/inputnumber';
    import AutoComplete from 'primevue/autocomplete';
    import Toast from 'primevue/toast';
    import { useToast } from "primevue/usetoast";
    import { useBaseUrl } from '@/stores/baseUrl'
    import AxiosInstance from '@/api/axiosInstance';
    import type { IDocument, IAchievement, IBuild, IFile } from '@/interfaces';
    import filterItems from '@/api/filterItems';
    import uploadFile from '@/api/uploadFile';
    import loadFile from '@/api/loadFile';
    import { useFetch } from '@/api/useFetch';

    const props = defineProps( {
      id: {
        type: String,
        required: true,
      }}
    )

    const baseUrl       = useBaseUrl()
    const toast         = useToast(); // уведомление о загрузке файла
    const achievement   = ref<IDocument<IAchievement>>({data:[], error: null, loading: true}) 
    const builds        = ref<IDocument<IBuild>>({data:[], error: null, loading: true}) // дома    
    const photoBefore   = ref<IFile>()
    const photoAfter    = ref<IFile>()
    const buildId       = ref<string>('')
    const selectedBuild = ref<IBuild>({id:0, name:''})  // выбор дома из комбо
    const loading       = ref<boolean>(true) 
    const saving        = ref<boolean>(false) // флаг состояния процесса сохранения
    const filteredItems = ref<IBuild[]>([]);

    const disableSaveButton = computed<boolean> (()=>{
        return !(buildId.value && 
                 achievement.value.data[0].name && 
                 achievement.value.data[0].info_before && 
                 achievement.value.data[0].info_after && 
                 achievement.value.data[0].year_before && 
                 achievement.value.data[0].year_after)
    })

    const submission = async () => {
        saving.value = true
        const url = baseUrl.baseUrl + 'achievements/'+ props.id + '/';
       
        const config = { headers: { 'content-type': 'multipart/form-data', }, };
        const formData = new FormData();        

        formData.append("name", achievement.value.data[0].name)
        formData.append("year_before", achievement.value.data[0].year_before.toString())
        formData.append("info_before", achievement.value.data[0].info_before.toString())
        formData.append("year_after", achievement.value.data[0].year_after.toString())
        formData.append("info_after", achievement.value.data[0].info_after.toString())
        formData.append("build", selectedBuild.value.toString())

        photoBefore.value && photoBefore.value.file_blob && formData.append("photo_before", photoBefore.value.file_blob, photoBefore.value.file_name)
        photoAfter.value && photoAfter.value.file_blob && formData.append("photo_after", photoAfter.value.file_blob, photoAfter.value.file_name)

        const res = await AxiosInstance.put(url, formData, config)
          .then(function(response) {
            toast.add({ severity: 'info', summary: 'Успешно', detail: 'Документ сохранён', life: 3000 });
            console.log(response);
        }).catch(function(error) {
          console.log(error);
        })
        saving.value = false
    }

    const upload_file_before = async (event:any) => { photoBefore.value = await uploadFile(event) } 
    const upload_file_after  = async (event:any) => { photoAfter.value  = await uploadFile(event) }
    const searchItems = (event: any) => { filteredItems.value = filterItems(builds.value.data, event.query) }

    onMounted(async () => {
        builds.value = await useFetch('catalogs/builds?city=1',{})
        achievement.value = await useFetch('achievements/' + props.id,{})
        buildId.value = String(achievement.value.data[0].build)
        selectedBuild.value = {"id":Number(buildId.value), "name":achievement.value.data[0].address}

        achievement.value.data[0].photo_before && (photoBefore.value = await loadFile(baseUrl.baseUrl + achievement.value.data[0].photo_before))
        achievement.value.data[0].photo_after &&  (photoAfter.value  = await loadFile(baseUrl.baseUrl + achievement.value.data[0].photo_after))
        loading.value = false
    })    
</script>

<template>
    <div class="content-achievement">
        <Card>                  
            <template #title><h1>Редактировние Было/стало</h1></template>
            <template #content>

                <div v-if= "!loading" class="card flex justify-center w-full">
                    <FloatLabel style="width:100%">
                        <AutoComplete class="input mb-5" v-model="selectedBuild" :suggestions="filteredItems" @complete="searchItems" :virtualScrollerOptions="{ itemSize: 10 }" optionLabel="name" inputId="buildId" dropdown />
                        <label for="buildId">Дом</label>
                    </FloatLabel>
                </div>
                <div v-else>
                    <Skeleton width="100%" height="50px"/>
                </div>

                <div v-if="!loading" class="mt-3">

                <FloatLabel>
                    <InputText class="input mb-3" id="name" v-model="achievement.data[0].name" />
                    <label for="name">Описание</label>
                </FloatLabel>
                <div class="flex justify-content-center flex-wrap mt-5">
                    <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                        <Card style="background-color:lightgray; color:black;  width: 350px; height: 600px; overflow: hidden">
                            <template #header>
                                <img v-if="photoBefore" v-bind:src="photoBefore.file_base64data" width="350" height="262">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" width="350" height="262"/>
                            </template>
                            <template #title>Было</template>
                            <template #content>
                                <div class="mt-5">
                                    <div class="field">
                                        <FloatLabel>
                                            <InputNumber class="input mb-3" v-model="achievement.data[0].year_before" inputId="year_before" :useGrouping="false" :step="1"/>
                                            <label for="year_before" class="font-light">Год</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <FloatLabel>
                                            <InputText class="input mb-3" id="info_before" v-model="achievement.data[0].info_before" />
                                            <label for="info_before" class="font-light">Информация</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <div class="card flex flex-col gap-6 items-center justify-center">
                                            <div class="card flex justify-center">
                                                <Toast />
                                                <div class="grid">
                                                    <div class="col-12">
                                                        <label>Изображение</label>
                                                    </div>
                                                    <div class="col-12">
                                                        <FileUpload mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000" customUpload @uploader="upload_file_before" :auto="true" chooseLabel="Выбрать" />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>    
                                </div>                                
                            </template>
                        </Card>
                    </div>

                    <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                        <Card style="background-color:lightgray; color:black;  width: 350px; height: 600px; overflow: hidden">
                            <template #header>
                                <img v-if="photoAfter" v-bind:src="photoAfter.file_base64data" width="350" height="262">
                                <img v-else :src="`${baseUrl.baseUrl}media/achieves_images/no_photo.jpg`" width="350" height="262"/>
                            </template>
                            <template #title>Стало</template>
                            <template #content>
                                <div class="mt-5">
                                    <div class="field">
                                        <FloatLabel>
                                            <InputNumber class="input mb-3" v-model="achievement.data[0].year_after" inputId="year_after" :useGrouping="false" :step="1"/>
                                            <label for="year_after" class="font-light">Год</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <FloatLabel>
                                            <InputText  class="input mb-3" id="info_after" v-model="achievement.data[0].info_after" />
                                            <label for="info_after" class="font-light">Информация</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <div class="card flex flex-col gap-6 items-center justify-center">
                                            <div class="card flex justify-center">
                                                <Toast />
                                                <div class="grid">
                                                    <div class="col-12">
                                                        <label>Изображение</label>
                                                    </div>
                                                    <div class="col-12">
                                                        <FileUpload mode="basic" name="demo[]" url="/api/upload" accept="image/*" :maxFileSize="1000000" customUpload @uploader="upload_file_after" :auto="true" chooseLabel="Выбрать" />
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>    
                                    
                                </div>
                            </template>
                        </Card>
                    </div>


                </div>
                </div>

            </template>



            <template #footer>
                <div class="flex flex-wrap justify-center gap-4">
                    <router-link to="/achievements" rel="noopener">
                        <Button link label="Отменить" />
                    </router-link>
                    <router-link to="/delete_achievement/3" rel="noopener">
                        <Button label="Удалить" severity="danger" icon="pi pi-times" iconPos="right"/>
                    </router-link>
                    <Button v-if= "!disableSaveButton" label="Сохранить" severity="success" icon="pi pi-check" iconPos="right" @click="submission" :loading="saving"/>
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