import type { LngLat, YMap  } from '@yandex/ymaps3-types';

export interface IDocument<T> {
  data   : T[]
  error  : any
  loading: boolean
}

export interface IAchievement {
  id: number
  build: number
  address: string
  name: string
  year_before: number
  year_after: number
  info_before: string
  info_after: string
  photo_before?: string
  photo_after?: string  
} 

export interface IBuild {
  id: number
  name: string
}

export interface IBuildCard {
  id: number
  city_name: string
  addr_str: string
  management_str: string
  total_rub: string
  report_rub: string
  management_rub: string
  repair_rub: string
  report_number: string
  number: string
  litera: string 
  corpse: string
  ymap: string
  photo: string
  year: number
  floors: number
  q_porchs: number
  q_lifts: number
  q_flats: number
  q_uu: number
  s_live: string
  s_no_live: string
  s_mop: string
  s_zem: string
  kadnum_zem: string
  has_garret: boolean
  city: number
  street: number
  priority: number
  gas_type: number
  wall_material: number
  roof_material: number
}


export interface IFile {
  file_name: string
  file_blob?: Blob
  file_base64data?: string
}

export interface ICity {
  id: number
  name: string
  ymap: string
  qbuilds: number
}

export interface IMarker {
  buildid: number
  coordinates: LngLat
  title: string
  color: string
  draggable: boolean
}

export interface IYears {
  text: string
}

export interface IMapData {
  data: IMarker[]
  error: any
  loading: boolean
}


export interface IDataElement {
  color: string
  data: number[]
  name: string
  stack: string
}

export interface IMacroData {
  years: IYears[]
  macroData: IDataElement[]
  macroDataSum: IDataElement[]
  error: any
  loading: boolean
}

export interface IMicroInfo {
  name: string
  subtitle: string
  denominator: string
  container_max_value: string
  denominator_value: string
}

export interface IMicroElement {
  type: string
  name: string
  color: string
  data: number[]
  pointPlacement: string
  stack: string
}

export interface IMicroContainer {
  info: IMicroInfo[]
  element: IMicroElement[]
}

// export interface IMicroData {
//   microData: IMicroContainer[]
//   error: any
//   loading: boolean  
// }