import { describe, expect, it } from 'vitest'
import { layout3d, sample3d, type Point3 } from './trajectory3d'

// 30 items over 3 layers; the frame's second axis has the least spread
const rand = (seed: number) => () => { seed = (seed * 16807) % 2147483647; return seed / 2147483647 - 0.5 }
const r = rand(7)
const points: Point3[][] = Array.from({ length: 30 }, () =>
  Array.from({ length: 3 }, () => [r() * 10, r() * 1, r() * 6] as Point3))
const distance = (a: Point3, b: Point3) => Math.hypot(a[0] - b[0], a[1] - b[1], a[2] - b[2])

describe('layout3d', () => {
  it('runs the least-spread axis along the steps and draws the largest upright', () => {
    const layout = layout3d(points)
    expect(layout.along).toBe(1)
    expect(layout.across).toEqual([2, 0])
  })

  it('keeps every cloud its true shape, one scale on all three axes', () => {
    for (const scale of [1, 2.5]) {
      const layout = layout3d(points, 1.5, scale)
      const a = layout.place(points[0][1], 1)
      const b = layout.place(points[1][1], 1)
      expect(distance(a, b)).toBeCloseTo(scale * distance(points[0][1], points[1][1]), 8)
    }
  })

  it('scales the clouds, not the spacing between layers', () => {
    expect(layout3d(points, 1.5, 2).origins).toEqual(layout3d(points, 1.5, 1).origins)
  })

  it('never lets one cloud overlap the next, whatever the spacing factor at 1 or more', () => {
    for (const spacing of [1, 1.5, 3]) {
      const layout = layout3d(points, spacing)
      for (let li = 1; li < 3; li++) {
        const previous = Math.max(...points.map(item => layout.place(item[li - 1], li - 1)[0]))
        const next = Math.min(...points.map(item => layout.place(item[li], li)[0]))
        expect(next).toBeGreaterThan(previous)
      }
    }
  })
})

describe('sample3d', () => {
  const ids = Array.from({ length: 100 }, (_, i) => `probe_${i}`)
  const groupOf = (i: number) => (i < 70 ? 'a' : 'b')

  it('draws the same items every time, each group keeping its share', () => {
    const first = sample3d(ids, groupOf, 20, new Set())
    expect(sample3d(ids, groupOf, 20, new Set())).toEqual(first)
    expect(first.length).toBe(20)
    expect(first.filter(i => groupOf(i) === 'a').length).toBe(14)
  })

  it('always holds the lit items, and every item when n covers them', () => {
    const lit = new Set(['probe_99', 'probe_3'])
    const chosen = sample3d(ids, groupOf, 10, lit).map(i => ids[i])
    expect(chosen).toEqual(expect.arrayContaining(['probe_99', 'probe_3']))
    expect(sample3d(ids, groupOf, 100, new Set()).length).toBe(100)
  })
})
