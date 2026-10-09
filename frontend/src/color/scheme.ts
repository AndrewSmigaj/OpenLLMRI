// How designed axes become colours. Each value of an axis has one colour: a gradient's two ends
// for a two-valued axis, a categorical palette for more. A node or link mixes its values' colours
// in OKLab by their shares, on any designed axis. A second axis can share the colour as lightness
// (two axes in one colour), or fade one of its values toward grey (fade mode, the old ambiguity
// blend). Stripes show a node's exact shares instead of a mix.
import { hexToOklab, mixOklab, oklabToHex, type Oklab } from './oklab'

export type GradientScheme = 'red-blue' | 'yellow-cyan' | 'purple-green' | 'orange-teal' | 'pink-lime'

export const GRADIENT_SCHEMES: Record<GradientScheme, { start: string; end: string; name: string }> = {
  'red-blue': { start: '#dc267f', end: '#3b82f6', name: 'Red → Blue' },
  'yellow-cyan': { start: '#ffc107', end: '#06b6d4', name: 'Yellow → Cyan' },
  'purple-green': { start: '#9333ea', end: '#22c55e', name: 'Purple → Green' },
  'orange-teal': { start: '#f97316', end: '#14b8a6', name: 'Orange → Teal' },
  'pink-lime': { start: '#ec4899', end: '#84cc16', name: 'Pink → Lime' },
}

// For axes with more than two values (ColorBrewer Set1, with teal for an eighth)
const CATEGORICAL = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#a65628', '#f781bf', '#00aaa0']

export const NEUTRAL = '#888888'

export type AxisCounts = Record<string, Record<string, number>>

export interface ColourSpec {
  axis: string // the axis the hue shows
  values: string[] // its values, in a fixed order
  gradient: GradientScheme
  lightness?: { axis: string; values: string[] } // a second axis, shown as lightness
  fade?: { axis: string; value: string; amount: number } // a value that fades its items toward grey
}

export function valueColor(value: string, values: string[], gradient: GradientScheme): string {
  const i = values.indexOf(value)
  if (i < 0) return NEUTRAL
  const g = GRADIENT_SCHEMES[gradient]
  if (values.length === 1) {
    return oklabToHex(mixOklab([{ lab: hexToOklab(g.start), weight: 1 }, { lab: hexToOklab(g.end), weight: 1 }])!)
  }
  if (values.length === 2) return i === 0 ? g.start : g.end
  return CATEGORICAL[i % CATEGORICAL.length]
}

// A distinct colour per index (nodes of one layer, for example)
export const paletteColor = (i: number) => CATEGORICAL[((i % CATEGORICAL.length) + CATEGORICAL.length) % CATEGORICAL.length]

// The output column's colours when it has no colour axis of its own: a category named like a value
// of the colour axis takes that value's colour, and the others take the palette's next colours in
// name order, so each category keeps one colour in every chart and layout
export function answerColours(input: ColourSpec, categories: string[]): Record<string, string> {
  const others = [...new Set(categories.filter(c => !input.values.includes(c)))].sort()
  return Object.fromEntries(categories.map(c => [c, input.values.includes(c)
    ? valueColor(c, input.values, input.gradient)
    : paletteColor(input.values.length + others.indexOf(c))]))
}

// Lightness for each value of the second axis, darker to lighter, in a range where hues stay clear
export function lightnessLevels(n: number): number[] {
  if (n <= 1) return [0.65]
  return Array.from({ length: n }, (_, i) => 0.42 + (i * (0.86 - 0.42)) / (n - 1))
}

const sumOf = (shares: Record<string, number>) => Object.values(shares).reduce((s, n) => s + n, 0)

// The colour of a node or link from its counts on each axis. Mixing is linear in OKLab, so the
// hue's a and b mix by the colour axis's shares and the lightness by the second axis's shares:
// before gamut mapping, that equals the mix of every item's own colour, though only per-axis
// counts are known. Fade mode assumes the faded value is spread evenly over the hues.
export function distColor(counts: AxisCounts, spec: ColourSpec): string {
  const shares = counts[spec.axis] ?? {}
  const hue = mixOklab(spec.values.filter(v => shares[v] > 0)
    .map(v => ({ lab: hexToOklab(valueColor(v, spec.values, spec.gradient)), weight: shares[v] })))
  if (!hue) return NEUTRAL
  let lab: Oklab = hue
  if (spec.lightness) {
    const levels = lightnessLevels(spec.lightness.values.length)
    const second = counts[spec.lightness.axis] ?? {}
    const total = spec.lightness.values.reduce((s, v) => s + (second[v] ?? 0), 0)
    if (total > 0) {
      const L = spec.lightness.values.reduce((s, v, i) => s + levels[i] * (second[v] ?? 0), 0) / total
      lab = { ...hue, L }
    }
  }
  if (spec.fade) {
    const faded = counts[spec.fade.axis] ?? {}
    const total = sumOf(faded)
    const amount = total > 0 ? ((faded[spec.fade.value] ?? 0) / total) * spec.fade.amount : 0
    if (amount > 0) lab = mixOklab([{ lab, weight: 1 - amount }, { lab: hexToOklab(NEUTRAL), weight: amount }])!
  }
  return oklabToHex(lab)
}

// One item's colour, from its value on each axis
export function pointColor(values: Record<string, string | undefined>, spec: ColourSpec): string {
  const counts: AxisCounts = {}
  for (const axis of [spec.axis, spec.lightness?.axis, spec.fade?.axis]) {
    const value = axis ? values[axis] : undefined
    if (axis && value !== undefined) counts[axis] = { ...counts[axis], [value]: 1 }
  }
  return distColor(counts, spec)
}

// A node's exact shares on the colour axis as hard-edged bands, for a gradient fill
export function stripeStops(counts: AxisCounts, spec: ColourSpec): { offset: number; color: string }[] {
  const shares = counts[spec.axis] ?? {}
  const present = spec.values.filter(v => shares[v] > 0)
  const total = present.reduce((s, v) => s + shares[v], 0)
  const stops: { offset: number; color: string }[] = []
  let at = 0
  for (const v of present) {
    const color = valueColor(v, spec.values, spec.gradient)
    stops.push({ offset: at, color })
    at += shares[v] / total
    stops.push({ offset: Math.min(1, at), color })
  }
  return stops
}

export interface Legend {
  axis: string
  entries: { label: string; color: string }[] // one axis: a swatch per value
  grid?: { second: string; rows: string[]; cells: string[][] } // two axes: rows are the second axis's values
  fade?: { label: string; color: string } // fade mode: what a fully faded item looks like
}

// What every colour means, for the legend that is always on
export function legendOf(spec: ColourSpec): Legend {
  const entries = spec.values.map(v => ({ label: v, color: valueColor(v, spec.values, spec.gradient) }))
  const legend: Legend = { axis: spec.axis, entries }
  if (spec.lightness) {
    const { axis, values } = spec.lightness
    legend.grid = {
      second: axis,
      rows: values,
      cells: values.map(v2 => spec.values.map(v1 => pointColor({ [spec.axis]: v1, [axis]: v2 }, { ...spec, fade: undefined }))),
    }
  }
  if (spec.fade) {
    const sample = spec.values[0]
    legend.fade = {
      label: `${spec.fade.axis} = ${spec.fade.value}`,
      color: sample === undefined ? NEUTRAL
        : pointColor({ [spec.axis]: sample, [spec.fade.axis]: spec.fade.value }, { ...spec, lightness: undefined }),
    }
  }
  return legend
}
