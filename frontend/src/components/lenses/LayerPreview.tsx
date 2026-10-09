// A one-layer preview (DESIGN.md E3): pick a layer, set its settings and k, and see in seconds the
// layer's clusters in 3-D, coloured by node or by any designed axis, with how well they match each
// axis, before building every layer. Held out on request. Its scores leave out the test portion a
// later tune would hold out, so the tune's test score stays honest. "Use for this layer" copies the
// settings, and k, into the form's per-layer table.
import { useMemo, useState } from 'react'
import type * as echarts from 'echarts'
import 'echarts-gl'
import { apiClient } from '../../api/client'
import type { LayerPreview as Preview, Metric, PreviewBody, UmapSettings } from '../../types/lens'
import { paletteColor } from '../../color/scheme'
import { useEChart } from '../../hooks/useEChart'
import { useJobRunner } from '../../hooks/useJobRunner'
import JobProgress from './JobProgress'

type Values = UmapSettings & { k: number }

interface LayerPreviewProps {
  layers: number[]
  metrics: Metric[]
  initial: (li: number) => Values // the form's current settings and k for a layer
  base: Omit<PreviewBody, 'layer' | 'settings' | 'k' | 'held_out' | 'created_by'> // capture, site, filters, seed, held-out families
  disabled: boolean
  onUse: (li: number, values: Values, heldOut: boolean) => void
}

const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100'
const field = 'flex items-center gap-1.5 text-xs text-gray-700'
const fixed = (x: number | undefined, digits = 2) => (x === undefined ? '–' : x.toFixed(digits))

