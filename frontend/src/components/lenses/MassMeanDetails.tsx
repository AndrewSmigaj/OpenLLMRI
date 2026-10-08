// How a mass-mean lens bears on routing, and what its axis says, per layer: the routing change the
// axis predicts through the next layer's router, against random directions of the same length
// (above their 95th percentile, the routers single the concept out; inside their range, it rides
// in content they mostly ignore), and the tokens each class's mean favours over the other's.
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { useLensDetails } from '../../hooks/useLensDetails'
import type { LensSummary } from '../../types/lens'
import Tokens from '../common/Tokens'
import JobProgress from './JobProgress'

export default function MassMeanDetails({ session, lens, disabled }: { session: string; lens: LensSummary; disabled: boolean }) {
  const { details, missing, error, runner, compute } = useLensDetails(session, lens.name, false,
    !!lens.details?.includes('mass_mean'))
  const found = details?.kind === 'mass_mean' ? details : null
  const layers = useMemo(() => (found ? Object.keys(found.layers).map(Number).sort((a, b) => a - b) : []), [found])
  const [picked, setPicked] = useState<number | null>(null)
  const layer = picked ?? layers[layers.length - 1] // the logit lens reads most clearly near the output
  const box = useRef<HTMLDivElement>(null)
  const labelA = lens.contrast?.label_a ?? 'A'
  const labelB = lens.contrast?.label_b ?? 'B'

  const option = useMemo<echarts.EChartsOption | null>(() => {
    if (!found) return null
    const aligned = layers.filter(l => found.layers[String(l)].router_alignment)
    const read = (l: number) => found.layers[String(l)].router_alignment!
    return {
      title: { text: "The axis's effect on the next layer's routing, against random directions", left: 'center', textStyle: { fontSize: 12 } },
      tooltip: {
        trigger: 'axis',
        formatter: (params: unknown) => {
          const first = (params as { dataIndex: number }[])[0]
          const l = aligned[first.dataIndex]
          const a = read(l)
          return `L${l} → router L${l + 1}<br/>${a.ratio}× the random median<br/>above ${a.percentile}% of random directions`
            + `<br/>random 95th percentile: ${a.random_95}×`
        },
      },
      legend: { bottom: 0, textStyle: { fontSize: 10 } },
      grid: { left: 40, right: 36, top: 28, bottom: 40 },
      xAxis: { type: 'category', data: aligned.map(l => `L${l}`), axisLabel: { fontSize: 9 } },
      yAxis: { type: 'value', min: 0, name: '× random median', nameTextStyle: { fontSize: 9 }, axisLabel: { fontSize: 9 } },
      series: [
        { name: 'axis', type: 'line', data: aligned.map(l => read(l).ratio),
          markLine: { silent: true, symbol: 'none', data: [{ yAxis: 1, name: 'random median' }], lineStyle: { type: 'dotted', color: '#9ca3af' } } },
        { name: 'random 95th percentile', type: 'line', data: aligned.map(l => read(l).random_95),
          lineStyle: { type: 'dashed' }, symbol: 'none' },
      ],
      animation: false,
    }
  }, [found, layers])

  useEffect(() => {
    if (!box.current || !option) return
    const chart = echarts.getInstanceByDom(box.current) ?? echarts.init(box.current)
    chart.setOption(option, true)
  }, [option])
  useEffect(() => {
    const element = box.current
    return () => { if (element) echarts.getInstanceByDom(element)?.dispose() }
  }, [])

  const tokens = found && layer !== undefined ? found.layers[String(layer)]?.logit_lens : undefined
  return (
    <div className="space-y-1 pt-2 border-t border-gray-100">
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-gray-800">Routing and tokens</span>
        {(missing || details) && (
          <button onClick={compute} disabled={disabled || runner.running || runner.starting}
            className="px-2 py-0.5 text-[11px] rounded border border-blue-500 text-blue-700 hover:bg-blue-50 disabled:border-gray-300 disabled:text-gray-400">
            {details ? 'Work out again' : 'Work out'}
          </button>
        )}
      </div>
      {missing && !runner.job && (
        <p className="text-[11px] text-gray-500">Not worked out yet: the axis against each next layer's router, and the
          tokens each class's mean favours (about a minute, on the CPU).</p>
      )}
      {error && <p className="text-xs text-red-600">{error}</p>}
      {runner.error && <p className="text-xs text-red-600">{runner.error}</p>}
      {runner.job && <JobProgress job={runner.job} title="Routing and tokens" onCancel={runner.running ? runner.cancel : undefined} />}
      <div ref={box} style={{ height: found ? 220 : 0 }} />
      {found && (
        <p className="text-[11px] text-gray-500">
          Each point: how much the axis, pushed through the next layer's router, spreads its expert scores, as a
          multiple of a random direction of the same length (the median of 1,000). Above the dashed line (their 95th
          percentile), the routers single the concept out; below it, the concept rides in what they mostly ignore, and
          below the dotted line the routers see it less than a random direction. It skips the next layer's attention.
        </p>
      )}
      {tokens && (
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-[11px]">
            <span className="font-semibold text-gray-700">Logit lens at</span>
            <select value={layer} onChange={e => setPicked(Number(e.target.value))}
              className="px-1 py-0.5 text-[11px] border border-gray-300 rounded">
              {layers.map(l => <option key={l} value={l}>L{l}</option>)}
            </select>
          </div>
          <div className="text-[10px] text-gray-500">{labelB} favours, more than {labelA}</div>
          <Tokens tokens={tokens.b_over_a} unit={`logit above ${labelA}`} />
          <div className="text-[10px] text-gray-500">{labelA} favours, more than {labelB}</div>
          <Tokens tokens={tokens.a_over_b} unit={`logit above ${labelB}`} />
        </div>
      )}
    </div>
  )
}
