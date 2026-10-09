// Expert fingerprints: a population's mean gate weight on each of the 32 experts at each layer,
// from the model's own top-four weights (each row sums to 1). With a second population the grid
// shows their difference. Populations: every item, the selected node, or one value of an axis; an
// axis value can be set against the rest of the items (by class), with the experts whose weight
// differs beyond chance outlined (the lens's experts involved, DESIGN.md C7).
import { useEffect, useMemo, useRef, useState } from 'react'
import * as echarts from 'echarts'
import { apiClient } from '../../api/client'
import type { Fingerprint, LensRoutes, Population } from '../../types/lens'
import ExportMenu from '../common/ExportMenu'
import { chartPng, chartSvg, dataJson, download, rowsCsv, type ExportFormat } from '../../utils/exportFigure'

interface FingerprintPanelProps {
  session: string
  lens: string
  legacy: boolean
  axes: Record<string, string[]> // the designed axes and their values
  selectedNode?: { layer: number; node: number } // a selected cluster node, offered as a population
  involved?: LensRoutes['involved'] // the experts beyond chance per axis value, outlined by class
}

const ALL = 'all'
const NODE = 'node'
const NONE = 'none'
const REST = 'rest' // the items outside the first population's axis value

function populationOf(choice: string, selectedNode?: { layer: number; node: number }): Population | null {
  if (choice === ALL) return {}
  if (choice === NODE) return selectedNode ? { layer: selectedNode.layer, node: selectedNode.node } : null
  if (choice.startsWith('axis:')) {
    const [axis, value] = choice.slice(5).split('=')
    return { axis, value }
  }
  return null
}

function describe(choice: string, selectedNode?: { layer: number; node: number }): string {
  if (choice === ALL) return 'every item'
  if (choice === NODE) return selectedNode ? `node L${selectedNode.layer}C${selectedNode.node}` : 'the selected node'
  return choice.startsWith('axis:') ? choice.slice(5).replace('=', ' = ') : ''
}

// The heatmap's option: one population's weights, or a difference on a scale centred at zero;
// `outlined` cells (layer index, expert) get a dark border
function heatmapOption(grid: number[][], layers: number[], difference: boolean, title: string,
                       outlined: Set<string> = new Set()): echarts.EChartsOption {
  const data = grid.flatMap((row, li) => row.map((v, e) => (outlined.has(`${li}:${e}`)
    ? { value: [e, li, Number(v.toFixed(4))], itemStyle: { borderColor: '#111827', borderWidth: 1.5 } }
    : [e, li, Number(v.toFixed(4))])))
  const extreme = Math.max(1e-6, ...grid.flat().map(Math.abs))
  return {
    title: { text: title, left: 'center', top: 0, textStyle: { fontSize: 12 } },
    tooltip: { formatter: p => { const [e, li, v] = (p as { value: number[] }).value; return `L${layers[li]} · expert ${e}<br/>${difference ? 'difference' : 'weight'}: ${v}` } },
    grid: { left: 44, right: 70, top: 24, bottom: 28 },
    xAxis: { type: 'category', data: Array.from({ length: grid[0]?.length ?? 32 }, (_, e) => String(e)), name: 'expert',
      nameLocation: 'middle', nameGap: 18, axisLabel: { fontSize: 9 } },
    yAxis: { type: 'category', data: layers.map(l => `L${l}`), inverse: true, axisLabel: { fontSize: 9 } },
    visualMap: difference
      ? { min: -extreme, max: extreme, calculable: true, orient: 'vertical', right: 0, top: 'middle', itemHeight: 120,
          precision: 2, inRange: { color: ['#2166ac', '#f7f7f7', '#b2182b'] }, textStyle: { fontSize: 9 } }
      : { min: 0, max: extreme, calculable: true, orient: 'vertical', right: 0, top: 'middle', itemHeight: 120,
          precision: 2, inRange: { color: ['#ffffff', '#08306b'] }, textStyle: { fontSize: 9 } },
    series: [{ type: 'heatmap', data, progressive: 0, emphasis: { itemStyle: { borderColor: '#111', borderWidth: 1 } } }],
    animation: false,
  }
}

