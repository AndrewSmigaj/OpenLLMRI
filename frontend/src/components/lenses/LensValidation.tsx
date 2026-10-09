// A validated lens's results: held-out scores across the layers at its own k, and the k profile,
// a layers × k grid of one measure, with the lens's k and the held-out best (by AMI, DESIGN.md C3)
// marked. Choosing k by its held-out score is selection-biased; the chart says so. A tuned lens's
// own validation is partly selection-biased too, and says so: its tuning's test score is the honest one.
import { useEffect, useMemo, useState } from 'react'
import type * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { KProfileEntry, KSuggestion, LensSummary, Validation } from '../../types/lens'
import { heldoutBest } from '../../utils/validation'
import { exportElementChart } from '../../utils/exportFigure'
import { useEChart } from '../../hooks/useEChart'
import ExportMenu from '../common/ExportMenu'

const NO_KS: number[] = []

type Measure = { id: string; label: string; read: (e: KProfileEntry) => number | null | undefined }

function measuresFor(validation: Validation, axis: string): Measure[] {
  const agreement = Object.keys(Object.values(Object.values(validation.layers)[0] ?? {})[0]?.agreement ?? {})
  return [
    { id: 'kappa', label: `held-out κ (${axis})`, read: e => e.heldout[axis]?.kappa },
    { id: 'ami', label: `held-out AMI (${axis})`, read: e => e.heldout[axis]?.ami },
    { id: 'silhouette', label: 'silhouette (in-sample)', read: e => e.silhouette },
    { id: 'seed_ari', label: `agreement across ${validation.seeds} seeds (ARI)`, read: e => e.seed_ari },
    ...agreement.map(name => ({ id: `agree:${name}`, label: `agreement with ${name} (AMI, in-sample)`, read: (e: KProfileEntry) => e.agreement[name] })),
  ]
}

