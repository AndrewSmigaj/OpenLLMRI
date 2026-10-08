// The lens API (backend/src/api/routers/lenses.py): lenses and legacy schemas share these shapes.

export type AxisCounts = Record<string, Record<string, number>>

export interface LensSummary {
  name: string
  kind: string
  legacy: boolean
  session_id: string
  n_items: number | null
  settings: Record<string, unknown>
  site?: { source: string; token_position: number }
  filters?: { labels?: string[] | null; steps?: number[] | null; last_occurrence_only?: boolean; max_items?: number | null }
  current?: string | null
  versions?: string[]
  state?: string | null
  k_per_layer?: number[] | null
  created_at?: string | null
  created_by?: string | null
}

export interface FlowNode {
  id: string
  layer: number
  index: number
  count: number
  counts: AxisCounts
  weight?: number
}

export interface FlowLink {
  source: string
  target: string
  count: number
  counts?: AxisCounts
  output_counts?: AxisCounts // links into the output column: counts on the output's own axes
}

// The column after the last layer: each item's generated output, by its category or by its
// values on chosen output axes; `axes` are the outputs' own axes with their values.
export interface OutputColumn {
  axes: Record<string, string[]>
  nodes: (FlowNode & { value: string; output_counts?: AxisCounts })[]
  links: FlowLink[]
}

export interface LensFlows {
  kind: 'cluster' | 'expert'
  layers: number[]
  axes: Record<string, string[]>
  nodes: FlowNode[]
  links: FlowLink[]
  output: OutputColumn | null
  assignments?: Record<string, Record<string, number>>
  recipe: Record<string, unknown>
}

export interface LensMember {
  probe_id: string
  label: string | null
  categories: Record<string, unknown>
  output_category: string | null
  input_text: string
  target_word: string
  step?: number | null
  // Display fields read from the capture with each page
  generated_text?: string | null
  target_char_offset?: number | null
  turn_id?: number | null
  capture_type?: string | null
  game_text?: string | null
  analysis?: string | null
  action?: string | null
  previous_action?: string | null
  system_prompt?: string | null
}

export interface LensMembersPage {
  total: number
  offset: number
  items: LensMember[]
}

// A background job (backend/src/services/jobs/store.py), as GET /api/jobs returns it.
export type JobState = 'queued' | 'running' | 'done' | 'failed' | 'cancelled' | 'interrupted'

export interface JobView {
  id: string
  kind: string
  lane: string
  params: Record<string, unknown>
  state: JobState
  created_by: string
  created_at: string
  started_at?: string | null
  finished_at?: string | null
  progress: { stage: string; done: number; total: number }
  result?: Record<string, unknown> | null
  error?: string | null
  log_tail?: string | null
}

// What a members query can filter on: a node or an expert at a layer, a link to the next
// layer's node or expert, and the output column's category.
export interface MembersQuery {
  layer: number
  node?: number
  expert?: number
  rank?: number
  to_node?: number
  to_expert?: number
  output?: string
  offset?: number
  limit?: number
}
