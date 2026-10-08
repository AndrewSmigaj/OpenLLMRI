// One Sankey over every layer of a lens (or a legacy schema) and the output column. It replaces
// the four fixed six-layer windows, whose edges cut flows (DESIGN.md E5). The cluster and expert
// charts each use one; their parent sizes both alike, so their columns line up as they scroll.
import { useMemo } from 'react'
import type * as echarts from 'echarts'
import type { RouteAnalysisResponse, SankeyLink } from '../../types/api'
import { isOutputLink } from '../../constants/outputNodes'
import { linkSelection, nodeSelection } from '../../utils/selection'
import { orderByBarycentre } from '../../utils/sankeyOrder'
import SankeyChart, { type SankeyColours } from './SankeyChart'

export interface SankeyGeometry {
  width: number // the chart's full width, in pixels
  height: number
  left: number // margins, in pixels
  right: number
  nodeWidth: number
  showLabels: boolean
}

interface AllLayerSankeyViewProps {
  routes: RouteAnalysisResponse
  geometry: SankeyGeometry
  colours: SankeyColours
  top?: number | null // links kept per layer; null or undefined keeps all
  keepOrder?: boolean // draw the nodes in the order given (the experts' fixed order)
  onSelect: (selection: string) => void
  onChartReady?: (chart: echarts.ECharts | null) => void
}

// The strongest `n` links leaving each layer, plus every link into the output column.
function topLinks(links: SankeyLink[], n: number): SankeyLink[] {
  const byLayer = new Map<string, SankeyLink[]>()
  const kept: SankeyLink[] = []
  for (const link of links) {
    if (isOutputLink(link)) { kept.push(link); continue }
    const layer = /^L(\d+)/.exec(link.source)?.[1] ?? ''
    byLayer.set(layer, [...(byLayer.get(layer) ?? []), link])
  }
  for (const group of byLayer.values()) {
    kept.push(...[...group].sort((a, b) => b.value - a.value).slice(0, n))
  }
  return kept
}

export default function AllLayerSankeyView({ routes, geometry, colours, top, keepOrder, onSelect, onChartReady }: AllLayerSankeyViewProps) {
  const nodes = useMemo(() => (keepOrder ? routes.nodes : orderByBarycentre(routes.nodes, routes.links)), [routes, keepOrder])
  const links = useMemo(() => (top ? topLinks(routes.links, top) : routes.links), [routes, top])

  return (
    <div style={{ width: geometry.width }}>
      <SankeyChart
        nodes={nodes}
        links={links}
        colours={colours}
        width={geometry.width}
        height={geometry.height}
        left={geometry.left}
        right={geometry.right}
        nodeWidth={geometry.nodeWidth}
        showLabels={geometry.showLabels}
        onNodeClick={id => onSelect(nodeSelection(id))}
        onLinkClick={link => onSelect(linkSelection(link.source, link.target))}
        onChartReady={onChartReady}
      />
    </div>
  )
}
