// A mass-mean lens: one designed contrast, label A against label B, an axis at every layer. Its
// readings are positions along the contrast (A's mean at -1, B's at +1); it is validated on
// held-out scene families as it is built.
import { useState } from 'react'
import { apiClient } from '../../api/client'
import type { LensOptions } from '../../types/lens'
import { useJobRunner } from '../../hooks/useJobRunner'
import JobProgress from './JobProgress'

interface MassMeanFormProps {
  session: string
  options: LensOptions
  takenNames: string[]
  disabled: boolean
  onBuilt: () => void
}

const NAME = /^[a-z0-9][a-z0-9_-]{0,63}$/
const slug = (text: string) => text.toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+/, '').slice(0, 64)
const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100'

export default function MassMeanForm({ session, options, takenNames, disabled, onBuilt }: MassMeanFormProps) {
  const labels = Object.keys(options.labels)
  const positions = options.sources.residual_stream ?? [1]
  const [a, setA] = useState(labels[0] ?? '')
  const [b, setB] = useState(labels[1] ?? '')
  const [position, setPosition] = useState(positions.includes(1) ? 1 : positions[0])
  const [name, setName] = useState('')
  const build = useJobRunner(() => onBuilt())
  const finalName = name || slug(`${a}-vs-${b}-axis-p${position}`)
  const problem = a === b ? 'choose two different labels' : !NAME.test(finalName) ? 'lower-case letters, digits, - and _ only'
    : takenNames.includes(finalName) ? 'a lens of this name exists' : ''
  const locked = disabled || build.running || build.starting

  if (labels.length < 2) return null
  return (
    <div className="bg-white border border-gray-200 rounded p-3 space-y-2">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-700">
        <span className="text-sm font-semibold text-gray-900">Mass-mean lens</span>
        <label className="flex items-center gap-1">A (−1)
          <select value={a} onChange={e => setA(e.target.value)} disabled={locked} className={input}>
            {labels.map(l => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">B (+1)
          <select value={b} onChange={e => setB(e.target.value)} disabled={locked} className={input}>
            {labels.map(l => <option key={l} value={l}>{l}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">Token position
          <select value={position} onChange={e => setPosition(Number(e.target.value))} disabled={locked} className={input}>
            {positions.map(pos => <option key={pos} value={pos}>{pos}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">Name
          <input value={finalName} onChange={e => setName(slug(e.target.value))} disabled={locked} className={`${input} w-56 font-mono`} />
        </label>
        <button disabled={locked || !!problem}
          onClick={() => build.start(() => apiClient.buildMassMean({ session_id: session, name: finalName, label_a: a,
            label_b: b, token_position: position, created_by: 'app' }))}
          className="px-3 py-1 text-xs font-medium rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">
          {build.starting ? 'Starting…' : 'Build'}
        </button>
        <span className="text-gray-400">one axis per layer: B's mean minus A's; validated on held-out scenes as it is built</span>
      </div>
      {problem && a !== b && <p className="text-[11px] text-red-600">Name: {problem}.</p>}
      {build.error && <p className="text-xs text-red-600">{build.error}</p>}
      {build.job && <JobProgress job={build.job} title="Build" onCancel={build.running ? build.cancel : undefined} />}
    </div>
  )
}
