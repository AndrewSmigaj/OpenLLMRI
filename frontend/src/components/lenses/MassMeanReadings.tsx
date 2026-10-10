// Where each class of a capture sits along a mass-mean lens's axis, layer by layer: its median and
// its middle half (25th to 75th percentile). The capture is the lens's own by default, so a class the
// lens wasn't fitted on (the dual-purpose objects between benign and harmful) shows its position;
// any other capture can be read at the lens's site.
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import { valueColor } from '../../color/scheme'
import type { SessionListItem } from '../../types/api'
import type { LensSummary, MassMeanReadings as Readings } from '../../types/lens'
import { classBands } from '../../utils/massMeanBands'
import { exportElementChart } from '../../utils/exportFigure'
import ExportMenu from '../common/ExportMenu'

export default function MassMeanReadings({ session, lens }: { session: string; lens: LensSummary }) {
  const [target, setTarget] = useState(session)
  const [captures, setCaptures] = useState<SessionListItem[]>([])
  const [found, setFound] = useState<Readings | null>(null)
  const [error, setError] = useState<string | null>(null)
  const box = useRef<HTMLDivElement>(null)

  useEffect(() => {
    apiClient.listSessions().then(setCaptures).catch(() => setCaptures([]))
  }, [])

  useEffect(() => {
    let current = true
    setFound(null)
    setError(null)
    apiClient.getMassMeanReadings(session, lens.name, target)
      .then(read => { if (current) setFound(read) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens.name, target])

  const bands = useMemo(() => (found ? classBands(found) : []), [found])

  const option = useMemo<echarts.EChartsOption | null>(() => {
    if (!found) return null
    const names = bands.map(b => b.name)
    const colour = (name: string) => valueColor(name, names, 'red-blue')
    const x = found.layers.map(l => `L${l}`)
    const series: echarts.SeriesOption[] = bands.flatMap(b => [
      // the middle half as a band: an invisible lower edge, then the width stacked on it. The edge
      // is often negative, so the stack must add across signs ('all'); by default ECharts stacks a
      // positive width on the last positive value, which draws the band up from zero
      { name: `${b.name} lower`, type: 'line' as const, data: b.q1, stack: b.name, stackStrategy: 'all' as const,
        symbol: 'none', lineStyle: { opacity: 0 }, silent: true, tooltip: { show: false } },
      { name: `${b.name} middle half`, type: 'line' as const, data: b.q3.map((v, i) => v - b.q1[i]), stack: b.name,
        stackStrategy: 'all' as const, symbol: 'none', lineStyle: { opacity: 0 },
        areaStyle: { color: colour(b.name), opacity: 0.15 }, silent: true, tooltip: { show: false } },
      { name: b.name, type: 'line' as const, data: b.median, symbol: 'circle', symbolSize: 4,
        lineStyle: { color: colour(b.name), width: 2 }, itemStyle: { color: colour(b.name) } },
    ])
    const { label_a, label_b } = found.contrast
    const first = series[2] as echarts.LineSeriesOption | undefined
    if (first) {
      first.markLine = { silent: true, symbol: 'none', lineStyle: { type: 'dotted', color: '#9ca3af' },
        label: { fontSize: 9, formatter: '{b}' },
        data: [{ yAxis: -1, name: `${label_a} −1` }, { yAxis: 1, name: `${label_b} +1` }] }
    }
    return {
      title: { text: `Readings along ${label_a} (−1) to ${label_b} (+1): median and middle half`, left: 'center',
        textStyle: { fontSize: 12 } },
      tooltip: {
        trigger: 'axis',
        formatter: (params: unknown) => {
          const index = (params as { dataIndex: number }[])[0]?.dataIndex ?? 0
          return [`L${found.layers[index]}`, ...bands.map(b =>
            `${b.name} (${b.n}): ${b.median[index].toFixed(2)} [${b.q1[index].toFixed(2)}, ${b.q3[index].toFixed(2)}]`)].join('<br/>')
        },
      },
      legend: { bottom: 0, data: names, textStyle: { fontSize: 10 } },
      grid: { left: 44, right: 64, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: x, axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', name: 'reading', nameTextStyle: { fontSize: 9 }, axisLabel: { fontSize: 9 } },
      series,
      animation: false,
    }
  }, [found, bands])

  useEffect(() => {
    if (!box.current || !option) return
    const chart = echarts.getInstanceByDom(box.current) ?? echarts.init(box.current)
    chart.setOption(option, true)
  }, [option])
  useEffect(() => {
    const element = box.current
    return () => { if (element) echarts.getInstanceByDom(element)?.dispose() }
  }, [])

  const others = captures.filter(c => c.session_id !== session)
  return (
    <div className="space-y-1 pt-2 border-t border-gray-100">
      <div className="flex items-center gap-2 flex-wrap">
        <span className="text-xs font-semibold text-gray-800">Readings</span>
        <label className="text-[11px] text-gray-600">capture
          <select value={target} onChange={e => setTarget(e.target.value)}
            className="ml-1 text-[11px] border border-gray-300 rounded px-1 py-0.5 max-w-[22rem]">
            <option value={session}>its own ({session})</option>
            {others.map(c => <option key={c.session_id} value={c.session_id}>{c.session_name} ({c.session_id})</option>)}
          </select>
        </label>
        <div className="ml-auto">
          <ExportMenu formats={['png', 'svg', 'csv', 'json']} disabled={!option || !found}
            onExport={format => found && exportElementChart(format, box.current, `${session}_${lens.name}_readings_${found.target}`, {
              figure: 'mass-mean readings: median and middle half per class',
              lens: { session, name: lens.name, contrast: found.contrast },
              target: found.target, position: found.position,
              classes: bands.map(b => ({ name: b.name, n: b.n })) }, option)} />
        </div>
      </div>
      {error && <p className="text-xs text-red-600">{error}</p>}
      {!error && !found && <p className="text-xs text-gray-500">Reading the capture…</p>}
      {found && (
        <p className="text-[11px] text-gray-500">
          {found.items.length} items of {found.target} at token position {found.position}; the lens's own classes
          average −1 and +1 by construction
        </p>
      )}
      <div ref={box} style={{ height: 260 }} />
    </div>
  )
}
