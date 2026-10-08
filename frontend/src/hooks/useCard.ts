// LLM cards on a lens's current version. `useCardList` reads which cards exist (once per lens,
// and again after a job writes some); `useCard` reads one of them, and only when the list has it,
// so nothing is asked for that isn't there.
import { useCallback, useEffect, useState } from 'react'
import { apiClient } from '../api/client'
import { useShell } from '../components/shell/shellContext'
import type { Card } from '../types/cards'

export function useCardList(session: string, lens: string, enabled: boolean) {
  const [ids, setIds] = useState<Set<string> | undefined>(undefined)
  const [reads, setReads] = useState(0)
  const { events } = useShell() // reports written by any job (the app's, Claude Code's) show up
  useEffect(() => {
    setIds(undefined)
    if (!enabled || !session || !lens) return
    let current = true
    apiClient.listCards(session, lens)
      .then(found => { if (current) setIds(new Set(found.cards.map(c => c.card_id))) })
      .catch(() => { if (current) setIds(new Set()) })
    return () => { current = false }
  }, [session, lens, enabled, reads, events.lensRevision])
  const reload = useCallback(() => setReads(n => n + 1), [])
  return { ids, reload }
}

// `listed`: whether the card exists (undefined while the list loads)
export function useCard(session: string, lens: string, cardId: string, listed: boolean | undefined) {
  const [card, setCard] = useState<Card | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [reads, setReads] = useState(0)
  const { events } = useShell() // a card rewritten by any job shows its new text
  useEffect(() => {
    setCard(null)
    setError(null)
    if (!listed) return
    let current = true
    apiClient.getCard(session, lens, cardId)
      .then(found => { if (current) setCard(found) })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens, cardId, listed, reads, events.lensRevision])
  const reload = useCallback(() => setReads(n => n + 1), [])
  return { card, missing: listed === false, error, reload }
}
