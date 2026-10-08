// Starts a background job (a lens build, a validation) and follows it until it ends, by polling
// (10b.11's event stream replaces the polling). The page stays usable: jobs run in their own process.
import { useCallback, useEffect, useRef, useState } from 'react'
import { apiClient } from '../api/client'
import type { JobView } from '../types/lens'

const POLL_MS = 1000
const ENDED = new Set(['done', 'failed', 'cancelled', 'interrupted'])

export function useJobRunner(onDone: (job: JobView) => void) {
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

  // `launch` asks the backend to start the job and returns its id
  const start = useCallback(async (launch: () => Promise<{ job_id: string }>) => {
    setError(null)
    setStarting(true)
    try {
      const { job_id } = await launch()
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
