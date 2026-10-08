// The background jobs that are queued or running, polled every few seconds (10b.11's event
// stream replaces the polling). `finished` counts jobs that have ended since the page opened, so
// views can reload what a job wrote.
import { useEffect, useRef, useState } from 'react'
import { apiClient } from '../api/client'
import type { JobView } from '../types/lens'

const POLL_MS = 3000

export function useJobs(): { active: JobView[]; finished: number } {
  const [active, setActive] = useState<JobView[]>([])
  const [finished, setFinished] = useState(0)
  const seen = useRef<Set<string>>(new Set())

  useEffect(() => {
    let alive = true
    const poll = async () => {
      try {
        const jobs = await apiClient.listJobs(true)
        if (!alive) return
        const ids = new Set(jobs.map(j => j.id))
        const ended = [...seen.current].filter(id => !ids.has(id)).length
        seen.current = ids
        if (ended) setFinished(n => n + ended)
        setActive(jobs)
      } catch {
        // the backend may be restarting; the next poll tries again
      }
    }
    poll()
    const timer = setInterval(poll, POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [])

  return { active, finished }
}
