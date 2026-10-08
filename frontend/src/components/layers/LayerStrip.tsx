// The overview strip: one cell per column (each layer, then the output), the ones in view
// highlighted; a click brings that layer into view. Below it, inside the scrolling area, the layer
// header labels each column of the charts.
interface LayerStripProps {
  columns: string[] // a label per column, in order
  first: number // the first column in view
  shown: number // how many columns fit in view
  onPick: (column: number) => void
}

export function LayerStrip({ columns, first, shown, onPick }: LayerStripProps) {
  return (
    <div className="flex gap-px" role="navigation" aria-label="Layers">
      {columns.map((label, i) => {
        const inView = i >= first && i < first + shown
        return (
          <button key={label} onClick={() => onPick(i)} title={label} aria-label={`Go to ${label}`}
            className={`flex-1 h-4 text-[9px] leading-4 rounded-sm ${inView
              ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500 hover:bg-gray-300'}`}>
            {label.replace(/^L/, '')}
          </button>
        )
      })}
    </div>
  )
}

interface LayerHeaderProps {
  columns: string[]
  left: number // the charts' left margin, in pixels
  spacing: number // pixels between columns
  width: number
}

export function LayerHeader({ columns, left, spacing, width }: LayerHeaderProps) {
  return (
    <div className="relative h-5 bg-white/90 border-b border-gray-200" style={{ width }}>
      {columns.map((label, i) => (
        <span key={label} className="absolute top-0.5 text-[10px] font-medium text-gray-600"
          style={{ left: left + i * spacing }}>
          {label}
        </span>
      ))}
    </div>
  )
}
