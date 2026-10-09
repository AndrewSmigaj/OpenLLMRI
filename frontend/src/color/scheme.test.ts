import { describe, expect, it } from 'vitest'
import { hexToOklab } from './oklab'
import { GRADIENT_SCHEMES, NEUTRAL, answerColours, distColor, legendOf, lightnessLevels, pointColor, stripeStops, valueColor, type ColourSpec } from './scheme'

const senses = ['aquarium', 'clothing', 'scuba', 'septic', 'vehicle']
const byLabel: ColourSpec = { axis: 'label', values: ['fact', 'fiction'], gradient: 'red-blue' }

describe('value colours', () => {
  it('gives a two-valued axis the gradient ends, more values the palette, unknowns grey', () => {
    expect(valueColor('fact', byLabel.values, 'red-blue')).toBe(GRADIENT_SCHEMES['red-blue'].start)
    expect(valueColor('fiction', byLabel.values, 'red-blue')).toBe(GRADIENT_SCHEMES['red-blue'].end)
    expect(new Set(senses.map(s => valueColor(s, senses, 'red-blue'))).size).toBe(5)
    expect(valueColor('other', senses, 'red-blue')).toBe(NEUTRAL)
  })

  it('output categories keep one colour whatever their order, matching the axis by name', () => {
    const answers = ['unsure', 'fact', 'no_answer', 'fictional']
    const colours = answerColours(byLabel, answers)
    expect(answerColours(byLabel, [...answers].reverse())).toEqual(colours)
    expect(colours.fact).toBe(GRADIENT_SCHEMES['red-blue'].start)
    expect(new Set(Object.values(colours)).size).toBe(4)
    expect(Object.values(colours)).not.toContain(GRADIENT_SCHEMES['red-blue'].end)
  })
})

describe('node colours', () => {
  it('colours by any axis: register and label give different colours to the same node', () => {
    const counts = { label: { fact: 9, fiction: 1 }, register: { casual: 1, formal: 9 } }
    const byRegister: ColourSpec = { axis: 'register', values: ['casual', 'formal'], gradient: 'red-blue' }
    expect(distColor(counts, byLabel)).not.toBe(distColor(counts, byRegister))
  })

  it('a pure node takes its value colour exactly', () => {
    expect(distColor({ label: { fact: 12 } }, byLabel)).toBe(GRADIENT_SCHEMES['red-blue'].start)
  })

  it('two axes in one colour: lightness follows the second axis, hue the first', () => {
    const spec: ColourSpec = { ...byLabel, lightness: { axis: 'voice', values: ['active', 'passive'] } }
    const [dark, light] = lightnessLevels(2)
    const a = hexToOklab(pointColor({ label: 'fiction', voice: 'active' }, spec))
    const b = hexToOklab(pointColor({ label: 'fiction', voice: 'passive' }, spec))
    expect(a.L).toBeCloseTo(dark, 2)
    expect(b.L).toBeCloseTo(light, 2)
    expect(Math.atan2(a.b, a.a)).toBeCloseTo(Math.atan2(b.b, b.a), 1) // the same hue
    // a node holding one combination is that combination's colour
    expect(distColor({ label: { fiction: 5 }, voice: { passive: 5 } }, spec)).toBe(pointColor({ label: 'fiction', voice: 'passive' }, spec))
  })

  it('fade mode greys a node by the share of the faded value', () => {
    const spec: ColourSpec = { ...byLabel, fade: { axis: 'step', value: '0', amount: 0.6 } }
    const chroma = (hex: string) => { const c = hexToOklab(hex); return Math.hypot(c.a, c.b) }
    const committed = distColor({ label: { fact: 4 }, step: { '1': 4 } }, spec)
    const half = distColor({ label: { fact: 4 }, step: { '0': 2, '1': 2 } }, spec)
    const all = distColor({ label: { fact: 4 }, step: { '0': 4 } }, spec)
    expect(chroma(committed)).toBeGreaterThan(chroma(half))
    expect(chroma(half)).toBeGreaterThan(chroma(all))
  })
})

describe('stripes and the legend', () => {
  it('stripes are exact shares in the axis order', () => {
    const stops = stripeStops({ label: { scuba: 1, aquarium: 3 } }, { axis: 'label', values: senses, gradient: 'red-blue' })
    expect(stops.map(s => s.offset)).toEqual([0, 0.75, 0.75, 1])
    expect(stops[0].color).toBe(valueColor('aquarium', senses, 'red-blue'))
    expect(stops[2].color).toBe(valueColor('scuba', senses, 'red-blue'))
  })

  it('one axis lists its values; two axes give a square grid; fade adds its swatch', () => {
    expect(legendOf(byLabel).entries.map(e => e.label)).toEqual(['fact', 'fiction'])
    const grid = legendOf({ ...byLabel, lightness: { axis: 'voice', values: ['active', 'passive'] } }).grid!
    expect(grid.rows).toEqual(['active', 'passive'])
    expect(grid.cells.map(r => r.length)).toEqual([2, 2])
    expect(new Set(grid.cells.flat()).size).toBe(4)
    expect(legendOf({ ...byLabel, fade: { axis: 'step', value: '0', amount: 0.6 } }).fade?.label).toBe('step = 0')
  })
})
