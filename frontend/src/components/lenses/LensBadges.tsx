// A lens's checks at a glance: the build's self-check, and its held-out score once validated, with
// a button that validates it in the background.
import { apiClient } from '../../api/client'
import type { LensSummary } from '../../types/lens'
import { useJobRunner } from '../../hooks/useJobRunner'
import JobProgress from './JobProgress'

const badge = (tone: 'good' | 'bad' | 'none') => `text-[10px] rounded px-1.5 py-0.5 border ${
  tone === 'good' ? 'bg-green-50 text-green-800 border-green-300'
    : tone === 'bad' ? 'bg-red-50 text-red-800 border-red-300' : 'bg-gray-50 text-gray-600 border-gray-300'}`

interface LensBadgesProps {
  session: string
  lens: LensSummary
  disabled: boolean
  onValidated: () => void
}

export default function LensBadges({ session, lens, disabled, onValidated }: LensBadgesProps) {
  const runner = useJobRunner(() => onValidated())
  const check = lens.self_check
  const headline = lens.validation
  const best = headline?.best

  if (lens.kind === 'mass_mean') {
    return (
      <div className="flex flex-wrap items-center gap-2">
        {best ? (
          <span className={badge(best.accuracy >= 0.8 ? 'good' : 'none')}
            title={`${headline?.folds.kind}, ${headline?.folds.n_folds} folds; κ ${best.kappa}, worst fold ${best.worst_fold}`}>
            held out: accuracy {best.accuracy.toFixed(3)} at L{best.layer}
            {headline?.folds.weaker ? ' · weaker folds' : ` · ${headline?.folds.n_folds} scene-family folds`}
          </span>
        ) : <span className={badge('none')}>no held-out scores</span>}
      </div>
    )
  }
  return (
    <div className="space-y-1">
      <div className="flex flex-wrap items-center gap-2">
        {check ? (
          <span className={badge(check.passed ? 'good' : 'bad')}
            title={`Planted classes found: ARI ${check.planted.ari_k5} (needs ${check.thresholds.planted_ari}); `
              + `structure found in noise: AMI ${check.null.ami_k5} (must stay under ${check.thresholds.null_ami}); `
              + `${check.items} items × ${check.dims} dimensions`}>
            self-check {check.passed ? 'passed' : 'failed'}
          </span>
        ) : <span className={badge('none')} title="Built before the self-check existed">no self-check</span>}
        {headline ? (
          <span className={badge(best && best.kappa >= 0.6 ? 'good' : 'none')}
            title={`${headline.folds.kind}, ${headline.folds.n_folds} folds${headline.folds.weaker ? ' (weaker than scene families)' : ''}`}>
            held out: {best ? `κ ${best.kappa.toFixed(2)} at L${best.layer} (k ${best.k})` : 'no label scores'}
            {headline.folds.weaker ? ' · weaker folds' : ` · ${headline.folds.n_folds} scene-family folds`}
          </span>
        ) : <span className={badge('none')}>not validated</span>}
        <button onClick={() => runner.start(() => apiClient.validateLens(session, lens.name))}
          disabled={disabled || runner.running || runner.starting}
          className="px-2 py-0.5 text-[11px] rounded border border-blue-500 text-blue-700 hover:bg-blue-50 disabled:border-gray-300 disabled:text-gray-400">
          {headline ? 'Validate again' : 'Validate'}
        </button>
      </div>
      {runner.error && <p className="text-xs text-red-600">{runner.error}</p>}
      {runner.job && <JobProgress job={runner.job} title="Validation" onCancel={runner.running ? runner.cancel : undefined} />}
    </div>
  )
}
