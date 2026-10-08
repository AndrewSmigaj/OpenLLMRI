// A small "Export" menu for a chart; each choice saves a file that carries the chart's recipe.
import { useState } from 'react'
import type { ExportFormat } from '../../utils/exportFigure'

interface ExportMenuProps {
  formats: ExportFormat[]
  onExport: (format: ExportFormat) => void
  disabled?: boolean
}

const LABELS: Record<ExportFormat, string> = {
  png: 'PNG image', svg: 'SVG drawing', csv: 'CSV table', json: 'JSON data',
}

export default function ExportMenu({ formats, onExport, disabled }: ExportMenuProps) {
  const [open, setOpen] = useState(false)
  return (
    <div className="relative inline-block">
      <button onClick={() => setOpen(o => !o)} disabled={disabled}
        className="px-1.5 py-0.5 text-[10px] border border-gray-300 rounded bg-white text-gray-700 hover:bg-gray-50 disabled:text-gray-300">
        Export ▾
      </button>
      {open && (
        <div className="absolute left-0 mt-1 bg-white border border-gray-300 rounded shadow-lg z-50 py-1 min-w-[110px]"
          onMouseLeave={() => setOpen(false)}>
          {formats.map(format => (
            <button key={format} onClick={() => { setOpen(false); onExport(format) }}
              className="block w-full text-left px-2 py-1 text-xs text-gray-700 hover:bg-gray-100">
              {LABELS[format]}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
