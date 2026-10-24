import { describe, expect, it } from 'vitest'
import type { InstituteLayout, InstituteRoom } from '../types/institute'
import { CELL_H, CELL_W, GAP_X, floorPlans, roomCaption, roomColour, stackFloors, wrapWords } from './instituteMap'

const room = (id: string, floor: string, at: [number, number], exits: InstituteRoom['exits'],
  extra: Partial<InstituteRoom> = {}): InstituteRoom => ({
  id, name: id, floor, at, summary: '', opens: null, department: null, stage: null, exits, closed: {}, characters: [],
  ...extra,
})

const LAYOUT: InstituteLayout = {
  version: 1,
  title: 'A small institute',
  about: '',
  floors: [
    { id: 'ground', name: 'Ground', note: '', closed: false },
    { id: 'upper', name: 'Upper', note: '', closed: false },
    { id: 'attic', name: 'Attic', note: 'closed', closed: true },
  ],
  departments: [{ id: 'a', name: 'A' }, { id: 'b', name: 'B' }],
  rooms: [
    room('hall', 'ground', [1, 1], { north: 'sim', west: 'lounge', northeast: 'shop', up: 'landing' }, { opens: 'entrance' }),
    room('sim', 'ground', [1, 0], { south: 'hall' }, { opens: 'simulation' }),
    room('shop', 'ground', [2, 0], { southwest: 'hall' }, { opens: 'workshop' }),
    room('lounge', 'ground', [0, 1], { east: 'hall' }),
    room('landing', 'upper', [5, 5], { down: 'hall', east: 'dept' }, { closed: { up: 'Out of service.' } }),
    room('dept', 'upper', [6, 5], { west: 'landing' }, { opens: 'department', department: 'b' }),
  ],
}

describe('the institute map', () => {
  const plans = floorPlans(LAYOUT)

  it('draws the top floor first', () => {
    expect(plans.map(p => p.floor.id)).toEqual(['attic', 'upper', 'ground'])
  })

  it('gives a closed floor no rooms', () => {
    expect(plans[0].boxes).toEqual([])
    expect(plans[0].height).toBeGreaterThan(0)
  })

  it('places rooms on their grid without overlapping, from the first column and row of each floor', () => {
    const ground = plans[2]
    for (const a of ground.boxes) {
      for (const b of ground.boxes) {
        if (a === b) continue
        const apart = a.x + a.w <= b.x || b.x + b.w <= a.x || a.y + a.h <= b.y || b.y + b.h <= a.y
        expect(apart).toBe(true)
      }
    }
    const upper = plans[1]
    expect(Math.min(...upper.boxes.map(b => b.x))).toBe(Math.min(...ground.boxes.map(b => b.x))) // offset removed
    expect(upper.width).toBeGreaterThanOrEqual(2 * CELL_W)
    expect(ground.height).toBeGreaterThanOrEqual(2 * CELL_H)
  })

  it('draws each exit within a floor once, diagonals included, and stairs as marks', () => {
    const ground = plans[2]
    expect(ground.edges.map(e => [e.from, e.to].sort().join('-')).sort()).toEqual(['hall-lounge', 'hall-shop', 'hall-sim'])
    expect(ground.stairs).toEqual([{ room: 'hall', direction: 'up', to: LAYOUT.rooms[4], closed: null }])
    expect(plans[1].stairs).toContainEqual({ room: 'landing', direction: 'up', to: null, closed: 'Out of service.' })
    expect(plans[1].stairs).toContainEqual({ room: 'landing', direction: 'down', to: LAYOUT.rooms[0], closed: null })
  })

  it('stacks the floors under their names without overlapping', () => {
    const { tops, width, height } = stackFloors(plans)
    for (let i = 1; i < plans.length; i++) expect(tops[i]).toBeGreaterThanOrEqual(tops[i - 1] + plans[i - 1].height)
    expect(width).toBe(Math.max(...plans.map(p => p.width)))
    expect(height).toBe(tops[tops.length - 1] + plans[plans.length - 1].height)
  })

  it('wraps a name at spaces', () => {
    expect(wrapWords('Mechanistic interpretability simulation room', 22))
      .toEqual(['Mechanistic', 'interpretability', 'simulation room'])
    expect(wrapWords('Lounge', 22)).toEqual(['Lounge'])
    expect(wrapWords('Public simulation room 1', 22)).toEqual(['Public simulation', 'room 1'])
  })

  it('names what a room opens, or that it is suggested or planned for later', () => {
    expect(roomCaption(LAYOUT.rooms[0])).toBe('opens the entrance hall')
    expect(roomCaption(LAYOUT.rooms[3])).toBe('in the MUD only')
    expect(roomCaption({ ...LAYOUT.rooms[3], stage: 'suggested' })).toBe('suggested by Claude')
    expect(roomCaption({ ...LAYOUT.rooms[0], stage: 'later' })).toBe('planned for later')
  })

  it('draws an exit that crosses empty places as one line', () => {
    const long: InstituteLayout = { ...LAYOUT, rooms: [
      room('hall', 'ground', [0, 0], { east: 'far' }, { opens: 'entrance' }),
      room('far', 'ground', [3, 0], { west: 'hall' }),
    ] }
    const [plan] = floorPlans(long).filter(p => p.floor.id === 'ground')
    expect(plan.edges).toHaveLength(1)
    expect(Math.abs(plan.edges[0].x2 - plan.edges[0].x1)).toBe(3 * (CELL_W + GAP_X))
  })

  it('gives a department its own colour and other rooms the colour of what they open', () => {
    const [hall, sim, , lounge, landing, dept] = LAYOUT.rooms
    expect(roomColour(dept, LAYOUT)).not.toBe(roomColour(hall, LAYOUT))
    expect(roomColour(sim, LAYOUT)).not.toBe(roomColour(hall, LAYOUT))
    expect(roomColour(lounge, LAYOUT)).toBe(roomColour(landing, LAYOUT)) // both in the MUD only
  })
})
