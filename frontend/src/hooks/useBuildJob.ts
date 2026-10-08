// Starts a lens build and follows its job until it ends, by polling (10b.11's event stream
// replaces the polling). The page stays usable throughout: the build runs in its own process.
import { useCallback, useEffect, useRef, useState } from 'react'
import { apiClient } from '../api/client'
import type { JobView, LensBuildBody } from '../types/lens'

const POLL_MS = 1000
const ENDED = new Set(['done', 'failed', 'cancelled', 'interrupted'])

export function useBuildJob(onDone: (job: JobView) => void) {
  const [job, setJob] = useState<JobView | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [starting, setStarting] = useState(false)
  const onDoneRef = useRef(onDone)
  onDoneRef.current = onDone
  const jobId = job && !ENDED.has(job.state) ? job.id : null

  useEffect(() => {
    if (!jobId) return
    let alive = true
    const timer = setInterval(async () => {
      try {
        const latest = await apiClient.getJob(jobId)
        if (!alive) return
        setJob(latest)
        if (latest.state === 'done') onDoneRef.current(latest)
      } catch {
        // the backend may be restarting; a running job carries on and is re-adopted
      }
    }, POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [jobId])

  const start = useCallback(async (body: LensBuildBody) => {
    setError(null)
    setStarting(true)
    try {
      const { job_id } = await apiClient.buildLens(body)
      setJob(await apiClient.getJob(job_id))
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setStarting(false)
    }
  }, [])

  const cancel = useCallback(async () => {
    if (jobId) setJob(await apiClient.cancelJob(jobId))
  }, [jobId])

  return { job, error, starting, running: !!jobId, start, cancel }
}
