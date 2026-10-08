// The app's frame: the top bar, a workspace (Layers or Build) and the MUD terminal's dock. The MUD
// steers the view: entering a lab room opens its capture and lens, with the terminal folded.
import { useCallback, useRef, useState } from 'react'
import { Outlet } from 'react-router-dom'
import { Group, Panel, Separator, usePanelRef } from 'react-resizable-panels'
import { apiClient } from '../api/client'
import type { ConnectionStatus } from '../hooks/useEvennia'
import { useViewState } from '../hooks/useViewState'
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

  const toggleDock = useCallback(() => {
    if (dock.current?.isCollapsed()) dock.current.expand()
    else dock.current?.collapse()
  }, [dock])

  const handleOOB = useCallback((cmdname: string, args: unknown[], kwargs: Record<string, unknown>) => {
    if (cmdname === 'room_left') { setRoom(null); return }
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
  }, [update, dock])

  const context: ShellContext = { room }
  return (
    <div className="h-screen flex flex-col bg-gray-100">
      <TopBar view={view} update={update} room={room} mudStatus={mudStatus} />
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
