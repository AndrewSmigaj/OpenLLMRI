// The bar across the top: the workspace, the capture and lens, background jobs, and the MUD's
// connection with the viewer's role. Visitors only look; a lab room locks its capture.
import { useEffect, useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { apiClient } from '../../api/client'
import type { SessionListItem } from '../../types/api'
import type { LensSummary } from '../../types/lens'
import type { RoomContext } from '../../types/evennia'
import type { ConnectionStatus } from '../../hooks/useEvennia'
import { DEFAULT_VIEW, type UpdateView, type ViewState } from '../../hooks/useViewState'
import { useJobs } from '../../hooks/useJobs'
import JobsMenu from './JobsMenu'

interface TopBarProps {
  view: ViewState
  update: UpdateView
  room: RoomContext | null
  mudStatus: ConnectionStatus
}

const ctrl = 'px-2 py-1 text-xs border border-gray-300 rounded bg-white disabled:bg-gray-100 disabled:text-gray-400'
const STATUS_DOT: Record<ConnectionStatus, string> = {
  connected: 'bg-green-500', connecting: 'bg-amber-400', reconnecting: 'bg-amber-400', disconnected: 'bg-red-500',
}
const lensKey = (legacy: boolean, name: string) => `${legacy ? 'legacy' : 'lens'}:${name}`

export default function TopBar({ view, update, room, mudStatus }: TopBarProps) {
  const [sessions, setSessions] = useState<SessionListItem[]>([])
  const [lenses, setLenses] = useState<LensSummary[]>([])
  const jobs = useJobs()
  const { search } = useLocation()
  const visitor = room?.role === 'visitor'
  const locked = room?.roomType === 'micro_world'

  useEffect(() => {
    apiClient.listSessions().then(setSessions).catch(() => setSessions([]))
  }, [])

  // The lens list reloads when a job ends, so a new build shows up
  useEffect(() => {
    if (!view.session) { setLenses([]); return }
    let current = true
    apiClient.listLenses(view.session)
      .then(found => { if (current) setLenses(found) })
      .catch(() => { if (current) setLenses([]) })
    return () => { current = false }
  }, [view.session, jobs.finished])

  const chooseSession = (session: string) => update({
    ...DEFAULT_VIEW, session, zoom: view.zoom, tab: view.tab,
  })
  const chooseLens = (key: string) => {
    const [kind, ...rest] = key.split(':')
    update({ lens: rest.join(':'), legacy: kind === 'legacy', sel: '' })
  }
  const session = sessions.find(s => s.session_id === view.session)
  const made = lenses.filter(l => !l.legacy && l.kind === 'umap') // mass-mean lenses have no clusters to show
  const legacy = lenses.filter(l => l.legacy)
  const tab = ({ isActive }: { isActive: boolean }) =>
    `px-2.5 py-1 text-xs rounded ${isActive ? 'bg-gray-800 text-white' : 'text-gray-700 hover:bg-gray-200'}`

  return (
    <div className="flex items-center gap-3 bg-gray-50 border-b border-gray-300 px-3 py-1.5">
      <span className="text-sm font-semibold text-gray-900">OpenLLMRI</span>
      <nav className="flex gap-1">
        <NavLink to={`/layers${search}`} className={tab}>Layers</NavLink>
        <NavLink to={`/build${search}`} className={tab}>Build</NavLink>
      </nav>
      <label className="flex items-center gap-1.5 text-xs text-gray-600 min-w-0">
        Capture
        <select value={view.session} onChange={e => chooseSession(e.target.value)}
          disabled={visitor || locked} className={`${ctrl} min-w-[180px] max-w-[260px]`}>
          <option value="">Choose a capture…</option>
          {sessions.filter(s => s.state === 'completed').map(s => (
            <option key={s.session_id} value={s.session_id}>{s.session_name}</option>
          ))}
        </select>
      </label>
      {session && (
        <span className="text-xs text-gray-400 whitespace-nowrap">
          {session.probe_count} items{session.target_word && ` · "${session.target_word}"`}
        </span>
      )}
      <label className="flex items-center gap-1.5 text-xs text-gray-600">
        Lens
        <select value={view.lens ? lensKey(view.legacy, view.lens) : ''} onChange={e => chooseLens(e.target.value)}
          disabled={visitor || !view.session} className={`${ctrl} min-w-[200px] max-w-[300px]`}>
          <option value="">{lenses.length ? 'Choose a lens…' : 'No lenses yet'}</option>
          {made.length > 0 && <optgroup label="Lenses">
            {made.map(l => <option key={l.name} value={lensKey(false, l.name)}>{l.name}</option>)}
          </optgroup>}
          {legacy.length > 0 && <optgroup label="Legacy schemas">
            {legacy.map(l => <option key={l.name} value={lensKey(true, l.name)}>{l.name}</option>)}
          </optgroup>}
        </select>
      </label>
      <div className="flex-1" />
      <JobsMenu jobs={jobs.active} canCancel={!visitor} />
      {room && (
        <span className={`text-[10px] font-medium rounded px-1.5 py-0.5 border ${visitor
          ? 'bg-amber-100 text-amber-800 border-amber-300' : 'bg-green-100 text-green-800 border-green-300'}`}>
          {visitor ? 'Visitor' : 'Researcher'}
        </span>
      )}
      <span className="flex items-center gap-1 text-xs text-gray-600" title={`MUD: ${mudStatus}`}>
        <span className={`inline-block w-2 h-2 rounded-full ${STATUS_DOT[mudStatus]}`} />
        MUD
      </span>
    </div>
  )
}
