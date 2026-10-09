// Reading a lens's validation: the held-out best k per layer.
import type { Validation } from '../types/lens'

// Each layer's k with the best held-out AMI on an axis, the nodes that best match the classes on
// held-out items (DESIGN.md C3); ties go to the smaller k (as the backend)
export function heldoutBest(validation: Validation, axis = 'label'): Record<string, number> {
  const best: Record<string, number> = {}
  for (const [layer, profile] of Object.entries(validation.layers)) {
    let top: [number, number] | null = null
    for (const [k, entry] of Object.entries(profile)) {
      const ami = entry.heldout[axis]?.ami
      if (ami === undefined) continue
      if (!top || ami > top[0] || (ami === top[0] && Number(k) < top[1])) top = [ami, Number(k)]
    }
    if (top) best[layer] = top[1]
  }
  return best
}
