import type { Analysis } from '../types'

interface HeatMapProps {
  analysis: Analysis
}

const TERRAIN_LEGEND = [
  { label: 'Vegetação', color: '#228B22' },
  { label: 'Solo', color: '#8B4513' },
  { label: 'Água', color: '#0077BE' },
  { label: 'Rocha', color: '#808080' },
  { label: 'Areia', color: '#F4A460' },
  { label: 'Floresta', color: '#006400' },
]

export default function HeatMap({ analysis }: HeatMapProps) {
  if (!analysis.heatmap_image) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6 text-center text-gray-500">
        Mapa de calor não disponível para esta análise.
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Mapa de Calor do Terreno</h3>
      <div className="rounded-lg overflow-hidden border border-gray-200">
        <img
          src={`data:image/png;base64,${analysis.heatmap_image}`}
          alt="Mapa de calor do terreno"
          className="w-full object-contain"
        />
      </div>

      <div className="mt-4">
        <h4 className="text-sm font-medium text-gray-600 mb-2">Legenda Geral</h4>
        <div className="flex flex-wrap gap-3">
          {TERRAIN_LEGEND.map((item) => (
            <div key={item.label} className="flex items-center space-x-1.5">
              <div
                className="w-4 h-4 rounded"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-xs text-gray-600">{item.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
