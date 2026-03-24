import { useState, useRef, DragEvent, ChangeEvent } from 'react'
import { uploadImage } from '../api/client'
import type { Analysis } from '../types'
import LoadingAnimation from './LoadingAnimation'

interface UploadProps {
  onAnalysisComplete: (analysis: Analysis) => void
}

export default function Upload({ onAnalysisComplete }: UploadProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = (file: File) => {
    setSelectedFile(file)
    setError(null)
    const reader = new FileReader()
    reader.onload = (e) => setPreview(e.target?.result as string)
    reader.readAsDataURL(file)
  }

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
      handleFile(file)
    }
  }

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
  }

  const handleAnalyze = async () => {
    if (!selectedFile) return
    setIsLoading(true)
    setError(null)
    try {
      const result = await uploadImage(selectedFile)
      onAnalysisComplete(result)
    } catch (err: unknown) {
      const message =
        err instanceof Error ? err.message : 'Erro ao analisar imagem. Tente novamente.'
      setError(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!isLoading && (
        <>
          <div
            data-testid="upload-zone"
            onDragOver={(e) => { e.preventDefault(); setIsDragging(true) }}
            onDragLeave={() => setIsDragging(false)}
            onDrop={handleDrop}
            onClick={() => inputRef.current?.click()}
            className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
              isDragging ? 'border-green-500 bg-green-50' : 'border-gray-300 hover:border-green-400 hover:bg-gray-50'
            }`}
          >
            <input
              ref={inputRef}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={handleChange}
              data-testid="file-input"
            />
            {preview ? (
              <img
                src={preview}
                alt="Preview"
                className="mx-auto max-h-64 rounded-lg object-contain"
              />
            ) : (
              <div className="space-y-3">
                <div className="text-5xl">🌍</div>
                <p className="text-lg font-medium text-gray-700">
                  Arraste uma imagem ou clique para selecionar
                </p>
                <p className="text-sm text-gray-400">PNG, JPG, JPEG até 10MB</p>
              </div>
            )}
          </div>

          {selectedFile && (
            <div className="mt-4 flex flex-col items-center space-y-3">
              <p className="text-sm text-gray-600">
                Arquivo selecionado: <strong>{selectedFile.name}</strong>
              </p>
              <button
                onClick={handleAnalyze}
                className="px-8 py-3 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                disabled={isLoading}
              >
                Analisar Terreno
              </button>
            </div>
          )}

          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
              {error}
            </div>
          )}
        </>
      )}

      <LoadingAnimation isLoading={isLoading} />
    </div>
  )
}
