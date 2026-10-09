// The lens API (backend/src/api/routers/lenses.py): lenses and legacy schemas share these shapes.

export type AxisCounts = Record<string, Record<string, number>>

// UMAP's distance metrics (a lens built before the metric existed reads as Euclidean)
export type Metric = 'euclidean' | 'cosine' | 'correlation' | 'manhattan'

// One layer's UMAP settings
export interface UmapSettings {
  n_neighbors: number
  dimensions: number
  min_dist: number
  metric: Metric
}

// Where a layer's settings came from: the form, the per-layer table, a preview (in-sample or held
// out) or a search. Held-out previews and searches make the lens's own validation selection-biased.
export type SettingsSource = 'form' | 'table' | 'preview' | 'preview held out' | 'tuned'

// A UMAP lens's settings, as its manifest holds them
export interface LensSettings extends Partial<UmapSettings> {
  seed?: number
  grouping?: string
  per_layer?: UmapSettings[] | null
  sources?: SettingsSource[] | null
}

// How a lens is held out (DESIGN.md C4): whole families by a categories field (null: stratified
// folds, marked weaker), at most max_folds family folds, and the share a search's test portion takes
export interface HoldoutDesign {
  family_field: string | null
  whole_families: boolean
  max_folds: number | null
  test_share: number
}

export interface LensSummary {
  name: string
  kind: string // 'umap' or 'mass_mean'
  legacy: boolean
  contrast?: { label_a: string; label_b: string } | null
  session_id: string
  n_items: number | null
  settings: LensSettings
  settings_origin?: 'tuned' | 'by hand' | 'form' // only a search's settings read as tuned
  selection_biased?: boolean // some layer's settings were chosen on held-out scores of these items
  holdout?: HoldoutDesign // the lens's own design (older lenses: the one their validation used)
  site?: { source: string; token_position: number }
  filters?: { labels?: string[] | null; steps?: number[] | null; last_occurrence_only?: boolean; max_items?: number | null }
  current?: string | null
  versions?: string[]
  state?: string | null
  k_per_layer?: number[] | null
  created_at?: string | null
  created_by?: string | null
  self_check?: SelfCheck | null
  validation?: ValidationHeadline | null
  tuning?: TuningHeadline | null // a tuned lens: its headline layer (picked on selection folds) and that layer's test scores
  details?: string[] // the versions with node details worked out ('mass_mean' for a mass-mean lens)
  readings?: ReadingListing[] // a UMAP lens: the captures read through it
  axes?: boolean // a UMAP lens: whether the axes analysis has run on it
}

// A capture read through a UMAP lens (DESIGN.md B5), as the lens's summary lists it
export interface ReadingListing {
  key: string
  target: string // the capture read
  n_items: number
  n_in_lens: number // of them, the lens's own items (they keep their stored nodes)
  filters: { labels?: string[] | null; steps?: number[] | null; last_occurrence_only?: boolean; max_items?: number | null }
  steps: number[] | null
  far_out: boolean // the capture's median sits beyond the 75th percentile of the lens's own at some layer
  max_median_percentile: number | null
  created_at: string
}

export interface ReadingItem {
  probe_id: string
  label: string | null
  categories: Record<string, string>
  output_category: string | null
  input_text: string | null
  target_word: string | null
  step: number | null
  run: string | null
}

// A reading at one of the lens's versions: per item and layer, its node (voted from its nearest
// lens items, or stored for the lens's own), the winner's share of the vote (null for lens items),
// how far out it sits (a percentile, in the residual stream) and its expert at the rank
export interface LensReading {
  key: string
  lens: string
  version: string
  target: string
  site: { source: string; token_position: number }
  layers: number[]
  rank: number
  items: ReadingItem[]
  in_lens: number[]
  nodes: number[][]
  shares: (number | null)[][]
  pct: number[][]
  experts: number[][]
  distance: { median_percentile: number[]; far_out: boolean[]; threshold: number; measure: string }
}

