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
import { useCardList } from '../hooks/useCard'
import { useLensDetails } from '../hooks/useLensDetails'
import { useLensMarks } from '../hooks/useLensMarks'
import { useSelectionMembers } from '../hooks/useSelectionMembers'
import { useViewState, ZOOMS, type Fill, type UpdateView, type ViewState } from '../hooks/useViewState'
import { useLensTrajectory } from '../hooks/useLensTrajectory'
import { NEUTRAL, pointColor } from '../color/scheme'
import { nodeFill } from '../components/charts/sankeyOption'
import type { TrajectoryItem } from '../types/lens'
import { useShell } from '../components/shell/shellContext'
import { chartPng, chartSvg, dataJson, download, rowsCsv, sankeyRows, type ExportFormat, type Recipe } from '../utils/exportFigure'
import { columnsOf, lastFirst, stepsInView } from '../utils/layerGeometry'
import { membersQuery, parseNodeId, parseSelection, probeSelection, type Selection } from '../utils/selection'
import { cardIdFor, splitCardFor } from '../utils/cardId'
import { cardFor } from '../utils/selectionCard'
import { isOutputNode, stripOutputPrefix } from '../constants/outputNodes'
import { atStep, clusterPath as clusterPathOf, expertPath, ghostFlows, linkKey, litFlows, litItems, placesOf, readMaps } from '../utils/lighting'
import { useStepReading } from '../hooks/useStepReading'
import ColourControls from '../components/layers/ColourControls'
import ColourLegend from '../components/layers/ColourLegend'
import DetailsPanel from '../components/layers/DetailsPanel'
import NodeDetails from '../components/layers/NodeDetails'
import AnalysisReport from '../components/analysis/AnalysisReport'
import LayerCharts from '../components/layers/LayerCharts'
import { LayerStrip } from '../components/layers/LayerStrip'
import LowerTabs from '../components/layers/LowerTabs'
import FilteredWordDisplay from '../components/FilteredWordDisplay'
import WindowAnalysis from '../components/analysis/WindowAnalysis'
import SteppedTrajectoryPlot, { type TrajectoryExport } from '../components/charts/SteppedTrajectoryPlot'
import ExportMenu from '../components/common/ExportMenu'
import PanelErrorBoundary from '../components/common/PanelErrorBoundary'
import FingerprintPanel from '../components/layers/FingerprintPanel'
import ItemPath from '../components/layers/ItemPath'
import StepControl from '../components/layers/StepControl'

