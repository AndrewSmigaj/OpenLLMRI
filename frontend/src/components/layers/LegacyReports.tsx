// The reports /analyze wrote for a legacy schema, one per transition (w_17_18) and one per
// six-layer window (w_17_23). The picker lists the keys that exist, so none is missed, and starts
// on the window holding the first layer in view. (10b.10's analysis panel replaces these.)
import { useMemo, useState } from 'react'
import ReactMarkdown from 'react-markdown'

const span = (key: string) => {
  const m = /^w_(\d+)_(\d+)$/.exec(key)
  return m ? { start: Number(m[1]), end: Number(m[2]) } : null
}

const labelOf = (key: string) => {
  const s = span(key)
  if (!s) return key
  return s.end - s.start === 1 ? `Layers ${s.start}→${s.end}` : `Layers ${s.start}–${s.end} (window)`
}

export default function LegacyReports({ reports, layer }: { reports: Record<string, string>; layer: number }) {
  const keys = useMemo(() => Object.keys(reports).sort((a, b) => {
    const x = span(a), y = span(b)
    return x && y ? (x.start - y.start) || (y.end - y.start) - (x.end - x.start) : a.localeCompare(b)
  }), [reports])
  const windowWhere = (inside: (s: { start: number; end: number }) => boolean) =>
    keys.find(k => { const s = span(k); return !!s && s.end - s.start > 1 && inside(s) })
  const preferred = windowWhere(s => s.start <= layer && layer < s.end) ?? windowWhere(s => s.end === layer)
    ?? keys.find(k => span(k)?.start === layer) ?? keys[0]
  const [picked, setPicked] = useState<string | null>(null)
  const shown = picked && reports[picked] ? picked : preferred

  if (keys.length === 0) return null
  return (
    <div className="border-t border-gray-200 pt-2 mt-2">
      <div className="flex items-center gap-2 mb-1">
        <span className="text-[10px] font-semibold text-gray-600">Report (written by /analyze)</span>
        <select value={shown} onChange={e => setPicked(e.target.value)}
          className="px-1 py-0.5 text-[10px] border border-gray-300 rounded bg-white">
          {keys.map(k => <option key={k} value={k}>{labelOf(k)}</option>)}
        </select>
      </div>
      <div className="prose prose-sm max-w-none text-[10px] text-gray-700">
        <ReactMarkdown>{reports[shown]}</ReactMarkdown>
      </div>
    </div>
  )
}
