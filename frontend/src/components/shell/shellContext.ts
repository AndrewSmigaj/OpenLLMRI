// What the shell hands its workspaces: the MUD room the viewer is in (role and room type), and the
// backend's event stream (live jobs and lens changes).
import { useOutletContext } from 'react-router-dom'
import type { AppEvents } from '../../hooks/useAppEvents'
import type { RoomContext } from '../../types/evennia'

export interface ShellContext {
  room: RoomContext | null
  events: AppEvents
}

export const useShell = () => useOutletContext<ShellContext>()
