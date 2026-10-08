// Reading a lens's validation: the held-out best k per layer.
import type { Validation } from '../types/lens'

// Each layer's k with the best held-out kappa on an axis; ties go to the smaller k (as the backend)
export function heldoutBest(validation: Validation, axis = 'label'): Record<string, number> {
  const best: Record<string, number> = {}
  for (const [layer, profile] of Object.entries(validation.layers)) {
    let top: [number, number] | null = null
    for (const [k, entry] of Object.entries(profile)) {
      const kappa = entry.heldout[axis]?.kappa
      if (kappa === undefined) continue
      if (!top || kappa > top[0] || (kappa === top[0] && Number(k) < top[1])) top = [kappa, Number(k)]
    }
    if (top) best[layer] = top[1]
  }
  return best
}
