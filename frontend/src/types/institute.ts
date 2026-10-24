// The institute's layout as GET /api/institute/layout serves it (data/institute/layout.yaml;
// backend/src/services/institute.py holds the rules a whole layout keeps).

export type Direction = 'north' | 'south' | 'east' | 'west' | 'northeast' | 'northwest' | 'southeast'
  | 'southwest' | 'up' | 'down'

export type AppRoom = 'entrance' | 'simulation' | 'department' | 'lab' | 'observatory' | 'workshop'
  | 'library' | 'studies' | 'meeting'

// A room not built yet: 'later', planned by the design for later; 'suggested', Claude's suggestion,
// waiting for Andrew to keep it or veto it
export type RoomStage = 'later' | 'suggested'

export interface InstituteFloor {
  id: string
  name: string
  note: string
  closed: boolean
}

export interface InstituteDepartment {
  id: string
  name: string
}

export interface InstituteCharacter {
  id: string
  name: string
  note: string
}

export interface InstituteRoom {
  id: string
  name: string
  floor: string
  at: [number, number] // [column, row] on its floor's grid; columns run east, rows south
  summary: string
  opens: AppRoom | null // the app room it opens; null: in the MUD only
  department: string | null
  stage: RoomStage | null
  exits: Partial<Record<Direction, string>>
  closed: Partial<Record<Direction, string>> // out of service, with what a player is told
  characters: InstituteCharacter[]
}

export interface InstituteLayout {
  version: number
  title: string
  about: string // what the layout is built around
  floors: InstituteFloor[] // from the bottom up
  departments: InstituteDepartment[]
  rooms: InstituteRoom[]
}

// The layout in use ('current') or a draft of a polishing pass (data/institute/drafts/)
export interface InstituteLayoutEntry {
  name: string
  title: string
  file: string
  problems: number
}

export interface InstituteLayoutReport {
  layout: InstituteLayout | null
  problems: string[]
  error: string | null
}
