// An LLM card's marks and text (DESIGN.md E8): who wrote it and how it was checked, then its
// title, pattern, summary, findings, caveats and, for a reconciled report, where its drafts differed.
import type { Card, CardOutput, Fact } from '../../types/cards'
import CitedText from './CitedText'

const chip = (tone: 'good' | 'warn' | 'plain') => `text-[9px] rounded px-1 py-px border ${
  tone === 'good' ? 'bg-green-50 text-green-800 border-green-300'
    : tone === 'warn' ? 'bg-amber-50 text-amber-800 border-amber-300' : 'bg-white text-gray-600 border-gray-300'}`

export function CardMarks({ card }: { card: Card }) {
  const byClaudeCode = card.written_by === 'Claude Code'
  return (
    <span className="inline-flex flex-wrap gap-1" title={`${card.model} · ${card.created_at.slice(0, 16).replace('T', ' ')} · ${card.calls} call(s)`}>
      <span className={chip('plain')}>LLM-written</span>
      <span className={chip('plain')}>{byClaudeCode ? 'written in Claude Code' : card.analysts === 2 ? 'two analysts, reconciled' : 'one analyst'}</span>
      {!byClaudeCode && <span className={chip(card.tested ? 'good' : 'warn')}>{card.tested ? 'tested analyst' : 'untested analyst'}</span>}
      {card.check && <span className={chip(card.check.passed ? 'good' : 'warn')}>
        {card.check.passed ? `numbers checked (${card.check.numerals})` : 'numbers flagged'}</span>}
      {card.stale && <span className={chip('warn')} title="Its evidence has changed since it was written">out of date</span>}
    </span>
  )
}

const tone = { clear: 'text-green-800 bg-green-50', weak: 'text-amber-800 bg-amber-50', none: 'text-gray-600 bg-gray-100' }

export function CardText({ output, facts }: { output: CardOutput; facts: Record<string, Fact> }) {
  const list = (items: string[], marker: string, colour: string) => (
    <ul className="space-y-0.5">
      {items.map((item, i) => <li key={i} className={`pl-3 -indent-3 ${colour}`}>{marker} <CitedText text={item} facts={facts} /></li>)}
    </ul>
  )
  return (
    <div className="space-y-1">
      <div className="flex items-baseline gap-1.5">
        <span className="font-semibold text-gray-900">{output.title}</span>
        <span className={`text-[9px] rounded px-1 ${tone[output.pattern]}`}>{output.pattern === 'none' ? 'no clear pattern' : `${output.pattern} pattern`}</span>
      </div>
      <p><CitedText text={output.summary} facts={facts} /></p>
      {output.points.length > 0 && list(output.points, '•', 'text-gray-800')}
      {output.caveats.length > 0 && list(output.caveats, '!', 'text-amber-800')}
      {output.disagreements && output.disagreements.length > 0 && (
        <div><div className="text-[10px] text-gray-500">where the two drafts differed</div>
          {list(output.disagreements, '≠', 'text-gray-700')}</div>
      )}
    </div>
  )
}
