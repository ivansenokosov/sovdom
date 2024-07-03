import { defineStore } from 'pinia'

export const useBaseUrl = defineStore('baseUrl', () => {
  const baseUrl = 'http://localhost:8000/'
  
  return { baseUrl }
})
