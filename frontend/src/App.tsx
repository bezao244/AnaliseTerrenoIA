import { useState, useEffect } from 'react'
import Upload from './components/Upload'
import AnalysisResult from './components/AnalysisResult'
import HeatMap from './components/HeatMap'
import AnalysisHistory from './components/AnalysisHistory'
import ReportExport from './components/ReportExport'
import { getAnalyses } from './api/client'
import type { Analysis } from './types'

type Tab = 'nova' | 'historico'

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>('nova')
  const [currentAnalysis, setCurrentAnalysis] = useState<Analysis | null>(null)
  const [history, setHistory] = useState<Analysis[]>([])

  const loadHistory = async () => {
    try {
      const data = await getAnalyses()
      setHistory(data)
    } catch {
      // silently fail if backend not available
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  const handleAnalysisComplete = (analysis: Analysis) => {
    setCurrentAnalysis(analysis)
    setHistory((prev) => [analysis, ...prev.filter((a) => a.id !== analysis.id)])
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <span className="text-3xl">🌿</span>
            <div>
              <h1 className="text-xl font-bold text-green-800">AnaliseTerrenoIA</h1>
              <p className="text-xs text-gray-500">Análise Inteligente de Terrenos</p>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-6">
        <div className="flex space-x-1 bg-white rounded-xl shadow-sm p-1 mb-6 w-fit">
          <button
            onClick={() => setActiveTab('nova')}
            className={`px-6 py-2.5 rounded-lg font-medium text-sm transition-colors ${
              activeTab === 'nova'
                ? 'bg-green-600 text-white shadow-sm'
                : 'text-gray-600 hover:text-green-700'
            }`}
          >
            🌱 Nova Análise
          </button>
          <button
            onClick={() => setActiveTab('historico')}
            className={`px-6 py-2.5 rounded-lg font-medium text-sm transition-colors ${
              activeTab === 'historico'
                ? 'bg-green-600 text-white shadow-sm'
                : 'text-gray-600 hover:text-green-700'
            }`}
          >
            📋 Histórico
          </button>
        </div>

        {activeTab === 'nova' && (
          <div className="space-y-8">
            <Upload onAnalysisComplete={handleAnalysisComplete} />

            {currentAnalysis && (
              <>
                <AnalysisResult analysis={currentAnalysis} />
                <HeatMap analysis={currentAnalysis} />
                <div className="flex justify-center">
                  <ReportExport analysisId={currentAnalysis.id} />
                </div>
              </>
            )}
          </div>
        )}

        {activeTab === 'historico' && (
          <AnalysisHistory
            analyses={history}
            onSelect={(analysis) => {
              setCurrentAnalysis(analysis)
              setActiveTab('nova')
            }}
          />
        )}
      </div>
    </div>
  )
}
