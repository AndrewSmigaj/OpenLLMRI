// Background jobs in the top bar: how many are running, and a list with progress and cancel.
import { useState } from 'react'
import { apiClient } from '../../api/client'
import type { JobView } from '../../types/lens'

interface JobsMenuProps {
  jobs: JobView[]
  canCancel: boolean
}

const describe = (job: JobView) => {
  const name = typeof job.params.name === 'string' ? job.params.name : ''
  return name ? `${job.kind} · ${name}` : job.kind
}

export default function JobsMenu({ jobs, canCancel }: JobsMenuProps) {
  const [open, setOpen] = useState(false)
  const running = jobs.filter(j => j.state === 'running').length

  return (
    <div className="relative">
      <button onClick={() => setOpen(o => !o)}
        className={`px-2 py-1 text-xs rounded border whitespace-nowrap ${jobs.length
          ? 'border-blue-300 bg-blue-50 text-blue-800' : 'border-gray-300 bg-white text-gray-500'}`}>
        Jobs {jobs.length ? `(${running} running${jobs.length > running ? `, ${jobs.length - running} queued` : ''})` : '(none)'}
      </button>
      {open && (
        <div className="absolute right-0 mt-1 w-80 bg-white border border-gray-300 rounded shadow-lg z-50 p-2 space-y-1.5">
          {jobs.length === 0 && <p className="text-xs text-gray-500">No jobs are queued or running.</p>}
          {jobs.map(job => {
            const { stage, done, total } = job.progress
            return (
              <div key={job.id} className="text-xs border-b border-gray-100 pb-1.5 last:border-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-800 flex-1 truncate" title={job.id}>{describe(job)}</span>
                  <span className="text-gray-500">{job.state}</span>
                  {canCancel && (
                    <button onClick={() => apiClient.cancelJob(job.id).catch(() => undefined)}
                      className="text-red-600 hover:underline">cancel</button>
                  )}
                </div>
                {total > 0 && (
                  <div className="mt-1 flex items-center gap-2">
                    <div className="flex-1 h-1.5 bg-gray-200 rounded">
                      <div className="h-1.5 bg-blue-500 rounded" style={{ width: `${Math.round((100 * done) / total)}%` }} />
                    </div>
                    <span className="text-gray-500 tabular-nums">{stage} {done}/{total}</span>
                  </div>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
