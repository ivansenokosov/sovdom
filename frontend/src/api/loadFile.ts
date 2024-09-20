import type { IFile } from "@/interfaces";

const fetchImage = async <T extends Blob>(url:string): Promise <T> => {
  const response : any= await fetch(url)
  const blob : Blob = await response.blob()
  return blob as T
}
  
const blobToBase64 = async <T extends string>(blob:Blob): Promise <T> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result as T)
    reader.onerror = err => reject(err)
    reader.readAsDataURL(blob)
  })
}
  
const loadFile = async <T extends IFile>(url: string): Promise <T> => {
  const imageBlob : Blob = await fetchImage(url)
  const imageBase64 : string = await blobToBase64(imageBlob)
  let fileI : IFile = {"file_name": "filename.jpg", "file_blob": imageBlob, "file_base64data": imageBase64}
  return fileI as T
}

export default loadFile

