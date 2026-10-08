// A lens's node details (a mass-mean lens's layer details): read once per lens, and worked out in
// the background on request. The lens's listing says whether they exist (`available`; undefined
// while it loads), so nothing is asked for that isn't there.
import { useCallback, useEffect, useState } from 'react'
import { ApiError, apiClient } from '../api/client'
import type { LensNodeDetails, MassMeanDetails } from '../types/lens'
import { useJobRunner } from './useJobRunner'

export interface LensDetailsState {
  details: LensNodeDetails | MassMeanDetails | null
  missing: boolean // not worked out for this version yet
  error: string | null
  runner: ReturnType<typeof useJobRunner>
  compute: () => void
}

export function useLensDetails(session: string, lens: string, legacy: boolean,
                               available: boolean | undefined): LensDetailsState {
  const [details, setDetails] = useState<LensNodeDetails | MassMeanDetails | null>(null)
  const [missing, setMissing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reads, setReads] = useState(0)
  const runner = useJobRunner(() => setReads(n => n + 1))
  const { start } = runner

  useEffect(() => {
    setDetails(null)
    setMissing(false)
    setError(null)
    if (legacy || !session || !lens || available === undefined) return
    if (!available && reads === 0) { setMissing(true); return }
    let current = true
    apiClient.getLensDetails(session, lens)
      .then(found => { if (current) setDetails(found) })
      .catch(err => {
        if (!current) return
        if (err instanceof ApiError && err.status === 404) setMissing(true)
        else setError(err instanceof Error ? err.message : String(err))
      })
    return () => { current = false }
  }, [session, lens, legacy, available, reads])

  const compute = useCallback(() => { void start(() => apiClient.computeLensDetails(session, lens)) }, [start, session, lens])
  return { details, missing, error, runner, compute }
}