// A lens's expert pipelines, hubs and the experts involved in each designed value (DESIGN.md C7)
export interface RouteStep { layer: number; expert: number; share: number }
export interface RoutePipeline {
  id: string // P1, P2, ... strongest first
  layers: number[]
  experts: number[] // the chain, one expert per layer
  members: number // items keeping every expert of the chain among their four
  weighted: number // the members' credit: the geometric mean of their weights along the chain
  mean_weight: number
  rank1: number // members taking the chain as their top expert all the way
  makeup: Record<string, Record<string, number>>
  replicated: boolean // found again by following the bundle in each half of the folds
  before: RouteStep[]
  after: RouteStep[]
  member_ids: string[]
  nodes: Record<string, number>[] // at each of its layers: node -> members, at the served version
}
export interface RouteHub {
  id: string
  layer: number
  expert: number
  weighted: number
  items: number
  sources: number // effective number of sources, between items
  from: { expert: number; share: number }[]
  to: { expert: number; share: number }[]
}
export interface InvolvedExpert { layer: number; expert: number; diff: number; favours: string; auc: number }
export interface LensRoutes {
  version: string | null
  n_items: number
  layers: number[]
  min_items: number
  base: Record<string, Record<string, number>>
  pipelines: RoutePipeline[]
  hubs: RouteHub[]
  involved: Record<string, Record<string, { n: number; threshold: number; permuted: string; experts: InvolvedExpert[] }>>
}

// The axes analysis (DESIGN.md C8): per layer and designed attribute, each technique's held-out
// kappa against decoys; the spectrum; the partial axes' angles beside the design's correlations
export type AxesTechnique = 'raw_ward' | 'raw_spectral' | 'probe' | 'directions' | 'component'
export interface AxesSpectrum { shares: number[]; participation_ratio: number; for_half: number; for_90: number }
export interface AxesGeometry {
  names: string[] // one row per two-valued attribute, one per value of a larger one
  cosines: number[][]
  null_cosines?: { low: number[][]; high: number[][] } // permuted design rows: each pair's 5th and 95th percentile
  independent: number // the independent directions among the partial axes (participation ratio)
  null: [number, number, number] // the same with design rows permuted: 5th, 50th, 95th percentile
}
export interface LensAxes {
  format_version: number
  lens: string
  version: string
  layers: number[]
  attributes: Record<string, string[]>
  folds: { kind: string; n_folds: number; weaker: boolean; field?: string }
  techniques: AxesTechnique[]
  level: number
  decoys: { count: number; given_per: 'families' | 'texts' }
  probe_decoy_layers: number[]
  scores: Record<AxesTechnique, Record<string, Record<string, number>>[]> // per layer: code set (real, decoy1…) → attribute → kappa
  chosen_component: Record<string, number>[] // per layer: attribute → its best-matching component, from 1
  thresholds: Record<AxesTechnique, Record<string, number | null>>
  spectrum: AxesSpectrum[]
  geometry: AxesGeometry[]
  design: { names: string[]; correlations: number[][] }
  provenance: { commit: string; dirty: boolean; job_id: string; seconds: number }
  umap: {
    at_k: Record<string, number>[]
    best_k: Record<string, { k: number; kappa: number }>[]
    thresholds: { at_k: Record<string, number | null>; best_k: Record<string, number | null> }
    decoys: boolean // whether the lens's validation scored decoys (else no UMAP threshold)
  } | null
  k_per_layer: number[]
  recovered: Record<string, number[]> // per technique (and umap_at_k, umap_best_k): attributes recovered per layer
}

// The 3-D view's points (DESIGN.md E5): every item at every layer in the lens's own frame, each
// layer lined up with the one before; a reading's items in the same frame
export interface TrajectoryItem {
  probe_id: string
  label: string | null
  categories: Record<string, string>
  step: number | null
  target_word: string | null
}

