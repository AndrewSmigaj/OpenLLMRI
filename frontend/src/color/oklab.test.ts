import { describe, expect, it } from 'vitest'
import { gamutMap, hexToOklab, inGamut, mixOklab, oklabToHex, oklabToRgb, rgbToOklab } from './oklab'

const distance = (x: { L: number; a: number; b: number }, y: { L: number; a: number; b: number }) =>
  Math.hypot(x.L - y.L, x.a - y.a, x.b - y.b)

describe('OKLab', () => {
  it('matches the reference values for white, black and sRGB red', () => {
    const white = rgbToOklab([1, 1, 1])
    expect(white.L).toBeCloseTo(1, 4)
    expect(Math.hypot(white.a, white.b)).toBeLessThan(1e-4)
    expect(rgbToOklab([0, 0, 0]).L).toBeCloseTo(0, 6)
    const red = rgbToOklab([1, 0, 0]) // Ottosson's published value: 0.628, 0.225, 0.126
    expect(red.L).toBeCloseTo(0.628, 3)
    expect(red.a).toBeCloseTo(0.2249, 3)
    expect(red.b).toBeCloseTo(0.1258, 3)
  })

  it('round-trips hex colours exactly', () => {
    for (const hex of ['#dc267f', '#3b82f6', '#ffc107', '#06b6d4', '#4daf4a', '#888888', '#000000', '#ffffff']) {
      expect(oklabToHex(hexToOklab(hex))).toBe(hex)
    }
  })

  it('maps a colour outside sRGB inside it, keeping lightness and hue', () => {
    const vivid = { L: 0.9, a: 0.3, b: 0.05 }
    expect(inGamut(oklabToRgb(vivid))).toBe(false)
    const mapped = gamutMap(vivid)
    expect(inGamut(oklabToRgb(mapped))).toBe(true)
    expect(mapped.L).toBeCloseTo(0.9, 6)
    expect(Math.atan2(mapped.b, mapped.a)).toBeCloseTo(Math.atan2(vivid.b, vivid.a), 6)
    expect(Math.hypot(mapped.a, mapped.b)).toBeLessThan(Math.hypot(vivid.a, vivid.b))
  })

  it('mixes halfway: the middle of two colours is as far from each', () => {
    const red = hexToOklab('#dc267f')
    const blue = hexToOklab('#3b82f6')
    const middle = mixOklab([{ lab: red, weight: 1 }, { lab: blue, weight: 1 }])!
    expect(distance(middle, red)).toBeCloseTo(distance(middle, blue), 10)
    // black and white meet at perceptual mid-grey; the RGB average, #808080, sits well above it
    const grey = mixOklab([{ lab: hexToOklab('#000000'), weight: 1 }, { lab: hexToOklab('#ffffff'), weight: 1 }])!
    expect(grey.L).toBeCloseTo(0.5, 6)
    expect(hexToOklab('#808080').L).toBeCloseTo(0.6, 2)
  })

  it('weights by share and ignores empty weights', () => {
    const a = hexToOklab('#dc267f')
    const b = hexToOklab('#3b82f6')
    const mostlyA = mixOklab([{ lab: a, weight: 3 }, { lab: b, weight: 1 }])!
    expect(distance(mostlyA, a)).toBeLessThan(distance(mostlyA, b))
    expect(mixOklab([{ lab: a, weight: 0 }])).toBeNull()
  })
})
