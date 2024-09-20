import type { IFile } from "@/interfaces";

const fetchImage = async (url:string) => {
  const response = await fetch(url, { mode: 'no-cors', })
  const blob = await response.blob()
  return blob
}
  
const blobToBase64 = async <T extends string>(blob:Blob): Promise <T> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as T)
    reader.onerror = err => reject(err)
    reader.readAsDataURL(blob)
  })
}
  
const uploadFile = async <T extends IFile>(event: any): Promise<T> => {
  const file = event.files[0];
  const imageBlob : Blob= await fetchImage(file.objectURL)
  const imageBase64 : string = await blobToBase64(imageBlob)
  let fileI : IFile = {"file_name": file.name, "file_blob": imageBlob, "file_base64data": imageBase64}
  return fileI as T
}

export default uploadFile

