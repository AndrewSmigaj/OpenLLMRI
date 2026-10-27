import { describe, expect, it } from 'vitest'
import type { InstituteLayout, InstituteRoom } from '../types/institute'
import { DOOR, FILLS, PAD, SCALE, floorPlan, mergeWalls, roomFill, visitorRooms, wrapWords } from './instituteMap'

const room = (id: string, area: InstituteRoom['area'], extra: Partial<InstituteRoom> = {}): InstituteRoom => ({
  id, name: id, area, summary: '', opens: null, department: null, corridor: false, notes: [], characters: [], ...extra,
})

// Two columns by three rows: a department and its simulation room at the back, a corridor, and the
// entrance hall beside a public room at the front
const LAYOUT: InstituteLayout = {
  version: 2, title: 'A small institute', about: '',
  grid: { columns: [6, 6], rows: [4, 2, 4] },
  departments: [{ id: 'd', name: 'D' }],
  entrance: 'hall',
  rooms: [
    room('dept', [0, 0, 0, 0], { department: 'd', opens: 'department' }),
    room('deptsim', [1, 0, 1, 0], { department: 'd', opens: 'simulation' }),
    room('corridor', [0, 1, 1, 1], { corridor: true }),
    room('public', [0, 2, 0, 2], { opens: 'simulation' }),
    room('hall', [1, 2, 1, 2], { opens: 'entrance' }),
  ],
  doors: [['hall', 'public'], ['hall', 'corridor'], ['corridor', 'dept'], ['dept', 'deptsim']],
}

const onSegment = (p: { x: number; y: number }, w: { x1: number; y1: number; x2: number; y2: number }) =>
  (w.x1 === w.x2 && p.x === w.x1 && p.y >= Math.min(w.y1, w.y2) && p.y <= Math.max(w.y1, w.y2)) ||
  (w.y1 === w.y2 && p.y === w.y1 && p.x >= Math.min(w.x1, w.x2) && p.x <= Math.max(w.x1, w.x2))

describe('the institute floor plan', () => {
  const plan = floorPlan(LAYOUT)

  it('sizes the building from the grid in metres', () => {
    expect(plan.width).toBe(12 * SCALE + 2 * PAD)
    expect(plan.height).toBe(10 * SCALE + 2 * PAD)
  })

  it('places each room as a rectangle that tiles the building', () => {
    const area = plan.rooms.reduce((sum, r) => sum + r.w * r.h, 0)
    expect(area).toBeCloseTo(12 * SCALE * 10 * SCALE)
    const corridor = plan.rooms.find(r => r.room.id === 'corridor')!
    expect(corridor.w).toBe(12 * SCALE)
    expect(corridor.h).toBe(2 * SCALE)
  })

  it('puts every door in a wall its two rooms share, with a gap in that wall', () => {
    expect(plan.doors).toHaveLength(LAYOUT.doors.length)
    const hallPublic = plan.doors.find(d => d.a === 'hall' && d.b === 'public')!
    expect(hallPublic.x).toBe(PAD + 6 * SCALE) // the wall between the two front rooms
    for (const door of plan.doors) {
      expect(plan.walls.some(w => onSegment(door, w))).toBe(false) // nothing blocks the doorway
      const near = plan.walls.filter(w => onSegment({ x: door.x, y: door.y - DOOR / 2 }, w) ||
        onSegment({ x: door.x - DOOR / 2, y: door.y }, w))
      expect(near.length).toBeGreaterThan(0) // the wall runs up to the door
    }
  })

  it('opens the front door in the middle of the entrance room front wall', () => {
    expect(plan.entrance).toEqual({ x: PAD + 9 * SCALE, y: PAD + 10 * SCALE })
  })

  it('draws no wall inside a room', () => {
    const corridorMiddle = { x: PAD + 6 * SCALE, y: PAD + 5 * SCALE } // where the two corridor cells meet
    expect(plan.walls.some(w => onSegment(corridorMiddle, w))).toBe(false)
  })

  it('tints the visitors, the departments and the corridors apart', () => {
    const visitors = visitorRooms(LAYOUT)
    expect([...visitors].sort()).toEqual(['hall', 'public'])
    const fill = (id: string) => roomFill(LAYOUT.rooms.find(r => r.id === id)!, LAYOUT, visitors)
    expect(fill('public')).toBe(FILLS.visitors)
    expect(fill('corridor')).toBe(FILLS.corridor)
    expect(fill('dept')).toBe(fill('deptsim'))
    expect(fill('dept')).not.toBe(FILLS.shared)
  })

  it('joins wall pieces that continue one another, and keeps door gaps open', () => {
    expect(mergeWalls([{ x1: 0, y1: 0, x2: 10, y2: 0 }, { x1: 10, y1: 0, x2: 20, y2: 0 }, { x1: 25, y1: 0, x2: 30, y2: 0 }]))
      .toEqual([{ x1: 0, y1: 0, x2: 20, y2: 0 }, { x1: 25, y1: 0, x2: 30, y2: 0 }])
    const outer = plan.walls.filter(w => w.y1 === w.y2 && w.y1 === PAD) // the back wall: one line
    expect(outer).toEqual([{ x1: PAD, y1: PAD, x2: PAD + 12 * SCALE, y2: PAD }])
  })

  it('wraps a name at spaces', () => {
    expect(wrapWords('Public simulation room 1', 18)).toEqual(['Public simulation', 'room 1'])
    expect(wrapWords('Lounge', 18)).toEqual(['Lounge'])
  })
})
