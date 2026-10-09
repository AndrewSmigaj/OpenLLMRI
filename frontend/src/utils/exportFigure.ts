// Exports a chart with the recipe that made it, so a figure can always be traced and remade:
// PNG keeps it in an iTXt chunk, SVG in <metadata>, CSV in a leading comment, JSON as a field.
// A recipe names the lens and its settings, the view, and the link that reopens it.
import * as echarts from 'echarts'
import type { SankeyLink, SankeyNode } from '../types/api'

export type Recipe = Record<string, unknown>
export type ExportFormat = 'png' | 'svg' | 'csv' | 'json'

export function download(filename: string, blob: Blob): void {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

const CRC_TABLE = (() => {
  const table = new Uint32Array(256)
  for (let n = 0; n < 256; n++) {
    let c = n
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1
    table[n] = c >>> 0
  }
  return table
})()

function crc32(bytes: Uint8Array): number {
  let c = 0xffffffff
  for (const b of bytes) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8)
  return (c ^ 0xffffffff) >>> 0
}

// A PNG with an iTXt chunk (UTF-8 text under a keyword) placed right after its header chunk.
export function pngWithText(png: Uint8Array, keyword: string, text: string): Uint8Array {
  const encoder = new TextEncoder()
  const key = encoder.encode(keyword)
  const value = encoder.encode(text)
  // keyword, NUL, no compression (flag 0, method 0), empty language tag and translated keyword
  const data = new Uint8Array(key.length + 5 + value.length)
  data.set(key, 0)
  data.set(value, key.length + 5)
  const typed = new Uint8Array(4 + data.length)
  typed.set(encoder.encode('iTXt'), 0)
  typed.set(data, 4)
  const chunk = new Uint8Array(8 + data.length + 4)
  const view = new DataView(chunk.buffer)
  view.setUint32(0, data.length)
  chunk.set(typed, 4)
  view.setUint32(8 + data.length, crc32(typed))
  const headerEnd = 8 + 25 // the signature, then IHDR (length, type, 13 bytes of data, CRC)
  const out = new Uint8Array(png.length + chunk.length)
  out.set(png.subarray(0, headerEnd), 0)
  out.set(chunk, headerEnd)
  out.set(png.subarray(headerEnd), headerEnd + chunk.length)
  return out
}

const recipeText = (recipe: Recipe) => JSON.stringify(recipe)

function dataUrlBytes(url: string): Uint8Array {
  const binary = atob(url.slice(url.indexOf(',') + 1))
  return Uint8Array.from(binary, ch => ch.charCodeAt(0))
}

export function chartPng(chart: echarts.ECharts, recipe: Recipe): Blob {
  const url = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: '#ffffff' })
  return new Blob([pngWithText(dataUrlBytes(url), 'recipe', recipeText(recipe))], { type: 'image/png' })
}

// The chart redrawn by ECharts' SVG renderer (canvas charts can't give an SVG themselves), with
// animation off so the drawing is the finished one.
export function chartSvg(chart: echarts.ECharts, recipe: Recipe): Blob {
  const ssr = echarts.init(null, undefined, {
    renderer: 'svg', ssr: true, width: chart.getWidth(), height: chart.getHeight(),
  })
  ssr.setOption({ ...(chart.getOption() as echarts.EChartsOption), animation: false })
  const svg = ssr.renderToSVGString()
  ssr.dispose()
  const cdata = recipeText(recipe).replaceAll(']]>', ']]]]><![CDATA[>')
  const tagEnd = svg.indexOf('>') + 1
  const withRecipe = `${svg.slice(0, tagEnd)}<metadata><![CDATA[${cdata}]]></metadata>${svg.slice(tagEnd)}`
  return new Blob([withRecipe], { type: 'image/svg+xml' })
}

const csvCell = (value: unknown) => {
  const text = value === undefined || value === null ? '' : String(value)
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text
}

// Rows as CSV, the recipe in a leading comment line
export function rowsCsv(rows: Record<string, unknown>[], recipe: Recipe): Blob {
  const columns = [...new Set(rows.flatMap(row => Object.keys(row)))]
  const lines = [`# recipe: ${recipeText(recipe)}`, columns.map(csvCell).join(',')]
  for (const row of rows) lines.push(columns.map(c => csvCell(row[c])).join(','))
  return new Blob([lines.join('\n') + '\n'], { type: 'text/csv' })
}

export function dataJson(data: Record<string, unknown>, recipe: Recipe): Blob {
  return new Blob([JSON.stringify({ recipe, ...data }, null, 2)], { type: 'application/json' })
}

// A Sankey's nodes and links as table rows, each axis value's count in its own column
export function sankeyRows(nodes: SankeyNode[], links: SankeyLink[]): Record<string, unknown>[] {
  const spread = (label?: Record<string, number>, categories?: Record<string, Record<string, number>>) => ({
    ...Object.fromEntries(Object.entries(label ?? {}).map(([v, n]) => [`label=${v}`, n])),
    ...Object.fromEntries(Object.entries(categories ?? {}).flatMap(([axis, counts]) =>
      Object.entries(counts).map(([v, n]) => [`${axis}=${v}`, n]))),
  })
  return [
    ...nodes.map(n => ({ type: 'node', id: n.id, layer: n.layer, count: n.token_count, weight: n.weight,
      ...spread(n.label_distribution, n.category_distributions) })),
    ...links.map(l => ({ type: 'link', source: l.source, target: l.target, count: l.value,
      ...spread(l.label_distribution, l.category_distributions) })),
  ]
}

// The rows behind a chart drawn from a category axis: one row per category with a column per line
// series, or, for a heatmap, one row per cell
export function optionRows(option: echarts.EChartsOption): Record<string, unknown>[] {
  const labels = (axis: unknown) => ((Array.isArray(axis) ? axis[0] : axis) as { data?: unknown[] } | undefined)?.data ?? []
  const x = labels(option.xAxis)
  const y = labels(option.yAxis)
  const series = (Array.isArray(option.series) ? option.series : [option.series]) as { type?: string; name?: string; data?: unknown[] }[]
  const heat = series.find(s => s?.type === 'heatmap')
  if (heat) return ((heat.data ?? []) as [number, number, unknown][]).map(([xi, yi, value]) => ({ x: x[xi], y: y[yi], value }))
  const lines = series.filter(s => s?.type === 'line')
  return x.map((label, i) => Object.fromEntries([['x', label], ...lines.map(s => [s.name ?? 'value', s.data?.[i] ?? null])]))
}

// Export the chart drawn in an element (its picture, or the rows behind it), with its recipe
export function exportElementChart(format: ExportFormat, element: HTMLElement | null, name: string, recipe: Recipe,
                                   option: echarts.EChartsOption | null): void {
  const chart = element ? echarts.getInstanceByDom(element) : undefined
  const made = { app: 'OpenLLMRI', link: window.location.href, exported_at: new Date().toISOString(), ...recipe }
  if (format === 'png' && chart) download(`${name}.png`, chartPng(chart, made))
  if (format === 'svg' && chart) download(`${name}.svg`, chartSvg(chart, made))
  if (format === 'csv' && option) download(`${name}.csv`, rowsCsv(optionRows(option), made))
  if (format === 'json' && option) download(`${name}.json`, dataJson({ rows: optionRows(option) }, made))
}
