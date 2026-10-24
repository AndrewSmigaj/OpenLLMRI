// The institute's map, worked out from its layout (types/institute.ts): one plan per floor, the top
// floor first, each room a box at its grid place, each exit within a floor a line between two
// boxes, and the stairs as marks in the rooms they leave from. Pure, so it is unit-tested.
import type { Direction, InstituteFloor, InstituteLayout, InstituteRoom } from '../types/institute'

export const CELL_W = 176
export const CELL_H = 100
export const GAP_X = 52
export const GAP_Y = 44
export const PAD = 16
export const CLOSED_FLOOR_H = 56 // a closed floor holds no rooms: a band with its note

export interface RoomBox {
  room: InstituteRoom
  x: number
  y: number
  w: number
  h: number
}

export interface MapEdge {
  from: string
  to: string
  x1: number
  y1: number
  x2: number
  y2: number
}

export interface StairMark {
  room: string
  direction: 'up' | 'down'
  to: InstituteRoom | null // null when the stairs are out of service
  closed: string | null // what a player is told, when they are
}

export interface FloorPlan {
  floor: InstituteFloor
  boxes: RoomBox[]
  edges: MapEdge[]
  stairs: StairMark[]
  width: number
  height: number
}

const VERTICAL: Direction[] = ['up', 'down']

export function floorPlans(layout: InstituteLayout): FloorPlan[] {
  const byId = new Map(layout.rooms.map(room => [room.id, room]))
  const plans = layout.floors.map(floor => {
    const rooms = layout.rooms.filter(room => room.floor === floor.id)
    if (rooms.length === 0) {
      return { floor, boxes: [], edges: [], stairs: [], width: 2 * PAD + CELL_W, height: CLOSED_FLOOR_H }
    }
    const minCol = Math.min(...rooms.map(r => r.at[0]))
    const minRow = Math.min(...rooms.map(r => r.at[1]))
    const cols = Math.max(...rooms.map(r => r.at[0])) - minCol + 1
    const rows = Math.max(...rooms.map(r => r.at[1])) - minRow + 1
    const boxes = rooms.map(room => ({
      room,
      x: PAD + (room.at[0] - minCol) * (CELL_W + GAP_X),
      y: PAD + (room.at[1] - minRow) * (CELL_H + GAP_Y),
      w: CELL_W,
      h: CELL_H,
    }))
    const boxOf = new Map(boxes.map(box => [box.room.id, box]))
    const centre = (box: RoomBox) => [box.x + box.w / 2, box.y + box.h / 2]
    const edges: MapEdge[] = []
    const stairs: StairMark[] = []
    for (const box of boxes) {
      for (const [direction, target] of Object.entries(box.room.exits) as [Direction, string][]) {
        if (VERTICAL.includes(direction)) {
          stairs.push({ room: box.room.id, direction: direction as 'up' | 'down', to: byId.get(target) ?? null, closed: null })
          continue
        }
        const other = boxOf.get(target)
        if (!other || box.room.id > target) continue // each pair once
        const [x1, y1] = centre(box)
        const [x2, y2] = centre(other)
        edges.push({ from: box.room.id, to: target, x1, y1, x2, y2 })
      }
      for (const [direction, told] of Object.entries(box.room.closed) as [Direction, string][]) {
        if (VERTICAL.includes(direction)) {
          stairs.push({ room: box.room.id, direction: direction as 'up' | 'down', to: null, closed: told })
        }
      }
    }
    return {
      floor, boxes, edges, stairs,
      width: 2 * PAD + cols * CELL_W + (cols - 1) * GAP_X,
      height: 2 * PAD + rows * CELL_H + (rows - 1) * GAP_Y,
    }
  })
  return plans.reverse() // the top floor first, as a building is drawn
}

export const FLOOR_HEADER = 30 // the floor's name above its plan
export const FLOOR_GAP = 18

// The whole map as one drawing: each floor's plan below the one above, under its name
export function stackFloors(plans: FloorPlan[]): { tops: number[]; width: number; height: number } {
  const tops: number[] = []
  let y = 0
  for (const plan of plans) {
    tops.push(y + FLOOR_HEADER)
    y += FLOOR_HEADER + plan.height + FLOOR_GAP
  }
  return { tops, width: Math.max(...plans.map(p => p.width), 0), height: Math.max(0, y - FLOOR_GAP) }
}

// A name broken into lines of at most `max` characters, at spaces (a longer word keeps its line)
export function wrapWords(text: string, max: number): string[] {
  const lines: string[] = []
  for (const word of text.split(/\s+/).filter(Boolean)) {
    const last = lines[lines.length - 1]
    if (last !== undefined && last.length + 1 + word.length <= max) lines[lines.length - 1] = `${last} ${word}`
    else lines.push(word)
  }
  // A short last word ("room 1") takes the word before it along, rather than stand alone
  const last = lines.length - 1
  if (last > 0 && lines[last].length <= 2 && lines[last - 1].includes(' ')) {
    const cut = lines[last - 1].lastIndexOf(' ')
    lines[last] = `${lines[last - 1].slice(cut + 1)} ${lines[last]}`
    lines[last - 1] = lines[last - 1].slice(0, cut)
  }
  return lines
}

// Each department's colour, and the rooms' colours by what they open; a department's rooms take
// its colour, its simulation room a lighter tint of it
const DEPARTMENT_COLOURS = ['#2563eb', '#7c3aed', '#059669', '#db2777', '#d97706', '#0891b2']
const ROOM_COLOURS: Record<string, string> = {
  entrance: '#b45309', simulation: '#0f766e', library: '#4338ca', observatory: '#0369a1',
  workshop: '#6d28d9', studies: '#047857', meeting: '#c2410c',
}
const IN_MUD_ONLY = '#6b7280'

export function roomColour(room: InstituteRoom, layout: InstituteLayout): string {
  if (room.department) {
    const index = layout.departments.findIndex(d => d.id === room.department)
    return DEPARTMENT_COLOURS[Math.max(0, index) % DEPARTMENT_COLOURS.length]
  }
  return room.opens ? ROOM_COLOURS[room.opens] ?? IN_MUD_ONLY : IN_MUD_ONLY
}

// What each app room is called on the map, and what does its job until the room is built
export const APP_ROOM_NAMES: Record<string, string> = {
  entrance: 'the entrance hall', simulation: 'a simulation room', department: 'a department', lab: 'a lab',
  observatory: 'the observatory', workshop: 'the lens workshop', library: 'the library',
  studies: 'the studies room', meeting: 'the meeting room',
}
export const TODAY: Record<string, string> = {
  observatory: '/layers', workshop: '/build', lab: '/layers',
}

// How a room not built yet is drawn and named: Claude's suggestions dashed, rooms planned for later dotted
export const STAGE_STYLE: Record<string, { stroke: string; dash: string; label: string }> = {
  suggested: { stroke: '#d97706', dash: '6 4', label: 'suggested by Claude' },
  later: { stroke: '#6b7280', dash: '2 3', label: 'planned for later' },
}

// What a room's box says under its name
export function roomCaption(room: InstituteRoom): string {
  if (room.stage) return STAGE_STYLE[room.stage].label
  return room.opens ? `opens ${APP_ROOM_NAMES[room.opens]}` : 'in the MUD only'
}
