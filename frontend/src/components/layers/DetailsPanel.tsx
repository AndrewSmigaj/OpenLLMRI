// Beside the charts: what the lens is, the card for the selection (with a legacy schema's written
// description of it), and the legacy schema's reports.
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
  onClose: () => void
}

export default function DetailsPanel({ summary, card, descriptions, reports, layer, clusterPath,
                                       axisValues, gradient, onClose }: DetailsPanelProps) {
  const key = card ? descriptionKey(card) : ''
  return (
    <div className="h-full overflow-y-auto overflow-x-hidden p-2 space-y-2 bg-white">
      {summary && <div className="pb-2 border-b border-gray-200"><SchemaSummary schema={summary} /></div>}
      {card ? (
        <PanelErrorBoundary key={key} name="Details card">
          <ContextSensitiveCard cardType={card.type} selectedData={card.data} valuesByAxis={axisValues}
            gradient={gradient} elementDescription={descriptions[key]} clusterAssignments={clusterPath} onClose={onClose} />
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
