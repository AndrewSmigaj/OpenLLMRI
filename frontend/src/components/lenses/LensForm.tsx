// The build form. Basic holds what most lenses need: UMAP's neighbours, dimensions, minimum distance
// and distance metric, k and a name. Advanced holds settings per layer (each row saying where its
// settings came from), k per layer by a named method or from that table, the held-out families, the
// grouping, the site and the filters. "Rebuild with…" on a lens card opens the form filled in from
// that lens, and a one-layer preview tries settings in seconds before a build (DESIGN.md E3).
// Defaults come from the backend, and the capture's own labels, steps, layers and categories fields
// fill the choices. The build runs in the background.
import { useState } from 'react'
import { apiClient } from '../../api/client'
import type {
  HoldoutDesign, LensFiltersBody, LensMethods, LensOptions, LensSettings, Metric, SettingsSource, UmapSettings,
} from '../../types/lens'
import JobProgress from './JobProgress'
import LayerPreview from './LayerPreview'
import { useJobRunner } from '../../hooks/useJobRunner'

// A lens to rebuild with other settings: everything the form can carry over from it
export interface LensFormStart {
  from: string
  settings: LensSettings
  k_per_layer: number[] | null
  site: { source: string; token_position: number }
  filters: LensFiltersBody
  holdout: HoldoutDesign | null
}

interface LensFormProps {
  session: string
  options: LensOptions
  methods: LensMethods
  takenNames: string[]
  disabled: boolean
  start?: LensFormStart | null
  onClearStart?: () => void
  onBuilt: (name: string) => void
}

interface Row extends UmapSettings { k: number; source: SettingsSource }

const NAME = /^[a-z0-9][a-z0-9_-]{0,63}$/
const slug = (text: string) => text.toLowerCase().replace(/[^a-z0-9_-]+/g, '-').replace(/^-+/, '').slice(0, 64)
const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100'
const field = 'flex items-center gap-1.5 text-xs text-gray-700'
const heading = 'text-[10px] font-medium text-gray-400 uppercase tracking-wide'
const SOURCE_NOTES: Record<SettingsSource, string> = {
  form: "the form's lens-wide settings",
  table: 'set in this table',
  preview: 'copied from an in-sample preview',
  'preview held out': 'copied from a held-out preview: chosen on held-out scores, so validation is selection-biased',
  tuned: 'chosen by a search on held-out scores: validation is selection-biased; its test score is the honest one',
}

function toggle<T>(list: T[], value: T): T[] {
  return list.includes(value) ? list.filter(v => v !== value) : [...list, value]
}

const settingsOf = (row: UmapSettings): UmapSettings =>
  ({ n_neighbors: row.n_neighbors, dimensions: row.dimensions, min_dist: row.min_dist, metric: row.metric })

// The held-out families a new lens starts with: the capture's declared design, else scene families
// when the items name them, else none (stratified folds, marked weaker)
function defaultHoldout(options: LensOptions, methods: LensMethods): HoldoutDesign {
  if (options.declared_holdout) return { ...methods.holdout, ...options.declared_holdout }
  return { ...methods.holdout, family_field: 'scene' in options.category_fields ? 'scene' : null }
}

