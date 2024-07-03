import type { IFile } from "@/interfaces";

const fetchImage = async (url:String) => {
  const response = await fetch(url, {
    mode: 'no-cors',
  })
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
  
const uploadFile = async <T extends IFile>(event: any): Promise<T> => {
  const file = event.files[0];
  const imageBlob = await fetchImage(file.objectURL)
  const imageBase64 = await blobToBase64(imageBlob)
  let fileI : T = {"file_name": file.name, "file_blob": imageBlob, "file_base64data": imageBase64}
  return fileI
}

export default uploadFile

