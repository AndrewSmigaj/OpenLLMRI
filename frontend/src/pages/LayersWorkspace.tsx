// Layers: a lens across all its layers. The cluster and expert charts scroll sideways together;
// the selection's details sit beside them; its members, the output table and the 3-D
// trajectories sit in tabs below. Views load as soon as a lens is chosen.
import { useCallback, useMemo, useRef, useState, type ReactNode } from 'react'
import type * as echarts from 'echarts'
import { Group, Panel, Separator } from 'react-resizable-panels'
import type { DynamicAxis, ProbeExample } from '../types/api'
import { DEFAULT_OUTPUT_COLOUR, outputGroupingOf, useAxisControls, type OutputColour } from '../hooks/useAxisControls'
import { useLensContext } from '../hooks/useLensContext'
import { useLensFlows } from '../hooks/useLensFlows'
import { useSelectionMembers } from '../hooks/useSelectionMembers'
import { useViewState, ZOOMS, type UpdateView, type ViewState } from '../hooks/useViewState'
import { useShell } from '../components/shell/shellContext'
import { chartPng, chartSvg, dataJson, download, rowsCsv, sankeyRows, type ExportFormat, type Recipe } from '../utils/exportFigure'
import { columnsOf, lastFirst, stepsInView } from '../utils/layerGeometry'
import { membersQuery, parseSelection, probeSelection } from '../utils/selection'
import { cardFor } from '../utils/selectionCard'
import ColourControls from '../components/layers/ColourControls'
import ColourLegend from '../components/layers/ColourLegend'
import DetailsPanel from '../components/layers/DetailsPanel'
import LayerCharts from '../components/layers/LayerCharts'
import { LayerStrip } from '../components/layers/LayerStrip'
import LowerTabs from '../components/layers/LowerTabs'
import FilteredWordDisplay from '../components/FilteredWordDisplay'
import WindowAnalysis from '../components/analysis/WindowAnalysis'
import SteppedTrajectoryPlot, { type TrajectoryExport } from '../components/charts/SteppedTrajectoryPlot'
import ExportMenu from '../components/common/ExportMenu'

const NO_AXES: DynamicAxis[] = []
const NO_SENTENCES: ProbeExample[] = []
const NO_LAYERS: number[] = []
const NO_VALUES: string[] = []

function Hint({ children }: { children: ReactNode }) {
  return <div className="m-4 bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs text-slate-700">{children}</div>
}

export default function LayersWorkspace() {
  const [view, update] = useViewState()
  const { room } = useShell()
  if (!view.session) return <Hint>Choose a capture in the top bar.</Hint>
  if (!view.lens) return <Hint>Choose a lens in the top bar, or build one in Build.</Hint>
  // A new capture or lens starts the page afresh (colours, selection data, trajectories)
  return <LayersView key={`${view.session}|${view.lens}|${view.legacy}`} view={view} update={update}
    visitor={room?.role === 'visitor'} />
}

