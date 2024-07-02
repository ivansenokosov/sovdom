import axios from 'axios'

const baseUrl = 'http://localhost:8000/'

const AxiosInstance = axios.create({
    baseURL: baseUrl,
    timeout: 100000,
    headers: {
        "Content-Type": "application/json",
        accept: "application/json"
    }
}) 

export default AxiosInstance