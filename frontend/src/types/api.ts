// API types matching backend Pydantic schemas


interface CaptureManifest {
  capture_session_id?: string;
  session_name: string;
  target_word: string;
  labels: string[];
  layers_captured?: number[];
  probe_count: number;
  created_at: string;
  model_name: string;
}

interface SessionStatus {
  session_id: string;
  state: 'pending' | 'running' | 'completed' | 'failed';
  progress: {
    completed: number;
    total: number;
    failed: number;
    percent: number;
  };
  manifest?: CaptureManifest;
  data_lake_paths?: {
    tokens: string;
    routing: string;
    expert_output: string;
    manifest: string;
  };
}

interface SessionListItem {
  session_id: string;
  session_name: string;
  created_at: string;
  probe_count: number;
  target_word?: string;
  labels?: string[];
  state: string;
}

interface SessionDetailResponse {
  manifest: CaptureManifest;
  data_lake_paths: {
    tokens: string;
    routing: string;
    expert_output: string;
    manifest: string;
  };
  labels: string[];
  target_word?: string;
  sentences?: ProbeExample[];
}

// Expert Route Analysis Types
interface ProbeExample {
  target_word: string
  label?: string
  input_text: string
  probe_id: string
  generated_text?: string
  output_category?: string
  target_char_offset?: number
  turn_id?: number
  capture_type?: string
  step?: number
  game_text?: string
  analysis?: string
  action?: string
  system_prompt?: string
}

interface RouteStatistics {
  total_routes: number
  total_probes: number
  routes_coverage: number
  window_layers: number[]
  [key: string]: unknown
}

interface AnalyzeRoutesRequest {
  session_ids: string[]
  schema_name: string
  transition_layers: number[]
  expert_rank?: number
  output_grouping_axes?: string[]
  top_n_routes?: number
}

interface AnalyzeClusterRoutesRequest {
  session_ids: string[]
  schema_name: string
  transition_layers: number[]
  output_grouping_axes?: string[]
  top_n_routes?: number
  max_examples_per_node?: number
}

interface SankeyNode {
  name: string
  id: string
  layer: number
  expert_id: number
  token_count: number
  label_distribution?: Record<string, number>
  target_word_distribution?: Record<string, number>
  category_distributions?: Record<string, Record<string, number>>
  specialization: string
  tokens?: ProbeExample[]
  probe_ids?: string[]
  weight?: number // experts: the model's own mean gate weight at this rank
  output_distributions?: Record<string, Record<string, number>> // the output column: counts on the output's own axes
}

interface SankeyLink {
  source: string
  target: string
  value: number
  probability: number
  route_signature: string
  label_distribution?: Record<string, number>
  target_word_distribution?: Record<string, number>
  category_distributions?: Record<string, Record<string, number>>
  output_distributions?: Record<string, Record<string, number>> // links into the output column
  token_count: number
  tokens?: ProbeExample[]
}

interface TopRoute {
  signature: string
  count: number
  coverage: number
  avg_confidence: number
  example_tokens: ProbeExample[]
}

interface DynamicAxis {
  id: string
  label: string
  label_a: string
  label_b: string
  values?: string[]
}

interface RouteAnalysisResponse {
  session_id: string
  window_layers: number[]
  nodes: SankeyNode[]
  links: SankeyLink[]
  top_routes: TopRoute[]
  statistics: RouteStatistics
  available_axes?: DynamicAxis[]
  output_available_axes?: DynamicAxis[]
  probe_assignments?: Record<string, Record<string, number>>
}

interface RouteDetailsResponse {
  signature: string
  window_layers: number[]
  tokens: ProbeExample[]
  count: number
  coverage: number
  avg_confidence: number
  category_breakdown: Record<string, unknown>
}

interface ExpertDetailsResponse {
  layer: number
  expert_id: number
  node_name: string
  tokens: ProbeExample[]
  total_tokens: number
  usage_rate: number
  avg_confidence: number
  category_breakdown: Record<string, unknown>
}

// LLM Insights Types
interface LLMInsightsRequest {
  session_id: string
  windows: Record<string, unknown>[]
  user_prompt: string
  api_key: string
  provider?: 'openai' | 'anthropic'
}

interface LLMInsightsResponse {
  narrative: string
  statistics: Record<string, unknown>
}

// Trajectory Types



// Sentence Experiment Types
interface SentenceExperimentRequest {
  sentence_set_name: string
  session_name?: string
  generate_output?: boolean
}

interface SentenceExperimentResponse {
  session_id: string
  session_name: string
  total_probes: number
  labels: string[]
  counts: Record<string, number>
}

// Trajectory points (3D UMAP coordinates persisted with each schema)
interface TrajectoryPoint {
  probe_id: string
  x: number
  y: number
  z: number
  label?: string
  target_word?: string
  step?: number
  categories_json?: string
}

interface TrajectoryPointsResponse {
  schema_name: string
  sample_size: number
  layers: number[]
  points_by_layer: Record<string, TrajectoryPoint[]>
}

// Clustering Schema Types
interface ClusteringSchema {
  name: string
  created_at: string
  created_by: string
  params: {
    clustering_method: string
    reduction_method: string
    reduction_dimensions: number
    n_clusters?: number
    embedding_source: string
    n_neighbors?: number | null
    layer_cluster_counts?: Record<string, number>
    clustering_dimensions?: number[] | null
    [key: string]: unknown
  }
  windows?: { id: string; layers: number[] }[]
  sample_size?: number
  filter_config?: { labels?: string[] } | null
  last_occurrence_only?: boolean
  max_probes?: number | null
  steps?: number[]
}

// Export all types
export type {
  CaptureManifest,
  SessionStatus,
  SessionListItem,
  SessionDetailResponse,
  ProbeExample,
  RouteStatistics,
  AnalyzeRoutesRequest,
  AnalyzeClusterRoutesRequest,
  RouteAnalysisResponse,
  SankeyNode,
  SankeyLink,
  TopRoute,
  RouteDetailsResponse,
  ExpertDetailsResponse,
  LLMInsightsRequest,
  LLMInsightsResponse,
  DynamicAxis,
  SentenceExperimentRequest,
  SentenceExperimentResponse,
  TrajectoryPoint,
  TrajectoryPointsResponse,
  ClusteringSchema
};
