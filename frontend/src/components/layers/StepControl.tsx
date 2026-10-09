// Which step the selection lights (DESIGN.md E5): every step, or one tick or context step. A step
// the lens doesn't cover is read through it once (a background job), and how far out its items sit
// is shown beside it: a median beyond the 75th percentile of the lens's own says the lens is reading
// outside the context it was built from (D2's rule 3).
import type { StepReading } from '../../hooks/useStepReading'

interface StepControlProps {
  label: string // 'Tick' for an agent run, 'Step' for a sentence run
  steps: number[]
  step: number | null
  onStep: (step: number | null) => void
  reading: StepReading
  disabled: boolean // visitors look, they don't start jobs
}

const btn = (on: boolean) => `px-1.5 py-0.5 text-[11px] rounded ${on ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`

export default function StepControl({ label, steps, step, onStep, reading, disabled }: StepControlProps) {
  const { covered, listed, runner, error } = reading
  const job = runner.job
  const progress = job?.progress?.total ? ` ${job.progress.stage} ${job.progress.done}/${job.progress.total}` : ''
  return (
    <span className="flex items-center gap-1 text-[11px] text-gray-600">
      {label}
      <button onClick={() => onStep(null)} className={btn(step === null)} title={`Every ${label.toLowerCase()}`}>all</button>
      {steps.map(s => (
        <button key={s} onClick={() => onStep(s)} className={btn(step === s)} aria-label={`${label} ${s}`}>{s}</button>
      ))}
      {step !== null && !covered && !listed && !runner.running && (
        <button onClick={reading.read} disabled={disabled || runner.starting}
          title={`The lens wasn't built on ${label.toLowerCase()} ${step}: place its items in the lens's space, layer by layer`}
          className="ml-1 px-1.5 py-0.5 text-[11px] rounded border border-blue-300 text-blue-700 hover:bg-blue-50 disabled:opacity-50">
          Read {label.toLowerCase()} {step} through this lens
        </button>
      )}
      {runner.running && <span className="text-gray-500">reading{progress}…</span>}
      {listed && (
        <span className={listed.far_out ? 'text-amber-700' : 'text-gray-500'}
          title={`How far out the read items sit, in the residual stream: their median among the lens's own items' distances to their neighbours, at the farthest layer. Beyond the 75th percentile, the lens is reading outside the context it was built from.`}>
          read through the lens{listed.far_out ? `, far out (median at the ${listed.max_median_percentile}th percentile)` : ''}
        </span>
      )}
      {(error || runner.error) && <span className="text-red-600">{error || runner.error}</span>}
    </span>
  )
}