const NO_AXES: DynamicAxis[] = []
const NO_SENTENCES: ProbeExample[] = []
const NO_LAYERS: number[] = []
const NO_VALUES: string[] = []
const DEFAULT_SAMPLE = 600 // trajectories drawn in 3-D until the slider asks for more
const nameOf = (selection: Selection | null) => selection?.kind === 'node' ? selection.id
  : selection?.kind === 'link' ? `${selection.source} → ${selection.target}` : ''

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
  const [maxTrajectories, setMaxTrajectories] = useState<number | null>(null) // null draws the default sample
  const trajectoryExport = useRef<TrajectoryExport | null>(null)
  const [trajectoryColour, setTrajectoryColour] = useState<'axis' | 'node'>('node')
  const grouping = outputGroupingOf(output)
  const cluster = useLensFlows(view.session, view.lens, view.legacy, 'cluster', 1, grouping)
  const expert = useLensFlows(view.session, view.lens, view.legacy, 'expert', view.rank, grouping)
  const routes = cluster.routes
  const axes = useAxisControls(routes?.available_axes ?? NO_AXES, routes?.output_available_axes ?? NO_AXES,
    view, update, output, setOutput)
  const context = useLensContext(view.session, view.lens, view.legacy)
  const listing = context.lens
  const outlined = useLensMarks(view.session, view.lens, view.legacy, listing && !!listing.validation)
  const nodeDetails = useLensDetails(view.session, view.lens, view.legacy,
    listing && !!listing.current && !!listing.details?.includes(listing.current))
  const sentences = context.details?.sentences ?? NO_SENTENCES
  // A step the lens doesn't cover is read through it (DESIGN.md B5); then its items light too
  const stepReading = useStepReading(view.session, view.lens, view.legacy ? undefined : listing, view.step,
    listing?.current ?? undefined, view.rank)
  const reading = stepReading.reading

  const layers = routes?.window_layers ?? NO_LAYERS
  const columns = columnsOf(routes)
  const answers = useMemo(() => (routes?.nodes ?? []).filter(n => isOutputNode(n.name)).map(n => stripOutputPrefix(n.name)),
    [routes])
  // Every item lighting can use: the lens's own, and a read step's items with their voted nodes
  const maps = useMemo(() => {
    const read = reading ? readMaps(reading) : null
    const byCategory = grouping.length === 0 // read items know their output category, not other output keys
    const outputOf = routes?.output_of ? { ...routes.output_of, ...(byCategory ? read?.outputOf : {}) } : undefined
    return {
      read, outputOf, readOutputOf: routes?.output_of && byCategory ? read?.outputOf : undefined,
      assignments: { ...routes?.probe_assignments, ...read?.assignments },
      experts: { ...expert.routes?.probe_assignments, ...read?.experts },
      // only items with a path: a tick writes several records, and only the lens's and the reading's have nodes
      places: placesOf(sentences.filter(sentence => routes?.probe_assignments?.[sentence.probe_id]), reading?.items ?? []),
    }
  }, [reading, routes, expert.routes, sentences, grouping.length])
  // What the selection lights (DESIGN.md E5): its items' paths in both charts, over faded flows; with
  // a step chosen, its items at that step (an item stands for its run's item there)
  const litList = useMemo(() => atStep(litItems(view.sel, maps.assignments, maps.outputOf, maps.experts),
    view.sel, view.step, maps.places), [view.sel, view.step, maps])
  const lit = useMemo(() => litList.length ? {
    cluster: litFlows(litList, clusterPathOf(maps.assignments, layers, maps.outputOf)),
    expert: litFlows(litList, expertPath(maps.experts, layers, maps.outputOf)),
  } : { cluster: null, expert: null }, [litList, maps, layers])
  // What only the read items take, drawn as ghosts while the reading is shown
  const ghosts = useMemo(() => {
    if (!maps.read || !routes || !expert.routes) return { cluster: null, expert: null }
    const present = (r: typeof routes) => [new Set(r.nodes.flatMap(n => [n.id, n.name])),
      new Set(r.links.map(l => linkKey(l.source, l.target)))] as const
    return {
      cluster: ghostFlows(maps.read.ids, clusterPathOf(maps.read.assignments, layers, maps.readOutputOf), ...present(routes)),
      expert: ghostFlows(maps.read.ids, expertPath(maps.read.experts, layers, maps.readOutputOf), ...present(expert.routes)),
    }
  }, [maps, routes, expert.routes, layers])
  const steps = stepsInView(columns.length, view.zoom)
  const first = Math.min(view.layer, lastFirst(columns.length, steps))
  const layersInView = useMemo(() => layers.slice(first, first + steps + 1), [layers, first, steps])

  const selection = parseSelection(view.sel)
  // A sentence picked from a node's or a link's members keeps that list in view, so the others can
  // be picked in turn; picked anywhere else (a 3-D point, the URL), the list is every sentence
  const [pickedFrom, setPickedFrom] = useState('')
  const listSel = selection?.kind === 'probe' ? pickedFrom : view.sel
  const listSelection = parseSelection(listSel)
  const pick = (probeId: string, from: string) => {
    setPickedFrom(from)
    update({ sel: probeSelection(probeId) })
  }
  const query = listSelection ? membersQuery(listSelection, layers[layers.length - 1] ?? 0, view.rank) : null
  const members = useSelectionMembers(view.session, view.lens, view.legacy, query)
  const selectedProbe = selection?.kind === 'probe' ? selection.probeId : null
  // An item's card shows the lit item: with a step chosen, its run's item at that step
  const shownProbe = selectedProbe && view.step !== null ? litList[0] ?? selectedProbe : selectedProbe
  const card = useMemo(
    () => (selection ? cardFor(shownProbe ? { kind: 'probe', probeId: shownProbe } : selection,
                               cluster.routes, expert.routes, sentences, members.items) : null),
    // eslint-disable-next-line react-hooks/exhaustive-deps -- view.sel stands for the parsed selection
    [view.sel, shownProbe, cluster.routes, expert.routes, sentences, members.items])
  // At a step read through the lens, the Members tab lists that step's items the list's selection
  // stands for (every read item when nothing is selected)
  const readList = useMemo(() => {
    if (!reading) return null
    const ids = listSel ? atStep(litItems(listSel, maps.assignments, maps.outputOf, maps.experts), listSel, view.step, maps.places)
      : reading.items.map(item => item.probe_id)
    const bySentence = new Map(sentences.map(sentence => [sentence.probe_id, sentence]))
    return ids.flatMap(id => bySentence.get(id) ?? [])
  }, [reading, listSel, maps, view.step, sentences])
  // The capture's steps (ticks for an agent run, context steps for a sentence run)
  const allSteps = useMemo(() => [...new Set(sentences.flatMap(s => (s.step === undefined || s.step === null ? [] : [s.step])))]
    .sort((a, b) => a - b), [sentences])
  const stepLabel = sentences.some(s => s.turn_id !== undefined && s.turn_id !== null) ? 'Tick' : 'Step'
  const shownRead = shownProbe && reading ? reading.items.findIndex(item => item.probe_id === shownProbe) : -1
  const shownRun = shownProbe ? maps.places[shownProbe]?.run : null
  // The run's steps in the capture, read or not (an unread one offers its reading)
  const runSteps = useMemo(() => (shownRun ? [...new Set(sentences.flatMap(sentence =>
    sentence.run === shownRun && sentence.step !== undefined && sentence.step !== null ? [sentence.step] : []))]
    .sort((a, b) => a - b) : []), [sentences, shownRun])
  const pickedNode = selection?.kind === 'node' ? parseNodeId(selection.id) : null
  const selectedClusterNode = pickedNode?.kind === 'cluster' ? { layer: pickedNode.layer, node: pickedNode.index } : undefined
  const clusterPath = shownProbe ? routes?.probe_assignments?.[shownProbe] : undefined
  // The 3-D view (DESIGN.md E5): the lens's own space, with the shown reading's items in it
  const trajectory = useLensTrajectory(view.session, view.lens, view.legacy, reading ? stepReading.listed?.key : undefined)
  const nodeOf = useCallback((probeId: string, layer: number) => maps.assignments[probeId]?.[String(layer)], [maps])
  // A point's colour: its node's, as the Sankey draws the node, or its own value on the colour axis
  const nodeColours = useMemo(() => Object.fromEntries((routes?.nodes ?? []).map(n =>
    [n.id, nodeFill(n, { input: axes.input, output: axes.output, stripes: false })])), [routes, axes.input, axes.output])
  const valueOf = useCallback((item: TrajectoryItem, axis: string) => axis === 'label' ? item.label ?? undefined
    : axis === 'step' ? (item.step === null ? undefined : String(item.step)) : item.categories?.[axis], [])
  const colourOf = useCallback((item: TrajectoryItem, layer: number) => {
    if (trajectoryColour === 'node') {
      const node = maps.assignments[item.probe_id]?.[String(layer)]
      return node === undefined ? NEUTRAL : nodeColours[`L${layer}C${node}`] ?? NEUTRAL
    }
    const spec = axes.input
    const values = Object.fromEntries([spec.axis, spec.lightness?.axis, spec.fade?.axis]
      .filter((a): a is string => !!a).map(a => [a, valueOf(item, a)]))
    return values[spec.axis] === undefined ? NEUTRAL : pointColor(values, spec)
  }, [trajectoryColour, maps, nodeColours, axes.input, valueOf])
  const groupOf = useCallback((item: TrajectoryItem) => valueOf(item, axes.input.axis) ?? '', [valueOf, axes.input.axis])
  const shapeAxisId = axes.shapeAxis?.id
  const shapeOf = useMemo(() => (shapeAxisId ? (item: TrajectoryItem) => valueOf(item, shapeAxisId) : undefined),
    [shapeAxisId, valueOf])
  const litSet = useMemo(() => new Set(litList), [litList])

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
      frame: { fit: trajectory.data?.fit, note: frameNote, share: trajectory.data?.share }, camera: handle.camera,
      sample: handle.sample, lit: litList.length, reading: trajectory.data?.read?.key ?? null }
    const name = `${baseName}_trajectories_L${layersInView[0]}-${layersInView[layersInView.length - 1]}`
    if (format === 'png') download(`${name}.png`, chartPng(handle.chart, made))
    if (format === 'csv') download(`${name}.csv`, rowsCsv(handle.rows, made))
    if (format === 'json') download(`${name}.json`, dataJson({ points: handle.rows }, made))
  }

  const sampleSize = trajectory.data?.items.length ?? context.summary?.sample_size ?? routes?.statistics.total_probes ?? 0
  const shownTrajectories = Math.min(maxTrajectories ?? DEFAULT_SAMPLE, sampleSize)
  // What the 3-D positions are, for the panel and the export's recipe
  const inView = trajectory.data ? layersInView.map(l => trajectory.data!.layers.indexOf(l)).filter(i => i >= 0) : []
  const shares = inView.map(i => trajectory.data!.share[i])
  const frameNote = trajectory.data?.fit === 'separate'
    ? "the schema's own 3-D fit, separate from the space it clusters in; each layer lined up with the one before"
    : `the lens's own space on its three main directions (${shares.length ? `${Math.round(100 * Math.min(...shares))}–${Math.round(100 * Math.max(...shares))}% of the variance` : ''}); each layer lined up with the one before`
  const selectionName = nameOf(selection)

  // The analysis panel (DESIGN.md E8): the report on the selection, or on the lens when nothing is
  // selected, and for a node whose items part ways, the split point's report too
  const cards = useCardList(view.session, view.lens, !view.legacy)
  const cardId = view.legacy ? null : cardIdFor(selection, view.rank)
  const splitId = !view.legacy && selection?.kind === 'node' && cluster.flows
    ? splitCardFor(selection.id, cluster.flows.nodes, cluster.flows.links) : null
  const reportOn = (id: string, label: string) => (
    <PanelErrorBoundary key={id} name="Report">
      <AnalysisReport session={view.session} lens={view.lens} cardId={id} label={label}
        listed={cards.ids ? cards.ids.has(id) : undefined} onWritten={cards.reload} disabled={visitor} />
    </PanelErrorBoundary>
  )
  const report = cardId && (
    <>
      {reportOn(cardId, cardId === 'lens' ? 'Report on this lens'
        : `Report on ${selectionName}${/r\d$/.test(cardId) ? ` at rank ${view.rank}` : ''}`)}
      {splitId && reportOn(splitId, `Where ${selectionName}'s items part ways`)}
    </>
  )
  // The Members and Output tabs open the report on what they show: the selection, or the lens
  const openReport = (on: string | null, clear: boolean) => on && (
    <button onClick={() => {
      if (clear) update({ sel: '' })
      requestAnimationFrame(() => document.getElementById('analysis-report')?.scrollIntoView({ behavior: 'smooth', block: 'start' }))
    }} className="text-[11px] text-violet-700 hover:underline">
      {on === 'lens' ? 'Report on this lens' : `Report on ${selectionName}`} ▸
    </button>
  )
  const panels = {
    members: (
      <div className="space-y-1">
        {openReport(cardId, false)}
        {readList
          ? <FilteredWordDisplay sentences={readList} targetWord={context.details?.target_word}
              heading={listSelection && listSelection.kind !== 'probe'
                ? `Members of ${nameOf(listSelection)} at ${stepLabel.toLowerCase()} ${view.step}, read through the lens`
                : `${stepLabel} ${view.step}, read through the lens`}
              labelValues={labelValues} gradient={axes.gradient}
              onPick={id => pick(id, listSel)} pickedId={shownProbe ?? undefined} />
          : listSelection && listSelection.kind !== 'probe'
          ? <FilteredWordDisplay sentences={members.items} heading={`Members of ${nameOf(listSelection)}`}
              targetWord={context.details?.target_word} total={members.total} onLoadMore={members.loadMore}
              isLoading={members.loading} labelValues={labelValues} gradient={axes.gradient}
              onPick={id => pick(id, listSel)} pickedId={shownProbe ?? undefined} />
          : <FilteredWordDisplay sentences={sentences} heading="Sentences" targetWord={context.details?.target_word}
              labelValues={labelValues} gradient={axes.gradient}
              onPick={id => pick(id, '')} pickedId={shownProbe ?? undefined} />}
      </div>
    ),
    output: (
      <div className="space-y-1">
        {openReport(view.legacy ? null : 'lens', true)}
        <WindowAnalysis routeData={routes} labelValues={labelValues} gradient={axes.gradient}
          windowLabel={`Layer ${layers[layers.length - 1] ?? ''} → generated output`} />
      </div>
    ),
    experts: (
      <FingerprintPanel session={view.session} lens={view.lens} legacy={view.legacy} axes={axes.axisValues}
        selectedNode={selectedClusterNode} />
    ),
  }

  const btn = (on: boolean) => `px-1.5 py-0.5 text-[11px] rounded ${on ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`
  // Any panel can fill the workspace and come back (DESIGN.md E2)
  const fillButton = (id: Fill) => (
    <button onClick={() => update({ fill: view.fill === id ? '' : id })} aria-label={view.fill === id ? 'Back to the layout' : 'Fill the workspace'}
      title={view.fill === id ? 'Back to the layout' : 'Fill the workspace'}
      className="px-1 text-[13px] leading-none text-gray-400 hover:text-gray-800">{view.fill === id ? '⤡' : '⤢'}</button>
  )

  const toolbar = (
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
      {allSteps.length > 1 && (
        <StepControl label={stepLabel} steps={allSteps} step={view.step} onStep={step => update({ step })}
          reading={stepReading} disabled={visitor} />
      )}
      <button onClick={() => update({ d3: !view.d3, fill: view.fill === 'd3' ? '' : view.fill })} className={btn(view.d3)}
        title="The 3-D view of the lens's own space, between the charts and the tabs">3-D</button>
      <ColourControls axes={axes} disabled={visitor} />
    </div>
  )
  const legend = (
    <div className="px-2 py-1 bg-white border-b border-gray-200">
      <ColourLegend input={axes.input} output={axes.output} stripes={axes.stripes} answers={answers} />
    </div>
  )
  const strip = (
    <div className="px-2 py-1 bg-white border-b border-gray-200">
      <LayerStrip columns={columns} first={first} shown={steps + 1}
        onPick={column => update({ layer: Math.min(column, lastFirst(columns.length, steps)) })} />
    </div>
  )
  const charts = (
    <div className="relative h-full">
      <span className="absolute top-0.5 right-1 z-10">{fillButton('charts')}</span>
      <LayerCharts cluster={cluster} expert={expert} view={view} update={update} colours={colours}
        outlined={outlined} lit={lit} ghosts={ghosts} onExport={exportFlows} />
    </div>
  )
  const space3d = (
    <div className="h-full flex flex-col min-h-0 bg-white px-2 py-1 border-t border-gray-100">
      <div className="flex flex-wrap items-center gap-2 text-xs text-gray-600 flex-shrink-0">
        <span className="font-medium text-gray-800">3-D</span>
        {sampleSize > 0 && (
          <label className="flex items-center gap-1" title="How many items to draw; the lit ones always are">
            Trajectories
            <input type="range" min={Math.min(10, sampleSize)} max={sampleSize} step={1} value={shownTrajectories}
              onChange={e => setMaxTrajectories(Number(e.target.value))} className="w-32 accent-blue-600" />
            <span className="tabular-nums">{shownTrajectories} / {sampleSize}</span>
          </label>
        )}
        <label className="flex items-center gap-1">
          Colour by
          <select value={trajectoryColour} onChange={e => setTrajectoryColour(e.target.value as 'axis' | 'node')}
            className="px-1 py-0.5 text-xs border border-gray-300 rounded bg-white">
            <option value="node">node</option>
            <option value="axis">{axes.input.axis}</option>
          </select>
        </label>
        <span className="text-gray-400">layers {layersInView[0]}–{layersInView[layersInView.length - 1]}</span>
        <span className="text-gray-400 truncate min-w-0 flex-1" title={frameNote}>{frameNote}</span>
        <ExportMenu formats={['png', 'csv', 'json']} onExport={exportTrajectories} />
        {fillButton('d3')}
      </div>
      <div className="flex-1 min-h-0">
        {trajectory.data && layersInView.length >= 1 ? (
          <SteppedTrajectoryPlot data={trajectory.data} layers={layersInView} colourOf={colourOf} groupOf={groupOf}
            nodeOf={nodeOf} shapeOf={shapeOf} shapeValues={axes.shapeAxis?.values} sampleSize={shownTrajectories}
            lit={litSet} showRead={!!reading} onPick={probeId => pick(probeId, '')}
            onExportable={handle => { trajectoryExport.current = handle }} />
        ) : (
          <p className="text-xs text-gray-500 p-2">
            {trajectory.missing ? 'This schema was built before its 3-D points were kept.'
              : trajectory.error ?? 'Loading the 3-D view…'}
          </p>
        )}
      </div>
    </div>
  )
  const lower = <LowerTabs tab={view.tab} onTab={tab => update({ tab })} panels={panels} extra={fillButton('lower')} />
  const side = (
    <div className="relative h-full">
      <span className="absolute top-0.5 right-1 z-10">{fillButton('side')}</span>
      <DetailsPanel summary={context.summary} card={card} descriptions={context.descriptions} reports={context.reports}
        layer={layers[first] ?? 0} clusterPath={clusterPath} axisValues={axes.axisValues} gradient={axes.gradient}
        report={report} legacy={view.legacy}
        nodeDetails={!view.legacy && pickedNode?.kind === 'cluster' && (
          <PanelErrorBoundary name="Node details">
            <NodeDetails state={nodeDetails} layer={pickedNode.layer} node={pickedNode.index} disabled={visitor} />
          </PanelErrorBoundary>
        )}
        itemPath={shownProbe && (
          <ItemPath experts={maps.experts[shownProbe]} rank={view.rank} output={maps.outputOf?.[shownProbe]}
            read={reading && shownRead >= 0 ? { layers: reading.layers, nodes: reading.nodes[shownRead],
              shares: reading.shares[shownRead], pct: reading.pct[shownRead] } : undefined}
            stepLabel={stepLabel} steps={runSteps} step={view.step} onStep={step => update({ step })} />
        )}
        onClose={() => update({ sel: '' })} />
    </div>
  )

  if (view.fill) {
    const filled = { charts, d3: space3d, lower, side }[view.fill]
    return (
      <div className="h-full flex flex-col min-w-0">
        {view.fill !== 'side' && toolbar}
        {(view.fill === 'charts' || view.fill === 'd3') && legend}
        {view.fill === 'charts' && strip}
        <div className="flex-1 min-h-0">{filled}</div>
      </div>
    )
  }
  return (
    <Group orientation="horizontal" className="h-full">
      <Panel id="main" defaultSize="74" minSize="40">
        <div className="h-full flex flex-col min-w-0">
          {toolbar}
          {legend}
          {strip}
          <Group orientation="vertical" className="flex-1 min-h-0">
            <Panel id="charts" defaultSize={view.d3 ? '42' : '68'} minSize="20">{charts}</Panel>
            {view.d3 && <Separator className="h-1 bg-gray-200 hover:bg-blue-400" />}
            {view.d3 && <Panel id="d3" defaultSize="36" minSize="12">{space3d}</Panel>}
            <Separator className="h-1 bg-gray-200 hover:bg-blue-400" />
            <Panel id="lower" defaultSize={view.d3 ? '22' : '32'} minSize="10">{lower}</Panel>
          </Group>
        </div>
      </Panel>
      <Separator className="w-1 bg-gray-200 hover:bg-blue-400" />
      <Panel id="side" defaultSize="26" minSize="15">{side}</Panel>
    </Group>
  )
}
