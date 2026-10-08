// The analysis panel's report on one thing (DESIGN.md E8): its LLM-written card and how it was
// checked, a button that writes it (or writes it again) in the background, and questions.
import { apiClient } from '../../api/client'
import { useCard } from '../../hooks/useCard'
import { useJobRunner } from '../../hooks/useJobRunner'
import JobProgress from '../lenses/JobProgress'
import { CardMarks, CardText } from './CardBody'
import CardQuestions from './CardQuestions'

interface AnalysisReportProps {
  session: string
  lens: string
  cardId: string
  label: string // what the report is on
  listed: boolean | undefined // whether the card exists (undefined while the lens's list loads)
  onWritten: () => void // re-reads the lens's card list
  disabled: boolean // visitors read only
}

export default function AnalysisReport({ session, lens, cardId, label, listed, onWritten, disabled }: AnalysisReportProps) {
  const { card, missing, error, reload } = useCard(session, lens, cardId, listed)
  const writer = useJobRunner(() => { onWritten(); reload() })
  // the lens report is two drafts and a reconciliation; any card may need one retry
  const budget = cardId === 'lens' ? 8 : 3
  const write = () => void writer.start(() => apiClient.startAnalysis(session, lens, [cardId], budget))
  return (
    <div id="analysis-report" className="border border-violet-200 bg-violet-50/40 rounded p-2 space-y-1.5 text-[11px] text-gray-800">
      <div className="flex items-center gap-1.5 flex-wrap">
        <span className="text-xs font-semibold text-violet-900">{label}</span>
        {card && <CardMarks card={card} />}
        {(missing || card) && (
          <button onClick={write} disabled={disabled || writer.running || writer.starting}
            className="ml-auto px-2 py-0.5 text-[11px] rounded border border-violet-500 text-violet-700 hover:bg-violet-50 disabled:border-gray-300 disabled:text-gray-400">
            {card ? 'Write again' : 'Write report'}</button>
        )}
      </div>
      {missing && !writer.job && (
        <p className="text-gray-500">Not written yet. An analyst writes it from this view's evidence, and every number it
          cites is checked (up to {budget} calls on the Claude subscription).</p>
      )}
      {(error || writer.error) && <p className="text-red-600">{error ?? writer.error}</p>}
      {writer.job && writer.job.state !== 'done' && (
        <JobProgress job={writer.job} title="Report" onCancel={writer.running ? writer.cancel : undefined} />
      )}
      {card && !card.output && <p className="text-red-600">The analyst didn't answer: {card.error}</p>}
      {card?.output && <CardText output={card.output} facts={card.facts} />}
      {card?.check && !card.check.passed && (
        <ul className="text-amber-800 text-[10px]">
          {card.check.failures.map((f, i) => <li key={i}>⚠ {f.numeral || 'a citation'}: {f.reason}</li>)}
        </ul>
      )}
      {card && <CardQuestions session={session} lens={lens} cardId={cardId} disabled={disabled} />}
    </div>
  )
}
