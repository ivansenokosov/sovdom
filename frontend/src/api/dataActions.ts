import AxiosInstance from "./axiosInstance";

const config = { headers: { 'content-type': 'application/json', }, };

export async function updateData(url: string, formData: any) {
    return new Promise ((resolve, reject) => {
         AxiosInstance.put(url, formData, config)
        .then(function(response) {
            resolve(response)
        })
        .catch(function(error) {
            reject(error)
        })
    })
}

export async function insertData(url: string, formData: any) {
    return new Promise ((resolve, reject) => {
        AxiosInstance.post(url, formData, config)
        .then(function(response) {
            resolve(response)
        })
        .catch(function(error) {
            reject(error)
        })
    }) 
}

export async function deleteData(url: string) {
    return new Promise ((resolve, reject) => {
        AxiosInstance.delete(url,{})
        .then(function(response) {
            resolve(response)
        })
        .catch(function(error) {
            reject(error)
        })
    })
}
