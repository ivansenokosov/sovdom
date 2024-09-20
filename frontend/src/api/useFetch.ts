import {toRefs, ref, reactive} from 'vue';
import { useBaseUrl } from '@/stores/baseUrl'

const baseUrl = useBaseUrl()

interface IFetch {
  data : any[]
  error: any
  loading: boolean
}

export async function useFetch<T extends IFetch>(url:string, options:any = {}): Promise<T> {
  const res = ref<IFetch>({data:[], error: null, loading: true})

  try {
    const result = await fetch(baseUrl.baseUrl + url, options)
    const data   = await result.json()
    if (!Array.isArray(data) && Array.isArray(res.value.data)) {
      res.value.data.push(data) // Если тип принимающего элемента массив, а пришёл не массив
    } else {
      res.value.data = data
    }


  } catch (e) {
    res.value.error = e;
  } finally {
    res.value.loading = false;
  }
  return {data: res.value.data, loading: res.value.loading, error: res.value.error} as T;
}

// export async function useFetch(url:string, options:any) {
//   const data = ref(null);
//   const state = reactive({
//     error: null,
//     loading: false
//   });

//   state.loading = true;

//   try {
//     const res = await fetch(baseUrl.baseUrl + url, options);
//     data.value = await res.json();
//   } catch (e) {
//     state.error = e;
//   } finally {
//     state.loading = false;
//   }
//   return {data, ...toRefs(state)};
// }