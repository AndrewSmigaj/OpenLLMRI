// Where each class of a capture sits along a mass-mean lens's axis, layer by layer: the median and
// the middle half (25th to 75th percentile) of its items' readings. The lens's own two classes sit
// at -1 and +1 on average by construction; any other class (the dual-purpose objects) is the reading.
import type { MassMeanReadings } from '../types/lens'

export interface ClassBand {
  name: string
  n: number
  median: number[]
  q1: number[]
  q3: number[]
}

// The q-th quantile of sorted values, interpolated linearly between ranks (NumPy's default).
export function quantile(sorted: number[], q: number): number {
  if (sorted.length === 0) return NaN
  const at = q * (sorted.length - 1)
  const low = Math.floor(at)
  const high = Math.ceil(at)
  return sorted[low] + (sorted[high] - sorted[low]) * (at - low)
}

// One band per class, in the order the classes first appear among the items.
export function classBands(found: MassMeanReadings): ClassBand[] {
  const members = new Map<string, number[]>()
  found.items.forEach((item, i) => {
    const list = members.get(item.label) ?? []
    list.push(i)
    members.set(item.label, list)
  })
  return [...members.entries()].map(([name, rows]) => {
    const band: ClassBand = { name, n: rows.length, median: [], q1: [], q3: [] }
    found.layers.forEach((_, li) => {
      const values = rows.map(i => found.readings[i][li]).sort((a, b) => a - b)
      band.median.push(quantile(values, 0.5))
      band.q1.push(quantile(values, 0.25))
      band.q3.push(quantile(values, 0.75))
    })
    return band
  })
}
