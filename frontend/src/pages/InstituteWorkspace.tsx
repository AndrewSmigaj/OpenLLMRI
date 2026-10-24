// The institute's map (ROOM-19): every floor of a layout, the top floor first, drawn as one picture
// for the polishing passes. The layout in use is data/institute/layout.yaml; a pass's drafts sit in
// data/institute/drafts/, and a selector switches between them. Choosing a room shows what it is
// for, where its exits lead and who stands in it; rooms Claude suggests are dashed, for Andrew to
// keep or veto. Rooms open the app's own rooms as they are built (the new app's later steps); until
// then the observatory, the workshop and the lab lead to Layers and Build.
import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { apiClient } from '../api/client'
import type { InstituteLayout, InstituteLayoutEntry, InstituteLayoutReport, InstituteRoom } from '../types/institute'
import { dataJson, download } from '../utils/exportFigure'
import {
  APP_ROOM_NAMES, CELL_W, STAGE_STYLE, TODAY, floorPlans, roomCaption, roomColour, stackFloors, wrapWords,
} from '../utils/instituteMap'

const NAME_CHARS = 22 // characters per line of a room's name in its box

function recipe(layout: InstituteLayout, file: string) {
  return { what: 'the institute map', layout: file, title: layout.title, version: layout.version,
           exported: new Date().toISOString(), link: window.location.href }
}

function InstituteMap({ layout, selected, choose, svgRef, fit }: {
  layout: InstituteLayout
  selected: string
  choose: (id: string) => void
  svgRef: React.RefObject<SVGSVGElement | null>
  fit: boolean // scale the picture to the panel's width
}) {
  const plans = useMemo(() => floorPlans(layout), [layout])
  const { tops, width, height } = stackFloors(plans)
  return (
    <svg ref={svgRef} width={fit ? '100%' : width} height={fit ? undefined : height}
      style={fit ? { maxWidth: width, height: 'auto' } : undefined} viewBox={`0 0 ${width} ${height}`}
      xmlns="http://www.w3.org/2000/svg" fontFamily="ui-sans-serif, system-ui, sans-serif" role="img"
      aria-label="Map of the institute, the top floor first">
      <defs>
        <pattern id="closed-floor" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
          <rect width="8" height="8" fill="#f3f4f6" />
          <line x1="0" y1="0" x2="0" y2="8" stroke="#d1d5db" strokeWidth="3" />
        </pattern>
      </defs>
      {plans.map((plan, i) => (
        <g key={plan.floor.id}>
          <text x={0} y={tops[i] - 10} fontSize={14} fontWeight={600} fill="#111827">
            {plan.floor.name}
            <tspan fontWeight={400} fill="#6b7280">{plan.floor.note ? ` · ${plan.floor.note}` : ''}</tspan>
          </text>
          <g transform={`translate(0 ${tops[i]})`}>
            <rect width={plan.width} height={plan.height} rx={10}
              fill={plan.floor.closed ? 'url(#closed-floor)' : '#f9fafb'} stroke="#e5e7eb" />
            {plan.floor.closed && (
              <text x={16} y={plan.height / 2 + 4} fontSize={12} fill="#6b7280">Closed: no rooms yet</text>
            )}
            {plan.edges.map(edge => (
              <line key={`${edge.from}-${edge.to}`} x1={edge.x1} y1={edge.y1} x2={edge.x2} y2={edge.y2}
                stroke="#9ca3af" strokeWidth={3} strokeLinecap="round" />
            ))}
            {plan.boxes.map(box => {
              const colour = roomColour(box.room, layout)
              const stage = box.room.stage ? STAGE_STYLE[box.room.stage] : null
              const chosen = box.room.id === selected
              const lines = wrapWords(box.room.name, NAME_CHARS)
              const stairs = plan.stairs.filter(s => s.room === box.room.id)
              return (
                <g key={box.room.id} transform={`translate(${box.x} ${box.y})`} onClick={() => choose(box.room.id)}
                  style={{ cursor: 'pointer' }} role="button" aria-label={box.room.name}>
                  <rect width={box.w} height={box.h} rx={8} fill={stage ? '#fffdf7' : 'white'}
                    stroke={stage ? stage.stroke : colour} strokeDasharray={stage?.dash}
                    strokeWidth={chosen ? 3.5 : stage ? 2 : 1.5} />
                  {!stage && <rect width={box.w} height={6} rx={3} fill={colour} />}
                  {lines.slice(0, 3).map((line, j) => (
                    <text key={j} x={10} y={24 + j * 15} fontSize={12.5} fontWeight={600} fill="#111827">{line}</text>
                  ))}
                  <text x={10} y={box.h - 10} fontSize={10.5} fill={stage ? stage.stroke : '#6b7280'}
                    fontStyle={stage ? 'italic' : undefined}>
                    {roomCaption(box.room)}
                    {box.room.characters.length > 0 ? ' · ' : ''}
                    {box.room.characters.length > 0 && <tspan fill={colour}>● {box.room.characters.length}</tspan>}
                  </text>
                  {stairs.length > 0 && (
                    <text x={10} y={26 + Math.min(lines.length, 3) * 15} fontSize={10.5}>
                      {stairs.map((stair, j) => (
                        <tspan key={`${stair.direction}-${j}`} fill={stair.closed ? '#b91c1c' : '#374151'}>
                          {j > 0 ? '  ' : ''}{stair.direction === 'up' ? '↑' : '↓'} {stair.closed ? 'out of service' : 'stairs'}
                        </tspan>
                      ))}
                    </text>
                  )}
                </g>
              )
            })}
          </g>
        </g>
      ))}
    </svg>
  )
}

