// The backend's event stream (GET /api/app/events, DESIGN.md E7): `show` commands open a view,
// `job` events keep every job's state current, so nothing polls while the stream is open, and
// `lens` events count lens changes, so views re-read what changed. On every connect the active
// jobs are read once, and any job the app thought active is read again, to catch up.
import { useEffect, useRef, useState } from 'react'
import { API_BASE_URL, apiClient } from '../api/client'
import type { JobView } from '../types/lens'

export interface AppEvents {
  jobs: Record<string, JobView>
  lensRevision: number // goes up with every lens change
  open: boolean // whether the stream is connected
}

export type ShowView = Record<string, unknown> & { workspace?: string }

const ACTIVE = new Set(['queued', 'running'])

export function useAppEvents(onShow: (view: ShowView) => void): AppEvents {
  const [jobs, setJobs] = useState<Record<string, JobView>>({})
  const [lensRevision, setLensRevision] = useState(0)
  const [open, setOpen] = useState(false)
  const onShowRef = useRef(onShow)
  onShowRef.current = onShow
  const jobsRef = useRef(jobs)
  jobsRef.current = jobs

  useEffect(() => {
    const source = new EventSource(`${API_BASE_URL}/app/events`)
    const put = (job: JobView) => setJobs(all => ({ ...all, [job.id]: job }))
    const catchUp = async () => {
      const active = await apiClient.listJobs(true)
      active.forEach(put)
      const seen = new Set(active.map(j => j.id))
      const stale = Object.values(jobsRef.current).filter(j => ACTIVE.has(j.state) && !seen.has(j.id))
      for (const job of stale) put(await apiClient.getJob(job.id))
    }
    source.onopen = () => { setOpen(true); catchUp().catch(() => undefined) }
    source.onerror = () => setOpen(false) // the browser reconnects by itself
    source.addEventListener('job', e => put(JSON.parse((e as MessageEvent).data) as JobView))
    source.addEventListener('lens', () => setLensRevision(n => n + 1))
    source.addEventListener('show', e => onShowRef.current((JSON.parse((e as MessageEvent).data) as { view: ShowView }).view))
    return () => source.close()
  }, [])

  return { jobs, lensRevision, open }
}
