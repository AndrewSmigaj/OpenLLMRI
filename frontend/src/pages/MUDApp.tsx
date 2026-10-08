// The app's frame: the top bar, a workspace (Layers or Build) and the MUD terminal's dock. The MUD
// steers the view: entering a lab room opens its capture and lens, with the terminal folded, and
// an `app_command` from the MUD shows a view. So do `show` commands on the backend's event stream
// (DESIGN.md E7), which also keeps jobs and lenses current.
import { useCallback, useRef, useState } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'
import { Group, Panel, Separator, usePanelRef } from 'react-resizable-panels'
import { apiClient } from '../api/client'
import type { ConnectionStatus } from '../hooks/useEvennia'
import { useAppEvents, type ShowView } from '../hooks/useAppEvents'
import { DEFAULT_VIEW, useViewState, viewQuery, type ViewState } from '../hooks/useViewState'
import type { RoomContext, RoomEnteredPayload } from '../types/evennia'
import type { LensSummary } from '../types/lens'
import { presetView } from '../utils/labPreset'
import TopBar from '../components/shell/TopBar'
import TerminalDock from '../components/shell/TerminalDock'
import type { ShellContext } from '../components/shell/shellContext'

const DOCK_LINE = 28 // pixels: the folded dock's one line

export default function MUDApp() {
  const [view, update] = useViewState()
  const [room, setRoom] = useState<RoomContext | null>(null)
  const [mudStatus, setMudStatus] = useState<ConnectionStatus>('disconnected')
  const [folded, setFolded] = useState(false)
  const dock = usePanelRef()
  const navigation = useRef(0) // drops a room's late reply once another room is entered
  const navigate = useNavigate()

  // A `show` command: the view it names, from defaults, in the workspace it names (Layers if none)
  const show = useCallback((view: ShowView) => {
    const { workspace, ...state } = view
    const next = { ...DEFAULT_VIEW, ...(state as Partial<ViewState>) }
    navigate({ pathname: workspace === 'build' ? '/build' : '/layers', search: `?${viewQuery(next)}` })
  }, [navigate])
  const events = useAppEvents(show)

  const toggleDock = useCallback(() => {
    if (dock.current?.isCollapsed()) dock.current.expand()
    else dock.current?.collapse()
  }, [dock])

  const handleOOB = useCallback((cmdname: string, args: unknown[], kwargs: Record<string, unknown>) => {
    if (cmdname === 'room_left') { setRoom(null); return }
    if (cmdname === 'app_command') {
      const command = (args[0] || kwargs || {}) as { verb?: string; view?: ShowView }
      if (command.verb === 'show' && command.view) show(command.view)
      return
    }
    if (cmdname !== 'room_entered') return
    const payload = (args[0] || kwargs || {}) as RoomEnteredPayload
    const gen = ++navigation.current
    setRoom({
      role: payload.role === 'researcher' ? 'researcher' : 'visitor',
      roomType: (payload.room_type || 'hub') as RoomContext['roomType'],
    })
    const session = payload.session_id
    if (!session) return
    const lens = payload.viz_preset?.clustering_schema ?? payload.clustering_schema ?? ''
    apiClient.listLenses(session).catch((): LensSummary[] => []).then(found => {
      if (gen !== navigation.current) return
      const legacy = found.find(l => l.name === lens)?.legacy ?? true
      update(presetView(session, lens, legacy, payload.viz_preset))
      dock.current?.collapse()
    })
  }, [update, dock, show])

  const context: ShellContext = { room, events }
  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <TopBar view={view} update={update} room={room} mudStatus={mudStatus} events={events} />
      <Group orientation="vertical" className="flex-1 min-h-0">
        <Panel id="workspace" minSize="25">
          <Outlet context={context} />
        </Panel>
        <Separator className="h-1 bg-gray-300 hover:bg-blue-400" />
        <Panel id="dock" panelRef={dock} collapsible collapsedSize={DOCK_LINE} minSize={120} defaultSize="25"
          onResize={() => setFolded(dock.current?.isCollapsed() ?? false)}>
          <TerminalDock folded={folded} onToggle={toggleDock} status={mudStatus} room={room}
            onOOB={handleOOB} onStatus={setMudStatus} />
        </Panel>
      </Group>
    </div>
  )
}
