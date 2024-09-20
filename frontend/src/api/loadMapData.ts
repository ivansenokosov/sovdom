import {toRefs, ref, reactive} from 'vue';

import { useBaseUrl } from '@/stores/baseUrl'
import AxiosInstance from '@/api/axiosInstance';
import type { IDocument, IMarker } from '@/interfaces';

const baseUrl = useBaseUrl()

export async function loadMap <T extends IDocument<IMarker>>(): Promise<T> {

    const data = ref<IMarker[]>([]);    
    const error = ref<any>(null)
    const loading = ref<boolean>(true)

    try {
        const mapRawData = await AxiosInstance.get('map_json')
        let newmapdata =  []
        newmapdata = JSON.parse(mapRawData.data)
        let mapData = newmapdata
        mapData.map((item:any) => {
            data.value.push({buildid: item.id, 
                       coordinates:[item.geometry.coordinates[1], item.geometry.coordinates[0]], 
                       title:item.properties.iconContent,
                       color: '#343d44',
                       draggable: false,
                       })
        })
    } catch (e:any) {
        error.value = e;
    } finally {
        loading.value = false;
    }

    return {data: data.value, error: error.value, loading: loading.value} as T;
}

