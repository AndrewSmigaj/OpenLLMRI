import { describe, expect, it } from 'vitest'
import { cardIdFor, splitCardFor } from './cardId'
import { parseSelection } from './selection'

describe('card ids', () => {
  it('names the card each selection opens', () => {
    expect(cardIdFor(null, 1)).toBe('lens')
    expect(cardIdFor(parseSelection('L12C0'), 2)).toBe('L12C0')
    expect(cardIdFor(parseSelection('L12E5'), 2)).toBe('L12E5r2')
    expect(cardIdFor(parseSelection('L12C0>L13C2'), 1)).toBe('L12C0-L13C2')
    expect(cardIdFor(parseSelection('L12E5>L13E7'), 3)).toBe('L12E5-L13E7r3')
    expect(cardIdFor(parseSelection('L23C1>Generated:yes'), 1)).toBeNull()
    expect(cardIdFor(parseSelection('probe:p1'), 1)).toBeNull()
  })

  it('finds split points by the backend rule', () => {
    const nodes = [{ id: 'L4C0', layer: 4, index: 0, count: 40, counts: {} }]
    const link = (target: string, count: number) => ({ source: 'L4C0', target, count })
    expect(splitCardFor('L4C0', nodes, [link('L5C0', 20), link('L5C1', 12)])).toBe('split-L4C0')
    expect(splitCardFor('L4C0', nodes, [link('L5C0', 36), link('L5C1', 4)])).toBeNull()
  })
})
