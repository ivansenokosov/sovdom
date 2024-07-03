import { useBaseUrl } from '@/stores/baseUrl'
import AxiosInstance from "./axiosInstance"
import type { IAchievement } from '@/interfaces'

const baseUrl = useBaseUrl()

const loadAchievement = async <T extends IAchievement>(id:string): Promise<T> => {
    try {
        const url = baseUrl.baseUrl + 'achievements/' + id
        const rawData = await AxiosInstance.get(url)
        let achievement: T = rawData.data
        return achievement 
    } catch(error) {
        let nullAchievement: T
        console.log(error)
        return nullAchievement
    }
}

export default loadAchievement

