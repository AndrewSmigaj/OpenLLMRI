// The 3-D view in the lens's own space (DESIGN.md E5): each item's trajectory through the layers in
// view, every layer's cloud on the lens's three main directions, lined up with the layer before
// (the backend's frame), drawn side by side with one scale on all three axes so every cloud keeps
// its true shape. One chart instance, so the camera survives redraws until Fit; one line series for
// every trajectory; lit items drawn over faded ones; items read through the lens with their own
// marker. Colours, the sample and the lit items come from the page, so the view says nothing of
// any one study.
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import 'echarts-gl'
import type { LensTrajectory, TrajectoryItem } from '../../types/lens'
import { layout3d, sample3d, type Point3 } from '../../utils/trajectory3d'

// What an export needs: the drawn chart, one row per item and layer, and the camera
export interface TrajectoryExport {
  chart: echarts.ECharts
  rows: Record<string, unknown>[]
  camera: Record<string, unknown> | null
  sample: number
}

interface SteppedTrajectoryPlotProps {
  data: LensTrajectory
  layers: number[] // the layers in view, as the Sankeys show them
  colourOf: (item: TrajectoryItem, layer: number) => string // a point's colour at a layer
  groupOf: (item: TrajectoryItem) => string // its colour value, so the sample keeps each value's share
  nodeOf: (probeId: string, layer: number) => number | undefined
  shapeOf?: (item: TrajectoryItem) => string | undefined // a value on the shape axis, drawn as a symbol
  shapeValues?: string[]
  sampleSize: number
  lit: Set<string> // drawn over everything else, which fades
  showRead: boolean // draw the reading's items
  onPick: (probeId: string) => void
  onExportable?: (handle: TrajectoryExport | null) => void
}

// A scatter point's value: x, y, z, then what the tooltip and a click read back
type PointValue = [number, number, number, string, number, string]

const READ_MARK = 'diamond'
const HALO = '#111827'
const SHAPE_SYMBOLS = ['circle', 'triangle', 'diamond', 'rect', 'pin', 'arrow']
// The camera starts nearly in front of the layers, which run left to right, and far enough back to
// fit the scene to the canvas (echarts-gl's camera sees 50 degrees from top to bottom)
const CAMERA = { alpha: 20, beta: 0 }
const HALF_FOV = Math.tan((50 / 2) * Math.PI / 180)
function fitDistance(box: { boxWidth: number; boxDepth: number; boxHeight: number }, width: number, height: number) {
  const aspect = Math.max(0.2, width / Math.max(1, height))
  return 1.35 * Math.max(box.boxWidth / 2 / (HALF_FOV * aspect), box.boxHeight / 2 / HALF_FOV) + box.boxDepth / 2
}

interface Drawn { item: TrajectoryItem; points: Point3[]; read: boolean }

