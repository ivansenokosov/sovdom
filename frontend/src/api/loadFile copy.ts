import type { IFile } from "@/interfaces";

const fetchImage = async (url:String) => {
  const response = await fetch(url)
  const blob = await response.blob()
  return blob
}
  
const blobToBase64 = async (blob:Blob) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result)
    reader.onerror = err => reject(err)
    reader.readAsDataURL(blob)
  })
}
  
const loadFile = async <T extends IFile>(url: string): Promise<T> => {
  const imageBlob = await fetchImage(url)
  const imageBase64 = await blobToBase64(imageBlob)
  let fileI : T = {"file_name": "filename.jpg", "file_blob": imageBlob, "file_base64data": imageBase64}
  return fileI
}

export default loadFile

