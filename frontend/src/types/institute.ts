// The institute's layout as GET /api/institute/layout serves it (data/institute/layout.yaml;
// backend/src/services/institute.py holds the rules a whole layout keeps).

export type Direction = 'north' | 'south' | 'east' | 'west' | 'northeast' | 'northwest' | 'southeast'
  | 'southwest' | 'up' | 'down'

export type AppRoom = 'entrance' | 'simulation' | 'department' | 'observatory' | 'workshop' | 'library'
  | 'studies' | 'meeting'

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
  exits: Partial<Record<Direction, string>>
  closed: Partial<Record<Direction, string>> // out of service, with what a player is told
  characters: InstituteCharacter[]
}

export interface InstituteLayout {
  version: number
  floors: InstituteFloor[] // from the bottom up
  departments: InstituteDepartment[]
  rooms: InstituteRoom[]
}

export interface InstituteLayoutReport {
  layout: InstituteLayout | null
  problems: string[]
  error: string | null
}
