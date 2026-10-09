// The axes analysis (DESIGN.md C8): how many of a capture's designed attributes each technique
// recovers at each layer, scored on held-out items and judged against decoys (random values given
// per family or per text, in each attribute's proportions). Beside the count, the layer's effective
// dimensionality and how many independent directions the attributes' partial axes span, against
// permuted design rows; a heatmap of every attribute's score for one technique; and at one layer,
// the angles between the partial axes beside the design's own correlations, and the spectrum with
// each attribute's best-matching component. Generic: the attributes come from the lens.
import { useEffect, useMemo, useState } from 'react'
import type * as echarts from 'echarts'
import { apiClient, ApiError } from '../../api/client'
import type { AxesTechnique, LensAxes as Axes, LensSummary } from '../../types/lens'
import { exportElementChart, type ExportFormat } from '../../utils/exportFigure'
import { useEChart } from '../../hooks/useEChart'
import { useShell } from '../shell/shellContext'
import ExportMenu from '../common/ExportMenu'

type Row = AxesTechnique | 'umap_at_k' | 'umap_best_k'
const ROWS: { id: Row; label: string; color: string; type: 'solid' | 'dashed' | 'dotted' }[] = [
  { id: 'umap_at_k', label: 'UMAP lens (its k)', color: '#5470c6', type: 'solid' },
  { id: 'umap_best_k', label: "UMAP lens (each attribute's best k)", color: '#5470c6', type: 'dashed' },
  { id: 'raw_ward', label: 'raw: PCA-50, Ward', color: '#91cc75', type: 'solid' },
  { id: 'raw_spectral', label: 'raw: PCA-50, spectral', color: '#fac858', type: 'solid' },
  { id: 'component', label: 'one principal component', color: '#9a60b4', type: 'solid' },
  { id: 'directions', label: 'partial directions', color: '#fc8452', type: 'solid' },
  { id: 'probe', label: 'linear probe (the ceiling)', color: '#73c0de', type: 'dotted' },
]
const SPECTRUM_SHOWN = 30

function kappaOf(axes: Axes, row: Row, li: number, attribute: string): number | null {
  if (row === 'umap_at_k') return axes.umap?.at_k[li]?.[attribute] ?? null
  if (row === 'umap_best_k') return axes.umap?.best_k[li]?.[attribute]?.kappa ?? null
  return axes.scores[row]?.[li]?.real?.[attribute] ?? null
}

function limitOf(axes: Axes, row: Row, attribute: string): number | null {
  if (row === 'umap_at_k' || row === 'umap_best_k') {
    return axes.umap?.decoys ? axes.umap.thresholds[row === 'umap_at_k' ? 'at_k' : 'best_k'][attribute] ?? null : null
  }
  return axes.thresholds[row]?.[attribute] ?? null
}

interface ChartProps {
  option: echarts.EChartsOption | null
  height: number
  file: string
  recipe: Record<string, unknown>
}

function AxesChart({ option, height, file, recipe }: ChartProps) {
  const box = useEChart(option)
  return (
    <div>
      <div className="flex justify-end">
        <ExportMenu formats={['png', 'svg', 'csv', 'json']}
          onExport={(format: ExportFormat) => exportElementChart(format, box.current, file, recipe, option)} />
      </div>
      <div ref={box} style={{ height }} />
    </div>
  )
}

