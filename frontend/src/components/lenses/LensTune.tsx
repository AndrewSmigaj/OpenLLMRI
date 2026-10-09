// Tuning a UMAP lens (DESIGN.md C3, C4): a search over UMAP's settings and k, layer by layer, chosen
// by held-out AMI on selection folds and scored on a test portion the search never sees; then the
// tuned lens is built and validated. Basic asks for the axis to tune for and a name; Advanced holds
// the grid (metrics too), the k range, the test share, the folds, the family field and the seed,
// starting from the lens's own hold-out design and metric. The estimate is the search alone:
// building and validating the tuned lens add a few minutes.
import { useEffect, useState } from 'react'
import { apiClient } from '../../api/client'
import type { LensMethods, LensSummary, Metric, TuneBody } from '../../types/lens'
import { useJobRunner } from '../../hooks/useJobRunner'
import JobProgress from './JobProgress'

interface LensTuneProps {
  session: string
  lens: LensSummary
  methods: LensMethods
  takenNames: string[]
  disabled: boolean
  onTuned: (name: string) => void
}

const NAME = /^[a-z0-9][a-z0-9_-]{0,63}$/
const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100'
const listOf = (text: string) => text.split(/[\s,]+/).filter(Boolean).map(Number).filter(Number.isFinite)
const wordsOf = (text: string) => text.split(/[\s,]+/).filter(Boolean)
const joined = (values: number[]) => values.join(', ')

