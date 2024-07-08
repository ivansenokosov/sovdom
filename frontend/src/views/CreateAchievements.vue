<script setup lang="ts">
    import {ref, computed, onMounted} from 'vue'
    import { useRouter } from 'vue-router'    
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
    import type { IBuild } from '@/interfaces';
    import type { IFile } from '@/interfaces';
    import loadBuilds from '@/api/loadBuilds';
    import filterItems from '@/api/filterItems';
    import uploadFile from '@/api/uploadFile';

    const router = useRouter()
    const toast = useToast();
    const baseUrl = useBaseUrl()    

    const name = ref<string>('')
    const info_before  = ref<string>('')
    const info_after = ref<string>('')
    const year_before  = ref<number>()
    const year_after = ref<number>()
    const photo_before = ref<IFile>() 
    const photo_after = ref<IFile>() 

    const selectedBuild = ref()
    const builds = ref<IBuild[]>([]);    

    const loadingBuild = ref<boolean>(true)

    const saving= ref<Boolean>(false)
    const filteredItems = ref();

    const disableSaveButton = computed<boolean> (()=>{
        return !(selectedBuild.value && name.value && info_before.value && info_after.value && year_before.value && year_after.value)
    })

    const submission = async () => {
        saving.value = true
        const url = baseUrl.baseUrl + 'achievements/';
       
        const config = { headers: { 'content-type': 'multipart/form-data', }, };
        const formData = new FormData();        

        formData.append("name", name.value)
        formData.append("year_before", year_before.value)
        formData.append("info_before", info_before.value)
        formData.append("year_after", year_after.value)
        formData.append("info_after", info_after.value)
        formData.append("build", selectedBuild.value.id)

        photo_before.value && formData.append("photo_before", photo_before.value.file_blob, photo_before.value.file_name)
        photo_after.value && formData.append("photo_after", photo_after.value.file_blob, photo_after.value.file_name)

        const res = await AxiosInstance.post(url, formData, config)
          .then(function(response) {
          toast.add({ severity: 'info', summary: 'Успешно', detail: 'Документ создан', life: 3000 });
          router.push(`/achievements`)
        }).catch(function(error) {
          console.log(error);
        })
        saving.value = false
    }

    const searchItems = (event) => { filteredItems.value = filterItems(builds.value, event.query) }

    const upload_file_before = async (event:any) => { photo_before.value = await uploadFile(event) }
    const upload_file_after = async (event:any)  => { photo_after.value  = await uploadFile(event) }

    onMounted(async () => {
        builds.value = await loadBuilds()
        loadingBuild.value = false
    })    

</script>

<template>
    <div class="content-achievement">
        <Card>                  
            <template #title><h1>Создание Было/стало</h1></template>
            <template #content>

                <div v-if= "!loadingBuild" class="card flex justify-center w-full">
                    <FloatLabel style="width:100%">
                        <AutoComplete class="input mb-5" v-model="selectedBuild" :suggestions="filteredItems" @complete="searchItems" :virtualScrollerOptions="{ itemSize: 10 }" optionLabel="name" inputId="buildId" dropdown />
                        <label for="buildId">Дом</label>
                    </FloatLabel>
                </div>
                <div v-else>
                    <Skeleton width="100%" height="50px"/>
                </div>

                <div class="mt-3">

                <FloatLabel>
                    <InputText class="input mb-3" id="name" v-model="name" />
                    <label for="name">Описание</label>
                </FloatLabel>

                <div class="flex justify-content-center flex-wrap mt-5">
                    <div class="flex align-items-center justify-content-center bg-primary font-bold border-round m-2">
                        <Card style="background-color:lightgray; color:black;  width: 350px; height: 600px; overflow: hidden">
                            <template #header>
                                <img v-if="photo_before" v-bind:src="photo_before.file_base64data"  width="350" height="262"/>
                                <img v-else src="http://localhost:8000/media/achieves_images/no_photo.jpg" width="350" height="262"/>
                            </template>
                            <template #title>Было</template>
                            <template #content>
                                <div class="mt-5">
                                    <div class="field">
                                        <FloatLabel>
                                            <InputNumber class="input mb-3" v-model="year_before" inputId="year_before" :useGrouping="false" :step="1"/>
                                            <label for="year_before" class="font-light">Год</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <FloatLabel>
                                            <InputText class="input mb-3" id="info_before" v-model="info_before" />
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
                                <img v-if="photo_after" v-bind:src="photo_after.file_base64data"  width="350" height="262"/>
                                <img v-else src="http://localhost:8000/media/achieves_images/no_photo.jpg" width="350" height="262"/>
                            </template>
                            <template #title>Стало</template>
                            <template #content>
                                <div class="mt-5">
                                    <div class="field">
                                        <FloatLabel>
                                            <InputNumber class="input mb-3" v-model="year_after" inputId="year_after" :useGrouping="false" :step="1"/>
                                            <label for="year_after" class="font-light">Год</label>
                                        </FloatLabel>
                                    </div>
                                    <div class="field">
                                        <FloatLabel>
                                            <InputText  class="input mb-3" id="info_after" v-model="info_after" />
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
                    <Button v-if= "!disableSaveButton" label="Создать" severity="success" icon="pi pi-check" iconPos="right" @click="submission" :loading="saving"/>
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