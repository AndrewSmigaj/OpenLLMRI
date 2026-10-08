// A lab room's view preset (data/labs/*.yaml, sent with room_entered) as view state. The windows
// presets name (w0 to w3) were six-layer ranges; each becomes its first layer at zoom 6.
import type { VizPreset } from '../types/evennia'
import { GRADIENT_SCHEMES, type GradientScheme } from './colorBlending'
import { DEFAULT_VIEW, type ViewState } from '../hooks/useViewState'

const WINDOW_START: Record<string, number> = { w0: 0, w1: 5, w2: 11, w3: 17 }

export function presetView(session: string, lens: string, legacy: boolean, preset: VizPreset | undefined): ViewState {
  const gradient = preset?.gradient && preset.gradient in GRADIENT_SCHEMES
    ? preset.gradient as GradientScheme : DEFAULT_VIEW.gradient
  return {
    ...DEFAULT_VIEW,
    session, lens, legacy, gradient,
    layer: WINDOW_START[preset?.window ?? 'w0'] ?? 0,
    zoom: 6,
    color: preset?.primary_axis || DEFAULT_VIEW.color,
    top: preset?.top_routes ?? DEFAULT_VIEW.top,
  }
}
