import type { IBuild } from "@/interfaces"
import { useBaseUrl } from '@/stores/baseUrl'
import AxiosInstance from "./axiosInstance"

const baseUrl = useBaseUrl()

const loadBuilds = async <T extends IBuild>(): Promise<T[]> => {
    try {
        const url = baseUrl.baseUrl + 'catalogs/builds?city=1'
        const buildsRawData = await AxiosInstance.get(url)
        let builds: T[] = buildsRawData.data
        return builds 
    } catch(error) {
        console.log(error)
        let undefined: T[] = []
        undefined.push({'id':0, 'name':'undefined'})
        return undefined
    }
}

export default loadBuilds

