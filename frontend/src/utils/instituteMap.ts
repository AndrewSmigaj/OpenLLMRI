// The institute's floor plan, worked out from its layout (types/institute.ts): each room a rectangle
// on the grid, walls wherever two rooms (or a room and the outside) meet, and a gap in a shared wall
// for each door, plus the front door. Pure, so it is unit-tested.
import type { InstituteLayout, InstituteRoom } from '../types/institute'

export const SCALE = 22 // pixels per metre
export const DOOR = 1.2 * SCALE // a door's width
export const PAD = 12 // margin around the building

export interface RoomRect {
  room: InstituteRoom
  x: number
  y: number
  w: number
  h: number
}

export interface Wall {
  x1: number
  y1: number
  x2: number
  y2: number
}

export interface Plan {
  width: number
  height: number
  rooms: RoomRect[]
  walls: Wall[] // with the doors already cut out
  doors: { a: string; b: string; x: number; y: number }[] // the middle of each door
  entrance: { x: number; y: number } | null
}

const offsets = (sizes: number[]) => sizes.reduce<number[]>((acc, s) => [...acc, acc[acc.length - 1] + s * SCALE], [0])

interface Segment {
  x1: number
  y1: number
  x2: number
  y2: number
  sides: [string | null, string | null] // the rooms on either side; null is outside
}

export function floorPlan(layout: InstituteLayout): Plan {
  const xs = offsets(layout.grid.columns).map(x => x + PAD)
  const ys = offsets(layout.grid.rows).map(y => y + PAD)
  const C = layout.grid.columns.length
  const R = layout.grid.rows.length
  const owner: (string | null)[][] = Array.from({ length: R }, () => Array<string | null>(C).fill(null))
  for (const room of layout.rooms) {
    const [c0, r0, c1, r1] = room.area
    for (let r = r0; r <= r1; r++) for (let c = c0; c <= c1; c++) if (owner[r]?.[c] === null) owner[r][c] = room.id
  }
  const at = (c: number, r: number) => (r >= 0 && r < R && c >= 0 && c < C ? owner[r][c] : null)

  // Every unit of wall: between cells (or a cell and the outside) that belong to different rooms
  const segments: Segment[] = []
  for (let r = 0; r < R; r++) {
    for (let c = 0; c <= C; c++) {
      const left = at(c - 1, r)
      const right = at(c, r)
      if (left !== right) segments.push({ x1: xs[c], y1: ys[r], x2: xs[c], y2: ys[r + 1], sides: [left, right] })
    }
  }
  for (let r = 0; r <= R; r++) {
    for (let c = 0; c < C; c++) {
      const above = at(c, r - 1)
      const below = at(c, r)
      if (above !== below) segments.push({ x1: xs[c], y1: ys[r], x2: xs[c + 1], y2: ys[r], sides: [above, below] })
    }
  }

  // Each door goes in the middle of the wall its two rooms share
  const cuts = new Map<Segment, { x: number; y: number }>()
  const doors: Plan['doors'] = []
  const between = (s: Segment, a: string | null, b: string | null) =>
    (s.sides[0] === a && s.sides[1] === b) || (s.sides[0] === b && s.sides[1] === a)
  const cutMiddle = (shared: Segment[]) => {
    if (!shared.length) return null
    const s = shared[Math.floor((shared.length - 1) / 2)]
    const middle = { x: (s.x1 + s.x2) / 2, y: (s.y1 + s.y2) / 2 }
    cuts.set(s, middle)
    return middle
  }
  for (const [a, b] of layout.doors) {
    const middle = cutMiddle(segments.filter(s => between(s, a, b)))
    if (middle) doors.push({ a, b, ...middle })
  }
  // The front door: the middle of the entrance room's front wall
  const entrance = cutMiddle(segments.filter(s => s.y1 === s.y2 && s.y1 === ys[R] && between(s, layout.entrance, null)))

  const walls: Wall[] = []
  for (const s of segments) {
    const cut = cuts.get(s)
    if (!cut) { walls.push({ x1: s.x1, y1: s.y1, x2: s.x2, y2: s.y2 }); continue }
    if (s.x1 === s.x2) { // a vertical wall: leave a gap around the door's middle
      walls.push({ x1: s.x1, y1: s.y1, x2: s.x1, y2: cut.y - DOOR / 2 }, { x1: s.x1, y1: cut.y + DOOR / 2, x2: s.x1, y2: s.y2 })
    } else {
      walls.push({ x1: s.x1, y1: s.y1, x2: cut.x - DOOR / 2, y2: s.y1 }, { x1: cut.x + DOOR / 2, y1: s.y1, x2: s.x2, y2: s.y1 })
    }
  }

  return finish(layout, xs, ys, mergeWalls(walls), doors, entrance)
}

