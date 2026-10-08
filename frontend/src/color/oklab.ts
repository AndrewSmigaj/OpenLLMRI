// Colours in OKLab, a perceptual colour space (Björn Ottosson, 2020): equal steps look equal, so
// a weighted mean of two colours looks like it lies between them, where an RGB average turns
// muddy and dark. Colours leave OKLab through gamut mapping: chroma is reduced at the same
// lightness and hue until the colour fits sRGB.

export interface Oklab {
  L: number // lightness, 0 to 1
  a: number // green to red
  b: number // blue to yellow
}

type Rgb = [number, number, number] // sRGB, 0 to 1

const toLinear = (c: number) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)
const toGamma = (c: number) => (c <= 0.0031308 ? 12.92 * c : 1.055 * c ** (1 / 2.4) - 0.055)

export function hexToRgb(hex: string): Rgb {
  const h = hex.replace('#', '')
  const full = h.length === 3 ? h.split('').map(c => c + c).join('') : h
  return [0, 2, 4].map(i => parseInt(full.slice(i, i + 2), 16) / 255) as Rgb
}

export function rgbToHex(rgb: Rgb): string {
  return '#' + rgb.map(c => Math.round(Math.max(0, Math.min(1, c)) * 255).toString(16).padStart(2, '0')).join('')
}

export function rgbToOklab([r, g, b]: Rgb): Oklab {
  const [lr, lg, lb] = [toLinear(r), toLinear(g), toLinear(b)]
  const l = Math.cbrt(0.4122214708 * lr + 0.5363325363 * lg + 0.0514459929 * lb)
  const m = Math.cbrt(0.2119034982 * lr + 0.6806995451 * lg + 0.1073969566 * lb)
  const s = Math.cbrt(0.0883024619 * lr + 0.2817188376 * lg + 0.6299787005 * lb)
  return {
    L: 0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
    a: 1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
    b: 0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s,
  }
}

// Unclamped: a colour outside sRGB comes back with channels below 0 or above 1
export function oklabToRgb({ L, a, b }: Oklab): Rgb {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
  const s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3
  const lr = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
  const lg = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
  const lb = -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s
  return [lr, lg, lb].map(c => (c < 0 ? -toGamma(-c) : toGamma(c))) as Rgb
}

const EPS = 1e-6
export const inGamut = (rgb: Rgb) => rgb.every(c => c >= -EPS && c <= 1 + EPS)

// The colour with its chroma reduced (lightness and hue kept) until it fits sRGB
export function gamutMap(lab: Oklab): Oklab {
  const L = Math.max(0, Math.min(1, lab.L))
  if (inGamut(oklabToRgb({ L, a: lab.a, b: lab.b }))) return { L, a: lab.a, b: lab.b }
  let lo = 0
  let hi = 1
  for (let i = 0; i < 24; i++) {
    const mid = (lo + hi) / 2
    if (inGamut(oklabToRgb({ L, a: lab.a * mid, b: lab.b * mid }))) lo = mid
    else hi = mid
  }
  return { L, a: lab.a * lo, b: lab.b * lo }
}

export const hexToOklab = (hex: string) => rgbToOklab(hexToRgb(hex))
export const oklabToHex = (lab: Oklab) => rgbToHex(oklabToRgb(gamutMap(lab)))

// The weighted mean of colours in OKLab; null when the weights sum to nothing
export function mixOklab(parts: { lab: Oklab; weight: number }[]): Oklab | null {
  const total = parts.reduce((s, p) => s + Math.max(0, p.weight), 0)
  if (total <= 0) return null
  const sum = { L: 0, a: 0, b: 0 }
  for (const { lab, weight } of parts) {
    const w = Math.max(0, weight) / total
    sum.L += lab.L * w
    sum.a += lab.a * w
    sum.b += lab.b * w
  }
  return sum
}
