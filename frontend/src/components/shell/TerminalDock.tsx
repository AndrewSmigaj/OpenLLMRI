// The MUD terminal in a dock along the bottom. Folding it leaves one line showing the connection;
// the terminal stays mounted, so the MUD session stays connected.
import type { ConnectionStatus } from '../../hooks/useEvennia'
import type { RoomContext } from '../../types/evennia'
import MUDTerminal from '../terminal/MUDTerminal'
import PanelErrorBoundary from '../common/PanelErrorBoundary'

interface TerminalDockProps {
  folded: boolean
  onToggle: () => void
  status: ConnectionStatus
  room: RoomContext | null
  onOOB: (cmdname: string, args: unknown[], kwargs: Record<string, unknown>) => void
  onStatus: (status: ConnectionStatus) => void
}

export default function TerminalDock({ folded, onToggle, status, room, onOOB, onStatus }: TerminalDockProps) {
  return (
    <div className="h-full flex flex-col bg-gray-900">
      <button onClick={onToggle}
        className="flex items-center gap-2 px-3 h-7 flex-shrink-0 text-xs text-gray-300 bg-gray-800 hover:bg-gray-700 text-left">
        <span>{folded ? '▸' : '▾'}</span>
        <span className="font-medium">MUD terminal</span>
        <span className="text-gray-400">{status}{room ? ` · ${room.roomType.replace('_', ' ')}` : ''}</span>
        <span className="flex-1" />
        <span className="text-gray-500">{folded ? 'open' : 'fold'}</span>
      </button>
      <div className="flex-1 min-h-0">
        <PanelErrorBoundary name="MUD terminal">
          <MUDTerminal onOOB={onOOB} onStatus={onStatus} />
        </PanelErrorBoundary>
      </div>
    </div>
  )
}