// Wall pieces that continue one another become one line, so joins draw cleanly
export function mergeWalls(walls: Wall[]): Wall[] {
  const merged: Wall[] = []
  const flat = walls.filter(w => w.y1 === w.y2).map(w => ({ ...w, x1: Math.min(w.x1, w.x2), x2: Math.max(w.x1, w.x2) }))
  const upright = walls.filter(w => w.x1 === w.x2).map(w => ({ ...w, y1: Math.min(w.y1, w.y2), y2: Math.max(w.y1, w.y2) }))
  flat.sort((a, b) => a.y1 - b.y1 || a.x1 - b.x1)
  for (const w of flat) {
    const last = merged[merged.length - 1]
    if (last && last.y1 === last.y2 && last.y1 === w.y1 && w.x1 <= last.x2) last.x2 = Math.max(last.x2, w.x2)
    else merged.push({ ...w })
  }
  upright.sort((a, b) => a.x1 - b.x1 || a.y1 - b.y1)
  for (const w of upright) {
    const last = merged[merged.length - 1]
    if (last && last.x1 === last.x2 && last.x1 === w.x1 && w.y1 <= last.y2) last.y2 = Math.max(last.y2, w.y2)
    else merged.push({ ...w })
  }
  return merged
}

function finish(layout: InstituteLayout, xs: number[], ys: number[], walls: Wall[], doors: Plan['doors'],
  entrance: Plan['entrance']): Plan {
  const C = layout.grid.columns.length
  const R = layout.grid.rows.length
  const rooms = layout.rooms.map(room => {
    const [c0, r0, c1, r1] = room.area
    return { room, x: xs[c0], y: ys[r0], w: xs[c1 + 1] - xs[c0], h: ys[r1 + 1] - ys[r0] }
  })
  return { width: xs[C] + PAD, height: ys[R] + PAD, rooms, walls, doors, entrance }
}

// The visitors' rooms: the entrance room and every room with a door onto it, corridors aside
export function visitorRooms(layout: InstituteLayout): Set<string> {
  const corridors = new Set(layout.rooms.filter(r => r.corridor).map(r => r.id))
  const found = new Set([layout.entrance])
  for (const [a, b] of layout.doors) {
    if (a === layout.entrance && !corridors.has(b)) found.add(b)
    if (b === layout.entrance && !corridors.has(a)) found.add(a)
  }
  return found
}

// A room's fill: each department's rooms share a light tint of its colour; visitors' rooms are warm,
// shared rooms white, corridors pale
const DEPARTMENT_TINTS = ['#dbeafe', '#ede9fe', '#d1fae5', '#fce7f3', '#fef3c7', '#cffafe']
export const FILLS = { visitors: '#fff7ed', shared: '#ffffff', corridor: '#f3f4f6' }

export function roomFill(room: InstituteRoom, layout: InstituteLayout, visitors: Set<string>): string {
  if (room.corridor) return FILLS.corridor
  if (room.department) {
    const index = layout.departments.findIndex(d => d.id === room.department)
    return DEPARTMENT_TINTS[Math.max(0, index) % DEPARTMENT_TINTS.length]
  }
  return visitors.has(room.id) ? FILLS.visitors : FILLS.shared
}

// A name broken into lines of at most `max` characters, at spaces; a short last word ("room 1")
// takes the word before it along rather than stand alone
export function wrapWords(text: string, max: number): string[] {
  const lines: string[] = []
  for (const word of text.split(/\s+/).filter(Boolean)) {
    const last = lines[lines.length - 1]
    if (last !== undefined && last.length + 1 + word.length <= max) lines[lines.length - 1] = `${last} ${word}`
    else lines.push(word)
  }
  const end = lines.length - 1
  if (end > 0 && lines[end].length <= 2 && lines[end - 1].includes(' ')) {
    const cut = lines[end - 1].lastIndexOf(' ')
    lines[end] = `${lines[end - 1].slice(cut + 1)} ${lines[end]}`
    lines[end - 1] = lines[end - 1].slice(0, cut)
  }
  return lines
}

// What each app room is called, and what does its job until the room is built
export const APP_ROOM_NAMES: Record<string, string> = {
  entrance: 'the entrance hall', simulation: 'a simulation room', department: 'a department', lab: 'a lab',
  observatory: 'the observatory', workshop: 'the lens workshop', library: 'the library',
  studies: 'the studies room', meeting: 'the meeting room',
}
export const TODAY: Record<string, string> = {
  observatory: '/layers', workshop: '/build', lab: '/layers',
}
