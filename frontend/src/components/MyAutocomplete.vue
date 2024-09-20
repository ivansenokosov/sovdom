<script setup lang="ts">
    import { onMounted, ref, watch } from 'vue'
    import AutoComplete from 'primevue/autocomplete';
    import FloatLabel from 'primevue/floatlabel';

    const props       = defineProps(['options','label','value','disabled','optionLabel']) 
    const model       = defineModel<number>()
    const innermodel  = ref<any>(null)
    const optionLabel = ref<string>('name')

    const filteredOptions = ref<any[]>([]);

    const search = (event:any) => {
        filteredOptions.value = props.options.filter((item:any) => item[optionLabel.value].toString().toUpperCase().includes(event.query.toUpperCase().replace(',','.')))
    }

    watch(innermodel, () => {
        if (model.value) { model.value = innermodel.value.id }
    })

    onMounted(() => {        
        innermodel.value = props.options.filter((item:any) => item.id === props.value)[0]
        props.optionLabel ? optionLabel.value = props.optionLabel : optionLabel.value = 'name'
    })

</script>

<template>
    <FloatLabel>
        <AutoComplete v-model="innermodel" :optionLabel="optionLabel" :suggestions="filteredOptions" @complete="search" dropdown :disabled="disabled" class="w-full md:w-56"/> 
        <label>{{ props.label }}</label>
    </FloatLabel>
</template>