// Which LLM card a Layers selection opens (backend/src/services/llm/packets.py names them): a
// cluster node (L12C0), an expert at the chart's rank (L12E5r1), a route between nodes
// (L12C0-L13C2) or experts (L12E5-L13E7r1), and, for a node whose items part ways at the next
// layer, its split point (split-L12C0). Nothing selected opens the lens report; output nodes and
// single items have no card.
import type { FlowLink, FlowNode } from '../types/lens'
import { parseNodeId, type Selection } from './selection'

export function cardIdFor(selection: Selection | null, rank: number): string | null {
  if (!selection) return 'lens'
  if (selection.kind === 'probe') return null
  if (selection.kind === 'node') {
    const node = parseNodeId(selection.id)
    if (!node) return null
    return node.kind === 'cluster' ? selection.id : `${selection.id}r${rank}`
  }
  const from = parseNodeId(selection.source)
  const to = parseNodeId(selection.target)
  if (!from || !to || from.kind !== to.kind) return null
  return `${selection.source}-${selection.target}${from.kind === 'expert' ? `r${rank}` : ''}`
}

// The backend's rule for a branch: at least 5 items and 15% of the node's (packets.py)
const SPLIT_MIN_ITEMS = 5
const SPLIT_MIN_SHARE = 0.15

// A node's split-point card id when its items part ways at the next layer, else null
export function splitCardFor(nodeId: string, nodes: FlowNode[], links: FlowLink[]): string | null {
  const node = nodes.find(n => n.id === nodeId)
  if (!node || parseNodeId(nodeId)?.kind !== 'cluster') return null
  const floor = Math.max(SPLIT_MIN_ITEMS, SPLIT_MIN_SHARE * node.count)
  const branches = links.filter(l => l.source === nodeId && parseNodeId(l.target)?.kind === 'cluster' && l.count >= floor)
  return branches.length >= 2 ? `split-${nodeId}` : null
}
