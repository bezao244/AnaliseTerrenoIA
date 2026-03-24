import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'

interface LoadingAnimationProps {
  isLoading: boolean
}

const STEPS = [
  'Carregando imagem...',
  'Processando com IA...',
  'Gerando mapa de calor...',
  'Compilando relatório...',
]

export default function LoadingAnimation({ isLoading }: LoadingAnimationProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [completedSteps, setCompletedSteps] = useState<number[]>([])

  useEffect(() => {
    if (!isLoading) {
      setCurrentStep(0)
      setCompletedSteps([])
      return
    }

    setCurrentStep(0)
    setCompletedSteps([])

    const timers: ReturnType<typeof setTimeout>[] = []
    STEPS.forEach((_, i) => {
      timers.push(
        setTimeout(() => {
          setCurrentStep(i)
          if (i > 0) {
            setCompletedSteps((prev) => [...prev, i - 1])
          }
        }, i * 1500)
      )
    })

    return () => timers.forEach(clearTimeout)
  }, [isLoading])

  if (!isLoading) return null

  return (
    <div className="flex flex-col items-center justify-center py-12 space-y-4">
      <motion.div
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        className="text-2xl font-bold text-green-700 mb-4"
      >
        Analisando Terreno...
      </motion.div>

      <div className="space-y-3 w-full max-w-md">
        {STEPS.map((step, index) => {
          const isComplete = completedSteps.includes(index)
          const isActive = currentStep === index
          return (
            <motion.div
              key={step}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: isActive || isComplete ? 1 : 0.4, x: 0 }}
              transition={{ delay: index * 0.1 }}
              className="flex items-center space-x-3"
            >
              <div className="w-6 h-6 flex items-center justify-center">
                {isComplete ? (
                  <motion.span
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="text-green-500 text-xl"
                  >
                    ✓
                  </motion.span>
                ) : isActive ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
                    className="w-5 h-5 border-2 border-green-500 border-t-transparent rounded-full"
                  />
                ) : (
                  <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
                )}
              </div>
              <span
                className={`text-sm ${
                  isActive ? 'text-green-700 font-semibold' : isComplete ? 'text-gray-500' : 'text-gray-400'
                }`}
              >
                {step}
              </span>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
