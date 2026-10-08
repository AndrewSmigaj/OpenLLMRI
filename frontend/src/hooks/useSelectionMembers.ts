// The items a selected node or link holds, a page at a time, as the cards and lists show them.
import { useCallback, useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import type { ProbeExample } from '../types/api'
import type { LensMember, MembersQuery } from '../types/lens'

const PAGE = 50

export const memberToExample = (m: LensMember): ProbeExample => ({
  probe_id: m.probe_id, target_word: m.target_word, input_text: m.input_text,
  label: m.label ?? undefined, output_category: m.output_category ?? undefined,
  generated_text: m.generated_text ?? undefined, target_char_offset: m.target_char_offset ?? undefined,
  turn_id: m.turn_id ?? undefined, capture_type: m.capture_type ?? undefined, step: m.step ?? undefined,
  game_text: m.game_text ?? undefined, analysis: m.analysis ?? undefined, action: m.action ?? undefined,
  system_prompt: m.system_prompt ?? undefined,
})

interface MembersState {
  items: ProbeExample[]
  total: number
  loading: boolean
  error: string | null
}

const EMPTY: MembersState = { items: [], total: 0, loading: false, error: null }

export function useSelectionMembers(session: string, lens: string, legacy: boolean, query: MembersQuery | null) {
  const [state, setState] = useState<MembersState>(EMPTY)
  const key = query ? JSON.stringify(query) : ''

  useEffect(() => {
    if (!key) { setState(EMPTY); return }
    let current = true
    setState({ ...EMPTY, loading: true })
    apiClient.getLensMembers(session, lens, legacy, { ...JSON.parse(key), limit: PAGE })
      .then(page => { if (current) setState({ items: page.items.map(memberToExample), total: page.total, loading: false, error: null }) })
      .catch(err => { if (current) setState({ ...EMPTY, error: err instanceof Error ? err.message : String(err) }) })
    return () => { current = false }
  }, [session, lens, legacy, key])

  const loaded = state.items.length
  const loadMore = useCallback(() => {
    if (!key) return
    setState(s => ({ ...s, loading: true }))
    apiClient.getLensMembers(session, lens, legacy, { ...JSON.parse(key), offset: loaded, limit: PAGE })
      .then(page => setState(s => ({ ...s, items: [...s.items, ...page.items.map(memberToExample)], loading: false })))
      .catch(err => setState(s => ({ ...s, loading: false, error: err instanceof Error ? err.message : String(err) })))
  }, [session, lens, legacy, key, loaded])

  return { ...state, loadMore }
}
