// Laying out the 3-D view (DESIGN.md E5): each layer's cloud in the lens's own frame, the layers
// side by side along the frame's least-spread direction, with one scale on all three axes so every
// cloud keeps its true shape and none overlaps the next; and the sample of items it draws, the
// same every time, which always holds the lit items. Pure functions: the chart only draws them.

export type Point3 = [number, number, number]

export interface Layout3D {
  along: number // the frame axis that runs along the steps: the least spread
  across: [number, number] // the other two, drawn as depth and height
  origins: number[] // where each layer in view sits along the steps
  place: (point: Point3, li: number) => Point3 // a frame point at the li-th layer in view, as drawn
  ranges: { x: [number, number]; y: [number, number]; z: [number, number] }
}

const GAP = 0.15 // between clouds, as a share of the larger cross-section

/**
 * points: the frame points of the items drawn, [item][layer in view]
 * spacing: a factor on the automatic spacing (1 leaves a small gap between neighbouring clouds)
 * scale: each cloud's size around its own place, the same on all three axes; the layers stay where
 *   the spacing puts them, so clouds above 1 can reach their neighbours
 */
export function layout3d(points: Point3[][], spacing = 1.5, scale = 1): Layout3D {
  const layerCount = points[0]?.length ?? 0
  const spread = [0, 1, 2].map(axis => {
    const values = points.flatMap(item => item.map(p => p[axis]))
    const mean = values.reduce((s, v) => s + v, 0) / Math.max(1, values.length)
    return Math.sqrt(values.reduce((s, v) => s + (v - mean) ** 2, 0) / Math.max(1, values.length))
  })
  const along = spread.indexOf(Math.min(...spread))
  const rest = [0, 1, 2].filter(axis => axis !== along)
  const across: [number, number] = spread[rest[0]] >= spread[rest[1]] ? [rest[1], rest[0]] : [rest[0], rest[1]] // the larger spread is drawn upright
  const extent = (li: number, axis: number): [number, number] => {
    const values = points.map(item => item[li][axis])
    return [Math.min(...values), Math.max(...values)]
  }
  const cross = Math.max(...Array.from({ length: layerCount }, (_, li) =>
    Math.max(...across.map(axis => { const [lo, hi] = extent(li, axis); return hi - lo }))), 0)
  const origins: number[] = []
  for (let li = 0; li < layerCount; li++) {
    if (li === 0) { origins.push(0); continue }
    const [, previousEnd] = extent(li - 1, along)
    const [start] = extent(li, along)
    origins.push(origins[li - 1] + spacing * (previousEnd - start + GAP * cross))
  }
  const place = (point: Point3, li: number): Point3 =>
    [origins[li] + point[along] * scale, point[across[0]] * scale, point[across[1]] * scale]
  const placed = points.flatMap(item => item.map((p, li) => place(p, li)))
  const range = (i: number): [number, number] => placed.length
    ? [Math.min(...placed.map(p => p[i])), Math.max(...placed.map(p => p[i]))] : [0, 1]
  return { along, across, origins, place, ranges: { x: range(0), y: range(1), z: range(2) } }
}

// A stable order that doesn't follow capture order (FNV-1a over the id)
function hash(id: string): number {
  let h = 0x811c9dc5
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i)
    h = Math.imul(h, 0x01000193) >>> 0
  }
  return h
}

/**
 * The items drawn: n of them (every item when n covers them), each group (a colour value) keeping
 * its share, chosen in a stable order so the same items come back every time; the `keep` items
 * (the lit ones) are always among them. Returns indices into `ids`, in their order.
 */
export function sample3d(ids: string[], groupOf: (i: number) => string, n: number, keep: Set<string>): number[] {
  if (n >= ids.length) return ids.map((_, i) => i)
  const groups = new Map<string, number[]>()
  ids.forEach((_, i) => {
    const g = groupOf(i)
    groups.set(g, [...(groups.get(g) ?? []), i])
  })
  // each group's share of n, by the largest remainder so the shares add up to n
  const entries = [...groups.entries()]
  const exact = entries.map(([, members]) => (n * members.length) / ids.length)
  const counts = exact.map(Math.floor)
  const order = exact.map((value, i) => [value - counts[i], i] as const).sort((a, b) => b[0] - a[0])
  for (let k = 0; k < n - counts.reduce((s, c) => s + c, 0); k++) counts[order[k][1]] += 1
  const chosen = new Set<number>()
  entries.forEach(([, members], gi) => {
    [...members].sort((a, b) => hash(ids[a]) - hash(ids[b]) || a - b).slice(0, counts[gi]).forEach(i => chosen.add(i))
  })
  ids.forEach((id, i) => { if (keep.has(id)) chosen.add(i) })
  return [...chosen].sort((a, b) => a - b)
}
