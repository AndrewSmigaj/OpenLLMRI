// A background job's progress while it runs, and what went wrong if it failed
import type { JobView } from '../../types/lens'

export default function JobProgress({ job, title, onCancel }: { job: JobView; title: string; onCancel?: () => void }) {
  const { stage, done, total } = job.progress
  const share = total > 0 ? Math.round((100 * done) / total) : 0
  return (
    <div className="border-t border-gray-200 pt-2 space-y-1">
      <div className="flex items-center gap-2 text-xs">
        <span className="font-medium text-gray-800">{title} {job.state}</span>
        {stage && <span className="text-gray-500">{stage} {total > 0 ? `${done}/${total}` : ''}</span>}
        {onCancel && <button onClick={onCancel} className="text-red-600 hover:underline">cancel</button>}
      </div>
      {total > 0 && job.state === 'running' && (
        <div className="h-1.5 bg-gray-200 rounded"><div className="h-1.5 bg-blue-500 rounded" style={{ width: `${share}%` }} /></div>
      )}
      {job.error && <p className="text-xs text-red-600">{job.error}</p>}
      {job.log_tail && <pre className="text-[10px] bg-gray-50 border border-gray-200 rounded p-1 max-h-40 overflow-auto">{job.log_tail}</pre>}
    </div>
  )
}
