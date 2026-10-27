// The institute's map (ROOM-19): the floor plan in data/institute/layout.yaml, drawn as a plan with
// walls and doors. Choosing a room shows what it is for, which rooms its doors open onto and who is
// in it. Rooms open the app's own rooms as they are built (the new app's later steps); until then
// the observatory, the workshop and the lab lead to Layers and Build.
import { useEffect, useMemo, useRef, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { apiClient } from '../api/client'
import type { InstituteLayout, InstituteLayoutReport, InstituteRoom } from '../types/institute'
import { dataJson, download } from '../utils/exportFigure'
import { APP_ROOM_NAMES, DOOR, SCALE, TODAY, floorPlan, roomFill, visitorRooms, wrapWords } from '../utils/instituteMap'

const LAYOUT_FILE = 'data/institute/layout.yaml'
const WALL = '#374151'

function recipe(layout: InstituteLayout) {
  return { what: 'the institute floor plan', layout: LAYOUT_FILE, version: layout.version,
           exported: new Date().toISOString(), link: window.location.href }
}

function FloorPlan({ layout, selected, choose, svgRef }: {
  layout: InstituteLayout
  selected: string
  choose: (id: string) => void
  svgRef: React.RefObject<SVGSVGElement | null>
}) {
  const plan = useMemo(() => floorPlan(layout), [layout])
  const visitors = useMemo(() => visitorRooms(layout), [layout])
  return (
    <svg ref={svgRef} width="100%" viewBox={`0 0 ${plan.width} ${plan.height}`} style={{ maxWidth: plan.width * 1.4 }}
      xmlns="http://www.w3.org/2000/svg" fontFamily="ui-sans-serif, system-ui, sans-serif" role="img"
      aria-label="Floor plan of the institute">
      <defs>
        <pattern id="corridor" width="6" height="6" patternUnits="userSpaceOnUse">
          <rect width="6" height="6" fill="#f3f4f6" />
          <circle cx="3" cy="3" r="0.8" fill="#9ca3af" />
        </pattern>
      </defs>
      {plan.rooms.map(({ room, x, y, w, h }) => {
        const chosen = room.id === selected
        const lines = room.corridor ? [] : wrapWords(room.name, Math.max(8, Math.floor(w / 7)))
        return (
          <g key={room.id} onClick={() => choose(room.id)} style={{ cursor: 'pointer' }} role="button"
            aria-label={room.name}>
            <rect x={x} y={y} width={w} height={h}
              fill={room.corridor ? 'url(#corridor)' : roomFill(room, layout, visitors)} />
            {chosen && <rect x={x + 3} y={y + 3} width={w - 6} height={h - 6} fill="none" stroke="#2563eb" strokeWidth={2.5} />}
            {lines.map((line, i) => (
              <text key={i} x={x + w / 2} y={y + h / 2 + (i - (lines.length - 1) / 2) * 14 + 4} textAnchor="middle"
                fontSize={12} fontWeight={room.opens === 'department' || room.opens === 'entrance' ? 700 : 500}
                fill="#111827">{line}</text>
            ))}
          </g>
        )
      })}
      {plan.walls.map((wall, i) => (
        <line key={i} x1={wall.x1} y1={wall.y1} x2={wall.x2} y2={wall.y2} stroke={WALL} strokeWidth={2.5}
          strokeLinecap="square" />
      ))}
      {plan.entrance && (
        <text x={plan.entrance.x} y={plan.entrance.y + 11} textAnchor="middle" fontSize={10} fill="#6b7280">
          entrance
        </text>
      )}
      <text x={plan.width - 12} y={plan.height - 2} textAnchor="end" fontSize={9} fill="#9ca3af">
        {`a gap in a wall is a door (${(DOOR / SCALE).toFixed(1)} m)`}
      </text>
    </svg>
  )
}

function RoomDetails({ layout, room }: { layout: InstituteLayout; room: InstituteRoom | null }) {
  const { search } = useLocation()
  if (!room) {
    return <p className="text-sm text-gray-600">Choose a room to see what it is for, where its doors lead and who is in it.</p>
  }
  const name = (id: string) => layout.rooms.find(r => r.id === id)?.name ?? id
  const department = layout.departments.find(d => d.id === room.department)
  const today = room.opens ? TODAY[room.opens] : undefined
  const doors = layout.doors.flatMap(([a, b]) => (a === room.id ? [b] : b === room.id ? [a] : []))
  return (
    <div className="space-y-3 text-sm">
      <div>
        <h2 className="text-base font-semibold text-gray-900">{room.name}</h2>
        {department && <p className="text-xs text-gray-500">{department.name}</p>}
      </div>
      <p className="text-gray-800">{room.summary}</p>
      {!room.corridor && (
        <p className="text-gray-700">
          {room.opens ? <>Opens {APP_ROOM_NAMES[room.opens]} in the app</> : 'In the MUD only: it opens no room in the app'}
          {today && <> (for now: <Link className="text-blue-700 underline" to={`${today}${search}`}>{today === '/layers' ? 'Layers' : 'Build'}</Link>)</>}.
        </p>
      )}
      {room.notes.map(note => <p key={note} className="text-gray-700">{note}</p>)}
      <div>
        <h3 className="text-xs font-semibold uppercase tracking-wide text-gray-500">Doors to</h3>
        <ul className="mt-1 space-y-0.5">
          {room.id === layout.entrance && <li>outside (the front door)</li>}
          {doors.map(id => <li key={id}>{name(id)}</li>)}
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
  const [report, setReport] = useState<InstituteLayoutReport | null>(null)
  const [failed, setFailed] = useState('')
  const [selected, setSelected] = useState('')
  const svgRef = useRef<SVGSVGElement | null>(null)

  useEffect(() => {
    apiClient.getInstituteLayout().then(setReport).catch(error => setFailed(String(error)))
  }, [])

  const layout = report?.layout ?? null
  const room = layout?.rooms.find(r => r.id === selected) ?? null

  const exportSvg = () => {
    if (!svgRef.current || !layout) return
    const text = svgRef.current.outerHTML.replace('<defs>',
      `<metadata>${JSON.stringify(recipe(layout)).replace(/</g, '&lt;')}</metadata><defs>`)
    download('institute-plan.svg', new Blob([text], { type: 'image/svg+xml' }))
  }
  const exportJson = () => {
    if (layout) download('institute-layout.json', dataJson({ layout }, recipe(layout)))
  }

  return (
    <div className="flex h-full min-h-0">
      <div className="flex-1 min-w-0 overflow-auto p-4">
        <div className="mb-2 flex flex-wrap items-baseline gap-3">
          <h1 className="text-lg font-semibold text-gray-900">{layout?.title || 'The institute'}</h1>
          <span className="text-xs text-gray-500">Drawn from <code>{LAYOUT_FILE}</code></span>
          {layout && (
            <span className="ml-auto flex gap-1">
              <button type="button" onClick={exportSvg}
                className="px-2 py-1 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">SVG</button>
              <button type="button" onClick={exportJson}
                className="px-2 py-1 text-xs border border-gray-300 rounded bg-white hover:bg-gray-50">JSON</button>
            </span>
          )}
        </div>
        {layout?.about && <p className="mb-3 max-w-3xl text-sm text-gray-700">{layout.about}</p>}
        {failed && <p className="text-sm text-red-700">The layout didn't load: {failed}</p>}
        {report?.error && <p className="text-sm text-red-700">The layout file can't be read: {report.error}</p>}
        {report && report.problems.length > 0 && (
          <div className="mb-3 rounded border border-amber-300 bg-amber-50 p-2 text-xs text-amber-900">
            <p className="font-semibold">The layout isn't whole yet:</p>
            <ul className="list-disc pl-5">{report.problems.map(p => <li key={p}>{p}</li>)}</ul>
          </div>
        )}
        {layout && <FloorPlan layout={layout} selected={selected} choose={setSelected} svgRef={svgRef} />}
        {!report && !failed && <p className="text-sm text-gray-500">Loading the layout…</p>}
      </div>
      <aside className="w-80 shrink-0 border-l border-gray-200 bg-white p-4 overflow-auto">
        {layout && <RoomDetails layout={layout} room={room} />}
      </aside>
    </div>
  )
}
