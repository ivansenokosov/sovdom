import { ref } from 'vue'
import { useBaseUrl } from '@/stores/baseUrl'
import AxiosInstance from './axiosInstance';
import type { IDocument, IMicroContainer } from '@/interfaces';
const baseUrl = useBaseUrl()

export async function loadMicroData<T extends IDocument<IMicroContainer>>(buildId:number): Promise<T> {
  const microData = ref<IDocument<IMicroContainer>>({data: [], error: null, loading: true})

  const url = 'micro_details_json?build_id=' + buildId

  try {    
    const microRawData = await AxiosInstance.get(url)
    microData.value.data = JSON.parse(microRawData.data)
  } catch(error) {
    console.log(error)
    microData.value.error ="Нет данных по дому"
  } finally {
    microData.value.loading = false
  }


  return microData.value as T
}