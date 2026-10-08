// Where the columns of the all-layer charts fall. Zoom z fits z layer-to-layer steps in view
// (z + 1 columns), as the old six-step windows did; both charts share these numbers, so their
// columns line up as they scroll together.
import { isOutputNode } from '../constants/outputNodes'
import type { RouteAnalysisResponse } from '../types/api'

export const LEFT = 8 // pixels before the first column
export const RIGHT = 110 // room for the last column's labels
export const NODE_WIDTH = 6

// The column labels: every layer, then the output column when the capture has generated outputs
export function columnsOf(routes: RouteAnalysisResponse | null): string[] {
  if (!routes) return []
  const layers = (routes.window_layers ?? []).map(l => `L${l}`)
  return routes.nodes.some(n => isOutputNode(n.name)) ? [...layers, 'Output'] : layers
}

// Steps in view: the zoom, or every step when there are fewer
export const stepsInView = (columns: number, zoom: number) => Math.max(1, Math.min(zoom, columns - 1))

// Pixels from one column to the next, so `steps` steps fill the visible width
export const spacingFor = (visibleWidth: number, steps: number) =>
  Math.max(24, (visibleWidth - LEFT - RIGHT - NODE_WIDTH) / steps)

export const chartWidth = (columns: number, spacing: number) =>
  LEFT + RIGHT + NODE_WIDTH + spacing * Math.max(0, columns - 1)

// The furthest first column, so the last steps still fill the view
export const lastFirst = (columns: number, steps: number) => Math.max(0, columns - 1 - steps)
