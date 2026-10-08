// Whether the analysts that write reports have passed their tests (DESIGN.md E8): decoys left
// quiet, planted findings found, members picked from descriptions. A button tests them on a lens.
import { useEffect, useState } from 'react'
import { apiClient } from '../../api/client'
import { useJobRunner } from '../../hooks/useJobRunner'
import type { AnalystTests } from '../../types/cards'
import JobProgress from './JobProgress'

export default function AnalystStatus({ session, lens, disabled }: { session: string; lens: string | null; disabled: boolean }) {
  const [tests, setTests] = useState<AnalystTests | null>(null)
  const [reads, setReads] = useState(0)
  const runner = useJobRunner(() => setReads(n => n + 1))
  useEffect(() => {
    let current = true
    apiClient.getAnalystTests().then(found => { if (current) setTests(found) }).catch(() => undefined)
    return () => { current = false }
  }, [reads])

  const latest = tests?.latest
  const tested = !!tests && tests.passing.some(p => p.prompt_version === tests.prompt_version)
  return (
    <div className="space-y-1 text-[11px]">
      <div className="flex flex-wrap items-center gap-2">
        <span className="font-semibold text-gray-800">Report analysts</span>
        {latest ? (
          <span className={latest.passed ? 'text-green-800' : 'text-red-700'}>
            {latest.passed ? 'passed' : 'failed'} their tests on {latest.created_at.slice(0, 10)} ({latest.model}, prompts {latest.prompt_version}, at L{latest.layer} of {latest.lens.name}):
            {' '}decoys left quiet {latest.decoys.filter(d => !d.clear).length}/{latest.decoys.length},
            {' '}planted findings found {latest.planted.filter(p => p.found).length}/{latest.planted.length},
            {' '}members picked from descriptions {latest.mean_accuracy ?? '–'}
          </span>
        ) : <span className="text-gray-500">not tested yet: their reports are marked untested</span>}
        {tests && latest && !tested && <span className="text-amber-700">the current prompts ({tests.prompt_version}) aren't tested</span>}
        {lens && (
          <button onClick={() => void runner.start(() => apiClient.startAnalystTests(session, lens))}
            disabled={disabled || runner.running || runner.starting} title="About 20 calls on the Claude subscription"
            className="px-2 py-0.5 rounded border border-violet-500 text-violet-700 hover:bg-violet-50 disabled:border-gray-300 disabled:text-gray-400">
            Test them on {lens}</button>
        )}
      </div>
      {runner.error && <p className="text-red-600">{runner.error}</p>}
      {runner.job && runner.job.state !== 'done' && <JobProgress job={runner.job} title="Analyst tests" onCancel={runner.running ? runner.cancel : undefined} />}
    </div>
  )
}
