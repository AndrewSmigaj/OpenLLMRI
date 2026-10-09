// The details card for a selection, built from the loaded flows in the shape the card reads, and
// the key of a legacy schema's written description for it.
import { isOutputNode } from '../constants/outputNodes'
import type { SelectedCard } from '../types/analysis'
import type { ProbeExample, RouteAnalysisResponse } from '../types/api'
import { parseNodeId, type Selection } from './selection'

export function cardFor(selection: Selection, cluster: RouteAnalysisResponse | null, expert: RouteAnalysisResponse | null,
                        sentences: ProbeExample[], examples: ProbeExample[]): SelectedCard | null {
  if (selection.kind === 'probe') {
    const sentence = sentences.find(s => s.probe_id === selection.probeId)
    if (!sentence) return null
    return {
      type: 'route',
      data: {
        _fullData: sentence, name: sentence.target_word, label: sentence.label, tokens: [sentence],
        example_tokens: [sentence], probe_id: sentence.probe_id,
        signature: `Trajectory: ${sentence.label || 'probe'} · ${sentence.target_word || ''}`,
      },
    }
  }
  if (selection.kind === 'pipe') return null // its report is the card on pipes and hubs
  const id = selection.kind === 'node' ? selection.id : selection.source
  const kind = isOutputNode(id) ? 'cluster' : parseNodeId(id)?.kind
  const routes = kind === 'expert' ? expert : cluster
  if (!routes) return null
  const total = routes.statistics.total_probes
  const coverage = (n: number) => (total > 0 ? Math.round((n / total) * 100) : 0)

  if (selection.kind === 'node') {
    const node = routes.nodes.find(n => n.id === selection.id)
    if (!node) return null
    const data = {
      ...node, population: node.token_count, coverage: coverage(node.token_count),
      _fullData: node, _totalProbes: total, tokens: examples,
    }
    return kind === 'expert'
      ? { type: 'expert', data: { ...data, expertId: node.expert_id } }
      : { type: 'cluster', data: { ...data, clusterId: isOutputNode(node.id) ? undefined : node.expert_id } }
  }
  const link = routes.links.find(l => l.source === selection.source && l.target === selection.target)
  if (!link) return null
  return {
    type: kind === 'expert' ? 'highway' : 'route',
    data: {
      ...link, signature: link.route_signature, flow: link.value, coverage: coverage(link.value),
      _fullData: link, _totalProbes: total, tokens: examples,
    },
  }
}

// Cluster 0 and expert 0 are real ids, so the key uses `??`, not `||`.
export function descriptionKey(card: SelectedCard): string {
  const d = card.data
  if (card.type === 'expert') return `expert-${d.expertId ?? d.expert_id}-L${d.layer}`
  if (card.type === 'cluster') return `cluster-${d.clusterId ?? d.cluster_id}-L${d.layer}`
  return `route-${d.signature}`
}
