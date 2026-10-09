// Beside the charts: what the lens is, the LLM report on the selection (a lens's analysis panel),
// the card for the selection (with a legacy schema's written description of it, or a lens node's
// details), and the legacy schema's reports.
import type { ReactNode } from 'react'
import type { SelectedCard } from '../../types/analysis'
import type { ClusteringSchema } from '../../types/api'
import type { GradientScheme } from '../../color/scheme'
import { descriptionKey } from '../../utils/selectionCard'
import ContextSensitiveCard from '../analysis/ContextSensitiveCard'
import SchemaSummary from '../analysis/SchemaSummary'
import PanelErrorBoundary from '../common/PanelErrorBoundary'
import LegacyReports from './LegacyReports'

interface DetailsPanelProps {
  summary: ClusteringSchema | undefined
  card: SelectedCard | null
  descriptions: Record<string, string>
  reports: Record<string, string>
  layer: number
  clusterPath?: Record<string, number> // an item's cluster at each layer, for an item's card
  axisValues: Record<string, string[]> // every axis's values, in a fixed order
  gradient: GradientScheme
  nodeDetails?: ReactNode // a lens's cluster node: its neurons, logit lens, surface check, routing
  itemPath?: ReactNode // one item: its expert path and output, below its cluster path
  report?: ReactNode // a lens's LLM report on the selection, or on the lens when nothing is selected
  legacy: boolean // a legacy schema: its written descriptions stand in for reports
  onClose: () => void
}

export default function DetailsPanel({ summary, card, descriptions, reports, layer, clusterPath,
                                       axisValues, gradient, nodeDetails, itemPath, report, legacy, onClose }: DetailsPanelProps) {
  const key = card ? descriptionKey(card) : ''
  return (
    <div className="h-full overflow-y-auto overflow-x-hidden p-2 space-y-2 bg-white">
      {summary && <div className="pb-2 border-b border-gray-200"><SchemaSummary schema={summary} /></div>}
      {report}
      {card ? (
        <PanelErrorBoundary key={key} name="Details card">
          <ContextSensitiveCard cardType={card.type} selectedData={card.data} valuesByAxis={axisValues}
            gradient={gradient} elementDescription={descriptions[key]} clusterAssignments={clusterPath} legacyHint={legacy} onClose={onClose}>
            {nodeDetails}
            {itemPath}
          </ContextSensitiveCard>
        </PanelErrorBoundary>
      ) : (
        <p className="text-[10px] text-gray-400 py-6 text-center">Click a node or a flow for its details</p>
      )}
      <PanelErrorBoundary name="Reports">
        <LegacyReports reports={reports} layer={layer} />
      </PanelErrorBoundary>
    </div>
  )
}
