// The colour controls. In view: the colour axis, the gradient and stripes. Under "More": a
// second axis in the same colour (as lightness, or fading one of its values toward grey), the 3-D
// view's shape axis, and the output column's own colours. The legend beside the charts says what
// every colour means.
import { useState } from 'react'
import type { AxisControlsState } from '../../hooks/useAxisControls'
import { GRADIENT_SCHEMES, type GradientScheme } from '../../color/scheme'

const ctrl = 'px-1.5 py-0.5 text-[11px] border border-gray-300 rounded bg-white disabled:bg-gray-100 disabled:text-gray-400'
const row = 'flex items-center gap-2'
const name = 'text-[11px] text-gray-600 w-[78px] text-right flex-shrink-0'

function GradientSelect({ value, onChange, disabled }: { value: GradientScheme; onChange: (g: GradientScheme) => void; disabled?: boolean }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value as GradientScheme)} disabled={disabled} className={ctrl}
      title="The two colours of a two-valued axis (more values take a categorical palette)">
      {Object.entries(GRADIENT_SCHEMES).map(([key, scheme]) => <option key={key} value={key}>{scheme.name}</option>)}
    </select>
  )
}

export default function ColourControls({ axes, disabled }: { axes: AxisControlsState; disabled?: boolean }) {
  const [more, setMore] = useState(false)
  const { allAxes, outputAxes, secondAxis } = axes
  const secondValues = secondAxis?.values ?? []

  return (
    <div className="relative flex items-center gap-1.5">
      <span className="text-[11px] text-gray-600">Colour</span>
      <select value={axes.colorAxis?.id ?? ''} onChange={e => axes.setColorAxisId(e.target.value)} disabled={disabled} className={ctrl}>
        {allAxes.length === 0 && <option value="">No axes</option>}
        {allAxes.map(axis => <option key={axis.id} value={axis.id}>{axis.label}</option>)}
      </select>
      <GradientSelect value={axes.gradient} onChange={axes.setGradient} disabled={disabled} />
      <label className="flex items-center gap-1 text-[11px] text-gray-600" title="Nodes show their exact shares as bands">
        <input type="checkbox" checked={axes.stripes} disabled={disabled} onChange={e => axes.setStripes(e.target.checked)} className="w-3 h-3" />
        Stripes
      </label>
      <button onClick={() => setMore(m => !m)} disabled={disabled}
        className="px-1.5 py-0.5 text-[11px] border border-gray-300 rounded bg-white text-gray-700 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400">
        More {more ? '▴' : '▾'}
      </button>
      {more && !disabled && (
        <div className="absolute left-0 top-full mt-1 z-40 w-[440px] bg-white border border-gray-300 rounded shadow-lg p-2 space-y-1.5">
          <div className={row}>
            <span className={name}>Second axis</span>
            <select value={secondAxis?.id ?? 'none'} onChange={e => axes.setSecondAxisId(e.target.value)} className={ctrl}>
              <option value="none">None</option>
              {allAxes.filter(a => a.id !== axes.colorAxis?.id).map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
            </select>
          </div>
          {secondAxis && (
            <div className={row}>
              <span className={name}>shown as</span>
              <label className="flex items-center gap-1 text-[11px] text-gray-700"
                title="Hue shows the colour axis, lightness the second axis (a square legend)">
                <input type="radio" checked={!axes.fadeValue} onChange={() => axes.setFadeValue('')} />
                lightness
              </label>
              <label className="flex items-center gap-1 text-[11px] text-gray-700"
                title="Items with this value fade toward grey (the old ambiguity blend)">
                <input type="radio" checked={!!axes.fadeValue} onChange={() => axes.setFadeValue(secondValues[0] ?? '')} />
                fading
              </label>
              {axes.fadeValue && (
                <select value={axes.fadeValue} onChange={e => axes.setFadeValue(e.target.value)} className={ctrl}>
                  {secondValues.map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              )}
            </div>
          )}
          <div className={row}>
            <span className={name}>Shape (3-D)</span>
            <select value={axes.shapeAxisId} onChange={e => axes.setShapeAxisId(e.target.value)} className={ctrl}>
              <option value="none">None</option>
              {allAxes.map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
            </select>
          </div>
          <div className={`border-t border-gray-200 pt-1.5 space-y-1.5 ${outputAxes.length ? '' : 'opacity-40 pointer-events-none'}`}>
            <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide">Output column</div>
            <div className={row}>
              <span className={name}>Colour axis</span>
              <select value={axes.outputChoice.axis} onChange={e => axes.setOutputColorAxisId(e.target.value)}
                disabled={!outputAxes.length} className={ctrl}>
                <option value="">Match input</option>
                {outputAxes.map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <GradientSelect value={axes.outputChoice.gradient} onChange={axes.setOutputGradient} disabled={!outputAxes.length} />
            </div>
            <div className={row}>
              <span className={name}>Second axis</span>
              <select value={axes.outputChoice.axis2} onChange={e => axes.setOutputColorAxis2Id(e.target.value)}
                disabled={!outputAxes.length || !axes.outputChoice.axis} className={ctrl}>
                <option value="none">None</option>
                {outputAxes.filter(a => a.id !== axes.outputChoice.axis).map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <span className="text-[10px] text-gray-400">as lightness</span>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
