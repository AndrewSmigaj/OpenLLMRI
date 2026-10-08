// The background jobs that are queued or running, oldest first, from the event stream's job map.
import type { JobView } from '../types/lens'

export function activeJobs(jobs: Record<string, JobView>): JobView[] {
  return Object.values(jobs).filter(j => j.state === 'queued' || j.state === 'running')
    .sort((a, b) => a.created_at.localeCompare(b.created_at))
}
