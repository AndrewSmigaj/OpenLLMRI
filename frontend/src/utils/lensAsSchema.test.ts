import { describe, expect, it } from 'vitest'
import type { LensSummary, UmapSettings } from '../types/lens'
import { settingsNote } from './lensAsSchema'

const row = (n: number, d: number, extra: Partial<UmapSettings> = {}): UmapSettings =>
  ({ n_neighbors: n, dimensions: d, min_dist: 0.1, metric: 'euclidean', ...extra })
const lens = (settings: LensSummary['settings'], origin?: LensSummary['settings_origin']): LensSummary =>
  ({ name: 'l', kind: 'umap', legacy: false, session_id: 's', n_items: 10, settings, settings_origin: origin })

describe('the settings in words', () => {
  it('says the usual words when the settings are the defaults', () => {
    expect(settingsNote(lens({ n_neighbors: 15, dimensions: 6, min_dist: 0.1, metric: 'euclidean' }, 'form'))).toBeUndefined()
  })

  it('names a minimum distance or metric other than the defaults', () => {
    expect(settingsNote(lens({ n_neighbors: 15, dimensions: 6, min_dist: 0, metric: 'cosine' }, 'form')))
      .toBe('6D, n=15, min dist 0, cosine')
  })

  it('says tuned only for a search, and set by hand otherwise', () => {
    const perLayer = [row(5, 3), row(50, 12, { metric: 'cosine' })]
    expect(settingsNote(lens({ per_layer: perLayer }, 'tuned'))).toBe('tuned per layer (3–12D, n=5–50, euclidean/cosine)')
    expect(settingsNote(lens({ per_layer: perLayer }, 'by hand'))).toBe('set by hand per layer (3–12D, n=5–50, euclidean/cosine)')
    // a table left at the form's values reads like the form's settings
    expect(settingsNote(lens({ n_neighbors: 15, dimensions: 6, per_layer: [row(15, 6)] }, 'form'))).toBeUndefined()
  })
})
