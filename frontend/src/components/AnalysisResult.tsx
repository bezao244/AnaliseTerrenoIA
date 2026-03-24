import type { Analysis } from '../types'

interface AnalysisResultProps {
  analysis: Analysis
}

export default function AnalysisResult({ analysis }: AnalysisResultProps) {
  const { analysis_result } = analysis

  return (
    <div className="w-full max-w-3xl mx-auto space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-bold text-green-800 mb-1">
          {analysis_result.terrain_type}
        </h2>
        <p className="text-sm text-gray-500">Arquivo: {analysis.filename}</p>
        <div className="mt-3 flex items-center space-x-2">
          <span className="text-sm font-medium text-gray-600">Score de Fertilidade:</span>
          <span className="text-xl font-bold text-green-600">
            {analysis_result.overall_fertility_score.toFixed(1)}
          </span>
          <span className="text-gray-400">/10</span>
        </div>
        <div className="mt-2 w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-green-500 h-3 rounded-full transition-all"
            style={{ width: `${(analysis_result.overall_fertility_score / 10) * 100}%` }}
          />
        </div>
      </div>

      {analysis_result.components.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">Composição do Terreno</h3>
          <div className="space-y-3">
            {analysis_result.components.map((comp) => (
              <div key={comp.name}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium" style={{ color: comp.color }}>{comp.name}</span>
                  <span className="text-gray-500">{comp.percentage.toFixed(1)}%</span>
                </div>
                <div className="w-full bg-gray-100 rounded-full h-4">
                  <div
                    className="h-4 rounded-full"
                    style={{ width: `${comp.percentage}%`, backgroundColor: comp.color }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {analysis_result.fertile_areas.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Áreas Férteis</h3>
          <ul className="space-y-2">
            {analysis_result.fertile_areas.map((area, i) => (
              <li key={i} className="flex items-start space-x-2">
                <span className="text-green-500 mt-0.5">🌱</span>
                <span className="text-gray-700">{area}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {analysis_result.technical_report && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Relatório Técnico</h3>
          <p className="text-gray-700 leading-relaxed">{analysis_result.technical_report}</p>
        </div>
      )}

      {analysis_result.recommendations.length > 0 && (
        <div className="bg-white rounded-xl shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Recomendações</h3>
          <ol className="space-y-2 list-decimal list-inside">
            {analysis_result.recommendations.map((rec, i) => (
              <li key={i} className="text-gray-700">{rec}</li>
            ))}
          </ol>
        </div>
      )}
    </div>
  )
}
