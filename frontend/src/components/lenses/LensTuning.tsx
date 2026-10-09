// A tuned lens's search (DESIGN.md C4): per layer, the winner's score on the selection folds it was
// chosen on (optimistic, so dashed), its score on the test portion the search never saw (the honest
// one), the lens it started from on the same test portion, and the raw-space groupings and the
// ceiling there too; then a table of each layer's winning settings and k, with the runners-up.
import { useEffect, useMemo, useState } from 'react'
import type * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { LensSearch, LensSummary, SearchScores, UmapSettings } from '../../types/lens'
import { exportElementChart } from '../../utils/exportFigure'
import { useEChart } from '../../hooks/useEChart'
import ExportMenu from '../common/ExportMenu'

type Measure = keyof SearchScores
const MEASURES: { id: Measure; label: string }[] = [
  { id: 'ami', label: 'AMI' }, { id: 'kappa', label: 'κ' }, { id: 'accuracy', label: 'accuracy' },
]
const settingsText = (s: UmapSettings) => `n ${s.n_neighbors}, ${s.dimensions}-D${s.min_dist !== 0.1 ? `, min ${s.min_dist}` : ''}`
const num = (v: number | null | undefined) => (v === null || v === undefined ? '' : v.toFixed(2))

export default function LensTuning({ session, lens }: { session: string; lens: LensSummary }) {
  const [search, setSearch] = useState<LensSearch | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [measure, setMeasure] = useState<Measure>('ami')

  useEffect(() => {
    let current = true
    apiClient.getLensSearch(session, lens.name)
      .then(found => { if (current) setSearch(found) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens.name])

  const option = useMemo<echarts.EChartsOption | null>(() => {
    if (!search) return null
    const read = (scores: SearchScores | null | undefined) => scores?.[measure] ?? null
    // The validation's comparison chart colours the raw groupings and the ceiling the same way;
    // the tuned lens is blue, chosen-on dashed and tested solid, and the lens it started from purple
    const line = (name: string, data: (number | null)[], color: string, type: 'solid' | 'dashed' | 'dotted' = 'solid', width = 1.5) =>
      ({ name, type: 'line' as const, data, connectNulls: true, itemStyle: { color }, lineStyle: { color, type, width } })
    const label = MEASURES.find(m => m.id === measure)?.label ?? measure
    return {
      title: { text: `Tuned on ${search.target_axis}: held-out ${label}`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { trigger: 'axis' }, legend: { bottom: 0, textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 16, top: 28, bottom: 56 },
      xAxis: { type: 'category', data: search.layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: -0.2, max: 1, axisLabel: { fontSize: 9 } },
      series: [
        line('tuned, on the folds it was chosen on (optimistic)', search.winners.map(w => read(w.selection)), '#5470c6', 'dashed'),
        line('tuned, on the test portion', search.winners.map(w => read(w.test)), '#5470c6', 'solid', 2.5),
        line(`${search.source.name}, on the test portion`, search.baseline.layers.map(b => read(b.test)), '#9a60b4'),
        line("raw: PCA-50, Ward (the winner's k)", search.comparison.map(c => read(c.raw_ward)), '#91cc75'),
        line("raw: PCA-50, spectral (the winner's k)", search.comparison.map(c => read(c.raw_spectral)), '#fac858'),
        line('relevant neurons (uses labels)', search.comparison.map(c => read(c.neurons)), '#ee6666', 'dashed'),
        line('ceiling: logistic regression', search.comparison.map(c => read(c.ceiling)), '#73c0de', 'dotted'),
      ],
      animation: false,
    }
  }, [search, measure])

  const box = useEChart(option)
  if (error) return <p className="text-xs text-red-600">{error}</p>
  if (!search) return <p className="text-xs text-gray-500">Loading the tuning…</p>
  const test = search.split.test
  const select = 'px-1 py-0.5 text-xs border border-gray-300 rounded bg-white'
  return (
    <div className="space-y-2 pt-2 border-t border-gray-100">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-600">
        <label className="flex items-center gap-1">Measure
          <select value={measure} onChange={e => setMeasure(e.target.value as Measure)} className={select}>
            {MEASURES.map(m => <option key={m.id} value={m.id}>{m.label}</option>)}
          </select>
        </label>
        <span className="text-gray-400">
          {search.configs.filter(c => c.eligible).length} of {search.configs.length} settings passed the self-check;
          test portion: {test.n_items} items, {test.kind}{test.weaker ? ' (weaker: no families)' : ''}, never used in choosing;
          selection: {search.split.selection.folds.n_folds} folds
        </span>
        <span className="ml-auto">
          <ExportMenu formats={['png', 'svg', 'csv', 'json']}
            onExport={format => exportElementChart(format, box.current, `${session}_${lens.name}_tuning`, {
              figure: 'tuning: held-out scores per layer', lens: { session, name: lens.name, version: lens.current },
              source: search.source, target_axis: search.target_axis, measure, grid: search.grid,
              split: { kind: test.kind, n_items: test.n_items, weaker: test.weaker },
              job: search.provenance.job_id }, option)} />
        </span>
      </div>
      <div ref={box} style={{ height: 280 }} />
      <div className="overflow-x-auto">
        <table className="text-[11px] text-gray-700 border-collapse">
          <thead>
            <tr className="text-gray-500">
              <th className="text-left pr-3 font-normal">layer</th>
              <th className="text-left pr-3 font-normal">settings</th>
              <th className="text-right pr-3 font-normal">k</th>
              <th className="text-right pr-3 font-normal" title="On the folds it was chosen on">AMI chosen on</th>
              <th className="text-right pr-3 font-normal">test AMI</th>
              <th className="text-right pr-3 font-normal">test κ</th>
              <th className="text-right pr-3 font-normal">test accuracy</th>
              <th className="text-right pr-3 font-normal">{search.source.name} test AMI</th>
              <th className="text-left font-normal">runners-up (AMI chosen on)</th>
            </tr>
          </thead>
          <tbody>
            {search.winners.map((w, li) => (
              <tr key={w.layer} className="border-t border-gray-100">
                <td className="pr-3">L{w.layer}</td>
                <td className="pr-3 whitespace-nowrap">{settingsText(w.settings)}</td>
                <td className="text-right pr-3">{w.k}</td>
                <td className="text-right pr-3 text-gray-500">{num(w.selection.ami)}</td>
                <td className="text-right pr-3 font-medium">{num(w.test?.ami)}</td>
                <td className="text-right pr-3">{num(w.test?.kappa)}</td>
                <td className="text-right pr-3">{num(w.test?.accuracy)}</td>
                <td className="text-right pr-3">{num(search.baseline.layers[li]?.test?.ami)}</td>
                <td className="text-gray-500 whitespace-nowrap">
                  {w.runners_up.map(r => `${settingsText(r.settings)}, k ${r.k}: ${num(r.ami)}`).join(' · ')}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {search.notes.map(note => <p key={note} className="text-[11px] text-gray-400">{note}.</p>)}
    </div>
  )
}