export default function LensAxes({ session, lens, disabled }: { session: string; lens: LensSummary; disabled: boolean }) {
  const { events } = useShell()
  const [axes, setAxes] = useState<Axes | null>(null)
  const [missing, setMissing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [working, setWorking] = useState<string | null>(null) // the job working them out
  const [family, setFamily] = useState(lens.holdout?.family_field ?? '') // the lens's own design to start
  const [whole, setWhole] = useState(lens.holdout?.whole_families ?? false)
  const [technique, setTechnique] = useState<Row>('probe')
  const [chosenLayer, setChosenLayer] = useState<number | null>(null)

  const name = lens.name, version = lens.current ?? undefined
  useEffect(() => {
    let current = true
    apiClient.getLensAxes(session, name, version)
      .then(found => { if (current) { setAxes(found); setMissing(false); setError(null); setWorking(null) } })
      .catch(err => {
        if (!current) return
        const absent = err instanceof ApiError && err.status === 404
        setMissing(absent)
        setError(absent ? null : err instanceof Error ? err.message : String(err))
      })
    return () => { current = false }
  }, [session, name, version, events.lensRevision])

  // a re-run starts from the family field the analysis used (single words: 'family')
  const usedField = axes?.folds.field
  useEffect(() => { if (usedField) setFamily(usedField) }, [usedField])

  const start = () => {
    setError(null)
    apiClient.workOutAxes(session, lens.name, { family_field: family, whole_families: whole })
      .then(job => setWorking(job.job_id))
      .catch(err => setError(err instanceof Error ? err.message : String(err)))
  }

  const rows = useMemo(() => (axes ? ROWS.filter(r => axes.recovered[r.id]) : []), [axes])
  const attrs = useMemo(() => (axes ? Object.keys(axes.attributes) : []), [axes])
  // The layer shown in the matrices and the spectrum: chosen, else where the partial directions
  // read best (the most attributes recovered, then the highest kappa summed over attributes)
  const layerIndex = useMemo(() => {
    if (!axes) return 0
    const at = chosenLayer === null ? -1 : axes.layers.indexOf(chosenLayer)
    if (at >= 0) return at
    const count = axes.recovered.directions ?? []
    const total = (li: number) => Object.values(axes.scores.directions?.[li]?.real ?? {}).reduce((a, b) => a + b, 0)
    return axes.layers.reduce((best, _, li) =>
      (count[li] > count[best] || (count[li] === count[best] && total(li) > total(best)) ? li : best), 0)
  }, [axes, chosenLayer])

  const recipe = useMemo(() => (axes ? {
    lens: { session, name: lens.name, version: axes.version }, attributes: axes.attributes, folds: axes.folds,
    decoys: axes.decoys, level: axes.level, probe_decoy_layers: axes.probe_decoy_layers, job: axes.provenance.job_id,
  } : {}), [axes, session, lens.name])

  const recoveredOption = useMemo<echarts.EChartsOption | null>(() => axes && {
    title: { text: `Attributes recovered (of ${attrs.length}), held out, beyond the decoys`, left: 'center', textStyle: { fontSize: 12 } },
    tooltip: { trigger: 'axis' }, legend: { bottom: 0, textStyle: { fontSize: 10 } },
    grid: { left: 36, right: 12, top: 28, bottom: 76 },
    xAxis: { type: 'category', data: axes.layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
    yAxis: { type: 'value', min: 0, max: attrs.length, minInterval: 1, axisLabel: { fontSize: 9 } },
    series: rows.map(r => ({
      name: r.label, type: 'line' as const, data: axes.recovered[r.id], symbolSize: 4,
      itemStyle: { color: r.color }, lineStyle: { color: r.color, type: r.type, width: r.id === 'umap_at_k' ? 2.5 : 1.5 },
    })),
    animation: false,
  }, [axes, attrs, rows])

  const dimensionOption = useMemo<echarts.EChartsOption | null>(() => {
    if (!axes) return null
    const g = axes.geometry, s = axes.spectrum
    return {
      title: { text: 'Independent directions and effective dimensionality', left: 'center', textStyle: { fontSize: 12 } },
      tooltip: {
        trigger: 'axis',
        formatter: (raw: unknown) => {
          const i = (Array.isArray(raw) ? raw[0] : raw as { dataIndex: number }).dataIndex
          return `L${axes.layers[i]}<br/>independent directions ${g[i].independent.toFixed(2)} (permuted design rows: ` +
            `${g[i].null[0].toFixed(2)}–${g[i].null[2].toFixed(2)})<br/>effective dimensionality ${s[i].participation_ratio.toFixed(1)}; ` +
            `half the variance in ${s[i].for_half} components, 90% in ${s[i].for_90}`
        },
      },
      legend: {
        bottom: 0, textStyle: { fontSize: 10 },
        data: ['independent directions among the partial axes', 'permuted design rows (5th–95th percentile)',
          'effective dimensionality (participation ratio)'],
      },
      grid: { left: 36, right: 44, top: 28, bottom: 76 },
      xAxis: { type: 'category', data: axes.layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: [
        { type: 'value', name: 'directions', nameTextStyle: { fontSize: 9 }, min: 0, axisLabel: { fontSize: 9 } },
        { type: 'value', name: 'dimensions', nameTextStyle: { fontSize: 9 }, min: 0, axisLabel: { fontSize: 9 }, splitLine: { show: false } },
      ],
      series: [
        { name: 'null floor', type: 'line', data: g.map(x => x.null[0]), stack: 'null', symbol: 'none', lineStyle: { opacity: 0 } },
        { name: 'permuted design rows (5th–95th percentile)', type: 'line', data: g.map(x => x.null[2] - x.null[0]), stack: 'null',
          symbol: 'none', lineStyle: { opacity: 0 }, areaStyle: { color: '#fc8452', opacity: 0.15 }, itemStyle: { color: '#fdd0b6' } },
        { name: 'independent directions among the partial axes', type: 'line', data: g.map(x => x.independent), symbolSize: 4,
          itemStyle: { color: '#fc8452' }, lineStyle: { color: '#fc8452', width: 2 } },
        { name: 'effective dimensionality (participation ratio)', type: 'line', yAxisIndex: 1, data: s.map(x => x.participation_ratio),
          symbolSize: 3, itemStyle: { color: '#64748b' }, lineStyle: { color: '#64748b', width: 1.5 } },
      ],
      animation: false,
    }
  }, [axes])

  const heatmapOption = useMemo<echarts.EChartsOption | null>(() => {
    if (!axes) return null
    const row = rows.find(r => r.id === technique) ?? rows[0]
    if (!row) return null
    const data = axes.layers.flatMap((_, li) => attrs.flatMap((attribute, ai) => {
      const kappa = kappaOf(axes, row.id, li, attribute)
      if (kappa === null) return []
      const limit = limitOf(axes, row.id, attribute)
      const passed = limit !== null && kappa > limit
      return [{ value: [li, ai, Math.max(0, kappa)], kappa, limit, attribute, layer: axes.layers[li],
        itemStyle: { borderColor: '#ffffff', borderWidth: 1, opacity: passed ? 1 : 0.3 } }]
    }))
    return {
      title: { text: `${row.label}: held-out κ per attribute (faded: within the decoys' range)`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: {
        formatter: (raw: unknown) => {
          const d = (raw as { data: { kappa: number; limit: number | null; attribute: string; layer: number } }).data
          return `${d.attribute} at L${d.layer}: κ ${d.kappa.toFixed(3)}` +
            (d.limit === null ? ' (no decoy threshold)' : `; the decoys' ${Math.round(100 * axes.level)}th percentile ${d.limit.toFixed(3)}`)
        },
      },
      grid: { left: 110, right: 16, top: 28, bottom: 44 },
      xAxis: { type: 'category', data: axes.layers.map(l => `L${l}`), axisLabel: { fontSize: 9 }, splitArea: { show: false } },
      yAxis: { type: 'category', data: attrs, inverse: true, axisLabel: { fontSize: 10 } },
      visualMap: { min: 0, max: 1, calculable: false, orient: 'horizontal', left: 'center', bottom: 0, itemHeight: 120,
        text: ['κ 1', '0'], textStyle: { fontSize: 9 }, inRange: { color: ['#f7fbff', '#08519c'] } },
      series: [{ type: 'heatmap', data, label: { show: axes.layers.length <= 24, fontSize: 8,
        formatter: (p: unknown) => (p as { data: { kappa: number } }).data.kappa.toFixed(2) } }],
      animation: false,
    }
  }, [axes, attrs, rows, technique])

  const matrixOption = useMemo<echarts.EChartsOption | null>(() => {
    if (!axes) return null
    const g = axes.geometry[layerIndex]
    const design = axes.design
    const cells = (matrix: number[][]) => matrix.flatMap((line, i) => line.map((v, j) => [j, i, v]))
    // a cosine inside the band permuted design rows give (the design's correlations kept) is faded
    const band = g.null_cosines
    const inside = (i: number, j: number, v: number) => Boolean(band) && i !== j && v >= band!.low[i][j] && v <= band!.high[i][j]
    const cosines = g.cosines.flatMap((line, i) => line.map((v, j) => ({ value: [j, i, v], itemStyle: { opacity: inside(i, j, v) ? 0.3 : 1 } })))
    const labels = g.names.length <= 14
    return {
      title: [
        { text: `L${axes.layers[layerIndex]}: cosines between the partial axes`, left: '25%', textAlign: 'center', textStyle: { fontSize: 12 },
          subtext: band ? 'faded: within the 5th–95th percentile of permuted design rows' : '', subtextStyle: { fontSize: 10 } },
        { text: "the design's own correlations", left: '75%', textAlign: 'center', textStyle: { fontSize: 12 } },
      ],
      tooltip: {
        formatter: (raw: unknown) => {
          const p = raw as { seriesIndex: number; value: number[] }
          const [j, i, v] = p.value
          if (p.seriesIndex === 1) return `${design.names[i]} · ${design.names[j]}: correlation ${v.toFixed(3)}`
          const range = band && i !== j ? ` (permuted design rows: ${band.low[i][j].toFixed(2)} to ${band.high[i][j].toFixed(2)})` : ''
          return `${g.names[i]} · ${g.names[j]}: cosine ${v.toFixed(3)}${range}`
        },
      },
      grid: [{ left: 110, right: '52%', top: 44, bottom: 80 }, { left: '58%', right: 16, top: 44, bottom: 80 }],
      xAxis: [
        { type: 'category', gridIndex: 0, data: g.names, axisLabel: { fontSize: 9, rotate: 45 } },
        { type: 'category', gridIndex: 1, data: design.names, axisLabel: { fontSize: 9, rotate: 45 } },
      ],
      yAxis: [
        { type: 'category', gridIndex: 0, data: g.names, inverse: true, axisLabel: { fontSize: 9 } },
        { type: 'category', gridIndex: 1, data: design.names, inverse: true, axisLabel: { show: false } },
      ],
      visualMap: { min: -1, max: 1, calculable: false, orient: 'horizontal', left: 'center', bottom: 0, itemHeight: 120,
        text: ['+1', '−1'], textStyle: { fontSize: 9 }, inRange: { color: ['#b2182b', '#ffffff', '#2166ac'] }, seriesIndex: [0, 1] },
      series: [
        { name: 'cosines', type: 'heatmap', xAxisIndex: 0, yAxisIndex: 0, data: cosines,
          label: { show: labels, fontSize: 8, formatter: (p: unknown) => (p as { value: number[] }).value[2].toFixed(2) } },
        { name: 'design correlations', type: 'heatmap', xAxisIndex: 1, yAxisIndex: 1, data: cells(design.correlations),
          label: { show: labels, fontSize: 8, formatter: (p: unknown) => (p as { value: number[] }).value[2].toFixed(2) } },
      ],
      animation: false,
    }
  }, [axes, layerIndex])

  const spectrumOption = useMemo<echarts.EChartsOption | null>(() => {
    if (!axes) return null
    const s = axes.spectrum[layerIndex]
    const matched: Record<number, string[]> = {}
    for (const [attribute, component] of Object.entries(axes.chosen_component[layerIndex] ?? {})) {
      (matched[component] ??= []).push(attribute)
    }
    const listed = Object.entries(matched).sort((a, b) => Number(a[0]) - Number(b[0]))
      .map(([component, names]) => `PC${component} ${names.join(', ')}`).join(' · ')
    return {
      title: {
        text: `L${axes.layers[layerIndex]}: share of variance per component (half in ${s.for_half}, 90% in ${s.for_90}; ` +
          `participation ratio ${s.participation_ratio.toFixed(1)})`,
        subtext: listed ? `the component that best separates each attribute (purple): ${listed}` : '',
        left: 'center', textStyle: { fontSize: 12 }, subtextStyle: { fontSize: 10 },
      },
      tooltip: { trigger: 'axis' },
      grid: { left: 44, right: 16, top: 48, bottom: 30 },
      xAxis: { type: 'category', data: s.shares.slice(0, SPECTRUM_SHOWN).map((_, i) => `PC${i + 1}`), axisLabel: { fontSize: 8 } },
      yAxis: { type: 'value', axisLabel: { fontSize: 9, formatter: (v: number) => `${Math.round(100 * v)}%` } },
      series: [{
        type: 'bar', name: 'share of variance',
        data: s.shares.slice(0, SPECTRUM_SHOWN).map((share, i) => ({
          value: share, itemStyle: { color: matched[i + 1] ? '#9a60b4' : '#cbd5e1' },
        })),
      }],
      animation: false,
    }
  }, [axes, layerIndex])

  const select = 'px-1 py-0.5 text-xs border border-gray-300 rounded bg-white'
  const form = (
    <span className="flex flex-wrap items-center gap-2">
      <label className="flex items-center gap-1" title="The categories field naming each item's family; decoys and folds keep a family together">
        family field <input value={family} onChange={e => setFamily(e.target.value)} className={`${select} w-20`} />
      </label>
      <label className="flex items-center gap-1" title="Family names as they are, not their first two tokens">
        <input type="checkbox" checked={whole} onChange={e => setWhole(e.target.checked)} /> whole names
      </label>
      <button onClick={start} disabled={disabled || working !== null}
        className="px-2 py-0.5 rounded border border-blue-300 text-blue-700 hover:bg-blue-50 disabled:opacity-50">
        {working ? 'Working them out…' : axes ? 'Work them out again' : 'Work out the axes'}
      </button>
    </span>
  )
  if (missing && !axes) {
    return (
      <div className="pt-2 border-t border-gray-100 text-xs text-gray-600 space-y-1">
        <p>The axes analysis hasn't run on this lens: how many of its capture's designed attributes each technique
          recovers, layer by layer, against decoys (a few minutes).</p>
        {form}
        {error && <p className="text-red-600">{error}</p>}
      </div>
    )
  }
  if (error && !axes) return <p className="text-xs text-red-600">{error}</p>
  if (!axes) return <p className="text-xs text-gray-500">Loading the axes analysis…</p>
  const umapNote = !axes.umap
    ? "The UMAP lens's own rows come from its validation: validate it to add them."
    : !axes.umap.decoys ? "Its validation predates decoys: validate it again to give the UMAP rows a threshold." : null
  return (
    <div className="space-y-2 pt-2 border-t border-gray-100">
      <div className="flex flex-wrap items-center gap-3 text-[11px] text-gray-600">
        <span>
          Held out over {axes.folds.n_folds} folds ({axes.folds.kind}{axes.folds.weaker ? ', weaker: no families' : ''}); chance from
          {' '}{axes.decoys.count} decoys per attribute, given per {axes.decoys.given_per === 'families' ? 'family' : 'text'}; recovered
          {' '}means above the {Math.round(100 * axes.level)}th percentile of the technique's decoy scores, pooled over layers
          (the probe's decoys at {axes.probe_decoy_layers.map(l => `L${l}`).join(', ')}).
        </span>
        {umapNote && <span className="text-amber-700">{umapNote}</span>}
        <span className="ml-auto">{form}</span>
      </div>
      {error && <p className="text-xs text-red-600">{error}</p>}
      <div className="grid grid-cols-1 xl:grid-cols-2 gap-2">
        <AxesChart option={recoveredOption} height={300} file={`${session}_${lens.name}_axes_recovered`}
          recipe={{ figure: 'axes: attributes recovered per layer and technique', ...recipe }} />
        <AxesChart option={dimensionOption} height={300} file={`${session}_${lens.name}_axes_dimensions`}
          recipe={{ figure: 'axes: independent directions among the partial axes, and effective dimensionality', ...recipe }} />
      </div>
      <label className="flex items-center gap-1 text-xs text-gray-600">Technique
        <select value={technique} onChange={e => setTechnique(e.target.value as Row)} className={select}>
          {rows.map(r => <option key={r.id} value={r.id}>{r.label}</option>)}
        </select>
      </label>
      <AxesChart option={heatmapOption} height={90 + 22 * attrs.length} file={`${session}_${lens.name}_axes_${technique}`}
        recipe={{ figure: 'axes: held-out kappa per attribute and layer', technique, ...recipe }} />
      <label className="flex items-center gap-1 text-xs text-gray-600">Layer
        <select value={axes.layers[layerIndex]} onChange={e => setChosenLayer(Number(e.target.value))} className={select}>
          {axes.layers.map(l => <option key={l} value={l}>L{l}</option>)}
        </select>
        <span className="text-gray-400">(first shown: where the partial directions read best)</span>
      </label>
      <AxesChart option={matrixOption} height={360} file={`${session}_${lens.name}_axes_angles_L${axes.layers[layerIndex]}`}
        recipe={{ figure: "axes: cosines between the partial axes beside the design's correlations", layer: axes.layers[layerIndex], ...recipe }} />
      <AxesChart option={spectrumOption} height={240} file={`${session}_${lens.name}_axes_spectrum_L${axes.layers[layerIndex]}`}
        recipe={{ figure: 'axes: the standardized PCA spectrum and the components that best match each attribute',
          layer: axes.layers[layerIndex], ...recipe }} />
    </div>
  )
}