export default function SteppedTrajectoryPlot({ data, layers, colourOf, groupOf, nodeOf, shapeOf, shapeValues, sampleSize,
                                               lit, showRead, onPick, onExportable }: SteppedTrajectoryPlotProps) {
  const boxRef = useRef<HTMLDivElement>(null)
  const chartRef = useRef<echarts.ECharts | null>(null)
  const placedOnce = useRef(false) // the camera is set on the first draw and by Fit, never by a redraw
  const [spacing, setSpacing] = useState(1.2)
  const [scale, setScale] = useState(1)
  const [pointSize, setPointSize] = useState(3)
  const [showLines, setShowLines] = useState(true)
  const [fitTick, setFitTick] = useState(0)
  const onPickRef = useRef(onPick)
  onPickRef.current = onPick
  const onExportableRef = useRef(onExportable)
  onExportableRef.current = onExportable

  // One chart for the life of the view; it follows its panel's size
  useEffect(() => {
    if (!boxRef.current) return
    const chart = echarts.init(boxRef.current)
    chartRef.current = chart
    chart.on('click', params => {
      const value = params.value as PointValue | undefined
      if (params.seriesType === 'scatter3D' && value?.[3]) onPickRef.current(value[3])
    })
    const observer = new ResizeObserver(() => requestAnimationFrame(() => chart.resize()))
    observer.observe(boxRef.current)
    return () => {
      observer.disconnect()
      onExportableRef.current?.(null)
      chart.dispose()
      chartRef.current = null
      placedOnce.current = false
    }
  }, [])

  // The items drawn and their frame points at the layers in view
  const drawn = useMemo(() => {
    const at = layers.map(layer => data.layers.indexOf(layer)).filter(li => li >= 0)
    const pick = (items: TrajectoryItem[], points: Point3[][], read: boolean): Drawn[] =>
      sample3d(items.map(item => item.probe_id), i => groupOf(items[i]), sampleSize, lit)
        .map(i => ({ item: items[i], points: at.map(li => points[i][li]), read }))
    const own = pick(data.items, data.points, false)
    const read = showRead && data.read ? pick(data.read.items, data.read.points, true) : []
    return { own, read, layers: at.map(li => data.layers[li]) }
  }, [data, layers, groupOf, sampleSize, lit, showRead])

  useEffect(() => {
    const chart = chartRef.current
    if (!chart || !drawn.own.length || drawn.layers.length < 1) return
    const layout = layout3d(drawn.own.map(d => d.points), spacing, scale)
    const everything = [...drawn.own, ...drawn.read]
    const placed = everything.map(d => d.points.map((p, li) => layout.place(p, li)))
    const all = placed.flat()
    const range = (i: number): [number, number] => [Math.min(...all.map(p => p[i])), Math.max(...all.map(p => p[i]))]
    const [x, y, z] = [range(0), range(1), range(2)]
    const unit = 100 / Math.max(y[1] - y[0], z[1] - z[0], 1e-9) // one scale on all three axes
    const box = { boxWidth: Math.max(1, unit * (x[1] - x[0])), boxDepth: unit * (y[1] - y[0]), boxHeight: unit * (z[1] - z[0]) }
    const anyLit = everything.some(d => lit.has(d.item.probe_id))

    // A point's symbol: its shape-axis value's, else a read item's own marker; with a shape axis,
    // read items keep their value's symbol and are outlined instead
    const shaped = !!shapeOf && !!shapeValues?.length
    const symbolOf = (d: Drawn) => {
      const i = shaped ? shapeValues!.indexOf(shapeOf!(d.item) ?? '') : -1
      return i >= 0 ? SHAPE_SYMBOLS[i % SHAPE_SYMBOLS.length] : d.read && !shaped ? READ_MARK : 'circle'
    }
    const pointsOf = (ds: Drawn[], offset: number, lighted: boolean) => ds.flatMap((d, k) => {
      if (anyLit ? lit.has(d.item.probe_id) !== lighted : lighted) return []
      return placed[offset + k].map((p, li) => ({
        value: [...p, d.item.probe_id, drawn.layers[li], d.read ? 'read' : 'lens'] as PointValue,
        symbol: symbolOf(d),
        itemStyle: { color: colourOf(d.item, drawn.layers[li]), opacity: anyLit && !lighted ? 0.08 : 0.9,
                     ...(d.read && shaped ? { borderWidth: 1, borderColor: '#111827' } : {}) },
      }))
    })
    // Every trajectory in one polyline: between two trajectories, a fully transparent bridge
    const lineOf = (lighted: boolean, halo = false) => everything.flatMap((d, k) => {
      if (anyLit ? lit.has(d.item.probe_id) !== lighted : lighted) return []
      const opacity = lighted ? 0.95 : anyLit ? 0.025 : 0.35 // faded lines pile up in bundles, so they fade far
      const steps = placed[k].map((p, li) => ({ value: p, lineStyle: { color: halo ? HALO : colourOf(d.item, drawn.layers[li]), opacity } }))
      return [{ value: steps[0].value, lineStyle: { color: steps[0].lineStyle.color, opacity: 0 } }, ...steps,
              { value: steps[steps.length - 1].value, lineStyle: { color: steps[0].lineStyle.color, opacity: 0 } }]
    })
    const scatter = (name: string, values: ReturnType<typeof pointsOf>, symbol: string, size: number) =>
      ({ type: 'scatter3D', name, data: values, symbol, symbolSize: size, emphasis: { itemStyle: { opacity: 1 } } })
    const line = (name: string, values: ReturnType<typeof lineOf>, width: number) =>
      ({ type: 'line3D', name, data: values, lineStyle: { width }, silent: true, animation: false })
    const labels = drawn.layers.map((layer, li) => ({
      value: [layout.origins[li], y[1], z[1]], label: { show: true, formatter: `L${layer}`, fontSize: 11, color: '#374151' },
    }))
    // A lit path keeps its colours over a dark halo, so it stands out of bundles of the same colour
    const series: Record<string, unknown>[] = [
      ...(showLines ? [line('trajectories', lineOf(false), 1), line('lit halo', lineOf(true, true), 6), line('lit', lineOf(true), 3)] : []),
      scatter('items', pointsOf(drawn.own, 0, false), 'circle', pointSize),
      scatter('read', pointsOf(drawn.read, drawn.own.length, false), READ_MARK, pointSize + 1),
      scatter('lit items', pointsOf(drawn.own, 0, true), 'circle', pointSize + 3),
      scatter('lit read', pointsOf(drawn.read, drawn.own.length, true), READ_MARK, pointSize + 4),
      { type: 'scatter3D', name: 'layers', data: labels, symbolSize: 0, silent: true },
    ]
    const hidden = { axisLabel: { show: false }, axisTick: { show: false }, splitLine: { show: false },
                     axisLine: { lineStyle: { color: '#d1d5db' } }, axisPointer: { show: false }, name: '' }
    const distance = fitDistance(box, boxRef.current?.clientWidth ?? 800, boxRef.current?.clientHeight ?? 300)
    const camera = { ...CAMERA, distance, minDistance: 5, maxDistance: distance * 8 }
    chart.setOption({
      tooltip: {
        formatter: (params: echarts.DefaultLabelFormatterCallbackParams) => {
          const [, , , probeId, layer, kind] = params.value as PointValue
          if (!probeId) return ''
          const item = everything.find(d => d.item.probe_id === probeId)?.item
          const node = nodeOf(probeId, layer)
          return `<strong>${item?.label ?? ''}</strong> · ${probeId}<br/>L${layer}${node !== undefined ? ` · node C${node}` : ''}
            ${kind === 'read' ? '<br/>read through the lens' : ''}<br/><em>Click to light its path</em>`
        },
      },
      xAxis3D: { type: 'value', min: x[0], max: x[1], ...hidden },
      yAxis3D: { type: 'value', min: y[0], max: y[1], ...hidden },
      zAxis3D: { type: 'value', min: z[0], max: z[1], ...hidden },
      grid3D: {
        ...box, axisPointer: { show: false },
        ...(placedOnce.current ? {} : { viewControl: camera }),
        light: { main: { intensity: 1.0 }, ambient: { intensity: 0.5 } },
      },
      series,
    }, { replaceMerge: ['series'] })
    placedOnce.current = true

    const viewControl = (chart.getOption() as { grid3D?: { viewControl?: Record<string, unknown> }[] }).grid3D?.[0]?.viewControl
    onExportableRef.current?.({
      chart, sample: sampleSize,
      camera: viewControl ? { alpha: viewControl.alpha, beta: viewControl.beta, distance: viewControl.distance } : null,
      rows: everything.flatMap(d => d.points.map((p, li) => ({
        probe_id: d.item.probe_id, label: d.item.label, step: d.item.step, ...d.item.categories,
        layer: drawn.layers[li], node: nodeOf(d.item.probe_id, drawn.layers[li]), colour: colourOf(d.item, drawn.layers[li]),
        frame_1: p[0], frame_2: p[1], frame_3: p[2], lit: lit.has(d.item.probe_id), read: d.read,
      }))),
    })
  }, [drawn, spacing, scale, pointSize, showLines, colourOf, nodeOf, shapeOf, shapeValues, lit, sampleSize])

  // Fit puts the camera back where it starts, fitted to the panel's size now
  useEffect(() => {
    if (!fitTick || !chartRef.current) return
    const grid = (chartRef.current.getOption() as { grid3D?: { boxWidth: number; boxDepth: number; boxHeight: number }[] }).grid3D?.[0]
    if (!grid) return
    const distance = fitDistance(grid, boxRef.current?.clientWidth ?? 800, boxRef.current?.clientHeight ?? 300)
    chartRef.current.setOption({ grid3D: { viewControl: { ...CAMERA, distance, maxDistance: distance * 8 } } })
  }, [fitTick])

  const range = 'w-20 accent-blue-600'
  return (
    <div className="h-full flex flex-col min-h-0">
      <div className="flex flex-wrap items-center gap-3 text-xs text-gray-500 flex-shrink-0">
        <label className="flex items-center gap-1" title="The gap between layers, as a factor on the gap that keeps clouds apart">
          Spacing
          <input type="range" min="1" max="5" step="0.1" value={spacing} onChange={e => setSpacing(Number(e.target.value))} className={range} />
        </label>
        <label className="flex items-center gap-1" title="Each cloud's size, the same on all three axes, so its shape holds">
          Scale
          <input type="range" min="0.5" max="3" step="0.1" value={scale} onChange={e => setScale(Number(e.target.value))} className={range} />
        </label>
        <label className="flex items-center gap-1">
          Points
          <input type="range" min="1" max="10" step="0.5" value={pointSize} onChange={e => setPointSize(Number(e.target.value))} className={range} />
        </label>
        <label className="flex items-center gap-1 cursor-pointer">
          <input type="checkbox" checked={showLines} onChange={e => setShowLines(e.target.checked)} className="w-3 h-3" />
          Lines
        </label>
        <button onClick={() => setFitTick(t => t + 1)} className="px-1.5 py-0.5 rounded bg-gray-100 text-gray-700 hover:bg-gray-200"
          title="Put the camera back where it starts">Fit</button>
        {showRead && data.read && <span className="text-gray-400">◆ read through the lens</span>}
      </div>
      <div ref={boxRef} className="flex-1 min-h-0" />
    </div>
  )
}