export default function LensTune({ session, lens, methods, takenNames, disabled, onTuned }: LensTuneProps) {
  const defaults = methods.tuning
  const [axes, setAxes] = useState<Record<string, string[]>>({})
  const [axis, setAxis] = useState('label')
  const [name, setName] = useState(`${lens.name}-tuned`.slice(0, 64))
  const [advanced, setAdvanced] = useState(false)
  const [neighbours, setNeighbours] = useState(joined(defaults?.grid.n_neighbors ?? [5, 15, 50]))
  const [dimensions, setDimensions] = useState(joined(defaults?.grid.dimensions ?? [3, 6, 12]))
  const [minDist, setMinDist] = useState(joined(defaults?.grid.min_dist ?? [0.1]))
  const [metrics, setMetrics] = useState<string>(lens.settings.metric ?? 'euclidean')
  const [kMin, setKMin] = useState(defaults?.k_min ?? 2)
  const [kMax, setKMax] = useState(defaults?.k_max ?? 10)
  const [share, setShare] = useState(lens.holdout?.test_share ?? defaults?.test_share ?? 0.2)
  const [folds, setFolds] = useState(defaults?.n_folds ?? 5)
  const [family, setFamily] = useState(lens.holdout?.family_field ?? '') // '' holds out no families
  const [seed, setSeed] = useState('')
  const tune = useJobRunner(() => onTuned(name))

  useEffect(() => {
    let current = true
    apiClient.getLens(session, lens.name, false)
      .then(found => { if (current) setAxes(found.axes) })
      .catch(() => undefined)
    return () => { current = false }
  }, [session, lens.name])

  const metricList = wordsOf(metrics) as Metric[]
  const grid = { n_neighbors: listOf(neighbours), dimensions: listOf(dimensions), min_dist: listOf(minDist), metric: metricList }
  const settings = grid.n_neighbors.length * grid.dimensions.length * grid.min_dist.length * metricList.length
  const layers = lens.k_per_layer?.length ?? 24
  const items = lens.n_items ?? 0
  const [perItem, perFit] = defaults?.seconds_per_fit ?? [0.005, 0.25]
  const train = items * (1 - share) * (1 - 1 / folds)
  const minutes = Math.max(1, Math.round((settings * layers * folds * (perItem * train + perFit)) / (defaults?.workers ?? 6) / 60))
  const tunable = Object.entries(axes).filter(([, values]) => values.length >= 2).map(([id]) => id)
  const problem = !NAME.test(name) ? 'the name takes lower-case letters, digits, - and _ only'
    : takenNames.includes(name) ? 'a lens of this name exists'
    : metricList.some(m => !methods.metrics.includes(m)) ? `metrics are ${methods.metrics.join(', ')}`
    : settings === 0 ? 'the grid is empty'
    : settings > (defaults?.max_settings ?? 60) ? `the grid has ${settings} settings; at most ${defaults?.max_settings ?? 60}`
    : kMin > kMax ? 'the smallest k is above the largest' : ''
  const locked = disabled || tune.running || tune.starting

  const body: TuneBody = {
    name, target_axis: axis, grid, k_min: kMin, k_max: kMax, test_share: share, n_folds: folds,
    family_field: family, seed: seed === '' ? null : Number(seed), created_by: 'app',
  }
  return (
    <div className="mt-2 pt-2 border-t border-gray-100 space-y-2">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-700">
        <span className="font-medium text-gray-900">Tune this lens</span>
        <label className="flex items-center gap-1" title="The designed axis the search matches its nodes to (held-out AMI)">Axis
          <select value={axis} onChange={e => setAxis(e.target.value)} disabled={locked} className={input}>
            {(tunable.length ? tunable : ['label']).map(a => <option key={a} value={a}>{a}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">Name
          <input value={name} onChange={e => setName(e.target.value)} disabled={locked} className={`${input} w-56 font-mono`} />
        </label>
        <button onClick={() => setAdvanced(a => !a)} className="text-blue-700 hover:underline">
          Advanced {advanced ? '▴' : '▾'}
        </button>
        <button disabled={locked || !!problem} onClick={() => tune.start(() => apiClient.tuneLens(session, lens.name, body))}
          className="px-3 py-1 text-xs font-medium rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">
          {tune.starting ? 'Starting…' : 'Tune'}
        </button>
        <span className="text-gray-400">
          {settings} settings × {layers} layers × {folds} folds: about {minutes} min to search, then the tuned lens is built and validated
        </span>
      </div>
      {advanced && (
        <div className="flex flex-wrap items-center gap-3 text-xs text-gray-700">
          <label className="flex items-center gap-1" title="UMAP's neighbourhood sizes to try">Neighbours
            <input value={neighbours} onChange={e => setNeighbours(e.target.value)} disabled={locked} className={`${input} w-28`} />
          </label>
          <label className="flex items-center gap-1" title="The dimensions UMAP reduces each layer to">Dimensions
            <input value={dimensions} onChange={e => setDimensions(e.target.value)} disabled={locked} className={`${input} w-24`} />
          </label>
          <label className="flex items-center gap-1" title="How tightly UMAP may pack points (0 to 0.99)">Min. distance
            <input value={minDist} onChange={e => setMinDist(e.target.value)} disabled={locked} className={`${input} w-20`} />
          </label>
          <label className="flex items-center gap-1" title={`Distance metrics to try: ${methods.metrics.join(', ')}`}>Metrics
            <input value={metrics} onChange={e => setMetrics(e.target.value)} disabled={locked} className={`${input} w-36`} />
          </label>
          <label className="flex items-center gap-1">k from
            <input type="number" min={2} max={10} value={kMin} onChange={e => setKMin(Number(e.target.value))} disabled={locked} className={`${input} w-12`} />
            to
            <input type="number" min={2} max={10} value={kMax} onChange={e => setKMax(Number(e.target.value))} disabled={locked} className={`${input} w-12`} />
          </label>
          <label className="flex items-center gap-1" title="The share held out for the honest test score">Test share
            <input type="number" min={0.1} max={0.5} step={0.05} value={share} onChange={e => setShare(Number(e.target.value))} disabled={locked} className={`${input} w-16`} />
          </label>
          <label className="flex items-center gap-1" title="Selection folds over the rest">Folds
            <input type="number" min={2} max={10} value={folds} onChange={e => setFolds(Number(e.target.value))} disabled={locked} className={`${input} w-12`} />
          </label>
          <label className="flex items-center gap-1" title="The categories field naming each item's family (the lens's own to start); empty: no families, so the split is stratified and weaker">Family field
            <input value={family} onChange={e => setFamily(e.target.value)} disabled={locked} placeholder="none" className={`${input} w-24 font-mono`} />
          </label>
          <label className="flex items-center gap-1" title="Empty: the lens's own seed">Seed
            <input value={seed} onChange={e => setSeed(e.target.value.replace(/[^0-9]/g, ''))} disabled={locked} className={`${input} w-16`} />
          </label>
        </div>
      )}
      {problem && <p className="text-[11px] text-red-600">{problem}.</p>}
      {tune.error && <p className="text-xs text-red-600">{tune.error}</p>}
      {tune.job && <JobProgress job={tune.job} title="Tuning" onCancel={tune.running ? tune.cancel : undefined} />}
    </div>
  )
}