export default function LensForm({ session, options, methods, takenNames, disabled, start, onClearStart, onBuilt }: LensFormProps) {
  const base = start?.settings ?? {}
  const sources = Object.keys(options.sources)
  const layers = options.layers.length ? options.layers : Array.from({ length: 24 }, (_, i) => i)
  const uniformK = start?.k_per_layer && new Set(start.k_per_layer).size === 1 ? start.k_per_layer[0] : null
  const [n, setN] = useState(base.n_neighbors ?? methods.defaults.n_neighbors ?? 15)
  const [dims, setDims] = useState(base.dimensions ?? methods.defaults.dimensions ?? 6)
  const [minDist, setMinDist] = useState(base.min_dist ?? methods.defaults.min_dist ?? 0.1)
  const [metric, setMetric] = useState<Metric>(base.metric ?? methods.defaults.metric ?? 'euclidean')
  const [k, setK] = useState(uniformK ?? methods.defaults.k)
  const [kAuto, setKAuto] = useState('') // '' takes k for every layer (or the table's, when kFromTable)
  const [rows, setRows] = useState<Row[] | null>(() => {
    // A rebuilt lens with settings or k that differ by layer opens with its table
    const perLayer = base.per_layer
    const ks = start?.k_per_layer ?? null
    if (!perLayer?.length && (!ks || uniformK !== null)) return null
    return layers.map((_, li) => ({
      ...(perLayer?.[li] ? settingsOf(perLayer[li]) : {
        n_neighbors: base.n_neighbors ?? 15, dimensions: base.dimensions ?? 6,
        min_dist: base.min_dist ?? 0.1, metric: base.metric ?? 'euclidean' }),
      k: ks?.[li] ?? k,
      source: base.sources?.[li] ?? (perLayer?.length ? 'tuned' : 'form'),
    }))
  })
  const [kFromTable, setKFromTable] = useState(rows !== null && start?.k_per_layer != null && uniformK === null)
  const [holdout, setHoldout] = useState<HoldoutDesign>(start?.holdout ?? defaultHoldout(options, methods))
  const [name, setName] = useState('') // '' takes the suggested name
  const [advanced, setAdvanced] = useState(rows !== null)
  const [previewing, setPreviewing] = useState(false)
  const [source, setSource] = useState(start?.site.source
    ?? (sources.includes(methods.defaults.source) ? methods.defaults.source : sources[0] ?? ''))
  const positions = options.sources[source] ?? [methods.defaults.token_position]
  const [position, setPosition] = useState(start?.site.token_position
    ?? (positions.includes(methods.defaults.token_position) ? methods.defaults.token_position : positions[0]))
  const [labels, setLabels] = useState<string[]>(start?.filters.labels ?? []) // none ticked keeps every label
  const [steps, setSteps] = useState<number[]>(start?.filters.steps ?? [])
  const [lastOnly, setLastOnly] = useState(start?.filters.last_occurrence_only ?? methods.defaults.last_occurrence_only)
  const [maxItems, setMaxItems] = useState(start?.filters.max_items ? String(start.filters.max_items) : '')
  const [seed, setSeed] = useState(base.seed ?? methods.defaults.seed)
  const build = useJobRunner(job => onBuilt(String(job.params.name)))

  const target = Object.keys(options.target_words)[0] ?? 'lens'
  const free = (stem: string) => {
    for (let i = 1; ; i++) if (!takenNames.includes(`${stem}-r${i}`)) return `${stem}-r${i}`.slice(0, 64)
  }
  const suggested = start ? free(start.from)
    : slug(`${target}-${kAuto ? `k-${kAuto}` : `k${k}`}-n${n}${metric === 'euclidean' ? '' : `-${metric.slice(0, 3)}`}`
      + `${minDist === 0.1 ? '' : `-md${minDist}`}`)
  const finalName = name || suggested
  const nameProblem = !NAME.test(finalName) ? 'lower-case letters, digits, - and _ only'
    : takenNames.includes(finalName) ? 'a lens of this name exists' : ''
  const tooMany = !maxItems && !steps.length && !labels.length && options.default_items > options.max_items
  const badRow = rows?.findIndex(r => !(r.n_neighbors >= 2 && r.n_neighbors <= 200 && r.dimensions >= 2
    && r.dimensions <= 50 && r.min_dist >= 0 && r.min_dist <= 0.99 && r.k >= 1 && r.k <= 50)) ?? -1

  // Basic's values reach the table's rows that still hold the form's settings
  const setBasic = (change: Partial<UmapSettings>) => {
    if (change.n_neighbors !== undefined) setN(change.n_neighbors)
    if (change.dimensions !== undefined) setDims(change.dimensions)
    if (change.min_dist !== undefined) setMinDist(change.min_dist)
    if (change.metric !== undefined) setMetric(change.metric)
    setRows(current => current?.map(r => (r.source === 'form' ? { ...r, ...change } : r)) ?? null)
  }
  // A row's own settings make it the table's; its k is not a UMAP setting and leaves the source alone
  const editRow = (li: number, change: Partial<Row>) =>
    setRows(current => current?.map((r, i) => (i !== li ? r
      : { ...r, ...change, source: 'k' in change ? r.source : 'table' })) ?? null)
  const setTable = (on: boolean) => {
    setRows(on ? layers.map(() => ({ n_neighbors: n, dimensions: dims, min_dist: minDist, metric, k, source: 'form' })) : null)
    if (!on) setKFromTable(false)
  }

  // A preview's settings and k fill its layer's row, marked as from a preview (held out or not)
  const usePreview = (li: number, values: UmapSettings & { k: number }, heldOut: boolean) => {
    const from: SettingsSource = heldOut ? 'preview held out' : 'preview'
    setRows(current => (current ?? layers.map(() => ({ n_neighbors: n, dimensions: dims, min_dist: minDist, metric, k, source: 'form' as const })))
      .map((r, i) => (i === li ? { ...settingsOf(values), k: values.k, source: from } : r)))
    if (values.k !== (rows?.[li]?.k ?? k)) { setKAuto(''); setKFromTable(true) }
    setAdvanced(true)
  }

  const filters: LensFiltersBody = {
    labels: labels.length ? labels : null, steps: steps.length ? steps : null,
    last_occurrence_only: lastOnly, max_items: maxItems ? Number(maxItems) : null,
  }
  const submit = () => build.start(() => apiClient.buildLens({
    session_id: session, name: finalName, n_neighbors: n, dimensions: dims, min_dist: minDist, metric,
    ...(rows ? { per_layer: rows.map(settingsOf), sources: rows.map(r => r.source) } : {}),
    ...(kAuto ? { k_auto: kAuto } : kFromTable && rows ? { k_per_layer: rows.map(r => r.k) } : { k }),
    holdout, source, token_position: position, seed, created_by: 'app', filters,
  }))
  const locked = disabled || build.running || build.starting

  return (
    <div className="bg-white border border-gray-200 rounded p-3 space-y-2">
      <div className="flex items-center gap-2">
        <h2 className="text-sm font-semibold text-gray-900 flex-1">
          {start ? <>Rebuild <span className="font-mono">{start.from}</span> with other settings</> : 'Build a lens'}
        </h2>
        {start && onClearStart && (
          <button onClick={onClearStart} className="text-xs text-blue-700 hover:underline">a new lens instead</button>
        )}
        <span className="text-[11px] text-gray-500">
          {options.default_items} items with the default filters (a lens holds up to {options.max_items.toLocaleString()})
        </span>
      </div>
      <div className="flex flex-wrap items-center gap-4">
        <label className={field} title="UMAP's neighbourhood size: small sees local detail, large sees broad structure">
          Neighbours <input type="number" min={2} max={200} value={n} disabled={locked}
            onChange={e => setBasic({ n_neighbors: Number(e.target.value) || 2 })} className={`${input} w-14`} />
        </label>
        <label className={field} title="The dimensions UMAP reduces each layer to; the clusters are found there">
          Dimensions <input type="number" min={2} max={50} value={dims} disabled={locked}
            onChange={e => setBasic({ dimensions: Number(e.target.value) || 2 })} className={`${input} w-14`} />
        </label>
        <label className={field} title="How tightly UMAP may pack points: 0 packs clusters tight, larger values spread them">
          Min distance <input type="number" min={0} max={0.99} step={0.05} value={minDist} disabled={locked}
            onChange={e => setBasic({ min_dist: Math.min(0.99, Math.max(0, Number(e.target.value) || 0)) })}
            className={`${input} w-16`} />
        </label>
        <label className={field} title="How UMAP measures distance between states before it finds neighbours">
          Metric
          <select value={metric} disabled={locked} className={input}
            onChange={e => setBasic({ metric: e.target.value as Metric })}>
            {methods.metrics.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </label>
        <label className={field} title="Clusters per layer (Advanced chooses it per layer by a method or from the table)">
          k <input type="number" min={1} max={50} value={k} disabled={locked || !!kAuto || kFromTable}
            onChange={e => setK(Number(e.target.value) || 1)} className={`${input} w-14`} />
        </label>
        <label className={field}>
          Name <input value={finalName} disabled={locked} onChange={e => setName(slug(e.target.value))}
            className={`${input} w-56 font-mono`} />
        </label>
        <button onClick={submit} disabled={locked || !!nameProblem || tooMany || badRow >= 0}
          className="px-3 py-1 text-xs font-medium rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">
          {build.starting ? 'Starting…' : 'Build'}
        </button>
        <button onClick={() => setAdvanced(a => !a)} className="text-xs text-blue-700 hover:underline">
          Advanced {advanced ? '▴' : '▾'}
        </button>
        <button onClick={() => setPreviewing(p => !p)} className="text-xs text-blue-700 hover:underline"
          title="Fit one layer with these settings in seconds: its clusters in 3-D and how well they match each axis">
          Preview a layer {previewing ? '▴' : '▾'}
        </button>
      </div>
      {previewing && (
        <LayerPreview layers={layers} metrics={methods.metrics} disabled={locked} onUse={usePreview}
          initial={li => (rows ? { ...settingsOf(rows[li]), k: rows[li].k }
            : { n_neighbors: n, dimensions: dims, min_dist: minDist, metric, k })}
          base={{ session_id: session, seed, source, token_position: position, filters, holdout }} />
      )}
      {nameProblem && <p className="text-[11px] text-red-600">Name: {nameProblem}.</p>}
      {tooMany && (
        <p className="text-[11px] text-amber-700">
          Too many items for one lens: set Max items, or choose labels or steps, under Advanced.
        </p>
      )}
      {badRow >= 0 && (
        <p className="text-[11px] text-red-600">
          Layer {layers[badRow]}'s row is out of range (neighbours 2–200, dimensions 2–50, min distance 0–0.99, k 1–50).
        </p>
      )}
      {advanced && (
        <div className="border-t border-gray-200 pt-2 space-y-3">
          <div className="grid grid-cols-2 gap-x-6 gap-y-2">
            <div className="space-y-1.5">
              <div className={heading}>k per layer</div>
              <label className={field}>
                <input type="radio" checked={!kAuto && !kFromTable} disabled={locked}
                  onChange={() => { setKAuto(''); setKFromTable(false) }} />
                k = {k} at every layer
              </label>
              {methods.k_auto.map(m => (
                <label key={m.id} className={field} title={m.note}>
                  <input type="radio" checked={kAuto === m.id} disabled={locked}
                    onChange={() => { setKAuto(m.id); setKFromTable(false) }} />
                  Each layer's k by <span className="font-medium">{m.id}</span>
                  <span className="text-gray-400">— {m.note}</span>
                </label>
              ))}
              <label className={field} title="Each layer's k as the settings table below gives it">
                <input type="radio" checked={kFromTable} disabled={locked}
                  onChange={() => { if (!rows) setTable(true); setKAuto(''); setKFromTable(true) }} />
                Each layer's k from the table below
              </label>
              <p className="text-[10px] text-gray-500">
                After a build, any layer's k can be changed by hand from its suggestions (a new version).
              </p>
              <div className={`${heading} pt-1`}>Grouping and site</div>
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
              <div className={heading}>Filters</div>
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
              <div className={`${heading} pt-1`}>Held-out families</div>
              <div className="flex flex-wrap items-center gap-3">
                <label className={field} title="Validation, tuning, routes and the axes analysis hold out whole families named by this field">
                  Families
                  <select value={holdout.family_field ?? ''} disabled={locked} className={input}
                    onChange={e => setHoldout(h => ({ ...h, family_field: e.target.value || null }))}>
                    <option value="">none (stratified folds, weaker)</option>
                    {Object.entries(options.category_fields).map(([key, count]) => (
                      <option key={key} value={key}>{key} ({count} values)</option>
                    ))}
                  </select>
                </label>
                <label className={field} title="Keep family names whole, not just their first two underscore parts">
                  <input type="checkbox" checked={holdout.whole_families} disabled={locked}
                    onChange={e => setHoldout(h => ({ ...h, whole_families: e.target.checked }))} />
                  whole names
                </label>
                <label className={field} title="More family folds than this merge round-robin, each still holding out whole families">
                  Fold cap <input type="number" min={2} max={50} value={holdout.max_folds ?? ''} placeholder="none"
                    disabled={locked} className={`${input} w-14`}
                    onChange={e => setHoldout(h => ({ ...h, max_folds: e.target.value ? Number(e.target.value) : null }))} />
                </label>
              </div>
              <p className="text-[10px] text-gray-500">
                {options.declared_holdout
                  ? `The capture's set declares ${options.declared_holdout.family_field ?? 'no families'}${options.declared_holdout.whole_families ? ', names whole' : ''}. `
                  : ''}
                The lens keeps this design, and its later jobs use it.
              </p>
            </div>
          </div>
          <div className="space-y-1">
            <label className={`${field} font-medium`}>
              <input type="checkbox" checked={rows !== null} disabled={locked} onChange={e => setTable(e.target.checked)} />
              Settings per layer
            </label>
            {rows && (
              <div className="overflow-x-auto">
                <table className="text-[11px] text-gray-700">
                  <thead>
                    <tr className="text-gray-400">
                      <th className="text-left font-normal pr-2">layer</th>
                      <th className="text-left font-normal pr-2">neighbours</th>
                      <th className="text-left font-normal pr-2">dimensions</th>
                      <th className="text-left font-normal pr-2">min dist</th>
                      <th className="text-left font-normal pr-2">metric</th>
                      <th className="text-left font-normal pr-2">k</th>
                      <th className="text-left font-normal">from</th>
                    </tr>
                  </thead>
                  <tbody>
                    {rows.map((row, li) => (
                      <tr key={layers[li]}>
                        <td className="pr-2 font-mono">L{layers[li]}</td>
                        <td className="pr-2"><input type="number" min={2} max={200} value={row.n_neighbors} disabled={locked}
                          onChange={e => editRow(li, { n_neighbors: Number(e.target.value) || 2 })} className={`${input} w-14`} /></td>
                        <td className="pr-2"><input type="number" min={2} max={50} value={row.dimensions} disabled={locked}
                          onChange={e => editRow(li, { dimensions: Number(e.target.value) || 2 })} className={`${input} w-14`} /></td>
                        <td className="pr-2"><input type="number" min={0} max={0.99} step={0.05} value={row.min_dist} disabled={locked}
                          onChange={e => editRow(li, { min_dist: Math.min(0.99, Math.max(0, Number(e.target.value) || 0)) })}
                          className={`${input} w-16`} /></td>
                        <td className="pr-2">
                          <select value={row.metric} disabled={locked} className={input}
                            onChange={e => editRow(li, { metric: e.target.value as Metric })}>
                            {methods.metrics.map(m => <option key={m} value={m}>{m}</option>)}
                          </select>
                        </td>
                        <td className="pr-2"><input type={kAuto ? 'text' : 'number'} min={1} max={50}
                          value={kFromTable ? row.k : kAuto ? kAuto : k} disabled={locked || !kFromTable}
                          title={kFromTable ? '' : 'Choose "Each layer\'s k from the table" to set it here'}
                          onChange={e => editRow(li, { k: Number(e.target.value) || 1 })} className={`${input} w-16`} /></td>
                        <td className="text-gray-500" title={SOURCE_NOTES[row.source]}>{row.source}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      )}
      {build.error && <p className="text-xs text-red-600">Could not start the build: {build.error}</p>}
      {build.job && <JobProgress job={build.job} title="Build" onCancel={build.running ? build.cancel : undefined} />}
    </div>
  )
}