// With no room chosen: the rooms not built yet, Claude's suggestions first, each a click away
function NotBuilt({ layout, choose }: { layout: InstituteLayout; choose: (id: string) => void }) {
  const groups: [string, string, InstituteRoom[]][] = [
    ['suggested', 'Suggested by Claude (keep or veto)', layout.rooms.filter(r => r.stage === 'suggested')],
    ['later', 'Planned for later', layout.rooms.filter(r => r.stage === 'later')],
  ]
  return (
    <div className="space-y-4 text-sm">
      <p className="text-gray-600">Choose a room to see what it is for, where its exits lead and who stands in it.</p>
      {groups.filter(([, , rooms]) => rooms.length > 0).map(([stage, heading, rooms]) => (
        <div key={stage}>
          <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500">{heading}</h3>
          <ul className="mt-1 space-y-2">
            {rooms.map(r => (
              <li key={r.id}>
                <button type="button" onClick={() => choose(r.id)}
                  className="text-left font-medium text-blue-800 hover:underline">{r.name}</button>
                <p className="text-xs text-gray-600">{r.summary}</p>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  )
}

function RoomDetails({ layout, room, choose }: {
  layout: InstituteLayout
  room: InstituteRoom | null
  choose: (id: string) => void
}) {
  const { search } = useLocation()
  if (!room) return <NotBuilt layout={layout} choose={choose} />
  const name = (id: string) => layout.rooms.find(r => r.id === id)?.name ?? id
  const floor = layout.floors.find(f => f.id === room.floor)
  const department = layout.departments.find(d => d.id === room.department)
  const today = room.opens ? TODAY[room.opens] : undefined
  return (
    <div className="space-y-3 text-sm">
      <div>
        <h2 className="text-base font-semibold text-gray-900">{room.name}</h2>
        <p className="text-xs text-gray-500">
          {floor?.name}{department ? ` · ${department.name}` : ''} · place {room.at.join(', ')}
        </p>
      </div>
      <p className="text-gray-800">{room.summary}</p>
      {room.stage ? (
        <p className="italic" style={{ color: STAGE_STYLE[room.stage].stroke }}>
          {room.stage === 'suggested' ? 'Suggested by Claude: keep it or veto it.' : 'Planned for later.'}
        </p>
      ) : (
        <p className="text-gray-700">
          {room.opens ? <>Opens {APP_ROOM_NAMES[room.opens]} in the app</> : 'In the MUD only: it opens no room in the app'}
          {today && <> (for now: <Link className="text-blue-700 underline" to={`${today}${search}`}>{today === '/layers' ? 'Layers' : 'Build'}</Link>)</>}.
        </p>
      )}
      <div>
        <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500">Exits</h3>
        <ul className="mt-1 space-y-0.5">
          {Object.entries(room.exits).map(([direction, target]) => (
            <li key={direction}><span className="text-gray-500">{direction}</span> to {name(target)}</li>
          ))}
          {Object.entries(room.closed).map(([direction, told]) => (
            <li key={direction} className="text-red-700"><span>{direction}</span>: {told}</li>
          ))}
        </ul>
      </div>
      {room.characters.length > 0 && (
        <div>
          <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500">Who is here</h3>
          <ul className="mt-1 space-y-1">
            {room.characters.map(c => <li key={c.id}><span className="font-medium">{c.name}:</span> {c.note}</li>)}
          </ul>
        </div>
      )}
    </div>
  )
}

export default function InstituteWorkspace() {
  const [entries, setEntries] = useState<InstituteLayoutEntry[]>([])
  const [draft, setDraft] = useState('')
  const [report, setReport] = useState<InstituteLayoutReport | null>(null)
  const [failed, setFailed] = useState('')
  const [selected, setSelected] = useState('')
  const [fit, setFit] = useState(true)
  const svgRef = useRef<SVGSVGElement | null>(null)

  // The layouts to choose from; a pass's drafts first, when there are any
  useEffect(() => {
    apiClient.listInstituteLayouts().then(found => {
      setEntries(found)
      setDraft(found.find(e => e.name !== 'current')?.name ?? 'current')
    }).catch(error => setFailed(String(error)))
  }, [])

  useEffect(() => {
    if (!draft) return
    let current = true
    setSelected('')
    apiClient.getInstituteLayout(draft)
      .then(found => { if (current) setReport(found) })
      .catch(error => { if (current) setFailed(String(error)) })
    return () => { current = false }
  }, [draft])

  const layout = report?.layout ?? null
  const room = layout?.rooms.find(r => r.id === selected) ?? null
  const file = entries.find(e => e.name === draft)?.file ?? ''

  const exportSvg = () => {
    if (!svgRef.current || !layout) return
    const text = svgRef.current.outerHTML.replace('<defs>',
      `<metadata>${JSON.stringify(recipe(layout, file)).replace(/</g, '&lt;')}</metadata><defs>`)
    download(`institute-${draft}.svg`, new Blob([text], { type: 'image/svg+xml' }))
  }
  const exportJson = () => {
    if (layout) download(`institute-${draft}.json`, dataJson({ layout }, recipe(layout, file)))
  }

  return (
    <div className="flex h-full min-h-0">
      <div className="flex-1 min-w-0 overflow-auto p-4">
        <div className="mb-3 flex flex-wrap items-baseline gap-3">
          <h1 className="text-lg font-semibold text-gray-900">The institute</h1>
          <label className="flex items-center gap-1.5 text-xs text-gray-600">
            Layout
            <select value={draft} onChange={e => setDraft(e.target.value)}
              className="px-2 py-1 text-xs border border-gray-300 rounded bg-white">
              {entries.map(e => (
                <option key={e.name} value={e.name}>
                  {e.name === 'current' ? `In use: ${e.title}` : e.title}{e.problems ? ` (${e.problems} problems)` : ''}
                </option>
              ))}
            </select>
          </label>
          <span className="text-xs text-gray-500">Drawn from <code>{file}</code></span>
          {layout && (
            <span className="ml-auto flex items-center gap-1">
              <label className="mr-2 flex items-center gap-1 text-xs text-gray-600">
                <input type="checkbox" checked={fit} onChange={e => setFit(e.target.checked)} /> Fit to width
              </label>
              <button type="button" onClick={exportSvg}
                className="px-2 py-1 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">SVG</button>
              <button type="button" onClick={exportJson}
                className="px-2 py-1 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">JSON</button>
            </span>
          )}
        </div>
        {failed && <p className="text-sm text-red-700">The layout didn't load: {failed}</p>}
        {report?.error && <p className="text-sm text-red-700">The layout file can't be read: {report.error}</p>}
        {report && report.problems.length > 0 && (
          <div className="mb-3 rounded border border-amber-300 bg-amber-50 p-2 text-xs text-amber-900">
            <p className="font-semibold">The layout isn't whole yet:</p>
            <ul className="list-disc pl-5">{report.problems.map(p => <li key={p}>{p}</li>)}</ul>
          </div>
        )}
        {layout?.about && <p className="mb-3 max-w-3xl text-sm text-gray-700">{layout.about}</p>}
        {layout && <InstituteMap layout={layout} selected={selected} choose={setSelected} svgRef={svgRef} fit={fit} />}
        {!report && !failed && <p className="text-sm text-gray-500">Loading the layout…</p>}
        <p className="mt-2 text-xs text-gray-500" style={{ maxWidth: CELL_W * 4 }}>
          Lines are exits on a floor; ↑ and ↓ mark stairs, &quot;out of service&quot; when closed; ● counts the
          characters in a room. Each department&apos;s rooms share its colour. Dashed amber boxes are rooms
          Claude suggests, for you to keep or veto; dotted grey boxes are rooms planned for later.
        </p>
      </div>
      <aside className="w-80 shrink-0 border-l border-gray-200 bg-white p-4 overflow-auto">
        {layout && <RoomDetails layout={layout} room={room} choose={setSelected} />}
      </aside>
    </div>
  )
}
