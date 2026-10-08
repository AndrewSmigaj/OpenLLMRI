// Where a validated UMAP lens and raw space disagree: each cluster node holding items whose
// co-members differ in the best raw grouping, with how many. Nothing for legacy schemas or lenses
// not yet validated.
import { useEffect, useState } from 'react'
import { apiClient } from '../api/client'

export function useLensMarks(session: string, lens: string, legacy: boolean): Record<string, number> | undefined {
  const [outlined, setOutlined] = useState<Record<string, number> | undefined>(undefined)
  useEffect(() => {
    if (legacy || !session || !lens) { setOutlined(undefined); return }
    let current = true
    apiClient.getLensMarks(session, lens)
      .then(marks => {
        if (current) setOutlined(Object.assign({}, ...Object.values(marks.layers).map(layer => layer.nodes)))
      })
      .catch(() => { if (current) setOutlined(undefined) }) // not validated yet
    return () => { current = false }
  }, [session, lens, legacy])
  return outlined
}
