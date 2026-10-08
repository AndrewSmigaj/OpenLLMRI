// A validated lens's results: held-out scores across the layers at its own k, and the k profile,
// a layers × k grid of one measure, with the lens's k and the held-out best marked. Choosing k by
// its held-out score is selection-biased; the chart says so.
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { KProfileEntry, LensSummary, Validation } from '../../types/lens'
import { heldoutBest } from '../../utils/validation'

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

function useChart(option: echarts.EChartsOption | null) {
  const box = useRef<HTMLDivElement>(null)
  const chart = useRef<echarts.ECharts | null>(null)
  useEffect(() => {
    if (!box.current || !option) return
    chart.current ??= echarts.init(box.current)
    chart.current.setOption(option, true)
  }, [option])
  useEffect(() => () => { chart.current?.dispose(); chart.current = null }, [])
  return box
}

export default function LensValidation({ session, lens }: { session: string; lens: LensSummary }) {
  const [validation, setValidation] = useState<Validation | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [axis, setAxis] = useState('label')
  const [measureId, setMeasureId] = useState('kappa')

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
      legend: { bottom: 0, textStyle: { fontSize: 10 }, data: ["this version's k", 'held-out best (selection-biased)'] },
      grid: { left: 40, right: 70, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'category', data: ks.map(k => `k ${k}`), axisLabel: { fontSize: 9 } },
      visualMap: { seriesIndex: 0, min: 0, max: 1, calculable: true, right: 0, top: 'middle', itemHeight: 110,
        inRange: { color: ['#f7fbff', '#6baed6', '#08306b'] }, textStyle: { fontSize: 9 } },
      series: [
        { type: 'heatmap', data: values, progressive: 0 },
        { name: "this version's k", type: 'scatter', data: marks((_, li) => own[li]), symbol: 'rect', symbolSize: 12,
          itemStyle: { color: 'transparent', borderColor: '#111', borderWidth: 1.5 }, z: 3 },
        { name: 'held-out best (selection-biased)', type: 'scatter', data: marks(layer => best[String(layer)]),
          symbol: 'diamond', symbolSize: 7, itemStyle: { color: '#f59e0b', borderColor: '#111', borderWidth: 0.5 }, z: 4 },
      ],
      animation: false,
    }
  }, [validation, measure, layers, ks, own, best])

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

  const lineBox = useChart(byLayer)
  const gridBox = useChart(profile)
  const versusBox = useChart(versus)
  if (error) return <p className="text-xs text-red-600">{error}</p>
  if (!validation) return <p className="text-xs text-gray-500">Loading the validation…</p>
  const select = 'px-1 py-0.5 text-xs border border-gray-300 rounded bg-white'
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
      <div className="grid grid-cols-2 gap-3">
        <div ref={lineBox} style={{ height: 260 }} />
        <div ref={gridBox} style={{ height: 260 }} />
      </div>
      {validation.comparison
        ? <div ref={versusBox} style={{ height: 260 }} />
        : <p className="text-[11px] text-gray-400">Validate again to compare with raw space (this validation predates it).</p>}
    </div>
  )
}
