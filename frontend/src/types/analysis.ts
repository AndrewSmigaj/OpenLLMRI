import type { ProbeExample, SankeyLink, SankeyNode, TopRoute } from './api'

/**
 * What a click on a Sankey node, a Sankey link or a trajectory point hands to the card.
 * The node and link fields come from the route analysis; the rest is added by the click
 * handlers (MultiSankeyView, ClusterRoutesSection).
 */
export interface SelectedElementData {
  name?: string
  id?: string
  layer?: number
  expert_id?: number
  cluster_id?: number
  token_count?: number
  value?: number
  count?: number
  probability?: number
  label?: string
  label_distribution?: Record<string, number>
  target_word_distribution?: Record<string, number>
  category_distributions?: Record<string, Record<string, number>>
  specialization?: string
  tokens?: ProbeExample[]
  example_tokens?: ProbeExample[]
  probe_ids?: string[]
  // Added by the click handlers
  source?: string
  target?: string
  route_signature?: string
  signature?: string
  probe_id?: string
  population?: number
  coverage?: number
  flow?: number
  avg_confidence?: number
  clusterId?: number
  expertId?: number
  _fullData?: SankeyNode | SankeyLink | ProbeExample
  _routeInfo?: TopRoute
  _totalProbes?: number
  _window?: string
}

export type SelectedCard = {
  type: 'expert' | 'highway' | 'cluster' | 'route'
  data: SelectedElementData
}
