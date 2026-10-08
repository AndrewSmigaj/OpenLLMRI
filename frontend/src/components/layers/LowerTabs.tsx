// The tabs under the charts: the members of the selection, the output table, and the 3-D
// trajectories. Only the open tab is drawn; which one is open is kept in the URL.
import type { ReactNode } from 'react'
import type { LowerTab } from '../../hooks/useViewState'
import PanelErrorBoundary from '../common/PanelErrorBoundary'

const TABS: { id: LowerTab; label: string }[] = [
  { id: 'members', label: 'Members' },
  { id: 'output', label: 'Output' },
  { id: 'trajectories', label: '3-D trajectories' },
  { id: 'experts', label: 'Expert fingerprints' },
]

interface LowerTabsProps {
  tab: LowerTab
  onTab: (tab: LowerTab) => void
  panels: Record<LowerTab, ReactNode>
}

export default function LowerTabs({ tab, onTab, panels }: LowerTabsProps) {
  return (
    <div className="h-full flex flex-col bg-white">
      <div className="flex gap-1 px-2 pt-1 border-b border-gray-200 flex-shrink-0">
        {TABS.map(t => (
          <button key={t.id} onClick={() => onTab(t.id)}
            className={`px-2 py-1 text-xs rounded-t ${tab === t.id
              ? 'bg-white border border-b-white border-gray-200 -mb-px font-medium text-gray-900' : 'text-gray-500 hover:text-gray-800'}`}>
            {t.label}
          </button>
        ))}
      </div>
      <div className="flex-1 min-h-0 overflow-auto p-2">
        <PanelErrorBoundary key={tab} name={TABS.find(t => t.id === tab)?.label ?? tab}>
          {panels[tab]}
        </PanelErrorBoundary>
      </div>
    </div>
  )
}
