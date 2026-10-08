// What the shell hands its workspaces: the MUD room the viewer is in (role and room type).
import { useOutletContext } from 'react-router-dom'
import type { RoomContext } from '../../types/evennia'

export interface ShellContext {
  room: RoomContext | null
}

export const useShell = () => useOutletContext<ShellContext>()
