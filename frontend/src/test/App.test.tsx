import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import App from '../App'

vi.mock('../api/client', () => ({
  getAnalyses: vi.fn().mockResolvedValue([]),
  uploadImage: vi.fn(),
  getHeatmapUrl: vi.fn((id: number) => `/api/analyses/${id}/heatmap`),
  getReportUrl: vi.fn((id: number) => `/api/analyses/${id}/report`),
}))

describe('App', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('renders the app title', () => {
    render(<App />)
    expect(screen.getByText('AnaliseTerrenoIA')).toBeInTheDocument()
  })

  it('renders Nova Análise tab', () => {
    render(<App />)
    expect(screen.getByText(/Nova Análise/)).toBeInTheDocument()
  })

  it('renders Histórico tab', () => {
    render(<App />)
    expect(screen.getByText(/Histórico/)).toBeInTheDocument()
  })

  it('switches to Histórico tab when clicked', async () => {
    render(<App />)
    const historicoTab = screen.getByText(/Histórico/)
    fireEvent.click(historicoTab)
    await waitFor(() => {
      expect(screen.getByText(/Nenhuma análise encontrada/)).toBeInTheDocument()
    })
  })

  it('shows upload zone on Nova Análise tab', () => {
    render(<App />)
    expect(screen.getByTestId('upload-zone')).toBeInTheDocument()
  })

  it('switches back to Nova Análise tab', () => {
    render(<App />)
    const novaTab = screen.getByText(/Nova Análise/)
    fireEvent.click(novaTab)
    expect(screen.getByTestId('upload-zone')).toBeInTheDocument()
  })
})
