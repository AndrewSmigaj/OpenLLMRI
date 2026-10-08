// What surrounds a lens on the page: the capture's sentences and target word, the lens described
// as a schema summary, and for a legacy schema its /analyze reports and written descriptions.
import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import type { ClusteringSchema, SessionDetailResponse } from '../types/api'
import type { LensSummary } from '../types/lens'
import { lensAsSchema } from '../utils/lensAsSchema'

export interface LensContext {
  details: SessionDetailResponse | null
  summary: ClusteringSchema | undefined
  lens?: LensSummary // a lens's own listing (not a legacy schema's): what has been worked out for it
  reports: Record<string, string>
  descriptions: Record<string, string>
}

const EMPTY: LensContext = { details: null, summary: undefined, reports: {}, descriptions: {} }

export function useLensContext(session: string, lens: string, legacy: boolean): LensContext {
  const [context, setContext] = useState<LensContext>(EMPTY)

  useEffect(() => {
    let current = true
    apiClient.getSessionDetails(session)
      .then(details => { if (current) setContext(c => ({ ...c, details })) })
      .catch(() => undefined) // the sentence list stays empty; the charts don't need it
    return () => { current = false }
  }, [session])

  useEffect(() => {
    let current = true
    if (legacy) {
      apiClient.getClusteringDetails(session, lens)
        .then(d => {
          if (current) setContext(c => ({ ...c, summary: d.meta, reports: d.reports ?? {}, descriptions: d.element_descriptions ?? {} }))
        })
        .catch(() => undefined)
    } else {
      apiClient.listLenses(session)
        .then(all => {
          const found = all.find(l => !l.legacy && l.name === lens)
          if (current) setContext(c => ({ ...c, summary: found ? lensAsSchema(found) : undefined, lens: found, reports: {}, descriptions: {} }))
        })
        .catch(() => undefined)
    }
    return () => { current = false }
  }, [session, lens, legacy])

  return context
}
