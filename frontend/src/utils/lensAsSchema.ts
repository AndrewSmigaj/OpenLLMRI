// A lens's summary in the shape the schema summary reads, so lenses and legacy schemas are
// described the same way.
import type { ClusteringSchema } from '../types/api'
import type { LensSummary } from '../types/lens'

const span = (values: number[]) => {
  const low = Math.min(...values)
  const high = Math.max(...values)
  return low === high ? `${low}` : `${low}–${high}`
}

export function lensAsSchema(lens: LensSummary): ClusteringSchema {
  const settings = lens.settings as {
    n_neighbors?: number; dimensions?: number; grouping?: string
    per_layer?: { n_neighbors: number; dimensions: number }[] | null
  }
  const perLayer = settings.per_layer ?? []
  return {
    name: lens.name,
    created_at: lens.created_at ?? '',
    created_by: lens.created_by ?? '',
    params: {
      clustering_method: settings.grouping === 'ward' ? 'hierarchical' : String(settings.grouping ?? ''),
      reduction_method: lens.kind,
      reduction_dimensions: settings.dimensions ?? 0,
      n_neighbors: settings.n_neighbors,
      // A tuned lens: each layer has its own settings
      tuned_settings: perLayer.length
        ? `tuned per layer (${span(perLayer.map(l => l.dimensions))}D, n=${span(perLayer.map(l => l.n_neighbors))})` : undefined,
      embedding_source: lens.site?.source ?? 'residual_stream',
      layer_cluster_counts: Object.fromEntries((lens.k_per_layer ?? []).map((k, i) => [String(i), k])),
    },
    sample_size: lens.n_items ?? undefined,
    last_occurrence_only: lens.filters?.last_occurrence_only,
    steps: lens.filters?.steps ?? undefined,
    max_probes: lens.filters?.max_items ?? undefined,
  }
}
