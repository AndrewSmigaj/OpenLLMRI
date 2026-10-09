// A lens's expert pipelines, hubs and experts involved (DESIGN.md C7), read again when the lens
// changes (a build or a routes job finished).
import { useEffect, useState } from 'react'
import { apiClient, ApiError } from '../api/client'
import { useShell } from '../components/shell/shellContext'
import type { LensRoutes } from '../types/lens'

export interface RoutesState {
  routes: LensRoutes | null
  missing: boolean // not worked out yet (lenses built before routes were)
  error: string | null
}

export function useLensRoutes(session: string, lens: string, legacy: boolean, version: string | undefined): RoutesState {
  const { events } = useShell()
  const [state, setState] = useState<RoutesState>({ routes: null, missing: false, error: null })
  useEffect(() => {
    let current = true
    apiClient.getLensRoutes(session, lens, legacy, version)
      .then(routes => { if (current) setState({ routes, missing: false, error: null }) })
      .catch(err => {
        if (!current) return
        const missing = err instanceof ApiError && err.status === 404
        setState({ routes: null, missing, error: missing ? null : err instanceof Error ? err.message : String(err) })
      })
    return () => { current = false }
  }, [session, lens, legacy, version, events.lensRevision])
  return state
}
