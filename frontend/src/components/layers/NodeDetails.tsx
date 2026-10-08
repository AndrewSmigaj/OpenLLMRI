// What comes with a cluster node (DESIGN.md C5): the neurons whose values track membership, what
// its centre pushes toward through the output vocabulary, whether surface features alone predict
// it, and how much the next layer's routing differs between the layer's nodes. Worked out per lens
// version, in the background, on request.
import type { ReactNode } from 'react'
import type { LensDetailsState } from '../../hooks/useLensDetails'
import Tokens from '../common/Tokens'
import JobProgress from '../lenses/JobProgress'

interface NodeDetailsProps {
  state: LensDetailsState
  layer: number
  node: number
  disabled: boolean // visitors read only
}

const pct = (share: number) => `${(100 * share).toFixed(share < 0.1 ? 1 : 0)}%`

function Section({ title, note, children }: { title: string; note: string; children: ReactNode }) {
  return (
    <div className="space-y-0.5">
      <div className="text-[11px] font-semibold text-gray-700" title={note}>{title}</div>
      {children}
    </div>
  )
}

export default function NodeDetails({ state, layer, node, disabled }: NodeDetailsProps) {
  const { details, missing, error, runner, compute } = state
  const atLayer = details?.kind === 'umap' ? details.layers[String(layer)] : undefined
  const found = atLayer?.nodes[String(node)]
  const surface = found?.surface

  return (
    <div className="border-t border-gray-200 pt-2 space-y-2 text-[11px] text-gray-700">
      <div className="flex items-center gap-2">
        <span className="text-xs font-semibold text-gray-800">Node details</span>
        {(missing || details) && (
          <button onClick={compute} disabled={disabled || runner.running || runner.starting}
            className="px-2 py-0.5 text-[11px] rounded border border-blue-500 text-blue-700 hover:bg-blue-50 disabled:border-gray-300 disabled:text-gray-400">
            {details ? 'Work out again' : 'Work out'}
          </button>
        )}
      </div>
      {missing && !runner.job && (
        <p className="text-gray-500">Not worked out for this version yet: the neurons, the logit lens, the surface check
          and the routing measures, for every node at once (a few minutes, on the CPU).</p>
      )}
      {error && <p className="text-red-600">{error}</p>}
      {runner.error && <p className="text-red-600">{runner.error}</p>}
      {runner.job && <JobProgress job={runner.job} title="Node details" onCancel={runner.running ? runner.cancel : undefined} />}
      {details && !found && <p className="text-gray-500">No details for L{layer} node {node} in this version.</p>}
      {found && atLayer && (
        <>
          <Section title="Neurons" note="The neurons whose values correlate most with membership of the node (r, signed)">
            <div className="flex flex-wrap gap-1">
              {found.neurons.map(([neuron, r]) => (
                <span key={neuron} className={`font-mono text-[10px] rounded px-1 border ${
                  r >= 0 ? 'bg-green-50 border-green-200 text-green-800' : 'bg-red-50 border-red-200 text-red-800'}`}>
                  #{neuron} {r >= 0 ? '+' : '−'}{Math.abs(r).toFixed(2)}
                </span>
              ))}
            </div>
          </Section>
          <Section title="Logit lens" note="The node's centre (its members' mean state) through the final norm and the unembedding">
            <div className="text-[10px] text-gray-500">favoured more than by the layer's average item</div>
            <Tokens tokens={found.logit_lens.distinctive} unit="logit above the average" />
            <div className="text-[10px] text-gray-500">top tokens</div>
            <Tokens tokens={found.logit_lens.top} unit="logit" />
          </Section>
          <Section title="Surface check" note="Whether length, punctuation, the target word's place or the first word alone predict the node">
            {atLayer.surface_kappa !== null && (
              <div>surface features predict this layer's nodes at κ {atLayer.surface_kappa.toFixed(2)} (held out)</div>
            )}
            {surface ? (
              <div className="space-y-0.5">
                {surface.flagged && (
                  <span className="inline-block text-[10px] rounded px-1.5 border bg-amber-50 text-amber-800 border-amber-300">
                    surface feature: read this node with care
                  </span>
                )}
                {surface.feature && (
                  <div>{surface.feature}: members {surface.members_mean}, others {surface.others_mean}
                    {' '}<span className="text-gray-500">(AUC {surface.auc.toFixed(2)})</span></div>
                )}
                <div>first word “{surface.first_word.word}”: {pct(surface.first_word.in_node)} of members,
                  {' '}{pct(surface.first_word.outside)} of others</div>
              </div>
            ) : <div className="text-gray-500">the node holds every item</div>}
          </Section>
          <Section title="Routing" note="How much of the next layer's item-to-item routing difference lines up with this layer's nodes (the model's own top-four weights)">
            {atLayer.routing_effect === null || !found.routing ? (
              <div className="text-gray-500">no next layer</div>
            ) : (
              <>
                <div>this layer's nodes explain {pct(atLayer.routing_effect)} of L{layer + 1}'s routing variance;
                  {' '}this node's part is {pct(found.routing.share)}</div>
                <div>its mean routing sits {found.routing.shift.toFixed(2)} from the layer's
                  {' '}<span className="text-gray-500">(in items' typical distances)</span></div>
              </>
            )}
          </Section>
          <p className="text-[10px] text-gray-400">
            worked out {details?.provenance.created_at.slice(0, 16).replace('T', ' ')} in {details?.provenance.seconds} s
          </p>
        </>
      )}
    </div>
  )
}
