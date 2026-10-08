// The build form. Basic holds what most lenses need: UMAP's neighbours and dimensions, k and a
// name. Advanced holds k chosen per layer by a named method, the grouping, the site and the
// filters. Defaults come from the backend, and the capture's own labels, steps and token
// positions fill the choices. The build runs in the background while the app stays usable.
import { useState } from 'react'
import type { JobView, LensMethods, LensOptions } from '../../types/lens'
import { useBuildJob } from '../../hooks/useBuildJob'

interface LensFormProps {
  session: string
  options: LensOptions
  methods: LensMethods
  takenNames: string[]
  disabled: boolean
  onBuilt: (name: string) => void
}

const NAME = /^[a-z0-9][a-z0-9_-]{0,63}$/
const slug = (text: string) => text.toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+/, '').slice(0, 64)
const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100'
const field = 'flex items-center gap-1.5 text-xs text-gray-700'

function toggle<T>(list: T[], value: T): T[] {
  return list.includes(value) ? list.filter(v => v !== value) : [...list, value]
}

// A build's progress while it runs, and what went wrong if it failed
function JobProgress({ job, onCancel }: { job: JobView; onCancel?: () => void }) {
  const { stage, done, total } = job.progress
  const share = total > 0 ? Math.round((100 * done) / total) : 0
  return (
    <div className="border-t border-gray-200 pt-2 space-y-1">
      <div className="flex items-center gap-2 text-xs">
        <span className="font-medium text-gray-800">Build {job.state}</span>
        {stage && <span className="text-gray-500">{stage} {total > 0 ? `${done}/${total}` : ''}</span>}
        {onCancel && <button onClick={onCancel} className="text-red-600 hover:underline">cancel</button>}
      </div>
      {total > 0 && job.state === 'running' && (
        <div className="h-1.5 bg-gray-200 rounded"><div className="h-1.5 bg-blue-500 rounded" style={{ width: `${share}%` }} /></div>
      )}
      {job.error && <p className="text-xs text-red-600">{job.error}</p>}
      {job.log_tail && <pre className="text-[10px] bg-gray-50 border border-gray-200 rounded p-1 max-h-40 overflow-auto">{job.log_tail}</pre>}
    </div>
  )
}