function LayersView({ view, update, visitor }: { view: ViewState; update: UpdateView; visitor: boolean }) {
  const [output, setOutput] = useState<OutputColour>(DEFAULT_OUTPUT_COLOUR)
  const [maxTrajectories, setMaxTrajectories] = useState<number | null>(null) // null draws every item
  const trajectoryExport = useRef<TrajectoryExport | null>(null)
  const [trajectoryColour, setTrajectoryColour] = useState<'axis' | 'node'>('axis')
  const grouping = outputGroupingOf(output)
  const cluster = useLensFlows(view.session, view.lens, view.legacy, 'cluster', 1, grouping)
  const expert = useLensFlows(view.session, view.lens, view.legacy, 'expert', view.rank, grouping)
  const routes = cluster.routes
  const axes = useAxisControls(routes?.available_axes ?? NO_AXES, routes?.output_available_axes ?? NO_AXES,
    view, update, output, setOutput)
  const context = useLensContext(view.session, view.lens, view.legacy)
  const sentences = context.details?.sentences ?? NO_SENTENCES

  const layers = routes?.window_layers ?? NO_LAYERS
  const columns = columnsOf(routes)
  const steps = stepsInView(columns.length, view.zoom)
  const first = Math.min(view.layer, lastFirst(columns.length, steps))
  const layersInView = useMemo(() => layers.slice(first, first + steps + 1), [layers, first, steps])

  const selection = parseSelection(view.sel)
  const query = selection ? membersQuery(selection, layers[layers.length - 1] ?? 0, view.rank) : null
  const members = useSelectionMembers(view.session, view.lens, view.legacy, query)
  const card = useMemo(
    () => (selection ? cardFor(selection, cluster.routes, expert.routes, sentences, members.items) : null),
    // eslint-disable-next-line react-hooks/exhaustive-deps -- view.sel stands for the parsed selection
    [view.sel, cluster.routes, expert.routes, sentences, members.items])
  const selectedProbe = selection?.kind === 'probe' ? selection.probeId : null
  const clusterPath = selectedProbe ? routes?.probe_assignments?.[selectedProbe] : undefined
  // Each item's node at a layer, for colouring the 3-D points by what the lens counts
  const nodeOf = useCallback((probeId: string, layer: number) => routes?.probe_assignments?.[probeId]?.[String(layer)],
    [routes])

  const colours = useMemo(() => ({ input: axes.input, output: axes.output, stripes: axes.stripes }),
    [axes.input, axes.output, axes.stripes])
  const labelValues = axes.axisValues.label ?? NO_VALUES

  const recipe = (figure: string, lens: Record<string, unknown> | undefined): Recipe => ({
    app: 'OpenLLMRI', figure, link: window.location.href, exported_at: new Date().toISOString(),
    view, lens: lens ?? null,
    colours: { input: axes.input, output: axes.output, stripes: axes.stripes, shape: axes.shapeAxisId },
  })
  const baseName = `${view.session}_${view.lens}`

  const exportFlows = (kind: 'cluster' | 'expert', format: ExportFormat, chart: echarts.ECharts | null) => {
    const state = kind === 'cluster' ? cluster : expert
    if (!state.routes || !state.flows) return
    const what = kind === 'cluster' ? 'cluster flows, all layers' : `expert flows at rank ${view.rank}, all layers`
    const made = recipe(what, state.flows.recipe)
    const name = kind === 'cluster' ? `${baseName}_clusters` : `${baseName}_experts_rank${view.rank}`
    if (format === 'png' && chart) download(`${name}.png`, chartPng(chart, made))
    if (format === 'svg' && chart) download(`${name}.svg`, chartSvg(chart, made))
    if (format === 'csv') download(`${name}.csv`, rowsCsv(sankeyRows(state.routes.nodes, state.routes.links), made))
    if (format === 'json') download(`${name}.json`, dataJson({ flows: state.flows }, made))
  }

  const exportTrajectories = (format: ExportFormat) => {
    const handle = trajectoryExport.current
    if (!handle) return
    const made = { ...recipe(`3-D trajectories, layers ${layersInView.join(', ')}`, cluster.flows?.recipe),
      fit: "the lens's own 3-D fit, separate from the 6-D one it clusters in" }
    const name = `${baseName}_trajectories_L${layersInView[0]}-${layersInView[layersInView.length - 1]}`
    if (format === 'png') download(`${name}.png`, chartPng(handle.chart, made))
    if (format === 'csv') download(`${name}.csv`, rowsCsv(handle.rows, made))
    if (format === 'json') download(`${name}.json`, dataJson({ points: handle.rows }, made))
  }

  const sampleSize = context.summary?.sample_size ?? routes?.statistics.total_probes ?? 0
  const shownTrajectories = Math.min(maxTrajectories ?? sampleSize, sampleSize)
  const selectionName = selection?.kind === 'node' ? selection.id
    : selection?.kind === 'link' ? `${selection.source} → ${selection.target}` : ''
  const panels = {
    members: selection && selection.kind !== 'probe'
      ? <FilteredWordDisplay sentences={members.items} heading={`Members of ${selectionName}`}
          targetWord={context.details?.target_word} total={members.total} onLoadMore={members.loadMore}
          isLoading={members.loading} labelValues={labelValues} gradient={axes.gradient} />
      : <FilteredWordDisplay sentences={sentences} heading="Sentences" targetWord={context.details?.target_word}
          labelValues={labelValues} gradient={axes.gradient} />,
    output: <WindowAnalysis routeData={routes} labelValues={labelValues} gradient={axes.gradient}
      windowLabel={`Layer ${layers[layers.length - 1] ?? ''} → generated output`} />,
    trajectories: (
      <div className="space-y-1">
        <div className="flex items-center gap-2 text-xs text-gray-600">
          <span>Trajectories</span>
          {sampleSize > 0 && (
            <input type="range" min={Math.min(10, sampleSize)} max={sampleSize} step={1} value={shownTrajectories}
              onChange={e => setMaxTrajectories(Number(e.target.value))} className="w-40 accent-blue-600"
              title="How many items to draw in the 3-D plot" />
          )}
          <span className="tabular-nums">{shownTrajectories} / {sampleSize}</span>
          <label className="flex items-center gap-1">
            Colour by
            <select value={trajectoryColour} onChange={e => setTrajectoryColour(e.target.value as 'axis' | 'node')}
              className="px-1 py-0.5 text-xs border border-gray-300 rounded bg-white">
              <option value="axis">{axes.input.axis}</option>
              <option value="node">node</option>
            </select>
          </label>
          <span className="text-gray-400">layers {layersInView[0]}–{layersInView[layersInView.length - 1]}</span>
          <ExportMenu formats={['png', 'csv', 'json']} onExport={exportTrajectories} />
        </div>
        {layersInView.length >= 2 && (
          <SteppedTrajectoryPlot sessionId={view.session} schemaName={view.lens} legacy={view.legacy}
            layers={layersInView} colour={axes.input} colourBy={trajectoryColour} nodeOf={nodeOf}
            fitNote={view.legacy ? "the schema's own 3-D fit, separate from the 6-D one it clusters in"
              : "a 3-D UMAP of each layer with the lens's neighbours and seed, separate from the 6-D one it clusters in"}
            shapeAxisId={axes.shapeAxis?.id} shapeValues={axes.shapeAxis?.values} height={360} maxTrajectories={shownTrajectories}
            selectedProbeId={selectedProbe} onPointClick={info => update({ sel: probeSelection(info.probe_id) })}
            onExportable={handle => { trajectoryExport.current = handle }} />
        )}
      </div>
    ),
  }

  const btn = (on: boolean) => `px-1.5 py-0.5 text-[11px] rounded ${on ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`
  const analyze = `/analyze ${view.session} schema ${view.lens} transition ${layers[first] ?? 0}-${layers[first + 1] ?? 1}`

  return (
    <Group orientation="horizontal" className="h-full">
      <Panel id="main" defaultSize="74" minSize="40">
        <div className="h-full flex flex-col min-w-0">
          <div className="flex flex-wrap items-center gap-3 px-2 py-1 border-b border-gray-200 bg-gray-50">
            <span className="flex items-center gap-1 text-[11px] text-gray-600">
              Steps in view
              {ZOOMS.map(zoom => <button key={zoom} onClick={() => update({ zoom })} className={btn(view.zoom === zoom)}
                aria-label={`${zoom} steps in view`}>{zoom}</button>)}
            </span>
            <span className={`flex items-center gap-1 text-[11px] text-gray-600 ${visitor ? 'opacity-50 pointer-events-none' : ''}`}>
              Expert links
              <button onClick={() => update({ top: view.top ?? 10 })} className={btn(view.top !== null)}>top</button>
              {view.top !== null && (
                <input type="number" min={1} max={100} value={view.top}
                  onChange={e => update({ top: Math.max(1, Number(e.target.value) || 1) }, { replace: true })}
                  className="w-12 px-1 py-0.5 text-[11px] border border-gray-300 rounded" />
              )}
              <button onClick={() => update({ top: null })} className={btn(view.top === null)}>all</button>
            </span>
            <ColourControls axes={axes} disabled={visitor} />
            {view.legacy && (
              <span className="text-[11px] font-mono bg-blue-50 border border-blue-200 rounded px-1.5 py-0.5 cursor-pointer hover:bg-blue-100"
                title="Copy, then paste into Claude Code" onClick={() => navigator.clipboard?.writeText(analyze)}>
                {analyze}
              </span>
            )}
          </div>
          <div className="px-2 py-1 bg-white border-b border-gray-200">
            <ColourLegend input={axes.input} output={axes.output} stripes={axes.stripes} />
          </div>
          <div className="px-2 py-1 bg-white border-b border-gray-200">
            <LayerStrip columns={columns} first={first} shown={steps + 1}
              onPick={column => update({ layer: Math.min(column, lastFirst(columns.length, steps)) })} />
          </div>
          <Group orientation="vertical" className="flex-1 min-h-0">
            <Panel id="charts" defaultSize="68" minSize="25">
              <LayerCharts cluster={cluster} expert={expert} view={view} update={update} colours={colours} onExport={exportFlows} />
            </Panel>
            <Separator className="h-1 bg-gray-200 hover:bg-blue-400" />
            <Panel id="lower" defaultSize="32" minSize="10">
              <LowerTabs tab={view.tab} onTab={tab => update({ tab })} panels={panels} />
            </Panel>
          </Group>
        </div>
      </Panel>
      <Separator className="w-1 bg-gray-200 hover:bg-blue-400" />
      <Panel id="side" defaultSize="26" minSize="15">
        <DetailsPanel summary={context.summary} card={card} descriptions={context.descriptions} reports={context.reports}
          layer={layers[first] ?? 0} clusterPath={clusterPath} axisValues={axes.axisValues} gradient={axes.gradient}
          onClose={() => update({ sel: '' })} />
      </Panel>
    </Group>
  )
}
