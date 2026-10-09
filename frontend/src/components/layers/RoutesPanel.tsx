// Pipes and hubs (DESIGN.md C7, E8): the lens's expert pipelines, the hubs where items from
// different experts meet, and the experts whose weight differs by designed value. Choosing a
// pipeline lights its chain in the expert chart and its members' bundle in the cluster chart; a
// hub opens the weighted view of all four ranks at its expert. Generic: the axis shown and its
// colours come from the page.
import { useState, type ReactNode } from 'react'
import type { GradientScheme } from '../../color/scheme'
import { valueColor } from '../../color/scheme'
import type { RoutesState } from '../../hooks/useLensRoutes'
import type { RoutePipeline } from '../../types/lens'

interface RoutesPanelProps {
  state: RoutesState
  axis: string // the axis whose shares the pipelines show (the colour axis)
  axisValues: Record<string, string[]>
  gradient: GradientScheme
  selected: string // the page's selection
  onPipeline: (id: string) => void
  onHub: (layer: number, expert: number) => void
  onWorkOut: () => void // ask for the routes of a lens built before they were worked out
  working: boolean
  disabled: boolean
  report?: ReactNode // the link to the report on pipes and hubs
}

const pct = (x: number) => `${Math.round(100 * x)}%`
const chainText = (p: RoutePipeline) => {
  const steps = p.layers.map((layer, i) => `L${layer}E${p.experts[i]}`)
  return steps.length <= 6 ? steps.join(' › ') : `${steps.slice(0, 3).join(' › ')} › … › ${steps.slice(-2).join(' › ')}`
}

