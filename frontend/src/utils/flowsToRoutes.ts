// Converts the lens API's all-layer flows into the route shape the Sankey chart, the cards and
// the contingency table already read, so they work unchanged on every layer at once.
import type { DynamicAxis, RouteAnalysisResponse, SankeyLink, SankeyNode } from '../types/api'
import type { AxisCounts, FlowLink, FlowNode, LensFlows } from '../types/lens'

// The label's counts, the other designed axes' counts, and for the output column the counts on
// the output's own axes (kept apart: an output axis may share a designed axis's name)
function split(counts: AxisCounts | undefined, outputCounts?: AxisCounts) {
  const { label, ...categories } = counts ?? {}
  return { label_distribution: label ?? {}, category_distributions: categories, output_distributions: outputCounts }
}

function toNode(node: FlowNode, layer: number, outputCounts?: AxisCounts): SankeyNode {
  return {
    name: node.id, id: node.id, layer, expert_id: node.index, token_count: node.count,
    specialization: '', weight: node.weight, ...split(node.counts, outputCounts),
  }
}

function toLink(link: FlowLink, sourceCount: number): SankeyLink {
  return {
    source: link.source, target: link.target, value: link.count, token_count: link.count,
    probability: sourceCount > 0 ? link.count / sourceCount : 0,
    route_signature: `${link.source}→${link.target}`, ...split(link.counts, link.output_counts),
  }
}

function axesOf(axes: Record<string, string[]>): DynamicAxis[] {
  return Object.entries(axes).map(([id, values]) => ({
    id, label: id, label_a: values[0] ?? '', label_b: values[1] ?? '', values,
  }))
}

export function flowsToRoutes(flows: LensFlows, sessionId: string): RouteAnalysisResponse {
  const counts = new Map(flows.nodes.map(n => [n.id, n.count]))
  const lastLayer = flows.layers[flows.layers.length - 1]
  const nodes = flows.nodes.map(n => toNode(n, n.layer))
  const links = flows.links.map(l => toLink(l, counts.get(l.source) ?? 0))
  if (flows.output) {
    nodes.push(...flows.output.nodes.map(n => toNode({ ...n, index: -1 }, lastLayer + 1, n.output_counts)))
    links.push(...flows.output.links.map(l => toLink(l, counts.get(l.source) ?? 0)))
  }
  const totalProbes = flows.nodes.filter(n => n.layer === flows.layers[0]).reduce((s, n) => s + n.count, 0)
  return {
    session_id: sessionId, window_layers: flows.layers, nodes, links, top_routes: [],
    statistics: { total_routes: links.length, total_probes: totalProbes, routes_coverage: 1, window_layers: flows.layers },
    available_axes: axesOf(flows.axes), output_available_axes: flows.output ? axesOf(flows.output.axes) : [],
    probe_assignments: flows.assignments,
    output_of: flows.output_of,
  }
}
