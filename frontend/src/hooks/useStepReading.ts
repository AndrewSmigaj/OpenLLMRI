// The reading behind a step the lens doesn't cover (DESIGN.md B5 and E5): the lens's own capture,
// that step only, read through the lens once by a background job. Then every item of the step has
// a node at each layer and can light its path. A step the lens covers needs no reading.
import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import type { LensReading, LensSummary, ReadingListing } from '../types/lens'
import { useJobRunner } from './useJobRunner'

export interface StepReading {
  covered: boolean // the lens holds this step's items itself (or no step is chosen)
  listed: ReadingListing | null // the reading of this step, once made
  reading: LensReading | null // that reading, at the lens's version and the chart's rank
  read: () => void // make it
  runner: ReturnType<typeof useJobRunner>
  error: string | null
}

const sameSteps = (a: number[] | null | undefined, b: number[]) =>
  !!a && a.length === b.length && [...a].sort((x, y) => x - y).every((s, i) => s === b[i])

export function useStepReading(session: string, lens: string, listing: LensSummary | undefined, step: number | null,
                               version: string | undefined, rank: number): StepReading {
  const steps = listing?.filters?.steps
  const covered = step === null || !listing || listing.kind !== 'umap' || !steps || steps.includes(step)
  const lastOnly = listing?.filters?.last_occurrence_only ?? true
  const listed = covered || step === null ? null : listing?.readings?.find(r =>
    r.target === listing.session_id && sameSteps(r.steps, [step]) && (r.filters.last_occurrence_only ?? true) === lastOnly) ?? null
  const [reading, setReading] = useState<LensReading | null>(null)
  const [error, setError] = useState<string | null>(null)
  const key = listed?.key

  useEffect(() => {
    let current = true
    setReading(null)
    setError(null)
    if (!key) return
    apiClient.getLensReading(session, lens, key, version, rank)
      .then(found => { if (current) setReading(found) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens, key, version, rank])

  // The finished job's lens event reads the listing again, which then names the reading
  const runner = useJobRunner(() => undefined)
  const read = () => {
    if (step === null) return
    void runner.start(() => apiClient.readLens(session, lens,
      { filters: { steps: [step], last_occurrence_only: lastOnly }, created_by: 'app' }))
  }
  return { covered, listed, reading: listed ? reading : null, read, runner, error }
}
