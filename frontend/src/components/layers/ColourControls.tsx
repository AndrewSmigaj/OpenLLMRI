// The colour controls carried over from the old toolbar: the colour axis and gradient stay in
// view; the blend axis, ambiguity blend, shape axis and the output column's colours sit under
// "More". (10b.5 replaces the colour maths; the controls stay.)
import { useState } from 'react'
import type { AxisControlsState } from '../../hooks/useAxisControls'
import { getAxisPreview, GRADIENT_SCHEMES, type GradientScheme } from '../../utils/colorBlending'

const ctrl = 'px-1.5 py-0.5 text-[11px] border border-gray-300 rounded bg-white disabled:bg-gray-100 disabled:text-gray-400'
const row = 'flex items-center gap-2'
const name = 'text-[11px] text-gray-600 w-[78px] text-right flex-shrink-0'

function Swatches({ items }: { items: { label: string; color: string }[] }) {
  if (items.length === 0) return null
  return (
    <div className="flex flex-wrap items-center gap-2 pl-[86px]">
      {items.map(({ label, color }) => (
        <span key={label} className="flex items-center gap-1 text-[11px] text-gray-600" title={label}>
          <span className="w-3 h-3 rounded-sm border border-gray-300" style={{ backgroundColor: color }} />
          {label}
        </span>
      ))}
    </div>
  )
}

function GradientSelect({ value, onChange, disabled }: { value: GradientScheme; onChange: (g: GradientScheme) => void; disabled?: boolean }) {
  return (
    <select value={value} onChange={e => onChange(e.target.value as GradientScheme)} disabled={disabled} className={ctrl}>
      {Object.entries(GRADIENT_SCHEMES).map(([key, scheme]) => <option key={key} value={key}>{scheme.name}</option>)}
    </select>
  )
}

export default function ColourControls({ axes, disabled }: { axes: AxisControlsState; disabled?: boolean }) {
  const [more, setMore] = useState(false)
  const { allAxes, outputAxes } = axes
  const preview = axes.primaryValues.length ? getAxisPreview(axes.primaryValues, axes.gradient, axes.secondaryValues) : []
  const outputPreview = axes.outputPrimaryValues.length
    ? getAxisPreview(axes.outputPrimaryValues, axes.outputGradient, axes.outputSecondaryValues) : []

  return (
    <div className="relative flex items-center gap-1.5">
      <span className="text-[11px] text-gray-600">Colour</span>
      <select value={axes.colorAxisId} onChange={e => axes.setColorAxisId(e.target.value)} disabled={disabled} className={ctrl}>
        {allAxes.length === 0 && <option value="">No axes</option>}
        {allAxes.map(axis => <option key={axis.id} value={axis.id}>{axis.label}</option>)}
      </select>
      <GradientSelect value={axes.gradient} onChange={axes.setGradient} disabled={disabled} />
      <button onClick={() => setMore(m => !m)} disabled={disabled}
        className="px-1.5 py-0.5 text-[11px] border border-gray-300 rounded bg-white text-gray-700 hover:bg-gray-50 disabled:bg-gray-100 disabled:text-gray-400">
        More {more ? '▴' : '▾'}
      </button>
      {more && !disabled && (
        <div className="absolute left-0 top-full mt-1 z-40 w-[420px] bg-white border border-gray-300 rounded shadow-lg p-2 space-y-1.5">
          <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide">Input</div>
          <div className={row}>
            <span className={name}>Blend axis</span>
            <select value={axes.colorAxis2Id} onChange={e => axes.setColorAxis2Id(e.target.value)} className={ctrl}>
              <option value="none">None</option>
              {allAxes.filter(a => a.id !== axes.colorAxisId).map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
            </select>
            {axes.colorAxis2 && <span className="text-[11px] text-gray-400">{GRADIENT_SCHEMES[axes.secondaryGradient]?.name}</span>}
          </div>
          {axes.canBlend && (
            <div className={row}>
              <span className={name}>Ambig. blend</span>
              <label className="flex items-center gap-1 text-[11px] text-gray-600">
                <input type="checkbox" checked={axes.ambiguityBlendEnabled}
                  onChange={e => axes.setAmbiguityBlendEnabled(e.target.checked)} className="w-3 h-3" />
                Enable
              </label>
              {axes.ambiguityBlendEnabled && (
                <select value={axes.ambiguousValue} onChange={e => axes.setAmbiguousValue(e.target.value)} className={ctrl}>
                  {(axes.secondaryValues ?? []).map(v => <option key={v} value={v}>{v}</option>)}
                </select>
              )}
            </div>
          )}
          <div className={row}>
            <span className={name}>Shape axis</span>
            <select value={axes.shapeAxisId} onChange={e => axes.setShapeAxisId(e.target.value)} className={ctrl}>
              <option value="none">None</option>
              {allAxes.map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
            </select>
          </div>
          <Swatches items={preview} />
          <div className={`border-t border-gray-200 pt-1.5 space-y-1.5 ${outputAxes.length ? '' : 'opacity-40 pointer-events-none'}`}>
            <div className="text-[10px] font-medium text-gray-400 uppercase tracking-wide">Output column</div>
            <div className={row}>
              <span className={name}>Colour axis</span>
              <select value={axes.outputColorAxisId} onChange={e => axes.setOutputColorAxisId(e.target.value)}
                disabled={!outputAxes.length} className={ctrl}>
                <option value="">Match input</option>
                {outputAxes.map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
              <GradientSelect value={axes.outputGradient} onChange={axes.setOutputGradient} disabled={!outputAxes.length} />
            </div>
            <div className={row}>
              <span className={name}>Blend axis</span>
              <select value={axes.outputColorAxis2Id} onChange={e => axes.setOutputColorAxis2Id(e.target.value)}
                disabled={!outputAxes.length} className={ctrl}>
                <option value="none">None</option>
                {outputAxes.filter(a => a.id !== axes.outputColorAxisId).map(a => <option key={a.id} value={a.id}>{a.label}</option>)}
              </select>
            </div>
            <Swatches items={outputPreview} />
          </div>
        </div>
      )}
    </div>
  )
}
