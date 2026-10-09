import { describe, expect, it } from 'vitest'
import type { LensSearch, LensSummary, Validation } from '../types/lens'
import { compareLenses } from './compareLenses'

const lens = (name: string, k: number[], extra: Partial<LensSummary> = {}): LensSummary =>
  ({ name, kind: 'umap', legacy: false, session_id: 's', n_items: 100, settings: {}, k_per_layer: k, filters: {}, ...extra })

const scores = (ami: number) => ({ heldout: { label: { ami, kappa: ami - 0.1, accuracy: ami + 0.1, worst_fold: 0 } },
  silhouette: 0, seed_ari: null, agreement: {} })

const validation = (byLayer: Record<number, Record<number, number>>, folds: Partial<Validation['folds']> = {}): Validation => ({
  format: 1, folds: { kind: 'scene families', n_folds: 5, weaker: false, field: 'family', ...folds }, axes: { label: ['a', 'b'] },
  seeds: 3, vote_neighbours: 15,
  layers: Object.fromEntries(Object.entries(byLayer).map(([layer, ks]) =>
    [layer, Object.fromEntries(Object.entries(ks).map(([k, ami]) => [k, scores(ami)]))])),
  provenance: { commit: '', dirty: false, job_id: '', seconds: 0, created_at: '' },
})

describe('comparing lenses', () => {
  it("reads each lens at its own k, and leaves a gap where its k is above what validation scores", () => {
    const a = { lens: lens('a', [2, 3]), validation: validation({ 0: { 2: 0.5, 3: 0.4 }, 1: { 2: 0.6, 3: 0.7 } }), search: null }
    const b = { lens: lens('b', [12, 2]), validation: validation({ 0: { 2: 0.2 }, 1: { 2: 0.3 } }), search: null }
    const found = compareLenses([a, b], 'label', 'ami')
    expect(found.layers).toEqual([0, 1])
    expect(found.lines.map(l => l.values)).toEqual([[0.5, 0.7], [null, 0.3]])
    expect(found.gaps).toEqual([{ lens: 'b', layers: [0], why: expect.stringContaining('above 10') }])
    expect(compareLenses([a], 'label', 'kappa').lines[0].values.map(v => v?.toFixed(1))).toEqual(['0.4', '0.6'])
  })

  it("adds a tuned lens's test score and its source's, only for the axis it was tuned on", () => {
    const search = {
      target_axis: 'label', layers: [0, 1], source: { name: 'a', version: 'v1' },
      winners: [{ test: { ami: 0.8, kappa: 0.7, accuracy: 0.9, worst_fold: 0 } }, { test: null }],
      baseline: { name: 'a', version: 'v1', layers: [{ test: { ami: 0.6, kappa: 0.5, accuracy: 0.7, worst_fold: 0 } }, { test: null }] },
    } as unknown as LensSearch
    const tuned = { lens: lens('a-tuned', [2, 2], { selection_biased: true }), validation: validation({ 0: { 2: 0.9 }, 1: { 2: 0.9 } }), search }
    const found = compareLenses([tuned], 'label', 'ami')
    expect(found.lines.map(l => [l.kind, l.values])).toEqual([
      ['held out', [0.9, 0.9]], ['test', [0.8, null]], ['source on test', [0.6, null]]])
    expect(found.lines[0].biased && found.lines[0].name.includes('held-out scores')).toBe(true)
    expect(compareLenses([tuned], 'register', 'ami').lines).toHaveLength(1)
  })

  it('warns when the lenses were held out differently or hold other items', () => {
    const a = { lens: lens('a', [2]), validation: validation({ 0: { 2: 0.5 } }), search: null }
    const b = { lens: lens('b', [2], { n_items: 80 }), validation: validation({ 0: { 2: 0.5 } }, { field: 'order', merged_from: 30, n_folds: 12 }), search: null }
    const c = { lens: lens('c', [2]), validation: null, search: null }
    const warnings = compareLenses([a, b, c], 'label', 'ami').warnings.join(' | ')
    expect(warnings).toContain('not validated, so not shown: c')
    expect(warnings).toContain('12 folds (merged from 30), whole families by "order"')
    expect(warnings).toContain('different numbers of items: 100, 80')
  })
})