export default function LayerPreview({ layers, metrics, initial, base, disabled, onUse }: LayerPreviewProps) {
  const [li, setLi] = useState(() => Math.floor(layers.length / 2))
  const [values, setValues] = useState<Values>(() => initial(Math.floor(layers.length / 2)))
  const [colourBy, setColourBy] = useState('node')
  const [result, setResult] = useState<Preview | null>(null)
  const [problem, setProblem] = useState<string | null>(null)
  const runner = useJobRunner(job => {
    apiClient.getPreview(job.id).then(setResult).catch(err => setProblem(err instanceof Error ? err.message : String(err)))
  })
  const busy = runner.running || runner.starting
  const set = (change: Partial<Values>) => setValues(v => ({ ...v, ...change }))
  const chooseLayer = (next: number) => { setLi(next); setValues(initial(next)) }

  const run = async (heldOut: boolean) => {
    setProblem(null)
    if (runner.running) await runner.cancel() // the newest settings win
    const { k, ...settings } = values
    runner.start(() => apiClient.previewLayer({ ...base, layer: layers[li], settings, k, held_out: heldOut, created_by: 'app' }))
  }

  const option = useMemo((): echarts.EChartsOption | null => {
    if (!result) return null
    const of = (j: number) => (colourBy === 'node' ? String(result.nodes[j])
      : colourBy === 'label' ? String(result.items[j].label) : result.items[j].categories[colourBy] ?? '')
    const distinct = colourBy === 'node' ? [...new Set(result.nodes)].sort((a, b) => a - b).map(String)
      : result.axes[colourBy] ?? []
    const series = distinct.map((value, i) => ({
      type: 'scatter3D' as const, name: colourBy === 'node' ? `node ${value}` : value, symbolSize: 4,
      itemStyle: { color: paletteColor(i), opacity: 0.85 },
      data: result.points.flatMap((p, j) => (of(j) === value ? [[...p, j]] : [])),
    }))
    // The directions have no meaning of their own: faint axes, no labels (as the 3-D trajectory view;
    // echarts-gl fails on camera moves when the axis lines are hidden outright)
    const axis = { type: 'value' as const, name: '', axisLabel: { show: false }, axisTick: { show: false },
      axisLine: { lineStyle: { color: '#d1d5db' } }, splitLine: { show: false }, axisPointer: { show: false } }
    return {
      legend: { type: 'scroll', top: 0, textStyle: { fontSize: 10 } },
      tooltip: {
        formatter: (p: unknown) => {
          const j = (p as { value: number[] }).value?.[3]
          const item = j === undefined ? null : result.items[j]
          return item ? `${item.input_text ?? item.probe_id}<br/>node ${result.nodes[j]} · ${item.label ?? ''}` : ''
        },
      },
      grid3D: { boxWidth: 100, boxDepth: 100, boxHeight: 100, axisPointer: { show: false }, viewControl: { distance: 170 } },
      xAxis3D: axis, yAxis3D: axis, zAxis3D: axis,
      series,
    } as echarts.EChartsOption
  }, [result, colourBy])
  const box = useEChart(option)

  const at = result ? String(result.k) : ''
  const held = result?.heldout?.[at]
  const axes = result ? Object.keys(result.axes) : []
  const scored = result ? (result.in_sample.ami[colourBy] ? colourBy : 'label') : 'label'
  return (
    <div className="border border-gray-200 rounded p-2 space-y-2 bg-gray-50">
      <div className="flex flex-wrap items-center gap-3">
        <span className="text-xs font-medium text-gray-900">Preview one layer</span>
        <label className={field}>
          Layer
          <select value={li} disabled={disabled} className={input} onChange={e => chooseLayer(Number(e.target.value))}>
            {layers.map((layer, i) => <option key={layer} value={i}>L{layer}</option>)}
          </select>
        </label>
        <label className={field}>Neighbours <input type="number" min={2} max={200} value={values.n_neighbors} disabled={disabled}
          onChange={e => set({ n_neighbors: Number(e.target.value) || 2 })} className={`${input} w-14`} /></label>
        <label className={field}>Dimensions <input type="number" min={2} max={50} value={values.dimensions} disabled={disabled}
          onChange={e => set({ dimensions: Number(e.target.value) || 2 })} className={`${input} w-14`} /></label>
        <label className={field}>Min distance <input type="number" min={0} max={0.99} step={0.05} value={values.min_dist}
          disabled={disabled} onChange={e => set({ min_dist: Math.min(0.99, Math.max(0, Number(e.target.value) || 0)) })}
          className={`${input} w-16`} /></label>
        <label className={field}>Metric
          <select value={values.metric} disabled={disabled} className={input} onChange={e => set({ metric: e.target.value as Metric })}>
            {metrics.map(m => <option key={m} value={m}>{m}</option>)}
          </select>
        </label>
        <label className={field}>k <input type="number" min={2} max={50} value={values.k} disabled={disabled}
          onChange={e => set({ k: Number(e.target.value) || 2 })} className={`${input} w-12`} /></label>
        <button onClick={() => run(false)} disabled={disabled || runner.starting}
          className="px-2 py-0.5 text-xs rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">Preview</button>
        <button onClick={() => run(true)} disabled={disabled || runner.starting}
          title="Also score each k held out, on family folds of the items a tune would select from"
          className="px-2 py-0.5 text-xs rounded border border-blue-500 text-blue-700 hover:bg-blue-50 disabled:border-gray-300 disabled:text-gray-400">
          Hold out</button>
      </div>
      {runner.error && <p className="text-xs text-red-600">{runner.error}</p>}
      {problem && <p className="text-xs text-red-600">{problem}</p>}
      {runner.job && busy && <JobProgress job={runner.job} title="Preview" onCancel={runner.running ? runner.cancel : undefined} />}
      {result && (
        <div className="space-y-1.5">
          <div className="flex flex-wrap items-center gap-3 text-[11px] text-gray-600">
            <span>
              L{result.layer}: {result.n_items} items, {result.settings.n_neighbors} neighbours,{' '}
              {result.settings.dimensions}-D, min distance {result.settings.min_dist}, {result.settings.metric}, k {result.k};
              three main directions hold {Math.round(result.share * 100)}% of its spread; {result.seconds} s
            </span>
            <label className={field}>
              Colour by
              <select value={colourBy} className={input} onChange={e => setColourBy(e.target.value)}>
                <option value="node">node</option>
                {axes.map(a => <option key={a} value={a}>{a}</option>)}
              </select>
            </label>
            <button onClick={() => onUse(layers.indexOf(result.layer), { ...result.settings, k: result.k }, !!result.heldout)}
              disabled={disabled} title="Copy these settings and k into the form's per-layer table, marked as from a preview"
              className="px-2 py-0.5 text-xs rounded border border-gray-400 text-gray-800 hover:bg-white disabled:text-gray-300">
              Use for L{result.layer}</button>
          </div>
          <div ref={box} style={{ height: 320 }} className="bg-white border border-gray-200 rounded" />
          <table className="text-[11px] text-gray-700">
            <thead>
              <tr className="text-gray-400">
                <th className="text-left font-normal pr-3">at k {result.k}</th>
                {axes.map(a => <th key={a} className="text-left font-normal pr-3">{a}</th>)}
                <th className="text-left font-normal">silhouette</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="pr-3 text-gray-500">AMI, in-sample</td>
                {axes.map(a => <td key={a} className="pr-3 tabular-nums">{fixed(result.in_sample.ami[a]?.[at])}</td>)}
                <td className="tabular-nums">{fixed(result.in_sample.silhouette[at])}</td>
              </tr>
              {held && (
                <tr>
                  <td className="pr-3 text-gray-500">AMI / κ, held out</td>
                  {axes.map(a => <td key={a} className="pr-3 tabular-nums">{fixed(held[a]?.ami)} / {fixed(held[a]?.kappa)}</td>)}
                  <td />
                </tr>
              )}
            </tbody>
          </table>
          <p className="text-[11px] text-gray-600 tabular-nums">
            {scored} AMI by k{result.heldout ? ' (held out)' : ' (in-sample)'}:{' '}
            {result.ks.map(kk => {
              const v = result.heldout ? result.heldout[String(kk)]?.[scored]?.ami : result.in_sample.ami[scored]?.[String(kk)]
              return <span key={kk} className={kk === result.k ? 'font-semibold text-gray-900' : ''}>{kk}: {fixed(v)}{' '}</span>
            })}
          </p>
          <p className="text-[10px] text-gray-500">
            Scores leave out the {result.test.n_items} items a tune would test on
            {result.test.weaker ? ' (a stratified share: no held-out families)' : ` (whole ${result.holdout.family_field} families)`}
            {result.folds ? `; held out on ${result.folds.n_folds} folds${result.folds.weaker ? ' (weaker)' : ''}` : ''}.
            {result.heldout ? ' Settings chosen on these held-out scores make the lens\'s own validation selection-biased; a tune\'s test score stays honest.' : ''}
          </p>
        </div>
      )}
    </div>
  )
}