export interface LensTrajectory {
  lens: string
  legacy: boolean
  fit: 'lens' | 'separate' // a legacy schema's own 3-D fit is separate from the space it clusters in
  layers: number[]
  share: number[] // per layer, the share of the embedding's variance the three directions hold
  items: TrajectoryItem[]
  points: [number, number, number][][] // [item][layer]
  read?: { key: string; items: TrajectoryItem[]; points: [number, number, number][][] }
}

export interface ReadBody {
  target?: string // the capture to read; the lens's own (its other steps) by default
  key?: string
  filters?: { steps?: number[] | null; labels?: string[] | null; last_occurrence_only?: boolean; max_items?: number | null }
  position?: number
  created_by?: string
}

export interface UmapSettings {
  n_neighbors: number
  dimensions: number
  min_dist: number
}

export interface SearchScores {
  ami: number | null
  kappa: number | null
  accuracy: number | null
  worst_fold: number | null
}

export interface TuningHeadline {
  source: { name: string; version: string | null }
  target_axis: string
  layer: number
  k: number
  test: SearchScores | null
  test_items: number
  weaker: boolean
}

export interface SearchGrid {
  n_neighbors: number[]
  dimensions: number[]
  min_dist: number[]
  metric?: Metric[] | null // none: the source lens's own metric
}

// What a lens search starts from, and the numbers its time estimate uses (GET /lenses/methods)
export interface TuningDefaults {
  grid: SearchGrid
  k_min: number
  k_max: number
  test_share: number
  n_folds: number
  family_field: string | null // null: each lens's own hold-out design
  max_settings: number
  seconds_per_fit: [number, number]
  workers: number
}

export interface TuneBody {
  name?: string
  target_axis?: string
  grid?: SearchGrid
  k_min?: number
  k_max?: number
  test_share?: number
  family_field?: string
  n_folds?: number
  seed?: number | null
  created_by?: string
}

