// What a selection lights (DESIGN.md E5; Watch draws a tick's path the same way, E4): the items
// the selection stands for, then the nodes and links those items take through a chart, each with
// how many of them take it. One item lights one path; a node lights its members' bundle, each link
// weighted by its share of them. Pure functions: the charts only draw the result.

// A node id per column for one item ("L3C2", "L3E17", "Generated:yes"); null where it has none
export type PathOf = (item: string) => (string | null)[]

export interface Lit {
  nodes: Record<string, number> // node id: lit items through it
  links: Record<string, number> // "source>target": lit items along it
  total: number // the lit items
}

export const EMPTY_LIT: Lit = { nodes: {}, links: {}, total: 0 }

export const linkKey = (source: string, target: string) => `${source}>${target}`

// The nodes and links a set of items takes, counted
export function litFlows(items: string[], pathOf: PathOf): Lit {
  const nodes: Record<string, number> = {}
  const links: Record<string, number> = {}
  for (const item of items) {
    const path = pathOf(item)
    path.forEach((node, i) => {
      if (!node) return
      nodes[node] = (nodes[node] ?? 0) + 1
      const next = path[i + 1]
      if (next) links[linkKey(node, next)] = (links[linkKey(node, next)] ?? 0) + 1
    })
  }
  return { nodes, links, total: items.length }
}

// How strongly a lit link shows: a single path fully, a bundle's links by their share of the items
export const litOpacity = (count: number, total: number) => (total > 0 ? 0.35 + 0.6 * Math.min(1, count / total) : 0)

// The cluster chart's path for one item: its node at each layer, then its output node
export function clusterPath(assignments: Record<string, Record<string, number>> | undefined, layers: number[],
                            outputOf?: Record<string, string>): PathOf {
  return item => {
    const nodes: (string | null)[] = layers.map(layer => {
      const node = assignments?.[item]?.[String(layer)]
      return node === undefined ? null : `L${layer}C${node}`
    })
    if (outputOf) nodes.push(outputOf[item] !== undefined ? `Generated:${outputOf[item]}` : null)
    return nodes
  }
}

// The expert chart's path for one item at one rank: its expert at each layer, then its output node
export function expertPath(experts: Record<string, Record<string, number>> | undefined, layers: number[],
                           outputOf?: Record<string, string>): PathOf {
  return item => {
    const nodes: (string | null)[] = layers.map(layer => {
      const expert = experts?.[item]?.[String(layer)]
      return expert === undefined ? null : `L${layer}E${expert}`
    })
    if (outputOf) nodes.push(outputOf[item] !== undefined ? `Generated:${outputOf[item]}` : null)
    return nodes
  }
}

type Assignments = Record<string, Record<string, number>>

// The items a selection stands for: an item; a cluster node's, an expert's (at the chart's rank)
// or a link's members; an output node's items
export function litItems(selection: string, assignments: Assignments | undefined,
                         outputOf?: Record<string, string>, experts?: Assignments): string[] {
  if (!selection) return []
  if (selection.startsWith('probe:')) return [selection.slice('probe:'.length)]
  const items = Object.keys(assignments ?? experts ?? {})
  const at = (id: string): ((item: string) => boolean) | null => {
    if (id.startsWith('Generated:')) {
      const value = id.slice('Generated:'.length)
      return item => outputOf?.[item] === value
    }
    const found = /^L(\d+)([CE])(\d+)$/.exec(id)
    if (!found) return null
    const [, layer, kind, index] = found
    const source = kind === 'C' ? assignments : experts
    return item => source?.[item]?.[layer] === Number(index)
  }
  if (selection.includes('>')) {
    const [source, target] = selection.split('>')
    const first = at(source)
    const second = at(target)
    return first && second ? items.filter(item => first(item) && second(item)) : []
  }
  const member = at(selection)
  return member ? items.filter(member) : []
}

// Where an item sits in time: its step and its run (a run's items share it, one per step)
export interface ItemPlace {
  step?: number | null
  run?: string | null
}

// The selection's population at one step (DESIGN.md E5; null keeps every step): an item stands for
// its run's item at that step; a node's, a link's or an output's members are those at that step
export function atStep(items: string[], selection: string, step: number | null,
                       places: Record<string, ItemPlace>): string[] {
  if (step === null) return items
  if (selection.startsWith('probe:') && items.length) {
    const run = places[items[0]]?.run
    if (run) return Object.keys(places).filter(item => places[item].run === run && places[item].step === step)
  }
  return items.filter(item => places[item]?.step === step)
}

// What read items take that the lens's own items never do: nodes and links missing from the
// chart, each with how many read items take it. The chart draws them as ghosts once a reading
// loads, never as the lighting changes, so nothing moves while things are selected.
export function ghostFlows(items: string[], pathOf: PathOf, nodes: Set<string>, links: Set<string>): Lit {
  const taken = litFlows(items, pathOf)
  const keep = (counts: Record<string, number>, present: Set<string>) =>
    Object.fromEntries(Object.entries(counts).filter(([id]) => !present.has(id)))
  return { nodes: keep(taken.nodes, nodes), links: keep(taken.links, links), total: items.length }
}

// A reading's items as lighting reads them: each item's node and its expert at the reading's rank
// at every layer, and its output category
export function readMaps(reading: { layers: number[]; items: { probe_id: string; output_category?: string | null }[];
                                    nodes: number[][]; experts: number[][] }) {
  const assignments: Assignments = {}
  const experts: Assignments = {}
  const outputOf: Record<string, string> = {}
  reading.items.forEach((item, i) => {
    assignments[item.probe_id] = Object.fromEntries(reading.layers.map((layer, li) => [String(layer), reading.nodes[i][li]]))
    experts[item.probe_id] = Object.fromEntries(reading.layers.map((layer, li) => [String(layer), reading.experts[i][li]]))
    if (item.output_category) outputOf[item.probe_id] = item.output_category
  })
  return { assignments, experts, outputOf, ids: reading.items.map(item => item.probe_id) }
}

// Each item's step and run, from the capture's sentences and any reading's items
export function placesOf(...sources: { probe_id: string; step?: number | null; run?: string | null }[][]): Record<string, ItemPlace> {
  const places: Record<string, ItemPlace> = {}
  for (const source of sources) {
    for (const item of source) places[item.probe_id] = { step: item.step ?? null, run: item.run ?? null }
  }
  return places
}
