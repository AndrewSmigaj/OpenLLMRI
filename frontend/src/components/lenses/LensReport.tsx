// A lens's report (DESIGN.md C7) or its k advisor on the Build page: the analysis panel's report,
// with the lens's own card list.
import { useCardList } from '../../hooks/useCard'
import AnalysisReport from '../analysis/AnalysisReport'

interface LensReportProps {
  session: string
  lens: string
  cardId: 'lens' | 'k'
  label: string
  disabled: boolean
}

export default function LensReport({ session, lens, cardId, label, disabled }: LensReportProps) {
  const cards = useCardList(session, lens, true)
  return (
    <AnalysisReport session={session} lens={lens} cardId={cardId} label={label}
      listed={cards.ids ? cards.ids.has(cardId) : undefined} onWritten={cards.reload} disabled={disabled} />
  )
}
