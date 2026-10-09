import { describe, expect, it } from 'vitest'
import { optionRows } from './exportFigure'

describe('chart rows', () => {
  it('gives a line chart one row per category, a column per series', () => {
    const rows = optionRows({
      xAxis: { type: 'category', data: ['L0', 'L1'] },
      series: [{ type: 'line', name: 'κ', data: [0.1, 0.6] }, { type: 'line', name: 'worst fold', data: [0.0, null] }],
    })
    expect(rows).toEqual([{ x: 'L0', κ: 0.1, 'worst fold': 0.0 }, { x: 'L1', κ: 0.6, 'worst fold': null }])
  })

  it('gives a heatmap one row per cell, with its axis labels', () => {
    const rows = optionRows({
      xAxis: { type: 'category', data: ['L0', 'L1'] }, yAxis: { type: 'category', data: ['k 2', 'k 3'] },
      series: [{ type: 'heatmap', data: [[0, 1, 0.5], [1, 0, 0.7]] }, { type: 'scatter', data: [[0, 0]] }],
    })
    expect(rows).toEqual([{ x: 'L0', y: 'k 3', value: 0.5 }, { x: 'L1', y: 'k 2', value: 0.7 }])
  })
})
