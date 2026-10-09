// A lens's summary in the shape the schema summary reads, so lenses and legacy schemas are
// described the same way.
import type { ClusteringSchema } from '../types/api'
import type { LensSummary } from '../types/lens'

const span = (values: number[]) => {
  const low = Math.min(...values)
  const high = Math.max(...values)
  return low === high ? `${low}` : `${low}–${high}`
}

// The settings in words, when they say more than "6D, n=15": per layer (tuned by a search, or set by
// hand), or a minimum distance or metric other than UMAP's defaults
export function settingsNote(lens: LensSummary): string | undefined {
  const settings = lens.settings
  const perLayer = settings.per_layer ?? []
  const extras = (rows: { min_dist?: number; metric?: string }[]) => {
    const dists = rows.map(r => r.min_dist ?? 0.1)
    const metrics = [...new Set(rows.map(r => r.metric ?? 'euclidean'))]
    return [dists.some(d => d !== 0.1) ? `min dist ${span(dists)}` : '',
      metrics.some(m => m !== 'euclidean') ? metrics.join('/') : ''].filter(Boolean).map(t => `, ${t}`).join('')
  }
  if (perLayer.length && lens.settings_origin !== 'form') {
    const how = lens.settings_origin === 'by hand' ? 'set by hand per layer' : 'tuned per layer'
    return `${how} (${span(perLayer.map(l => l.dimensions))}D, n=${span(perLayer.map(l => l.n_neighbors))}${extras(perLayer)})`
  }
  const more = extras([settings])
  return more ? `${settings.dimensions ?? '?'}D, n=${settings.n_neighbors ?? '?'}${more}` : undefined
}

export function lensAsSchema(lens: LensSummary): ClusteringSchema {
  const settings = lens.settings
  return {
    name: lens.name,
    created_at: lens.created_at ?? '',
    created_by: lens.created_by ?? '',
    params: {
      clustering_method: settings.grouping === 'ward' ? 'hierarchical' : String(settings.grouping ?? ''),
      reduction_method: lens.kind,
      reduction_dimensions: settings.dimensions ?? 0,
      n_neighbors: settings.n_neighbors,
      settings_note: settingsNote(lens),
      embedding_source: lens.site?.source ?? 'residual_stream',
      layer_cluster_counts: Object.fromEntries((lens.k_per_layer ?? []).map((k, i) => [String(i), k])),
    },
    sample_size: lens.n_items ?? undefined,
    last_occurrence_only: lens.filters?.last_occurrence_only,
    steps: lens.filters?.steps ?? undefined,
    max_probes: lens.filters?.max_items ?? undefined,
  }
}
