// A mass-mean lens's held-out scores across the layers: the mean accuracy over folds (the paper's
// figure), the worst fold and Cohen's kappa, with chance marked.
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { LensSummary, MassMeanValidation } from '../../types/lens'
import { exportElementChart } from '../../utils/exportFigure'
import ExportMenu from '../common/ExportMenu'

export default function MassMeanResults({ session, lens }: { session: string; lens: LensSummary }) {
  const [validation, setValidation] = useState<MassMeanValidation | null>(null)
  const [error, setError] = useState<string | null>(null)
  const box = useRef<HTMLDivElement>(null)

  useEffect(() => {
    let current = true
    apiClient.getMassMeanValidation(session, lens.name)
      .then(found => { if (current) setValidation(found) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens.name])

  const option = useMemo<echarts.EChartsOption | null>(() => {
    if (!validation) return null
    const layers = Object.keys(validation.layers).map(Number).sort((a, b) => a - b)
    const line = (name: string, read: (s: MassMeanValidation['layers'][string]) => number) =>
      ({ name, type: 'line' as const, data: layers.map(l => read(validation.layers[String(l)])) })
    const { label_a, label_b } = validation.contrast
    return {
      title: { text: `${label_a} (−1) against ${label_b} (+1): held out`, left: 'center', textStyle: { fontSize: 12 } },
      tooltip: { trigger: 'axis' }, legend: { bottom: 0, textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 36, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: layers.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: 0, max: 1, axisLabel: { fontSize: 9 } },
      series: [
        { ...line('accuracy (mean over folds)', s => s.accuracy),
          markLine: { silent: true, symbol: 'none', data: [{ yAxis: 0.5, name: 'chance' }], lineStyle: { type: 'dotted', color: '#9ca3af' } } },
        line('worst fold', s => s.worst_fold),
        line('κ', s => s.kappa),
      ],
      animation: false,
    }
  }, [validation])

  useEffect(() => {
    if (!box.current || !option) return
    const chart = echarts.getInstanceByDom(box.current) ?? echarts.init(box.current)
    chart.setOption(option, true)
  }, [option])
  useEffect(() => {
    const element = box.current
    return () => { if (element) echarts.getInstanceByDom(element)?.dispose() }
  }, [])

  if (error) return <p className="text-xs text-red-600">{error}</p>
  if (!validation) return <p className="text-xs text-gray-500">Loading the validation…</p>
  return (
    <div className="space-y-1 pt-2 border-t border-gray-100">
      <p className="text-[11px] text-gray-500">
        {validation.folds.kind}, {validation.folds.n_folds} folds{validation.folds.weaker ? ' (weaker: no scene families)' : ''};
        each fold's axis comes from its training items; held-out items are classified by the sign of their reading
      </p>
      <div className="flex justify-end">
        <ExportMenu formats={['png', 'svg', 'csv', 'json']} disabled={!option}
          onExport={format => exportElementChart(format, box.current, `${session}_${lens.name}_heldout`, {
            figure: 'mass-mean axis, held out', lens: { session, name: lens.name, contrast: validation.contrast },
            validation: { folds: validation.folds, created_at: validation.provenance.created_at } }, option)} />
      </div>
      <div ref={box} style={{ height: 240 }} />
    </div>
  )
}
