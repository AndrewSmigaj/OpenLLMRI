// The 3-D view's points for a lens (DESIGN.md E5): its own space, lined up layer to layer, with a
// reading's items in the same frame when one is shown.
import { useEffect, useState } from 'react'
import { apiClient, ApiError } from '../api/client'
import type { LensTrajectory } from '../types/lens'

export interface TrajectoryState {
  data: LensTrajectory | null
  loading: boolean
  error: string | null
  missing: boolean // a legacy schema built before its 3-D points were kept
}

export function useLensTrajectory(session: string, lens: string, legacy: boolean, reading: string | undefined): TrajectoryState {
  const [state, setState] = useState<TrajectoryState>({ data: null, loading: true, error: null, missing: false })
  useEffect(() => {
    let current = true
    setState(s => ({ ...s, loading: true, error: null }))
    apiClient.getLensTrajectory(session, lens, legacy, reading)
      .then(data => { if (current) setState({ data, loading: false, error: null, missing: false }) })
      .catch(err => {
        if (!current) return
        const missing = err instanceof ApiError && err.status === 404 && legacy
        setState({ data: null, loading: false, missing, error: missing ? null : err instanceof Error ? err.message : String(err) })
      })
    return () => { current = false }
  }, [session, lens, legacy, reading])
  return state
}
