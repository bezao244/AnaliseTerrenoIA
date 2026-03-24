import { getReportUrl } from '../api/client'

interface ReportExportProps {
  analysisId: number
}

export default function ReportExport({ analysisId }: ReportExportProps) {
  const handleDownload = () => {
    const url = getReportUrl(analysisId)
    const link = document.createElement('a')
    link.href = url
    link.download = `relatorio_${analysisId}.pdf`
    link.click()
  }

  return (
    <button
      onClick={handleDownload}
      className="flex items-center space-x-2 px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors"
    >
      <span>📄</span>
      <span>Exportar Relatório PDF</span>
    </button>
  )
}
