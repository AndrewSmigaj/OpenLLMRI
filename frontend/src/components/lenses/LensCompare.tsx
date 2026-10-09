// Compare lenses (DESIGN.md E3): several UMAP lenses of one capture on one chart, so the better
// settings show at a glance: each lens's held-out score per layer at its version's k, and for a
// tuned lens its test score and its source lens's on the same test items. Lenses whose settings
// were chosen on held-out scores say so, and the chart warns when the lenses were held out
// differently, filtered differently or hold other items.
import { useEffect, useMemo, useRef, useState } from 'react'
import type * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { LensSearch, LensSummary, Validation } from '../../types/lens'
import { compareLenses, type CompareMeasure, type ComparedLens } from '../../utils/compareLenses'
import { exportElementChart } from '../../utils/exportFigure'
import { paletteColor } from '../../color/scheme'
import { useEChart } from '../../hooks/useEChart'
import ExportMenu from '../common/ExportMenu'

const MEASURES: { id: CompareMeasure; label: string }[] = [
  { id: 'ami', label: 'AMI' }, { id: 'kappa', label: 'κ' }, { id: 'accuracy', label: 'accuracy' },
]
const input = 'px-1.5 py-0.5 text-xs border border-gray-300 rounded bg-white'
// A lens's records are read once per validation, so a new validation is read again
const keyOf = (lens: LensSummary) => `${lens.name}@${lens.validation?.created_at ?? ''}@${lens.tuning ? 't' : ''}`

export default function LensCompare({ session, lenses }: { session: string; lenses: LensSummary[] }) {
  const umap = useMemo(() => lenses.filter(l => !l.legacy && l.kind === 'umap'), [lenses])
  const [picked, setPicked] = useState<string[]>(() => umap.filter(l => l.validation).slice(0, 3).map(l => l.name))
  const [axis, setAxis] = useState('label')
  const [measure, setMeasure] = useState<CompareMeasure>('ami')
  const [loaded, setLoaded] = useState<Record<string, { validation: Validation | null; search: LensSearch | null }>>({})
  const requested = useRef(new Set<string>())

  useEffect(() => {
    for (const lens of umap.filter(l => picked.includes(l.name))) {
      const key = keyOf(lens)
      if (requested.current.has(key)) continue
      requested.current.add(key)
      Promise.all([
        lens.validation ? apiClient.getLensValidation(session, lens.name).catch(() => null) : Promise.resolve(null),
        lens.tuning ? apiClient.getLensSearch(session, lens.name).catch(() => null) : Promise.resolve(null),
      ]).then(([validation, search]) => setLoaded(l => ({ ...l, [key]: { validation, search } })))
    }
  }, [session, picked, umap])

  const chosen: ComparedLens[] = useMemo(() => picked.flatMap(name => {
    const lens = umap.find(l => l.name === name)
    const found = lens && loaded[keyOf(lens)]
    return lens && found ? [{ lens, ...found }] : []
  }), [picked, umap, loaded])
  const axes = [...new Set(chosen.flatMap(c => Object.keys(c.validation?.axes ?? {})))]
  const found = useMemo(() => compareLenses(chosen, axis, measure), [chosen, axis, measure])

  const option = useMemo<echarts.EChartsOption | null>(() => {
    if (!found.lines.length) return null
    const label = MEASURES.find(m => m.id === measure)?.label ?? measure
    const colour = (lens: string) => paletteColor(Math.max(0, picked.indexOf(lens)))
    return {
      title: { text: `Held-out ${label} on ${axis}, per layer`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { trigger: 'axis' }, legend: { bottom: 0, type: 'scroll', textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 16, top: 28, bottom: 56 },
      xAxis: { type: 'category', data: found.layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: measure === 'accuracy' ? 0 : -0.2, max: 1, axisLabel: { fontSize: 9 } },
      series: found.lines.map(line => ({
        name: line.name, type: 'line' as const, data: line.values, connectNulls: false,
        itemStyle: { color: colour(line.lens) },
        lineStyle: { color: colour(line.lens), width: line.kind === 'test' ? 2.5 : 1.5,
          type: line.kind === 'held out' ? 'solid' as const : line.kind === 'test' ? 'dashed' as const : 'dotted' as const },
      })),
      animation: false,
    }
  }, [found, measure, axis, picked])
  const box = useEChart(option)

  if (!umap.length) return <p className="text-xs text-gray-500">No UMAP lenses on this capture yet.</p>
  return (
    <div className="bg-white border border-gray-200 rounded p-2 space-y-1.5">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-700">
        <span className="font-medium text-gray-900">Compare lenses</span>
        {umap.map(l => (
          <label key={l.name} className="flex items-center gap-1" title={l.validation ? '' : 'Not validated yet'}>
            <input type="checkbox" checked={picked.includes(l.name)}
              onChange={() => setPicked(p => (p.includes(l.name) ? p.filter(n => n !== l.name) : [...p, l.name]))} />
            <span className={`font-mono ${l.validation ? '' : 'text-gray-400'}`}>{l.name}</span>
          </label>
        ))}
        <label className="flex items-center gap-1">Axis
          <select value={axis} onChange={e => setAxis(e.target.value)} className={input}>
            {(axes.length ? axes : ['label']).map(a => <option key={a} value={a}>{a}</option>)}
          </select>
        </label>
        <label className="flex items-center gap-1">Measure
          <select value={measure} onChange={e => setMeasure(e.target.value as CompareMeasure)} className={input}>
            {MEASURES.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
          </select>
        </label>
        {option && (
          <span className="ml-auto">
            <ExportMenu formats={['png', 'svg', 'csv', 'json']}
              onExport={format => exportElementChart(format, box.current, `${session}_compare_${axis}_${measure}`, {
                figure: 'compare lenses: held-out scores per layer', session, axis, measure,
                lenses: chosen.map(c => ({ name: c.lens.name, version: c.lens.current, k_per_layer: c.lens.k_per_layer,
                  settings_origin: c.lens.settings_origin, selection_biased: c.lens.selection_biased,
                  folds: c.validation?.folds, validated_at: c.validation?.provenance.created_at })),
                gaps: found.gaps, warnings: found.warnings }, option)} />
          </span>
        )}
      </div>
      {found.warnings.map(w => <p key={w} className="text-[11px] text-amber-700">{w}</p>)}
      {found.gaps.map(g => (
        <p key={g.lens} className="text-[11px] text-gray-500">{g.lens}: no score at {g.layers.map(l => `L${l}`).join(', ')}, {g.why}.</p>
      ))}
      {option ? <div ref={box} style={{ height: 300 }} />
        : <p className="text-xs text-gray-500">Choose validated lenses to compare.</p>}
      <p className="text-[10px] text-gray-500">
        Solid: held out on the lens's own folds, at its version's k. A tuned lens adds its score on the test portion
        its search never saw (dashed) and its source lens's on the same items (dotted): those are the honest ones.
      </p>
    </div>
  )
}
