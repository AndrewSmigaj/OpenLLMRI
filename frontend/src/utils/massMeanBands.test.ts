import { describe, expect, it } from 'vitest'
import type { MassMeanReadings } from '../types/lens'
import { classBands, quantile } from './massMeanBands'

const item = (label: string) => ({ probe_id: label, label, categories: null, step: null })

describe('mass-mean bands', () => {
  it('interpolates quantiles between ranks, as NumPy does', () => {
    expect(quantile([1, 2, 3, 4], 0.5)).toBe(2.5)
    expect(quantile([1, 2, 3, 4], 0.25)).toBe(1.75)
    expect(quantile([7], 0.75)).toBe(7)
    expect(quantile([], 0.5)).toBeNaN()
  })

  it("gives each class its median and middle half at every layer, in the items' order", () => {
    const found: MassMeanReadings = {
      lens: 'harm', contrast: { label_a: 'benign', label_b: 'harmful' }, target: 's', position: 1,
      layers: [0, 5],
      items: [item('dual'), item('benign'), item('dual'), item('dual'), item('benign')],
      readings: [[0.2, 0.0], [-1, -0.8], [0.4, 0.6], [0.0, 0.3], [-0.6, -1.2]],
    }
    const bands = classBands(found)
    expect(bands.map(b => [b.name, b.n])).toEqual([['dual', 3], ['benign', 2]])
    expect(bands[0].median).toEqual([0.2, 0.3])
    expect(bands[0].q1.map(v => +v.toFixed(3))).toEqual([0.1, 0.15])
    expect(bands[0].q3.map(v => +v.toFixed(3))).toEqual([0.3, 0.45])
    expect(bands[1].median).toEqual([-0.8, -1])
  })
})
