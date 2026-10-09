// The rest of one item's path on its card (DESIGN.md E5): for an item read through the lens, its
// node at each layer with the vote that placed it there; its expert at each layer at the expert
// chart's rank; the output it went on to give; and its run's other steps, to step through.
interface ItemPathProps {
  experts?: Record<string, number> // layer: the item's expert at the rank
  rank: number
  output?: string // the item's output category, when the capture has one
  read?: { layers: number[]; nodes: number[]; shares: (number | null)[]; pct: number[] } // an item read through the lens
  stepLabel: string
  steps: number[] // the steps of the item's run
  step: number | null
  onStep: (step: number | null) => void
}

const median = (values: number[]) => {
  const sorted = [...values].sort((a, b) => a - b)
  return sorted.length ? sorted[Math.floor(sorted.length / 2)] : 0
}

export default function ItemPath({ experts, rank, output, read, stepLabel, steps, step, onStep }: ItemPathProps) {
  const path = Object.entries(experts ?? {}).sort(([a], [b]) => Number(a) - Number(b))
  const voted = read && read.shares.some(share => share !== null)
  return (
    <div className="space-y-1">
      {read && voted && (
        <div>
          <p className="text-[10px] font-medium text-gray-500 mb-0.5"
            title="Placed in the lens's space at each layer; its node is the vote of its 15 nearest lens items, weighted by closeness">
            Node path, read through the lens (share of the vote)
          </p>
          <div className="flex flex-wrap gap-0.5">
            {read.layers.map((layer, li) => (
              <span key={layer} className={`px-1 py-px rounded text-[9px] ${(read.shares[li] ?? 1) < 0.6 ? 'bg-amber-50 text-amber-800' : 'bg-blue-50 text-blue-700'}`}>
                L{layer}→C{read.nodes[li]} {read.shares[li] !== null ? (read.shares[li] as number).toFixed(2) : ''}
              </span>
            ))}
          </div>
          <p className="text-[10px] text-gray-500 mt-0.5"
            title="How far out it sits, in the residual stream: its distance to its 15 nearest lens items, as a percentile of the lens's own items'">
            How far out: median {median(read.pct).toFixed(0)}th percentile, at most {Math.max(...read.pct).toFixed(0)}th
          </p>
        </div>
      )}
      {path.length > 0 && (
        <div>
          <p className="text-[10px] font-medium text-gray-500 mb-0.5">Expert path, rank {rank}</p>
          <div className="flex flex-wrap gap-0.5">
            {path.map(([layer, expert]) => (
              <span key={layer} className="px-1 py-px bg-amber-50 text-amber-800 rounded text-[9px]">L{layer}→E{expert}</span>
            ))}
          </div>
        </div>
      )}
      {output !== undefined && (
        <p className="text-[10px] text-gray-500">Output <span className="font-medium text-gray-800">{output}</span></p>
      )}
      {steps.length > 1 && (
        <p className="flex flex-wrap items-center gap-1 text-[10px] text-gray-500">
          Its run's {stepLabel.toLowerCase()}s
          {steps.map(s => (
            <button key={s} onClick={() => onStep(s)}
              className={`px-1 py-px rounded ${step === s ? 'bg-gray-800 text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}>
              {s}
            </button>
          ))}
        </p>
      )}
    </div>
  )
}
