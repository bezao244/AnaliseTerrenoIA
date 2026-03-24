import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import Upload from '../components/Upload'
import * as apiClient from '../api/client'
import type { Analysis } from '../types'

vi.mock('../api/client', () => ({
  uploadImage: vi.fn(),
  getAnalyses: vi.fn().mockResolvedValue([]),
  getHeatmapUrl: vi.fn((id: number) => `/api/analyses/${id}/heatmap`),
  getReportUrl: vi.fn((id: number) => `/api/analyses/${id}/report`),
}))

const mockAnalysis: Analysis = {
  id: 1,
  filename: 'test.jpg',
  original_image: 'base64data',
  heatmap_image: null,
  analysis_result: {
    is_terrain: true,
    terrain_type: 'Solo Argiloso',
    components: [{ name: 'Vegetação', percentage: 60, color: '#228B22' }],
    fertile_areas: ['Área norte'],
    technical_report: 'Solo fértil.',
    recommendations: ['Irrigação regular'],
    overall_fertility_score: 8.0,
  },
  created_at: new Date().toISOString(),
}

describe('Upload', () => {
  const onAnalysisComplete = vi.fn()

  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the upload zone', () => {
    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    expect(screen.getByTestId('upload-zone')).toBeInTheDocument()
  })

  it('shows default upload prompt', () => {
    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    expect(screen.getByText(/Arraste uma imagem ou clique para selecionar/)).toBeInTheDocument()
  })

  it('shows file input', () => {
    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    expect(screen.getByTestId('file-input')).toBeInTheDocument()
  })

  it('shows analyze button after file selection', async () => {
    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    const input = screen.getByTestId('file-input')
    const file = new File(['content'], 'terrain.jpg', { type: 'image/jpeg' })

    Object.defineProperty(input, 'files', {
      value: [file],
      configurable: true,
    })
    fireEvent.change(input)

    await waitFor(() => {
      expect(screen.getByText('Analisar Terreno')).toBeInTheDocument()
    })
  })

  it('calls uploadImage and onAnalysisComplete on submit', async () => {
    vi.mocked(apiClient.uploadImage).mockResolvedValueOnce(mockAnalysis)

    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    const input = screen.getByTestId('file-input')
    const file = new File(['content'], 'terrain.jpg', { type: 'image/jpeg' })

    Object.defineProperty(input, 'files', {
      value: [file],
      configurable: true,
    })
    fireEvent.change(input)

    await waitFor(() => screen.getByText('Analisar Terreno'))
    fireEvent.click(screen.getByText('Analisar Terreno'))

    await waitFor(() => {
      expect(apiClient.uploadImage).toHaveBeenCalledWith(file)
      expect(onAnalysisComplete).toHaveBeenCalledWith(mockAnalysis)
    })
  })

  it('shows error message when upload fails', async () => {
    vi.mocked(apiClient.uploadImage).mockRejectedValueOnce(new Error('Upload falhou'))

    render(<Upload onAnalysisComplete={onAnalysisComplete} />)
    const input = screen.getByTestId('file-input')
    const file = new File(['content'], 'terrain.jpg', { type: 'image/jpeg' })

    Object.defineProperty(input, 'files', {
      value: [file],
      configurable: true,
    })
    fireEvent.change(input)

    await waitFor(() => screen.getByText('Analisar Terreno'))
    fireEvent.click(screen.getByText('Analisar Terreno'))

    await waitFor(() => {
      expect(screen.getByText('Upload falhou')).toBeInTheDocument()
    })
  })
})
