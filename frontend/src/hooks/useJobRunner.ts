// Starts a background job (a lens build, a validation, a report) and follows it until it ends.
// While the event stream is open its job events keep the job current; while the stream is down
// the job is polled, so a backend restart doesn't leave a view waiting. The page stays usable:
// jobs run in their own process.
import { useCallback, useEffect, useRef, useState } from 'react'
import { apiClient } from '../api/client'
import { useShell } from '../components/shell/shellContext'
import type { JobView } from '../types/lens'

const POLL_MS = 2000
const ENDED = new Set(['done', 'failed', 'cancelled', 'interrupted'])

export function useJobRunner(onDone: (job: JobView) => void) {
  const { events } = useShell()
  const [started, setStarted] = useState<JobView | null>(null)
  const [polled, setPolled] = useState<JobView | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [starting, setStarting] = useState(false)
  const onDoneRef = useRef(onDone)
  onDoneRef.current = onDone
  const announced = useRef<string | null>(null)

  // The freshest view of the job: the stream's while it's open, else the last poll
  const live = started ? events.jobs[started.id] : undefined
  const fresh = polled && started && polled.id === started.id ? polled : undefined
  const job = started ? (events.open ? live ?? fresh ?? started : fresh ?? live ?? started) : null
  const jobId = job && !ENDED.has(job.state) ? job.id : null

  useEffect(() => {
    if (!jobId || events.open) return
    let alive = true
    const timer = setInterval(async () => {
      try {
        const latest = await apiClient.getJob(jobId)
        if (alive) setPolled(latest)
      } catch {
        // the backend may be restarting; a running job carries on and is re-adopted
      }
    }, POLL_MS)
    return () => { alive = false; clearInterval(timer) }
  }, [jobId, events.open])

  useEffect(() => {
    if (job?.state === 'done' && announced.current !== job.id) {
      announced.current = job.id
      onDoneRef.current(job)
    }
  }, [job])

  // `launch` asks the backend to start the job and returns its id
  const start = useCallback(async (launch: () => Promise<{ job_id: string }>) => {
    setError(null)
    setStarting(true)
    try {
      const { job_id } = await launch()
      setPolled(null)
      setStarted(await apiClient.getJob(job_id))
    } catch (err) {
      setError(err instanceof Error ? err.message : String(err))
    } finally {
      setStarting(false)
    }
  }, [])

  const cancel = useCallback(async () => {
    if (jobId) setPolled(await apiClient.cancelJob(jobId))
  }, [jobId])

  return { job, error, starting, running: !!jobId, start, cancel }
}
