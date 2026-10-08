// The two all-layer charts, clusters above experts, in one area that scrolls sideways so their
// columns stay lined up. The first layer in view is kept in the URL.
import { useEffect, useRef, type ReactNode } from 'react'
import type * as echarts from 'echarts'
import type { RouteAnalysisResponse } from '../../types/api'
import { RANKS, type UpdateView, type ViewState } from '../../hooks/useViewState'
import { useElementSize } from '../../hooks/useElementSize'
import type { SankeyColours } from '../charts/SankeyChart'
import AllLayerSankeyView from '../charts/AllLayerSankeyView'
import ExportMenu from '../common/ExportMenu'
import type { ExportFormat } from '../../utils/exportFigure'
import { LEFT, NODE_WIDTH, RIGHT, STRIPED_NODE_WIDTH, chartWidth, columnsOf, lastFirst, spacingFor, stepsInView } from '../../utils/layerGeometry'
import { parseSelection, selectionKind } from '../../utils/selection'
import { LayerHeader } from './LayerStrip'

const CHART_HEADER = 24
const MIN_CHART = 160

interface FlowsState {
  routes: RouteAnalysisResponse | null
  loading: boolean
  error: string | null
}

interface LayerChartsProps {
  cluster: FlowsState
  expert: FlowsState
  view: ViewState
  update: UpdateView
  colours: SankeyColours
  outlined?: Record<string, number> // cluster nodes holding items raw space groups differently
  onExport: (kind: 'cluster' | 'expert', format: ExportFormat, chart: echarts.ECharts | null) => void
}

function Status({ state, height }: { state: FlowsState; height: number }) {
  return (
    <div className="flex items-center justify-center text-xs text-gray-500" style={{ height }}>
      {state.error ? <span className="text-red-600">Could not load: {state.error}</span> : 'Loading…'}
    </div>
  )
}

export default function LayerCharts({ cluster, expert, view, update, colours, outlined, onExport }: LayerChartsProps) {
  const scroller = useRef<HTMLDivElement>(null)
  const box = useElementSize(scroller)
  const charts = useRef<Record<'cluster' | 'expert', echarts.ECharts | null>>({ cluster: null, expert: null })
  const fromScroll = useRef<number | null>(null) // the layer the user's own scrolling last set
  const timer = useRef<ReturnType<typeof setTimeout> | null>(null)

  const columns = columnsOf(cluster.routes ?? expert.routes)
  const steps = stepsInView(columns.length, view.zoom)
  const nodeWidth = colours.stripes ? STRIPED_NODE_WIDTH : NODE_WIDTH
  const spacing = spacingFor(box.width, steps, nodeWidth)
  const width = chartWidth(columns.length, spacing, nodeWidth)
  const height = Math.max(MIN_CHART, Math.floor((box.height - 20 - 2 * CHART_HEADER - 8) / 2))
  const geometry = { width, height, left: LEFT, right: RIGHT, nodeWidth, showLabels: view.zoom <= 12 }
  const first = Math.min(view.layer, lastFirst(columns.length, steps))

  // The URL's first layer brings that column into view, unless the user's scrolling set it
  useEffect(() => {
    const element = scroller.current
    if (!element || !box.width) return
    if (fromScroll.current === view.layer) {
      fromScroll.current = null // used once: a later change to the same layer still scrolls
      return
    }
    element.scrollTo({ left: first * spacing, behavior: 'smooth' })
  }, [first, spacing, view.layer, box.width])

  const onScroll = () => {
    const element = scroller.current
    if (!element) return
    const layer = Math.round(element.scrollLeft / spacing)
    if (timer.current) clearTimeout(timer.current)
    timer.current = setTimeout(() => {
      if (layer === view.layer) return
      fromScroll.current = layer
      update({ layer }, { replace: true })
    }, 150)
  }
  useEffect(() => () => { if (timer.current) clearTimeout(timer.current) }, [])

  const header = (title: string, kind: 'cluster' | 'expert', extra?: ReactNode) => (
    <div className="sticky left-0 z-10 flex items-center gap-2 px-1 bg-white" style={{ height: CHART_HEADER, width: box.width || undefined }}>
      <span className="text-xs font-semibold text-gray-900">{title}</span>
      {extra}
      <ExportMenu formats={['png', 'svg', 'csv', 'json']} disabled={!(kind === 'cluster' ? cluster : expert).routes}
        onExport={format => onExport(kind, format, charts.current[kind])} />
    </div>
  )
  // An expert's id belongs to its rank, so an expert selection ends when the rank changes
  const parsed = parseSelection(view.sel)
  const expertSelected = !!parsed && selectionKind(parsed) === 'expert'
  const rankPicker = (
    <span className="flex items-center gap-0.5 text-[10px] text-gray-600">
      Rank
      {RANKS.map(rank => (
        <button key={rank} onClick={() => update({ rank, ...(expertSelected ? { sel: '' } : {}) })} aria-label={`Rank ${rank}`}
          className={`w-5 h-5 rounded ${view.rank === rank ? 'bg-gray-800 text-white' : 'bg-gray-100 hover:bg-gray-200'}`}>
          {rank}
        </button>
      ))}
    </span>
  )
  const select = (sel: string) => update({ sel })

  return (
    <div ref={scroller} onScroll={onScroll} className="h-full overflow-auto bg-white">
      <div style={{ width }}>
        <div className="sticky top-0 z-20">
          <LayerHeader columns={columns} left={LEFT} spacing={spacing} width={width} />
        </div>
        {header('Clusters', 'cluster', outlined && Object.keys(outlined).length > 0 ? (
          <span className="text-[10px] text-gray-500">outlined: nodes holding items that raw space groups differently</span>
        ) : undefined)}
        {cluster.routes
          ? <AllLayerSankeyView routes={cluster.routes} geometry={geometry} colours={colours} outlined={outlined} onSelect={select}
              onChartReady={chart => { charts.current.cluster = chart }} />
          : <Status state={cluster} height={height} />}
        <div className="h-2" />
        {header('Experts', 'expert', rankPicker)}
        {expert.routes
          ? <AllLayerSankeyView routes={expert.routes} geometry={geometry} colours={colours} top={view.top} keepOrder
              onSelect={select} onChartReady={chart => { charts.current.expert = chart }} />
          : <Status state={expert} height={height} />}
      </div>
    </div>
  )
}