export default function FingerprintPanel({ session, lens, legacy, axes, selectedNode, involved }: FingerprintPanelProps) {
  const [a, setA] = useState(ALL)
  const [b, setB] = useState(NONE)
  const [prints, setPrints] = useState<{ a: Fingerprint | null; b: Fingerprint | null }>({ a: null, b: null })
  const [error, setError] = useState<string | null>(null)
  const box = useRef<HTMLDivElement>(null)
  const chart = useRef<echarts.ECharts | null>(null)
  const byClass = b === REST && a.startsWith('axis:')
  const keyA = JSON.stringify(populationOf(a, selectedNode))
  const keyB = JSON.stringify(byClass ? {} : populationOf(b, selectedNode)) // by class: every item, for the rest

  useEffect(() => {
    let current = true
    const get = (key: string) => (key === 'null' ? Promise.resolve(null)
      : apiClient.getLensFingerprint(session, lens, legacy, JSON.parse(key) as Population))
    Promise.all([get(keyA), get(keyB)])
      .then(([fa, fb]) => { if (current) { setPrints({ a: fa, b: fb }); setError(null) } })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens, legacy, keyA, keyB])

  const difference = !!(prints.a && prints.b)
  const grid = useMemo(() => {
    if (!prints.a) return null
    const other = prints.b
    if (!other) return prints.a.grid
    if (byClass) {  // the rest's mean from every item's and the value's: (N·all − n·value) / (N − n)
      const n = prints.a.n_items
      const rest = other.n_items - n
      return prints.a.grid.map((row, li) => row.map((v, e) => (rest > 0 ? v - (other.n_items * other.grid[li][e] - n * v) / rest : 0)))
    }
    return prints.a.grid.map((row, li) => row.map((v, e) => v - other.grid[li][e]))
  }, [prints, byClass])
  // By class, the experts whose weight differs beyond chance (the lens's routes) are outlined
  const outlined = useMemo(() => {
    if (!byClass || !prints.a) return new Set<string>()
    const [axis, value] = a.slice(5).split('=')
    const layers = prints.a.layers
    return new Set((involved?.[axis]?.[value]?.experts ?? []).map(c => `${layers.indexOf(c.layer)}:${c.expert}`))
  }, [byClass, a, involved, prints.a])
  const title = !prints.a ? '' : byClass ? `${describe(a, selectedNode)} − the rest${outlined.size ? ' (outlined: beyond chance)' : ''}`
    : difference ? `${describe(a, selectedNode)} − ${describe(b, selectedNode)}` : `${describe(a, selectedNode)} (${prints.a.n_items} items)`

  useEffect(() => {
    if (!box.current || !grid || !prints.a) return
    chart.current ??= echarts.init(box.current)
    chart.current.setOption(heatmapOption(grid, prints.a.layers, difference, title, outlined), true)
  }, [grid, prints.a, difference, title, outlined])
  useEffect(() => {
    const element = box.current
    if (!element) return
    const observer = new ResizeObserver(() => chart.current?.resize())
    observer.observe(element)
    return () => { observer.disconnect(); chart.current?.dispose(); chart.current = null }
  }, [])

  const exportGrid = (format: ExportFormat) => {
    if (!grid || !prints.a) return
    const recipe = {
      app: 'OpenLLMRI', figure: 'expert fingerprint', link: window.location.href, exported_at: new Date().toISOString(),
      populations: { a: describe(a, selectedNode), b: byClass ? 'the rest' : difference ? describe(b, selectedNode) : null },
      outlined: byClass ? [...outlined] : undefined,
      lens: prints.a.recipe,
    }
    const name = `${session}_${lens}_fingerprint`
    if (format === 'png' && chart.current) download(`${name}.png`, chartPng(chart.current, recipe))
    if (format === 'svg' && chart.current) download(`${name}.svg`, chartSvg(chart.current, recipe))
    if (format === 'csv') download(`${name}.csv`, rowsCsv(grid.flatMap((row, li) =>
      row.map((v, e) => ({ layer: prints.a!.layers[li], expert: e, value: v }))), recipe))
    if (format === 'json') download(`${name}.json`, dataJson({ layers: prints.a.layers, grid }, recipe))
  }

  const choices = [
    { id: ALL, label: 'every item' },
    ...(selectedNode ? [{ id: NODE, label: describe(NODE, selectedNode) }] : []),
    ...Object.entries(axes).flatMap(([axis, values]) =>
      values.map(value => ({ id: `axis:${axis}=${value}`, label: `${axis} = ${value}` }))),
  ]
  const select = 'px-1 py-0.5 text-xs border border-gray-300 rounded bg-white'

  return (
    <div className="space-y-1">
      <div className="flex flex-wrap items-center gap-2 text-xs text-gray-600">
        <span>Fingerprint of</span>
        <select value={a} onChange={e => setA(e.target.value)} className={select}>
          {choices.map(c => <option key={c.id} value={c.id}>{c.label}</option>)}
        </select>
        <span>minus</span>
        <select value={b} onChange={e => setB(e.target.value)} className={select}>
          <option value={NONE}>nothing</option>
          {a.startsWith('axis:') && <option value={REST}>the rest (by class)</option>}
          {choices.map(c => <option key={c.id} value={c.id}>{c.label}</option>)}
        </select>
        <ExportMenu formats={['png', 'svg', 'csv', 'json']} onExport={exportGrid} disabled={!grid} />
        <span className="text-gray-400">mean gate weight on each expert at each layer (the model's own top four; rows sum to 1)</span>
      </div>
      {error && <p className="text-xs text-red-600">{error}</p>}
      <div ref={box} style={{ height: 440, width: '100%' }} />
    </div>
  )
}
