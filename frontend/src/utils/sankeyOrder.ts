// Orders each column of an all-layer Sankey to cut crossings: the first column by size, each later
// column by where its flows come from (a forward barycentre sweep over the drawn positions).
// ECharts keeps this order when its own layout iterations are off.
import type { SankeyLink, SankeyNode } from '../types/api'

export function orderByBarycentre(nodes: SankeyNode[], links: SankeyLink[]): SankeyNode[] {
  const columns = new Map<number, SankeyNode[]>()
  for (const node of nodes) columns.set(node.layer, [...(columns.get(node.layer) ?? []), node])
  const incoming = new Map<string, SankeyLink[]>()
  for (const link of links) incoming.set(link.target, [...(incoming.get(link.target) ?? []), link])

  const centre = new Map<string, number>() // a placed node's middle, as a share of its column
  const ordered: SankeyNode[] = []
  for (const layer of [...columns.keys()].sort((a, b) => a - b)) {
    const keyed = (columns.get(layer) ?? []).map(node => {
      let sum = 0
      let weight = 0
      for (const link of incoming.get(node.id) ?? []) {
        const at = centre.get(link.source)
        if (at !== undefined) { sum += at * link.value; weight += link.value }
      }
      return { node, key: weight > 0 ? sum / weight : Infinity }
    })
    keyed.sort((a, b) => (a.key - b.key) || (b.node.token_count - a.node.token_count))
    const total = keyed.reduce((s, k) => s + k.node.token_count, 0) || 1
    let before = 0
    for (const { node } of keyed) {
      centre.set(node.id, (before + node.token_count / 2) / total)
      before += node.token_count
      ordered.push(node)
    }
  }
  return ordered
}
