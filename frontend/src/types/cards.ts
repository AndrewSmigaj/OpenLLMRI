// LLM analysis (backend/src/api/routers/analysis.py): cards written from evidence packets, with
// every number checked against the packet's facts.

export type Pattern = 'clear' | 'weak' | 'none'

export interface CardOutput {
  title: string
  pattern: Pattern
  summary: string
  points: string[]
  caveats: string[]
  disagreements?: string[] // the lens report's two drafts, where they differed
  sections?: { clusters: string; experts: string; pipelines_and_hubs: string } // the lens report's
}

export interface NumberFailure {
  numeral: string
  context: string
  reason: string
}

export interface NumberCheck {
  passed: boolean
  numerals: number
  failures: NumberFailure[]
  retried?: boolean
}

export interface Fact {
  id: string
  what: string
  value: number
}

export interface Card {
  card_id: string
  kind: string
  subject: string
  model: string
  written_by: string // 'claude -p' or 'Claude Code'
  analysts: number
  output: CardOutput | null
  check: NumberCheck | null
  error: string | null
  calls: number
  seconds: number
  created_at: string
  prompt_version: string
  facts: Record<string, Fact> // the facts the card cites
  tested: boolean // its analyst passed the analyst tests for this model and prompt version
  stale: boolean // its evidence has changed since it was written
}

export interface QuestionAnswer {
  id: string
  card_id: string
  question: string
  answer: string | null
  error: string | null
  check: NumberCheck | null
  model: string
  created_at: string
  facts: Record<string, Fact> // the facts the answer cites
}

export interface AnalystTestRun {
  created_at: string
  model: string
  prompt_version: string
  layer: number
  passed: boolean
  decoys: { clear: boolean }[]
  planted: { found: boolean }[]
  mean_accuracy: number | null
  lens: { session_id: string; name: string }
}

export interface AnalystTests {
  latest: AnalystTestRun | null
  prompt_version: string
  passing: { model: string; prompt_version: string }[]
}
