// One Sankey over every layer of a lens (or a legacy schema) and the output column. It replaces
// the four fixed six-layer windows, whose edges cut flows (DESIGN.md E5). The cluster and expert
// charts each use one; their parent sizes both alike, so their columns line up as they scroll.
import { useMemo } from 'react'
import type * as echarts from 'echarts'
import type { RouteAnalysisResponse } from '../../types/api'
import type { Lit } from '../../utils/lighting'
import { linkSelection, nodeSelection } from '../../utils/selection'
import { orderByBarycentre } from '../../utils/sankeyOrder'
import SankeyChart from './SankeyChart'
import { topLinks, type SankeyColours } from './sankeyOption'

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
  outlined?: Record<string, number> // nodes to outline, with a count each
  lit?: Lit | null // what a selection lights (its links are kept even when the top-N trim drops them)
  ghosts?: Lit | null // nodes and links only read items take
  onSelect: (selection: string) => void
  onChartReady?: (chart: echarts.ECharts | null) => void
}

export default function AllLayerSankeyView({ routes, geometry, colours, top, keepOrder, outlined, lit, ghosts, onSelect, onChartReady }: AllLayerSankeyViewProps) {
  const nodes = useMemo(() => (keepOrder ? routes.nodes : orderByBarycentre(routes.nodes, routes.links)), [routes, keepOrder])
  const links = useMemo(() => (top ? topLinks(routes.links, top, lit) : routes.links), [routes, top, lit])

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
        outlined={outlined}
        lit={lit}
        ghosts={ghosts}
        onNodeClick={id => onSelect(nodeSelection(id))}
        onLinkClick={link => onSelect(linkSelection(link.source, link.target))}
        onChartReady={onChartReady}
      />
    </div>
  )
}