export default function LensValidation({ session, lens }: { session: string; lens: LensSummary }) {
  const [validation, setValidation] = useState<Validation | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [axis, setAxis] = useState('label')
  const [measureId, setMeasureId] = useState('ami')
  // The build's in-sample suggestions (elbow, silhouette, hierarchy levels), marked beside the profile
  const [suggestions, setSuggestions] = useState<Record<string, KSuggestion>>({})
  useEffect(() => {
    let current = true
    apiClient.getLens(session, lens.name, false)
      .then(found => { if (current) setSuggestions(found.manifest?.suggestions ?? {}) })
      .catch(() => undefined)
    return () => { current = false }
  }, [session, lens.name])

  useEffect(() => {
    let current = true
    apiClient.getLensValidation(session, lens.name)
      .then(found => { if (current) setValidation(found) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens.name, lens.validation?.created_at])

  const layers = useMemo(() => (validation ? Object.keys(validation.layers).map(Number).sort((a, b) => a - b) : []), [validation])
  const ks = useMemo(() => (validation ? Object.keys(validation.layers[String(layers[0])] ?? {}).map(Number).sort((a, b) => a - b) : []),
    [validation, layers])
  const own = lens.k_per_layer ?? NO_KS
  const measures = useMemo(() => (validation ? measuresFor(validation, axis) : []), [validation, axis])
  const measure = measures.find(m => m.id === measureId) ?? measures[0]
  const best = useMemo(() => (validation ? heldoutBest(validation, axis) : {}), [validation, axis])

  const byLayer = useMemo<echarts.EChartsOption | null>(() => {
    if (!validation) return null
    const at = (li: number) => validation.layers[String(layers[li])]?.[String(own[li])]?.heldout[axis]
    const line = (name: string, read: (s: NonNullable<ReturnType<typeof at>>) => number) =>
      ({ name, type: 'line' as const, data: layers.map((_, li) => { const s = at(li); return s ? read(s) : null }), connectNulls: true })
    return {
      title: { text: `Held out on ${axis}, at this version's k`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { trigger: 'axis' }, legend: { bottom: 0, textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 16, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: -0.2, max: 1, axisLabel: { fontSize: 9 } },
      series: [line('κ', s => s.kappa), line('accuracy', s => s.accuracy), line('worst fold', s => s.worst_fold), line('AMI', s => s.ami)],
      animation: false,
    }
  }, [validation, layers, own, axis])

  const profile = useMemo<echarts.EChartsOption | null>(() => {
    if (!validation || !measure) return null
    const values = layers.flatMap((layer, li) => ks.map((k, ki) => {
      const v = measure.read(validation.layers[String(layer)][String(k)])
      return [li, ki, v === null || v === undefined ? '-' : Number(v.toFixed(3))]
    }))
    const marks = (pick: (layer: number, li: number) => number | undefined) =>
      layers.flatMap((layer, li) => { const k = pick(layer, li); return k === undefined ? [] : [[li, ks.indexOf(k)]] })
    return {
      title: { text: `k profile: ${measure.label}`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { formatter: p => { const v = (p as { value: (number | string)[] }).value; return `L${layers[v[0] as number]}, k ${ks[v[1] as number]}: ${v[2] ?? ''}` } },
      legend: { bottom: 0, textStyle: { fontSize: 10 }, data: ["this version's k", 'held-out best by AMI (selection-biased)',
        'elbow (in-sample)', 'silhouette (in-sample)', 'hierarchy levels (in-sample)'] },
      grid: { left: 40, right: 70, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'category', data: ks.map(k => `k ${k}`), axisLabel: { fontSize: 9 } },
      visualMap: { seriesIndex: 0, min: 0, max: 1, calculable: true, right: 0, top: 'middle', itemHeight: 110,
        inRange: { color: ['#f7fbff', '#6baed6', '#08306b'] }, textStyle: { fontSize: 9 } },
      series: [
        { type: 'heatmap', data: values, progressive: 0 },
        { name: "this version's k", type: 'scatter', data: marks((_, li) => own[li]), symbol: 'rect', symbolSize: 12,
          itemStyle: { color: 'transparent', borderColor: '#111', borderWidth: 1.5 }, z: 3 },
        { name: 'held-out best by AMI (selection-biased)', type: 'scatter', data: marks(layer => best[String(layer)]),
          symbol: 'diamond', symbolSize: 7, itemStyle: { color: '#f59e0b', borderColor: '#111', borderWidth: 0.5 }, z: 4 },
        { name: 'elbow (in-sample)', type: 'scatter', data: marks(layer => suggestions[String(layer)]?.elbow), symbol: 'circle',
          symbolSize: 6, symbolOffset: [-11, 0], itemStyle: { color: '#ffffff', borderColor: '#111', borderWidth: 1 }, z: 5 },
        { name: 'silhouette (in-sample)', type: 'scatter', data: marks(layer => suggestions[String(layer)]?.silhouette),
          symbol: 'triangle', symbolSize: 7, symbolOffset: [11, 0], itemStyle: { color: '#22c55e', borderColor: '#111', borderWidth: 0.5 }, z: 5 },
        { name: 'hierarchy levels (in-sample)', type: 'scatter', symbol: 'rect', symbolSize: [10, 2], symbolOffset: [0, 7],
          itemStyle: { color: '#7c3aed' }, z: 5,
          data: layers.flatMap((layer, li) => (suggestions[String(layer)]?.levels ?? []).filter(k => ks.includes(k)).map(k => [li, ks.indexOf(k)])) },
      ],
      animation: false,
    }
  }, [validation, measure, layers, ks, own, best, suggestions])

  // The fair comparison (label only): the same folds and the same k for every grouping; the
  // relevant neurons use the labels, so they stand beside the ceiling, not the unsupervised ones
  const versus = useMemo<echarts.EChartsOption | null>(() => {
    const comparison = validation?.comparison
    if (!validation || !comparison) return null
    const at = (li: number) => String(own[li])
    const series = (name: string, read: (li: number) => number | undefined, type: 'solid' | 'dashed' | 'dotted' = 'solid') =>
      ({ name, type: 'line' as const, connectNulls: true, lineStyle: { type },
         data: layers.map((_, li) => read(li) ?? null) })
    const raw = (method: 'raw_ward' | 'raw_spectral' | 'neurons') => (li: number) =>
      comparison[String(layers[li])]?.[method]?.[at(li)]?.kappa
    return {
      title: { text: "UMAP against raw space: held-out κ on label at this version's k", left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { trigger: 'axis' }, legend: { bottom: 0, textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 16, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: -0.2, max: 1, axisLabel: { fontSize: 9 } },
      series: [
        series('UMAP lens', li => validation.layers[String(layers[li])]?.[at(li)]?.heldout.label?.kappa),
        series('raw: PCA-50, Ward', raw('raw_ward')),
        series('raw: PCA-50, spectral', raw('raw_spectral')),
        series('relevant neurons (uses labels)', raw('neurons'), 'dashed'),
        series('ceiling: logistic regression', li => comparison[String(layers[li])]?.ceiling?.kappa, 'dotted'),
      ],
      animation: false,
    }
  }, [validation, layers, own])

  const lineBox = useEChart(byLayer)
  const gridBox = useEChart(profile)
  const versusBox = useEChart(versus)
  if (error) return <p className="text-xs text-red-600">{error}</p>
  if (!validation) return <p className="text-xs text-gray-500">Loading the validation…</p>
  const select = 'px-1 py-0.5 text-xs border border-gray-300 rounded bg-white'
  // Each chart exports its picture and its rows, with the lens, the validation and the view in its recipe
  const exporter = (box: { current: HTMLDivElement | null }, option: echarts.EChartsOption | null, figure: string, file: string) => (
    <div className="flex justify-end">
      <ExportMenu formats={['png', 'svg', 'csv', 'json']} disabled={!option}
        onExport={format => exportElementChart(format, box.current, `${session}_${lens.name}_${file}`, {
          figure, lens: { session, name: lens.name, version: lens.current }, axis, measure: measure?.label,
          validation: { folds: validation.folds, created_at: validation.provenance.created_at } }, option)} />
    </div>
  )
  return (
    <div className="space-y-2 pt-2 border-t border-gray-100">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-600">
        <label className="flex items-center gap-1">Axis
          <select value={axis} onChange={e => setAxis(e.target.value)} className={select}>
            {Object.keys(validation.axes).map(a => <option key={a} value={a}>{a}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">Measure
          <select value={measure?.id} onChange={e => setMeasureId(e.target.value)} className={select}>
            {measures.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
          </select>
        </label>
        <span className="text-gray-400">
          {validation.folds.kind}, {validation.folds.n_folds} folds{validation.folds.weaker ? ' (weaker: no scene families)' : ''};
          each held-out item votes by its {validation.vote_neighbours} nearest training items; {validation.provenance.seconds} s
        </span>
      </div>
      {lens.tuning && (
        <p className="text-[11px] text-amber-700">
          This lens was tuned, so its own validation reuses items that chose its settings and is partly
          selection-biased. Its tuning's scores on the test portion, which the search never saw, are the honest ones.
        </p>
      )}
      <div className="grid grid-cols-2 gap-3">
        <div>{exporter(lineBox, byLayer, `held out on ${axis}, at this version's k`, 'heldout')}
          <div ref={lineBox} style={{ height: 260 }} /></div>
        <div>{exporter(gridBox, profile, `k profile: ${measure?.label ?? ''}`, 'k_profile')}
          <div ref={gridBox} style={{ height: 260 }} /></div>
      </div>
      {validation.comparison
        ? <div>{exporter(versusBox, versus, 'UMAP against raw space', 'versus_raw')}
            <div ref={versusBox} style={{ height: 260 }} /></div>
        : <p className="text-[11px] text-gray-400">Validate again to compare with raw space (this validation predates it).</p>}
    </div>
  )
}