export default function RoutesPanel({ state, axis, axisValues, gradient, selected, onPipeline, onHub, onWorkOut, working,
                                      disabled, report }: RoutesPanelProps) {
  const { routes } = state
  const axes = routes ? Object.keys(routes.involved) : []
  const [chosen, setChosen] = useState('')
  const shownAxis = chosen && axes.includes(chosen) ? chosen : axes.includes(axis) ? axis : axes[0] ?? ''

  if (state.missing) {
    return (
      <div className="text-xs text-gray-600 space-y-1">
        <p>This lens's pipes and hubs aren't worked out yet (it was built before lenses had them).</p>
        <button onClick={onWorkOut} disabled={disabled || working}
          className="px-2 py-0.5 rounded border border-blue-300 text-blue-700 hover:bg-blue-50 disabled:opacity-50">
          {working ? 'Working them out…' : 'Work out pipes and hubs'}
        </button>
      </div>
    )
  }
  if (state.error) return <p className="text-xs text-red-600">{state.error}</p>
  if (!routes) return <p className="text-xs text-gray-500">Loading the pipes and hubs…</p>
  const base = routes.base[axis] ?? {}
  const total = Object.values(base).reduce((s, n) => s + n, 0) || 1
  const values = axisValues[axis] ?? Object.keys(base).sort()
  const row = 'border-t border-gray-100 cursor-pointer hover:bg-blue-50'
  return (
    <div className="space-y-3 text-[11px] text-gray-700">
      {report}
      <section>
        <h4 className="text-xs font-medium text-gray-800">
          Pipelines <span className="font-normal text-gray-500">({routes.pipelines.length}; each holds at least {routes.min_items} items)</span>
        </h4>
        {routes.pipelines.length === 0 ? (
          <p className="text-gray-500">None: no group of items keeps the same experts for three layers.</p>
        ) : (
          <table className="border-collapse">
            <thead>
              <tr className="text-gray-500">
                {['', 'layers', 'members', 'credit', `most common ${axis}`, 'found again', 'chain'].map(h =>
                  <th key={h} className="text-left font-normal pr-3">{h}</th>)}
              </tr>
            </thead>
            <tbody>
              {routes.pipelines.map(p => {
                const makeup = p.makeup[axis] ?? {}
                const [top, count] = Object.entries(makeup).sort((a, b) => b[1] - a[1])[0] ?? ['', 0]
                const on = selected === `pipe:${p.id}`
                return (
                  <tr key={p.id} onClick={() => onPipeline(p.id)} className={`${row} ${on ? 'bg-amber-50' : ''}`}
                    title="Light its chain in the expert chart and its members in the cluster chart">
                    <td className="pr-3 font-medium">{p.id}</td>
                    <td className="pr-3 whitespace-nowrap">L{p.layers[0]}–L{p.layers[p.layers.length - 1]} ({p.layers.length})</td>
                    <td className="pr-3 text-right tabular-nums">{p.members}</td>
                    <td className="pr-3 text-right tabular-nums" title="The members' mean credit: the geometric mean of their gate weights along the chain">{p.mean_weight.toFixed(2)}</td>
                    <td className="pr-3 whitespace-nowrap">
                      {top && <span className="inline-block w-2 h-2 rounded-sm mr-1" style={{ backgroundColor: valueColor(top, values, gradient) }} />}
                      {top} {p.members ? pct(count / p.members) : ''} <span className="text-gray-400">(all {pct((base[top] ?? 0) / total)})</span>
                    </td>
                    <td className="pr-3">{p.replicated ? 'yes' : 'no'}</td>
                    <td className="text-gray-500 whitespace-nowrap">{chainText(p)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        )}
      </section>
      <section>
        <h4 className="text-xs font-medium text-gray-800">
          Hubs <span className="font-normal text-gray-500">({routes.hubs.length}; experts whose items arrive from two experts or more, counted between items)</span>
        </h4>
        {routes.hubs.length === 0 ? (
          <p className="text-gray-500">None: at every expert the items arrive from much the same experts.</p>
        ) : (
          <table className="border-collapse">
            <tbody>
              {routes.hubs.map(h => (
                <tr key={h.id} onClick={() => onHub(h.layer, h.expert)} className={row} title="Open the weighted view of all four ranks at this expert">
                  <td className="pr-3 font-medium">{h.id}</td>
                  <td className="pr-3">L{h.layer}E{h.expert}</td>
                  <td className="pr-3 tabular-nums">{h.sources.toFixed(2)} sources</td>
                  <td className="pr-3 tabular-nums">{h.weighted.toFixed(0)} weighted items</td>
                  <td className="text-gray-500">from {h.from.map(f => `L${h.layer - 1}E${f.expert} ${pct(f.share)}`).join(', ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>
      {axes.length > 0 && (
        <section>
          <h4 className="text-xs font-medium text-gray-800 flex items-center gap-2">
            Experts involved
            <select value={shownAxis} onChange={e => setChosen(e.target.value)} className="px-1 py-0.5 text-[11px] border border-gray-300 rounded bg-white font-normal">
              {axes.map(a => <option key={a} value={a}>{a}</option>)}
            </select>
            <span className="font-normal text-gray-500">mean weight, each value against the rest, beyond chance</span>
          </h4>
          {Object.entries(routes.involved[shownAxis] ?? {}).map(([value, found]) => (
            <div key={value} className="flex flex-wrap items-center gap-1 mt-0.5">
              <span className="inline-block w-2 h-2 rounded-sm" style={{ backgroundColor: valueColor(value, axisValues[shownAxis] ?? [], gradient) }} />
              <span className="w-24 truncate">{value}</span>
              {found.experts.length === 0 ? <span className="text-gray-400">none</span> : found.experts.slice(0, 6).map(e => (
                <button key={`${e.layer}-${e.expert}`} onClick={() => onHub(e.layer, e.expert)}
                  title={`Mean weight ${e.diff > 0 ? 'higher' : 'lower'} for ${value} by ${Math.abs(e.diff).toFixed(3)}; AUC ${e.auc.toFixed(2)}`}
                  className={`px-1 rounded ${e.diff > 0 ? 'bg-emerald-50 text-emerald-800' : 'bg-rose-50 text-rose-800'} hover:ring-1 hover:ring-gray-300`}>
                  L{e.layer}E{e.expert} {e.diff > 0 ? '+' : '−'}{Math.abs(e.diff).toFixed(2)}
                </button>
              ))}
            </div>
          ))}
        </section>
      )}
    </div>
  )
}
