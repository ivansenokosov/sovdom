export interface IAchievement {
  id: Number
  build: Number
  address: String
  name: String
  year_before: Number
  year_after: Number
  info_before: String
  info_after: String
  photo_before?: String
  photo_after?: String  
} 

export interface IBuild {
  id: Number
  name: String
}

export interface IFile {
  file_name: String
  file_blob?: Blob
  file_base64data?: String
}