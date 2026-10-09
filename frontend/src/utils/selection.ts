// The selection is one string in the URL: a node id (L3C2, L3E17, Generated:yes), a link
// ("source>target"), one item ("probe:<id>") or an expert pipeline ("pipe:P3"). These helpers read
// it and say which items it holds.
import { isOutputNode, stripOutputPrefix } from '../constants/outputNodes'
import type { MembersQuery } from '../types/lens'

export type Selection =
  | { kind: 'node'; id: string }
  | { kind: 'link'; source: string; target: string }
  | { kind: 'probe'; probeId: string }
  | { kind: 'pipe'; id: string }

const PROBE = 'probe:'
const PIPE = 'pipe:'

export function parseSelection(sel: string): Selection | null {
  if (!sel) return null
  if (sel.startsWith(PROBE)) return { kind: 'probe', probeId: sel.slice(PROBE.length) }
  if (sel.startsWith(PIPE)) return { kind: 'pipe', id: sel.slice(PIPE.length) }
  const [source, target] = sel.split('>')
  return target ? { kind: 'link', source, target } : { kind: 'node', id: source }
}

export const nodeSelection = (id: string) => id
export const linkSelection = (source: string, target: string) => `${source}>${target}`
export const probeSelection = (probeId: string) => `${PROBE}${probeId}`
export const pipeSelection = (id: string) => `${PIPE}${id}`

// "L3C2" -> layer 3, a cluster, 2; "L3E17" -> layer 3, an expert, 17
export function parseNodeId(id: string): { layer: number; kind: 'cluster' | 'expert'; index: number } | null {
  const m = /^L(\d+)([CE])(\d+)$/.exec(id)
  return m ? { layer: Number(m[1]), kind: m[2] === 'C' ? 'cluster' : 'expert', index: Number(m[3]) } : null
}

// Which chart a selection belongs to; output nodes belong to both, and are read from the cluster chart.
export function selectionKind(selection: Selection): 'cluster' | 'expert' | null {
  if (selection.kind === 'probe' || selection.kind === 'pipe') return null
  const id = selection.kind === 'node' ? selection.id : selection.source
  return isOutputNode(id) ? 'cluster' : parseNodeId(id)?.kind ?? null
}

// The members query for a node or a link; `lastLayer` places the output column, `rank` the experts.
export function membersQuery(selection: Selection, lastLayer: number, rank: number): MembersQuery | null {
  if (selection.kind === 'probe' || selection.kind === 'pipe') return null
  const source = selection.kind === 'node' ? selection.id : selection.source
  if (isOutputNode(source)) return { layer: lastLayer, output: stripOutputPrefix(source) }
  const from = parseNodeId(source)
  if (!from) return null
  const query: MembersQuery = from.kind === 'cluster'
    ? { layer: from.layer, node: from.index }
    : { layer: from.layer, expert: from.index, rank }
  if (selection.kind === 'link') {
    if (isOutputNode(selection.target)) return { ...query, output: stripOutputPrefix(selection.target) }
    const to = parseNodeId(selection.target)
    if (!to) return null
    return from.kind === 'cluster' ? { ...query, to_node: to.index } : { ...query, to_expert: to.index }
  }
  return query
}
