// The legend, always on: what every colour means. One axis gets a swatch per value; two axes in
// one colour get a square grid (hue across, lightness down); fade mode shows a faded swatch. The
// output column's own colours follow when it has them.
import { legendOf, type ColourSpec, type Legend } from '../../color/scheme'

const swatch = (color: string) => (
  <span className="inline-block w-3 h-3 rounded-sm border border-gray-300 flex-shrink-0" style={{ backgroundColor: color }} />
)

function LegendBlock({ title, legend }: { title: string; legend: Legend }) {
  return (
    <div className="flex items-start gap-2">
      <span className="text-[11px] font-medium text-gray-600 whitespace-nowrap pt-px">{title}: {legend.axis}</span>
      {legend.grid ? (
        <table className="text-[10px] text-gray-600 border-separate" style={{ borderSpacing: 2 }}>
          <thead>
            <tr>
              <th className="font-normal text-gray-400 text-left pr-1">{legend.grid.second} ↓</th>
              {legend.entries.map(e => <th key={e.label} className="font-normal px-0.5">{e.label}</th>)}
            </tr>
          </thead>
          <tbody>
            {legend.grid.rows.map((row, r) => (
              <tr key={row}>
                <td className="pr-1">{row}</td>
                {legend.grid!.cells[r].map((color, c) => (
                  <td key={c} className="text-center"><span className="inline-block w-5 h-3 rounded-sm border border-gray-300" style={{ backgroundColor: color }} /></td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="flex flex-wrap items-center gap-x-2 gap-y-0.5">
          {legend.entries.map(e => (
            <span key={e.label} className="flex items-center gap-1 text-[11px] text-gray-600">{swatch(e.color)}{e.label}</span>
          ))}
        </div>
      )}
      {legend.fade && (
        <span className="flex items-center gap-1 text-[11px] text-gray-500 whitespace-nowrap">
          {swatch(legend.fade.color)} faded: {legend.fade.label}
        </span>
      )}
    </div>
  )
}

export default function ColourLegend({ input, output, stripes }: { input: ColourSpec; output: ColourSpec | null; stripes: boolean }) {
  return (
    <div className="flex flex-wrap items-start gap-x-6 gap-y-1">
      <LegendBlock title="Colour" legend={legendOf(input)} />
      {stripes && <span className="text-[11px] text-gray-500">Stripes: each node's bands are its exact shares</span>}
      {output && <LegendBlock title="Output" legend={legendOf(output)} />}
    </div>
  )
}
