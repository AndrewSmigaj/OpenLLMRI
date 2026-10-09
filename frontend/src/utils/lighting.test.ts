import { describe, expect, it } from 'vitest'
import { atStep, chainLit, clusterPath, expertPath, ghostFlows, linkKey, litFlows, litItems, litOpacity, placesOf, readMaps } from './lighting'

const assignments = {
  a: { '0': 0, '1': 1, '2': 0 },
  b: { '0': 0, '1': 1, '2': 1 },
  c: { '0': 1, '1': 0, '2': 1 },
}
const layers = [0, 1, 2]
const outputOf = { a: 'yes', b: 'no', c: 'no' }

describe('lighting', () => {
  it('one item lights one node per layer, the links between them, and its output', () => {
    const lit = litFlows(litItems('probe:a', assignments, outputOf), clusterPath(assignments, layers, outputOf))
    expect(lit.total).toBe(1)
    expect(Object.keys(lit.nodes).sort()).toEqual(['Generated:yes', 'L0C0', 'L1C1', 'L2C0'])
    expect(lit.links).toEqual({ [linkKey('L0C0', 'L1C1')]: 1, [linkKey('L1C1', 'L2C0')]: 1, [linkKey('L2C0', 'Generated:yes')]: 1 })
  })

  it("a node lights its members' bundle, each link counted by the members that take it", () => {
    const members = litItems('L1C1', assignments, outputOf)
    expect(members.sort()).toEqual(['a', 'b'])
    const lit = litFlows(members, clusterPath(assignments, layers))
    expect(lit.nodes).toEqual({ L0C0: 2, L1C1: 2, L2C0: 1, L2C1: 1 })
    // every layer's counts add up to the bundle
    expect(lit.nodes.L2C0 + lit.nodes.L2C1).toBe(lit.total)
    expect(lit.links[linkKey('L0C0', 'L1C1')]).toBe(2)
  })

  it('a link lights the items along it, an output node its items', () => {
    expect(litItems('L1C1>L2C1', assignments)).toEqual(['b'])
    expect(litItems('Generated:no', assignments, outputOf).sort()).toEqual(['b', 'c'])
    expect(litItems('', assignments)).toEqual([])
  })

  it('the expert chart follows the rank given, and an expert lights its items', () => {
    const rank1 = { a: { '0': 5, '1': 7, '2': 7 }, b: { '0': 5, '1': 6, '2': 7 }, c: { '0': 4, '1': 7, '2': 7 } }
    expect(expertPath(rank1, layers)('a')).toEqual(['L0E5', 'L1E7', 'L2E7'])
    expect(expertPath(rank1, layers, outputOf)('a')).toEqual(['L0E5', 'L1E7', 'L2E7', 'Generated:yes'])
    expect(litItems('L1E7', assignments, outputOf, rank1).sort()).toEqual(['a', 'c'])
    expect(litItems('L0E5>L1E6', assignments, outputOf, rank1)).toEqual(['b'])
  })

  it('a single path shows fully, a bundle by its share', () => {
    expect(litOpacity(1, 1)).toBeCloseTo(0.95)
    expect(litOpacity(1, 4)).toBeCloseTo(0.5)
    expect(litOpacity(0, 0)).toBe(0)
  })

  it("with a step chosen, an item lights its run's item at that step and a node its members there", () => {
    const places = { a0: { step: 0, run: 'r1' }, a1: { step: 1, run: 'r1' }, b0: { step: 0, run: 'r2' }, b1: { step: 1, run: 'r2' } }
    expect(atStep(['a1'], 'probe:a1', 0, places)).toEqual(['a0'])
    expect(atStep(['a1'], 'probe:a1', null, places)).toEqual(['a1'])
    expect(atStep(['a0', 'a1', 'b1'], 'L3C2', 1, places).sort()).toEqual(['a1', 'b1'])
    expect(atStep(['x'], 'probe:x', 0, { x: { step: 1 } })).toEqual([]) // no run: nothing at another step
  })

  it('ghosts are what read items take and the lens never does', () => {
    const read = { r: { '0': 0, '1': 2, '2': 1 } }
    const ghosts = ghostFlows(['r'], clusterPath(read, layers), new Set(['L0C0', 'L1C1', 'L2C1']),
                              new Set([linkKey('L0C0', 'L1C1'), linkKey('L1C1', 'L2C1')]))
    expect(ghosts.nodes).toEqual({ L1C2: 1 })
    expect(ghosts.links).toEqual({ [linkKey('L0C0', 'L1C2')]: 1, [linkKey('L1C2', 'L2C1')]: 1 })
  })

  it("a reading's items light like the lens's own, and a run steps from one to the other", () => {
    const reading = { layers, items: [{ probe_id: 'a0', output_category: 'yes' }], nodes: [[1, 0, 1]], experts: [[3, 3, 4]] }
    const read = readMaps(reading)
    expect(read.assignments.a0).toEqual({ '0': 1, '1': 0, '2': 1 })
    expect(expertPath(read.experts, layers)('a0')).toEqual(['L0E3', 'L1E3', 'L2E4'])
    const places = placesOf([{ probe_id: 'a', step: 1, run: 'r1' }], [{ probe_id: 'a0', step: 0, run: 'r1' }])
    const all = { ...assignments, ...read.assignments }
    const items = atStep(litItems('probe:a', all), 'probe:a', 0, places)
    expect(items).toEqual(['a0'])
    expect(Object.keys(litFlows(items, clusterPath(all, layers)).nodes).sort()).toEqual(['L0C1', 'L1C0', 'L2C1'])
  })

  it("a pipeline lights its members' bundle, and its own chain in the expert chart", () => {
    expect(litItems('pipe:P1', assignments, outputOf, undefined, { P1: ['a', 'c'] })).toEqual(['a', 'c'])
    expect(litItems('pipe:P9', assignments, outputOf, undefined, { P1: ['a'] })).toEqual([])
    const chain = chainLit({ layers: [0, 1, 2], experts: [5, 7, 7] }, 2)
    expect(chain.nodes).toEqual({ L0E5: 2, L1E7: 2, L2E7: 2 })
    expect(chain.links).toEqual({ [linkKey('L0E5', 'L1E7')]: 2, [linkKey('L1E7', 'L2E7')]: 2 })
  })
})
