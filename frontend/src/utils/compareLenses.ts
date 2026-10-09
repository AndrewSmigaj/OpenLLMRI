// Comparing lenses of one capture (DESIGN.md E3): each lens's held-out score per layer at its
// version's k, read from its validation; a tuned lens's test score and its source lens's on the same
// test items, read from its search; the gaps where a layer's k lies outside what validation scores;
// and warnings where the lenses can't be compared fairly (other folds, filters or items).
import type { LensSearch, LensSummary, Validation } from '../types/lens'

export type CompareMeasure = 'ami' | 'kappa' | 'accuracy'

export interface ComparedLens {
  lens: LensSummary
  validation: Validation | null
  search: LensSearch | null
}

export interface CompareLine {
  name: string
  lens: string
  kind: 'held out' | 'test' | 'source on test'
  values: (number | null)[] // one per layer of the comparison
  biased: boolean // the lens's settings were chosen on held-out scores of these items
}

export interface LensComparison {
  layers: number[]
  lines: CompareLine[]
  gaps: { lens: string; layers: number[]; why: string }[]
  warnings: string[]
}

const foldsOf = (v: Validation) =>
  `${v.folds.n_folds} folds${v.folds.merged_from ? ` (merged from ${v.folds.merged_from})` : ''}, `
  + `${v.folds.weaker ? 'stratified' : `whole families by "${v.folds.field ?? 'scene'}"`}`

export function compareLenses(chosen: ComparedLens[], axis: string, measure: CompareMeasure): LensComparison {
  const validated = chosen.filter(c => c.validation)
  const layers = [...new Set(validated.flatMap(c => Object.keys(c.validation!.layers).map(Number)))].sort((a, b) => a - b)
  const lines: CompareLine[] = []
  const gaps: LensComparison['gaps'] = []
  for (const { lens, validation, search } of validated) {
    const own = Object.keys(validation!.layers).map(Number).sort((a, b) => a - b)
    const ks = lens.k_per_layer ?? []
    const above: number[] = []
    const values = layers.map(layer => {
      const k = ks[own.indexOf(layer)]
      if (k === undefined) return null
      const entry = validation!.layers[String(layer)]?.[String(k)]
      if (!entry) { above.push(layer); return null }
      return entry.heldout[axis]?.[measure] ?? null
    })
    const biased = !!lens.selection_biased
    lines.push({ name: `${lens.name}${biased ? ' (settings chosen on held-out scores)' : ''}`, lens: lens.name,
      kind: 'held out', values, biased })
    if (above.length) gaps.push({ lens: lens.name, layers: above, why: 'its k there is above 10; validation scores k from 2 to 10' })
    if (search && search.target_axis === axis) {
      const read = (scores: { [m in CompareMeasure]: number | null } | null | undefined) => scores?.[measure] ?? null
      const at = (values: (number | null)[]) => layers.map(layer => {
        const i = search.layers.indexOf(layer)
        return i < 0 ? null : values[i]
      })
      lines.push({ name: `${lens.name}, on its test portion`, lens: lens.name, kind: 'test',
        values: at(search.winners.map(w => read(w.test))), biased: false })
      lines.push({ name: `${search.source.name}, on the same test portion`, lens: lens.name, kind: 'source on test',
        values: at(search.baseline.layers.map(b => read(b.test))), biased: false })
    }
  }

  const warnings: string[] = []
  const unvalidated = chosen.filter(c => !c.validation).map(c => c.lens.name)
  if (unvalidated.length) warnings.push(`not validated, so not shown: ${unvalidated.join(', ')}`)
  const folds = new Set(validated.map(c => foldsOf(c.validation!)))
  if (folds.size > 1) warnings.push(`held out differently: ${[...folds].join('; ')}`)
  const filters = new Set(validated.map(c => JSON.stringify(c.lens.filters ?? {})))
  if (filters.size > 1) warnings.push('the lenses use different filters')
  const items = new Set(validated.map(c => c.lens.n_items))
  if (items.size > 1) warnings.push(`different numbers of items: ${[...items].join(', ')}`)
  return { layers, lines, gaps, warnings }
}