// A tuned lens's search (search.json): every candidate's scores, the winners and their test scores
export interface LensSearch {
  format: number
  source: { name: string; version: string | null }
  tuned: string
  target_axis: string
  values: string[]
  n_items: number
  grid: SearchGrid
  ks: number[]
  configs: (UmapSettings & { id: number; eligible: boolean; self_check: { passed: boolean; ari_k5: number; ami_k5: number } })[]
  split: {
    test: { kind: string; weaker: boolean; n_items: number; share: number; families: Record<string, string[]> | null }
    selection: { n_items: number; folds: { kind: string; n_folds: number; weaker: boolean; merged_from?: number } }
  }
  layers: number[]
  winners: {
    layer: number
    config: number
    settings: UmapSettings
    k: number
    selection: SearchScores
    test: SearchScores | null
    runners_up: { config: number; settings: UmapSettings; k: number; ami: number }[]
  }[]
  baseline: { name: string; version: string | null; layers: { settings: UmapSettings; k: number; test: SearchScores | null }[] }
  comparison: { k: number; raw_ward: SearchScores | null; raw_spectral: SearchScores | null; neurons: SearchScores | null; ceiling: SearchScores | null }[]
  notes: string[]
  provenance: Record<string, unknown>
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
  assignments?: Record<string, Record<string, number>> // each item's node (or expert at the rank) per layer
  output_of?: Record<string, string> // cluster flows: each item's output node
  order?: number[][] // experts: each layer's experts top to bottom, the same at every rank
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

// What a capture offers a lens (GET /captures/{sid}/lens-options)
export interface LensOptions {
  session_id: string
  n_records: number
  target_words: Record<string, number>
  labels: Record<string, number>
  steps: Record<string, number>
  sources: Record<string, number[]> // each captured source, with its token positions
  default_items: number
  max_items: number
  layers: number[] // the captured layers
  category_fields: Record<string, number> // each categories field, with its number of values
  declared_holdout: HoldoutDesign | null // the hold-out design the capture's sentence set declared
}

// The methods a build can use (GET /lenses/methods)
export interface LensMethods {
  reductions: { id: string; label: string; defaults: Record<string, number> }[]
  groupings: { id: string; label: string }[]
  k_auto: { id: string; note: string }[]
  defaults: UmapSettings & { k: number; seed: number; source: string; token_position: number; last_occurrence_only: boolean }
  metrics: Metric[]
  holdout: HoldoutDesign // the defaults for a capture that declares none
  tuning?: TuningDefaults
}

export interface LensFiltersBody {
  labels?: string[] | null
  steps?: number[] | null
  last_occurrence_only?: boolean
  max_items?: number | null
}

// POST /lenses: exactly one of k, k_per_layer or k_auto chooses each layer's k
export interface LensBuildBody {
  session_id: string
  name: string
  n_neighbors: number
  dimensions: number
  min_dist: number
  metric: Metric
  per_layer?: UmapSettings[] | null // each layer's own settings, with where each came from in sources
  sources?: SettingsSource[] | null
  holdout?: HoldoutDesign
  k?: number
  k_per_layer?: number[]
  k_auto?: string
  source: string
  token_position: number
  filters: LensFiltersBody
  seed: number
  created_by: string
}

// POST /lenses/preview: one layer of a capture fitted with these settings (DESIGN.md E3)
export interface PreviewBody {
  session_id: string
  layer: number
  settings: UmapSettings
  k: number
  seed: number
  source: string
  token_position: number
  filters: LensFiltersBody
  holdout?: HoldoutDesign
  held_out: boolean
  created_by: string
}

// A finished preview (GET /lenses/previews/{job}): the layer's points on its three main directions,
// its nodes at k, and its scores, none of them taken on the test portion a tune would hold out
export interface LayerPreview {
  layer: number
  settings: UmapSettings
  k: number
  n_items: number
  axes: Record<string, string[]>
  share: number // the layer's variance its three main directions hold
  ks: number[]
  items: { probe_id: string; label: string | null; categories: Record<string, string>; input_text: string | null }[]
  points: [number, number, number][]
  nodes: number[]
  in_sample: { ami: Record<string, Record<string, number>>; silhouette: Record<string, number> }
  test: { n_items: number; weaker: boolean; kind: string; families?: Record<string, string[]> | null }
  heldout: Record<string, Record<string, { ami: number; kappa: number; accuracy: number }>> | null
  folds: Folding | null
  holdout: HoldoutDesign
  seconds: number
}

export interface LensVersion {
  version: string
  k_per_layer: number[]
  k_source: string[]
  state: 'draft' | 'saved'
  keywords: string[]
  created_at: string
  saved_at?: string | null
  analysis_job_id?: string // a save's reports, being written in the background
}

// A layer's in-sample k suggestions, from the build
export interface KSuggestion {
  elbow: number
  silhouette: number
  levels: number[]
  silhouette_by_k: Record<string, number>
}

export interface LensDetail {
  name: string
  legacy: boolean
  layers: number[]
  axes: Record<string, string[]>
  n_items: number
  manifest?: { suggestions: Record<string, KSuggestion>; versions: string[]; current: string | null } & Record<string, unknown>
}

// A population's mean gate weight on each expert at each layer; each row sums to 1
export interface Fingerprint {
  layers: number[]
  experts: number
  grid: number[][]
  n_items: number
  recipe: Record<string, unknown>
}

// Every item, a node at a layer, or an axis value
export type Population = { layer?: number; node?: number; axis?: string; value?: string }

// The self-check every build runs: planted classes found, nothing found in noise
export interface SelfCheck {
  passed: boolean
  items: number
  dims: number
  planted: { ari_k5: number; passed: boolean; groups_ari_k2: number; levels: number[] }
  null: { ami_k5: number; passed: boolean }
  thresholds: { planted_ari: number; null_ami: number }
}

export interface HeldOut {
  kappa: number
  accuracy: number
  worst_fold: number
  ami: number
}

// One k at one layer: in-sample measures and held-out scores per axis
export interface KProfileEntry {
  silhouette: number
  seed_ari: number | null
  agreement: Record<string, number> // per axis and per pair of axes ("a×b")
  heldout: Record<string, HeldOut>
}

// The fair comparison at one layer, on the label: raw groupings at every k, and the ceiling
export type Comparison = Partial<Record<'raw_ward' | 'raw_spectral' | 'neurons', Record<string, HeldOut | null>>> & { ceiling?: HeldOut | null }

export interface Folding {
  kind: string
  n_folds: number
  weaker: boolean
  field?: string
  whole?: boolean
  families?: Record<string, string[]>
  merged_from?: number // family folds merged round-robin beyond the lens's fold cap
}

// A lens's validation.json: per layer, per k
export interface Validation {
  format: number
  folds: Folding
  axes: Record<string, string[]>
  seeds: number
  vote_neighbours: number
  layers: Record<string, Record<string, KProfileEntry>>
  comparison?: Record<string, Comparison>
  provenance: { commit: string; dirty: boolean; job_id: string; seconds: number; created_at: string }
}

export interface ValidationHeadline {
  folds: Folding
  best: ({ layer: number; k?: number; accuracy: number; kappa: number; worst_fold: number; ami?: number }) | null
  created_at: string
}

// Where the UMAP lens and the best raw grouping disagree, per layer (GET .../marks)
export interface LensMarks {
  threshold: number
  layers: Record<string, { method: string; k: number; marked: string[]; nodes: Record<string, number> }>
}

// A mass-mean lens's validation.json: held-out scores per layer (the paper's algorithm)
export interface MassMeanValidation {
  format: number
  kind: 'mass_mean'
  contrast: { label_a: string; label_b: string }
  folds: Folding
  layers: Record<string, { accuracy: number; pooled_accuracy: number; kappa: number; worst_fold: number;
    folds: number; n_a: number; n_b: number; axis_norm: number }>
  provenance: { seconds: number; created_at: string }
}

// A token and its logit (or its logit above a baseline), as the logit lens reads them
export type TokenScore = [string, number]

export interface Provenance {
  commit: string
  dirty: boolean
  job_id: string
  seconds: number
  created_at: string
}

// What comes with one cluster node (DESIGN.md C5)
export interface NodeDetail {
  neurons: [number, number][] // neuron index, correlation of its value with membership
  logit_lens: { top: TokenScore[]; distinctive: TokenScore[] }
  surface: {
    flagged: boolean
    feature: string // the numeric surface feature that separates the node most
    auc: number
    members_mean: number | null
    others_mean: number | null
    first_word: { word: string; in_node: number; outside: number }
  } | null
  routing: { share: number; shift: number } | null // null at the last layer
}

// A UMAP lens version's node details (GET .../details)
export interface LensNodeDetails {
  kind: 'umap'
  layers: Record<string, {
    surface_kappa: number | null // surface features alone predicting the layer's nodes, held out
    routing_effect: number | null // the nodes' share of the next layer's routing variance
    nodes: Record<string, NodeDetail>
  }>
  provenance: Provenance
}

// The routing change an axis predicts through the next layer's router, against random directions
// of the same length (ratio to their median; the share of them it exceeds)
export interface RouterAlignment {
  ratio: number
  percentile: number
  random_95: number
}

// A mass-mean lens's layer details (GET .../details)
export interface MassMeanDetails {
  kind: 'mass_mean'
  layers: Record<string, {
    router_alignment?: RouterAlignment // absent at the last layer
    logit_lens: { b_over_a: TokenScore[]; a_over_b: TokenScore[] }
  }>
  provenance: Provenance
}