export default function LensForm({ session, options, methods, takenNames, disabled, onBuilt }: LensFormProps) {
  const umap = methods.reductions[0]?.defaults ?? {}
  const sources = Object.keys(options.sources)
  const [n, setN] = useState(umap.n_neighbors ?? 15)
  const [dims, setDims] = useState(umap.dimensions ?? 6)
  const [k, setK] = useState(methods.defaults.k)
  const [kAuto, setKAuto] = useState('') // '' takes k for every layer
  const [name, setName] = useState('') // '' takes the suggested name
  const [advanced, setAdvanced] = useState(false)
  const [source, setSource] = useState(sources.includes(methods.defaults.source) ? methods.defaults.source : sources[0] ?? '')
  const positions = options.sources[source] ?? [methods.defaults.token_position]
  const [position, setPosition] = useState(positions.includes(methods.defaults.token_position) ? methods.defaults.token_position : positions[0])
  const [labels, setLabels] = useState<string[]>([]) // none ticked keeps every label
  const [steps, setSteps] = useState<number[]>([])
  const [lastOnly, setLastOnly] = useState(methods.defaults.last_occurrence_only)
  const [maxItems, setMaxItems] = useState('')
  const [seed, setSeed] = useState(methods.defaults.seed)
  const build = useBuildJob(job => onBuilt(String(job.params.name)))

  const target = Object.keys(options.target_words)[0] ?? 'lens'
  const finalName = name || slug(`${target}-${kAuto ? `k-${kAuto}` : `k${k}`}-n${n}`)
  const nameProblem = !NAME.test(finalName) ? 'lower-case letters, digits, - and _ only'
    : takenNames.includes(finalName) ? 'a lens of this name exists' : ''
  const tooMany = !maxItems && !steps.length && !labels.length && options.default_items > options.max_items

  const submit = () => build.start({
    session_id: session, name: finalName, n_neighbors: n, dimensions: dims,
    ...(kAuto ? { k_auto: kAuto } : { k }),
    source, token_position: position, seed, created_by: 'app',
    filters: {
      labels: labels.length ? labels : null, steps: steps.length ? steps : null,
      last_occurrence_only: lastOnly, max_items: maxItems ? Number(maxItems) : null,
    },
  })
  const locked = disabled || build.running || build.starting

  return (
    <div className="bg-white border border-gray-200 rounded p-3 space-y-2">
      <div className="flex items-center gap-2">
        <h2 className="text-sm font-semibold text-gray-900 flex-1">Build a lens</h2>
        <span className="text-[11px] text-gray-500">
          {options.default_items} items with the default filters (a lens holds up to {options.max_items.toLocaleString()})
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-4">
        <label className={field} title="UMAP's neighbourhood size: small sees local detail, large sees broad structure">
          Neighbours <input type="number" min={2} max={200} value={n} disabled={locked}
            onChange={e => setN(Number(e.target.value) || 2)} className={`${input} w-14`} />
        </label>
        <label className={field} title="The dimensions UMAP reduces each layer to; the clusters are found there">
          Dimensions <input type="number" min={2} max={50} value={dims} disabled={locked}
            onChange={e => setDims(Number(e.target.value) || 2)} className={`${input} w-14`} />
        </label>
        <label className={field} title="Clusters per layer (Advanced chooses it per layer by a method)">
          k <input type="number" min={1} max={50} value={k} disabled={locked || !!kAuto}
            onChange={e => setK(Number(e.target.value) || 1)} className={`${input} w-14`} />
        </label>
        <label className={field}>
          Name <input value={finalName} disabled={locked} onChange={e => setName(slug(e.target.value))}
            className={`${input} w-56 font-mono`} />
        </label>
        <button onClick={submit} disabled={locked || !!nameProblem || tooMany}
          className="px-3 py-1 text-xs font-medium rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">
          {build.starting ? 'Starting…' : 'Build'}
        </button>
        <button onClick={() => setAdvanced(a => !a)} className="text-xs text-blue-700 hover:underline">
          Advanced {advanced ? '▴' : '▾'}
        </button>
      </div>
      {nameProblem && <p className="text-[11px] text-red-600">Name: {nameProblem}.</p>}
      {tooMany && (
        <p className="text-[11px] text-amber-700">
          Too many items for one lens: set Max items, or choose labels or steps, under Advanced.
        </p>
      )}
      {advanced && (
        <div className="border-t border-gray-200 pt-2 grid grid-cols-2 gap-x-6 gap-y-2">
          <div className="space-y-1.5">
            <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide">k per layer</div>
            <label className={field}>
              <input type="radio" checked={!kAuto} disabled={locked} onChange={() => setKAuto('')} />
              k = {k} at every layer
            </label>
            {methods.k_auto.map(m => (
              <label key={m.id} className={field} title={m.note}>
                <input type="radio" checked={kAuto === m.id} disabled={locked} onChange={() => setKAuto(m.id)} />
                Each layer's k by <span className="font-medium">{m.id}</span>
                <span className="text-gray-400">— {m.note}</span>
              </label>
            ))}
            <p className="text-[10px] text-gray-500">
              After a build, any layer's k can be changed by hand from its suggestions (a new version).
            </p>
            <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide pt-1">Grouping and site</div>
            <p className="text-xs text-gray-700">{methods.groupings.map(g => g.label).join('; ')}</p>
            <div className="flex flex-wrap gap-4">
              <label className={field}>
                Source
                <select value={source} disabled={locked} className={input} onChange={e => {
                  const next = options.sources[e.target.value] ?? []
                  setSource(e.target.value)
                  if (!next.includes(position)) setPosition(next[0])
                }}>
                  {sources.map(s => <option key={s} value={s}>{s.replace('_', ' ')}</option>)}
                </select>
              </label>
              <label className={field}>
                Token position
                <select value={position} disabled={locked} className={input} onChange={e => setPosition(Number(e.target.value))}>
                  {positions.map(p => <option key={p} value={p}>{p}</option>)}
                </select>
              </label>
              <label className={field}>
                Seed <input type="number" value={seed} disabled={locked}
                  onChange={e => setSeed(Number(e.target.value) || 0)} className={`${input} w-16`} />
              </label>
            </div>
          </div>
          <div className="space-y-1.5">
            <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide">Filters</div>
            <div className="flex flex-wrap gap-x-3 gap-y-1">
              <span className="text-xs text-gray-500">Labels</span>
              {Object.entries(options.labels).map(([label, count]) => (
                <label key={label} className={field}>
                  <input type="checkbox" checked={labels.includes(label)} disabled={locked}
                    onChange={() => setLabels(l => toggle(l, label))} />
                  {label} <span className="text-gray-400">({count})</span>
                </label>
              ))}
              <span className="text-[10px] text-gray-400">{labels.length ? '' : 'none ticked keeps all'}</span>
            </div>
            {Object.keys(options.steps).length > 1 && (
              <div className="flex flex-wrap gap-x-3 gap-y-1">
                <span className="text-xs text-gray-500">Steps</span>
                {Object.entries(options.steps).map(([step, count]) => (
                  <label key={step} className={field}>
                    <input type="checkbox" checked={steps.includes(Number(step))} disabled={locked}
                      onChange={() => setSteps(s => toggle(s, Number(step)))} />
                    {step} <span className="text-gray-400">({count})</span>
                  </label>
                ))}
              </div>
            )}
            <label className={field}>
              <input type="checkbox" checked={lastOnly} disabled={locked} onChange={e => setLastOnly(e.target.checked)} />
              Only the last occurrence of the word in each text
            </label>
            <label className={field} title="A larger capture is subsampled to this many items, keeping the label shares">
              Max items <input type="number" min={10} max={options.max_items} value={maxItems} disabled={locked}
                placeholder="all" onChange={e => setMaxItems(e.target.value)} className={`${input} w-20`} />
            </label>
          </div>
        </div>
      )}
      {build.error && <p className="text-xs text-red-600">Could not start the build: {build.error}</p>}
      {build.job && <JobProgress job={build.job} onCancel={build.running ? build.cancel : undefined} />}
    </div>
  )
}
