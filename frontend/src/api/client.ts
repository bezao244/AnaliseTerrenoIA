import axios from 'axios'
import type { Analysis } from '../types'

const api = axios.create({
  baseURL: '/api',
})

export const uploadImage = async (file: File): Promise<Analysis> => {
  const formData = new FormData()
  formData.append('file', file)
  const response = await api.post<Analysis>('/analyses', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export const getAnalyses = async (): Promise<Analysis[]> => {
  const response = await api.get<Analysis[]>('/analyses')
  return response.data
}

export const getAnalysis = async (id: number): Promise<Analysis> => {
  const response = await api.get<Analysis>(`/analyses/${id}`)
  return response.data
}

export const getHeatmapUrl = (id: number): string => `/api/analyses/${id}/heatmap`

export const getReportUrl = (id: number): string => `/api/analyses/${id}/report`
