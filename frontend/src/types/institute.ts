// The institute's floor plan as GET /api/institute/layout serves it (data/institute/layout.yaml;
// backend/src/services/institute.py holds the rules a whole layout keeps).

export type AppRoom = 'entrance' | 'simulation' | 'department' | 'lab' | 'observatory' | 'workshop'
  | 'library' | 'studies' | 'meeting'

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
  area: [number, number, number, number] // first column, first row, last column, last row (rows from the back)
  summary: string
  opens: AppRoom | null // the app room it opens; null: in the MUD only
  department: string | null
  corridor: boolean // a way through, drawn as circulation
  notes: string[]
  characters: InstituteCharacter[]
}

export interface InstituteLayout {
  version: number
  title: string
  about: string
  grid: { columns: number[]; rows: number[] } // sizes in metres
  departments: InstituteDepartment[]
  rooms: InstituteRoom[]
  doors: [string, string][]
  entrance: string // the room the front door opens into
}

export interface InstituteLayoutReport {
  layout: InstituteLayout | null
  problems: string[]
  error: string | null
}
