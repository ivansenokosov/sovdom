// import {ref, reactive, toRefs  } from 'vue'
// import { useBaseUrl } from '@/stores/baseUrl'
// import AxiosInstance from './axiosInstance';
// import type { IYears } from '@/interfaces';
// const baseUrl = useBaseUrl()

// export async function loadYearsData(buildId:number):Promise<{years: IYears[], error: any, loading:boolean}> {
//   const data = ref<IYears[]>([]);
//   const state = reactive({
//     error: null,
//     loading: false
//   });

//   state.loading = true;

//   try {
//     const url = 'json?build_id=' + String(buildId) + '&extra_work=0'
//     const macroRawData = await AxiosInstance.get(url)
//     let newdata =  []
//     newdata = JSON.parse(macroRawData.data)
//     data.value = newdata[0].categories
//     } catch (error) {
//       state.error = error;
// //      state.error="Нет данных по дому"
//     } finally {
//       state.loading = false;
//     }
//     return {data, ...toRefs(state)};
// }