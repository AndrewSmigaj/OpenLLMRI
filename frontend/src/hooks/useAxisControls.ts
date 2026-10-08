// The colour controls. The colour axis, a second axis sharing the colour (as lightness, or by
// fading one of its values toward grey), the gradient and stripes live in the URL, since they
// change the figure a link names. The shape axis (3-D only) and the output column's colours are
// the page's own; the output colours also regroup the output column the flows are loaded with.
import { useMemo, useState } from 'react'
import type { DynamicAxis } from '../types/api'
import type { ColourSpec, GradientScheme } from '../color/scheme'
import type { UpdateView, ViewState } from './useViewState'

const valuesOf = (axis: DynamicAxis | undefined): string[] =>
  axis ? (axis.values?.length ? axis.values : [axis.label_a, axis.label_b]) : []

export interface OutputColour {
  axis: string // '' matches the input colours
  axis2: string // 'none' for no second axis (shown as lightness)
  gradient: GradientScheme
}

export const DEFAULT_OUTPUT_COLOUR: OutputColour = { axis: '', axis2: 'none', gradient: 'purple-green' }

// The output axes the output column is grouped by: the ones chosen for its colour
export const outputGroupingOf = (output: OutputColour) => [output.axis, output.axis2].filter(a => a && a !== 'none')

export const FADE_AMOUNT = 0.6 // a fully faded item moves 60% of the way to grey, as before

export function useAxisControls(allAxes: DynamicAxis[], outputAxes: DynamicAxis[], view: ViewState, update: UpdateView,
                                output: OutputColour, setOutput: (output: OutputColour) => void) {
  const [shapeAxisId, setShapeAxisId] = useState('none')
  // A colour axis this capture doesn't have falls back to its first axis
  const colorAxis = allAxes.find(a => a.id === view.color) ?? allAxes[0]
  const secondAxis = allAxes.find(a => a.id === view.color2 && a.id !== colorAxis?.id)
  const fadeValue = secondAxis && valuesOf(secondAxis).includes(view.fade) ? view.fade : ''
  const shapeAxis = allAxes.find(a => a.id === shapeAxisId)
  const outputAxis = outputAxes.find(a => a.id === output.axis)
  const outputAxis2 = outputAxes.find(a => a.id === output.axis2 && a.id !== outputAxis?.id)

  const input = useMemo<ColourSpec>(() => ({
    axis: colorAxis?.id ?? 'label', values: valuesOf(colorAxis), gradient: view.gradient,
    ...(secondAxis && !fadeValue ? { lightness: { axis: secondAxis.id, values: valuesOf(secondAxis) } } : {}),
    ...(secondAxis && fadeValue ? { fade: { axis: secondAxis.id, value: fadeValue, amount: FADE_AMOUNT } } : {}),
  }), [colorAxis, secondAxis, fadeValue, view.gradient])

  const outputSpec = useMemo<ColourSpec | null>(() => (outputAxis ? {
    axis: outputAxis.id, values: valuesOf(outputAxis), gradient: output.gradient,
    ...(outputAxis2 ? { lightness: { axis: outputAxis2.id, values: valuesOf(outputAxis2) } } : {}),
  } : null), [outputAxis, outputAxis2, output.gradient])

  // Every axis's values in one fixed order, so a value keeps its colour wherever it is shown
  const axisValues = useMemo(() => Object.fromEntries(allAxes.map(a => [a.id, valuesOf(a)])), [allAxes])

  return {
    allAxes, outputAxes, axisValues, colorAxis, secondAxis, fadeValue, shapeAxis,
    shapeAxisId: shapeAxis ? shapeAxisId : 'none',
    input, output: outputSpec, stripes: view.stripes, gradient: view.gradient,
    outputChoice: { axis: outputAxis?.id ?? '', axis2: outputAxis2?.id ?? 'none', gradient: output.gradient },
    setColorAxisId: (id: string) => update({ color: id }),
    setSecondAxisId: (id: string) => update({ color2: id, fade: '' }),
    setFadeValue: (value: string) => update({ fade: value }),
    setGradient: (gradient: GradientScheme) => update({ gradient }),
    setStripes: (stripes: boolean) => update({ stripes }),
    setShapeAxisId,
    setOutputColorAxisId: (axis: string) => setOutput({ ...output, axis }),
    setOutputColorAxis2Id: (axis2: string) => setOutput({ ...output, axis2 }),
    setOutputGradient: (gradient: GradientScheme) => setOutput({ ...output, gradient }),
  }
}

export type AxisControlsState = ReturnType<typeof useAxisControls>
