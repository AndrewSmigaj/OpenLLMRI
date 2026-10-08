// The colour controls. The input colour axis, blend axis and gradient live in the URL, since they
// change the figure a link names; the shape axis and the ambiguity blend are the page's own. The
// output colours are held by the page too, since they also regroup the output column the flows
// are loaded with. The axes themselves come from the loaded flows.
import { useMemo, useState } from 'react'
import type { DynamicAxis } from '../types/api'
import type { AmbiguityBlend, GradientScheme } from '../utils/colorBlending'
import { GRADIENT_AUTO_PAIRS } from '../utils/colorBlending'
import type { UpdateView, ViewState } from './useViewState'

const valuesOf = (axis: DynamicAxis | undefined) => axis ? (axis.values || [axis.label_a, axis.label_b]) : undefined

export interface OutputColour {
  axis: string // '' matches the input colours
  axis2: string // 'none' for no blend
  gradient: GradientScheme
}

export const DEFAULT_OUTPUT_COLOUR: OutputColour = { axis: '', axis2: 'none', gradient: 'purple-green' }

// The output axes the output column is grouped by: the ones chosen for its colour
export const outputGroupingOf = (output: OutputColour) => [output.axis, output.axis2].filter(a => a && a !== 'none')

export function useAxisControls(allAxes: DynamicAxis[], outputAxes: DynamicAxis[], view: ViewState, update: UpdateView,
                                output: OutputColour, setOutput: (output: OutputColour) => void) {
  const [shapeAxisId, setShapeAxisId] = useState('none')
  const [blendOn, setAmbiguityBlendEnabled] = useState(false)
  const [blendPole, setAmbiguousValue] = useState('')
  const { axis: outputColorAxisId, axis2: outputColorAxis2Id, gradient: outputGradient } = output

  // A colour axis this capture doesn't have falls back to its first axis
  const colorAxis = allAxes.find(a => a.id === view.color) ?? allAxes[0]
  const colorAxis2 = allAxes.find(a => a.id === view.color2)
  const shapeAxis = allAxes.find(a => a.id === shapeAxisId)
  const outputColorAxis = outputAxes.find(a => a.id === outputColorAxisId)
  const outputColorAxis2 = outputAxes.find(a => a.id === outputColorAxis2Id)

  const primaryValues = useMemo(() => valuesOf(colorAxis) ?? [], [colorAxis])
  const secondaryValues = useMemo(() => valuesOf(colorAxis2), [colorAxis2])
  const outputPrimaryValues = useMemo(() => valuesOf(outputColorAxis) ?? [], [outputColorAxis])
  const outputSecondaryValues = useMemo(() => valuesOf(outputColorAxis2), [outputColorAxis2])

  // The ambiguity blend applies to a two-valued blend axis; its pole defaults to the first value
  const canBlend = secondaryValues?.length === 2
  const ambiguousValue = canBlend && secondaryValues.includes(blendPole) ? blendPole : secondaryValues?.[0] ?? ''
  const ambiguityBlendEnabled = canBlend && blendOn
  const ambiguityBlend = useMemo<AmbiguityBlend | undefined>(
    () => (ambiguityBlendEnabled ? { enabled: true, ambiguousValue, mixRatio: 0.6 } : undefined),
    [ambiguityBlendEnabled, ambiguousValue])

  return {
    allAxes, outputAxes,
    colorAxisId: colorAxis?.id ?? view.color, colorAxis2Id: colorAxis2 ? colorAxis2.id : 'none',
    gradient: view.gradient, secondaryGradient: GRADIENT_AUTO_PAIRS[view.gradient],
    colorAxis, colorAxis2, shapeAxis, shapeAxisId: shapeAxis ? shapeAxisId : 'none',
    primaryValues, secondaryValues,
    canBlend, ambiguityBlendEnabled, ambiguousValue, ambiguityBlend,
    outputColorAxisId: outputColorAxis ? outputColorAxisId : '',
    outputColorAxis2Id: outputColorAxis2 ? outputColorAxis2Id : 'none',
    outputColorAxis, outputColorAxis2, outputGradient,
    outputSecondaryGradient: GRADIENT_AUTO_PAIRS[outputGradient],
    outputPrimaryValues, outputSecondaryValues,
    setColorAxisId: (id: string) => update({ color: id }),
    setColorAxis2Id: (id: string) => update({ color2: id }),
    setGradient: (gradient: GradientScheme) => update({ gradient }),
    setShapeAxisId, setAmbiguityBlendEnabled, setAmbiguousValue,
    setOutputColorAxisId: (axis: string) => setOutput({ ...output, axis }),
    setOutputColorAxis2Id: (axis2: string) => setOutput({ ...output, axis2 }),
    setOutputGradient: (gradient: GradientScheme) => setOutput({ ...output, gradient }),
  }
}

export type AxisControlsState = ReturnType<typeof useAxisControls>
