import axios from 'axios'
import { useBaseUrl } from '@/stores/baseUrl'

const baseUrl = useBaseUrl()

const AxiosInstance = axios.create({
    baseURL: baseUrl.baseUrl,
    timeout: 100000,
    headers: {
        "Content-Type": "application/json",
        accept: "application/json"
    }
}) 

export default AxiosInstance

