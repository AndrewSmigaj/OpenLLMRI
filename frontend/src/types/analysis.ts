import type { ProbeExample, SankeyLink, SankeyNode } from './api'

/**
 * What the card shows for a selected node, link or item. The node and link fields come from
 * the flows; the rest is added when the card is built (utils/selectionCard.ts).
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
  weight?: number
  clusterId?: number
  expertId?: number
  _fullData?: SankeyNode | SankeyLink | ProbeExample
  _totalProbes?: number
}

export type SelectedCard = {
  type: 'expert' | 'highway' | 'cluster' | 'route'
  data: SelectedElementData
}
