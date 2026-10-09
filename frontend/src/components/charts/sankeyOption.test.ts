import { describe, expect, it } from 'vitest'
import type { SankeyLink, SankeyNode } from '../../types/api'
import { clusterPath, litFlows, litItems } from '../../utils/lighting'
import { FADED_LINK, FADED_NODE, nodeFill, sankeyOption, topLinks, type SankeyColours } from './sankeyOption'

// Three items over two layers: a and b take L0C0 → L1C0, c takes L0C1 → L1C1
const node = (id: string, layer: number, count: number): SankeyNode =>
  ({ id, name: id, layer, expert_id: Number(id.slice(-1)), token_count: count, specialization: '', label_distribution: { x: count } })
const link = (source: string, target: string, value: number): SankeyLink =>
  ({ source, target, value, probability: 1, route_signature: `${source}→${target}`, token_count: value, label_distribution: { x: value } })
const nodes = [node('L0C0', 0, 2), node('L0C1', 0, 1), node('L1C0', 1, 2), node('L1C1', 1, 1)]
const links = [link('L0C0', 'L1C0', 2), link('L0C1', 'L1C1', 1)]
const assignments = { a: { '0': 0, '1': 0 }, b: { '0': 0, '1': 0 }, c: { '0': 1, '1': 1 } }
const colours: SankeyColours = { input: { axis: 'label', values: ['x'], gradient: 'red-blue' }, output: null, stripes: false }
const layout = { nodeWidth: 6, left: 0, right: 0, showLabels: true }

type Series = { data: { id: string; value: number; itemStyle: { color?: unknown; opacity?: number; borderWidth?: number } }[];
                links: { source: string; lineStyle: { opacity: number } }[] }
const seriesOf = (option: ReturnType<typeof sankeyOption>) => (option.series as Series[])[0]

describe('sankeyOption', () => {
  it('lighting an item fades everything off its path and keeps every node its size', () => {
    const lit = litFlows(litItems('probe:c', assignments), clusterPath(assignments, [0, 1]))
    const plain = seriesOf(sankeyOption({ nodes, links, colours, ...layout }))
    const lighted = seriesOf(sankeyOption({ nodes, links, colours, ...layout, lit }))
    expect(lighted.data.map(n => n.value)).toEqual(plain.data.map(n => n.value))
    const opacity = Object.fromEntries(lighted.data.map(n => [n.id, n.itemStyle.opacity]))
    expect(opacity).toEqual({ L0C0: FADED_NODE, L0C1: 1, L1C0: FADED_NODE, L1C1: 1 })
    const linkOpacity = Object.fromEntries(lighted.links.map(l => [l.source, l.lineStyle.opacity]))
    expect(linkOpacity.L0C1).toBeCloseTo(0.95) // one item, fully lit
    expect(linkOpacity.L0C0).toBe(FADED_LINK)
    expect(plain.data.every(n => n.itemStyle.opacity === undefined)).toBe(true) // nothing lit, nothing faded
  })

  it("a bundle's links show by their share of the lit items, and outlines stay", () => {
    const lit = litFlows(['a', 'b', 'c'], clusterPath(assignments, [0, 1]))
    const lighted = seriesOf(sankeyOption({ nodes, links, colours, ...layout, lit, outlined: { L1C0: 1 } }))
    const linkOpacity = Object.fromEntries(lighted.links.map(l => [l.source, l.lineStyle.opacity]))
    expect(linkOpacity.L0C0).toBeCloseTo(0.35 + 0.6 * (2 / 3))
    expect(linkOpacity.L0C1).toBeCloseTo(0.35 + 0.6 * (1 / 3))
    expect(lighted.data.find(n => n.id === 'L1C0')?.itemStyle.borderWidth).toBe(2)
  })

  it('the top-N trim keeps a lit link it would otherwise drop', () => {
    expect(topLinks(links, 1).map(l => l.source)).toEqual(['L0C0'])
    const lit = litFlows(['c'], clusterPath(assignments, [0, 1]))
    expect(topLinks(links, 1, lit).map(l => l.source).sort()).toEqual(['L0C0', 'L0C1'])
  })

  it("the 3-D view colours a node's points as the Sankey colours the node", () => {
    const drawn = seriesOf(sankeyOption({ nodes, links, colours, ...layout }))
    for (const node of nodes) {
      expect(drawn.data.find(n => n.id === node.id)?.itemStyle.color).toBe(nodeFill(node, colours))
    }
  })
})
