import { useState } from 'react'
import type { Analysis } from '../types'

interface AnalysisHistoryProps {
  analyses: Analysis[]
  onSelect: (analysis: Analysis) => void
}

export default function AnalysisHistory({ analyses, onSelect }: AnalysisHistoryProps) {
  const [expandedId, setExpandedId] = useState<number | null>(null)

  if (analyses.length === 0) {
    return (
      <div className="text-center py-16 text-gray-500">
        <div className="text-5xl mb-4">📂</div>
        <p className="text-lg">Nenhuma análise encontrada.</p>
        <p className="text-sm mt-1">Faça upload de uma imagem para começar.</p>
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {analyses.map((analysis) => {
        const date = new Date(analysis.created_at)
        const formatted = date.toLocaleDateString('pt-BR', {
          day: '2-digit',
          month: '2-digit',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
        })
        const isExpanded = expandedId === analysis.id

        return (
          <div key={analysis.id} className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="flex items-center p-4 cursor-pointer hover:bg-gray-50 transition-colors">
              <div className="w-16 h-16 rounded-lg overflow-hidden flex-shrink-0 border border-gray-200">
                <img
                  src={`data:image/jpeg;base64,${analysis.original_image}`}
                  alt={analysis.filename}
                  className="w-full h-full object-cover"
                />
              </div>

              <div className="ml-4 flex-1 min-w-0">
                <p className="font-semibold text-gray-800 truncate">{analysis.filename}</p>
                <p className="text-sm text-green-700">{analysis.analysis_result.terrain_type}</p>
                <p className="text-xs text-gray-400 mt-0.5">{formatted}</p>
              </div>

              <div className="ml-4 flex items-center space-x-2">
                <span className="text-sm font-bold text-green-600">
                  {analysis.analysis_result.overall_fertility_score.toFixed(1)}/10
                </span>
                <button
                  onClick={() => {
                    setExpandedId(isExpanded ? null : analysis.id)
                    onSelect(analysis)
                  }}
                  className="text-xs px-3 py-1.5 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
                >
                  {isExpanded ? 'Fechar' : 'Ver'}
                </button>
              </div>
            </div>

            {isExpanded && (
              <div className="border-t border-gray-100 p-4 bg-gray-50">
                <p className="text-sm text-gray-700">{analysis.analysis_result.technical_report}</p>
                <div className="mt-3 flex flex-wrap gap-2">
                  {analysis.analysis_result.components.map((c) => (
                    <span
                      key={c.name}
                      className="text-xs px-2 py-1 rounded-full text-white"
                      style={{ backgroundColor: c.color }}
                    >
                      {c.name} {c.percentage.toFixed(0)}%
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )
      })}
    </div>
  )
}
