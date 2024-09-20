import {ref} from 'vue'
import { useBaseUrl } from '@/stores/baseUrl'
import AxiosInstance from './axiosInstance';
import type { IMacroData } from '@/interfaces';

const baseUrl = useBaseUrl()

export async function loadMacroData<T extends IMacroData>(buildId:number, eW:number): Promise<T> {
  const data = ref<IMacroData>({years: [], macroData: [], macroDataSum: [], error: null, loading: true})


  data.value.loading = true;

  try {
    const url = 'json?build_id=' + String(buildId) + '&extra_work=' + String(eW)
    const macroRawData = await AxiosInstance.get(url)
    let newdata =  []
    newdata = JSON.parse(macroRawData.data)
    data.value.years = newdata[0].categories
    data.value.macroData = newdata[1].macro
    data.value.macroDataSum = newdata[2].macro_sum
  } catch (error) {
      data.value.error = error;
//      state.error="Нет данных по дому"
  } finally {
    data.value.loading = false;
  }
  return data.value as T;
}