// Build: the capture's lenses, newest builds and legacy schemas alike; opening one shows it in
// Layers. (The build form joins this page in 10b.4.)
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient } from '../api/client'
import type { LensSummary } from '../types/lens'
import { useJobs } from '../hooks/useJobs'
import { useViewState, viewQuery } from '../hooks/useViewState'
import { lensAsSchema } from '../utils/lensAsSchema'
import SchemaSummary from '../components/analysis/SchemaSummary'
import { useShell } from '../components/shell/shellContext'

export default function BuildWorkspace() {
  const [view] = useViewState()
  const { room } = useShell()
  const visitor = room?.role === 'visitor' // visitors only look
  const navigate = useNavigate()
  const jobs = useJobs()
  const [lenses, setLenses] = useState<LensSummary[] | null>(null)

  useEffect(() => {
    if (!view.session) return
    let current = true
    apiClient.listLenses(view.session)
      .then(found => { if (current) setLenses(found) })
      .catch(() => { if (current) setLenses([]) })
    return () => { current = false }
  }, [view.session, jobs.finished])

  if (!view.session) {
    return <div className="m-4 text-xs text-slate-700">Choose a capture in the top bar to see its lenses.</div>
  }
  const open = (lens: LensSummary) =>
    navigate({ pathname: '/layers', search: `?${viewQuery({ ...view, lens: lens.name, legacy: lens.legacy, sel: '', layer: 0 })}` })

  return (
    <div className="h-full overflow-y-auto p-3 space-y-2">
      <h2 className="text-sm font-semibold text-gray-900">Lenses on this capture</h2>
      {lenses === null && <p className="text-xs text-gray-500">Loading…</p>}
      {lenses?.length === 0 && <p className="text-xs text-gray-500">None yet. The /cluster skill builds one from Claude Code.</p>}
      {lenses?.map(lens => (
        <div key={`${lens.legacy}:${lens.name}`} className="bg-white border border-gray-200 rounded p-2 flex items-start gap-3">
          <div className="flex-1 min-w-0">
            {lens.legacy
              ? <div className="text-xs"><span className="font-mono">{lens.name}</span>
                  <span className="ml-2 text-[10px] text-gray-500">legacy schema · {lens.n_items ?? '?'} items</span></div>
              : <SchemaSummary schema={lensAsSchema(lens)} />}
            {!lens.legacy && (
              <div className="text-[10px] text-gray-500 mt-0.5">
                {lens.state ?? 'draft'} {lens.current} · built {lens.created_at?.slice(0, 16).replace('T', ' ')} by {lens.created_by}
              </div>
            )}
          </div>
          <button onClick={() => open(lens)} disabled={visitor}
            className="px-2 py-1 text-xs rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">Open in Layers</button>
        </div>
      ))}
    </div>
  )
}
