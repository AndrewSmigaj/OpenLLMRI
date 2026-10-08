// A lens's flows over every layer (its clusters, or the experts at one rank), in the route shape
// the charts, cards and contingency table read. Legacy schemas come through the same endpoints.
import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import type { RouteAnalysisResponse } from '../types/api'
import type { LensFlows } from '../types/lens'
import { flowsToRoutes } from '../utils/flowsToRoutes'

export interface LensFlowsState {
  flows: LensFlows | null
  routes: RouteAnalysisResponse | null
  loading: boolean
  error: string | null
}

const EMPTY: LensFlowsState = { flows: null, routes: null, loading: false, error: null }

// `outputAxes` groups the output column by those output axes (the output colour and blend axes).
export function useLensFlows(session: string, lens: string, legacy: boolean, kind: 'cluster' | 'expert',
                             rank = 1, outputAxes: string[] = []): LensFlowsState {
  const [state, setState] = useState<LensFlowsState>(EMPTY)
  const rankKey = kind === 'expert' ? rank : 0 // cluster flows don't depend on the rank
  const axesKey = outputAxes.join(',')

  useEffect(() => {
    if (!session || !lens) {
      setState(EMPTY)
      return
    }
    let current = true
    setState(s => ({ ...s, loading: true, error: null }))
    const grouped = axesKey ? axesKey.split(',') : []
    const request = kind === 'cluster'
      ? apiClient.getLensFlows(session, lens, legacy, grouped)
      : apiClient.getLensExpertFlows(session, lens, legacy, rankKey, grouped)
    request
      .then(flows => {
        if (current) setState({ flows, routes: flowsToRoutes(flows, session), loading: false, error: null })
      })
      .catch(err => {
        if (current) setState({ ...EMPTY, error: err instanceof Error ? err.message : String(err) })
      })
    return () => { current = false }
  }, [session, lens, legacy, kind, rankKey, axesKey])

  return state
}
