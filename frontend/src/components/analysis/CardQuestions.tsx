// Follow-up questions about a card's subject (DESIGN.md E8): an analyst answers from the same
// evidence, in the background; each answer's numbers are checked like a card's.
import { useCallback, useEffect, useState } from 'react'
import { apiClient } from '../../api/client'
import { useJobRunner } from '../../hooks/useJobRunner'
import type { QuestionAnswer } from '../../types/cards'
import JobProgress from '../lenses/JobProgress'
import CitedText from './CitedText'

interface CardQuestionsProps {
  session: string
  lens: string
  cardId: string
  disabled: boolean
}

export default function CardQuestions({ session, lens, cardId, disabled }: CardQuestionsProps) {
  const [answers, setAnswers] = useState<QuestionAnswer[]>([])
  const [question, setQuestion] = useState('')
  const [reads, setReads] = useState(0)
  const reread = useCallback(() => setReads(n => n + 1), [])
  const asker = useJobRunner(reread)

  useEffect(() => {
    let current = true
    apiClient.listQuestions(session, lens, cardId)
      .then(found => { if (current) setAnswers(found.questions) })
      .catch(() => { if (current) setAnswers([]) })
    return () => { current = false }
  }, [session, lens, cardId, reads])

  const ask = () => {
    const asked = question.trim()
    if (asked.length < 3) return
    void asker.start(() => apiClient.askQuestion(session, lens, cardId, asked))
    setQuestion('')
  }

  return (
    <div className="space-y-1 border-t border-violet-100 pt-1">
      <div className="flex gap-1">
        <input value={question} onChange={e => setQuestion(e.target.value)} onKeyDown={e => { if (e.key === 'Enter') ask() }}
          placeholder="Ask about this…" disabled={disabled || asker.running}
          className="flex-1 min-w-0 px-1.5 py-0.5 text-[11px] border border-gray-300 rounded" />
        <button onClick={ask} disabled={disabled || asker.running || question.trim().length < 3}
          className="px-2 py-0.5 text-[11px] rounded border border-violet-500 text-violet-700 hover:bg-violet-50 disabled:border-gray-300 disabled:text-gray-400">
          Ask</button>
      </div>
      {asker.error && <p className="text-red-600">{asker.error}</p>}
      {asker.job && asker.running && <JobProgress job={asker.job} title="Question" onCancel={asker.cancel} />}
      {answers.map(a => (
        <div key={a.id} className="text-[11px]">
          <div className="text-gray-500">Q: {a.question}</div>
          {a.answer ? <div><CitedText text={a.answer} facts={a.facts} />{a.check && !a.check.passed && <span className="ml-1 text-amber-700">(numbers flagged)</span>}</div>
            : <div className="text-red-600">{a.error}</div>}
        </div>
      ))}
    </div>
  )
}
