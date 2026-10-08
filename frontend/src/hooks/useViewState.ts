// The view's state lives in the URL, so a deep link, a command from Claude Code or the MUD, an
// exported figure's recipe and a screenshot all name the same view.
import { useCallback, useMemo } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { GRADIENT_SCHEMES, type GradientScheme } from '../utils/colorBlending'

export const ZOOMS = [6, 12, 24] as const
export type Zoom = typeof ZOOMS[number]
export const RANKS = [1, 2, 3, 4] as const
export type LowerTab = 'members' | 'output' | 'trajectories'

export interface ViewState {
  session: string
  lens: string
  legacy: boolean
  layer: number // the first layer in view
  zoom: Zoom
  color: string // the colour axis
  color2: string // the blend axis, or 'none'
  gradient: GradientScheme
  rank: number // the expert chart's rank, 1 to 4
  top: number | null // links kept per layer in the expert chart; null keeps all
  sel: string // the selected node, link ("source>target") or item ("probe:<id>"); '' for none
  tab: LowerTab
}

export const DEFAULT_VIEW: ViewState = {
  session: '', lens: '', legacy: false, layer: 0, zoom: 6, color: 'label', color2: 'none',
  gradient: 'red-blue', rank: 1, top: 10, sel: '', tab: 'members',
}

const isZoom = (n: number): n is Zoom => (ZOOMS as readonly number[]).includes(n)

export function parseView(params: URLSearchParams): ViewState {
  const get = (key: string) => params.get(key)
  const int = (key: string, fallback: number, ok: (n: number) => boolean) => {
    const raw = get(key)
    const n = Number(raw)
    return raw !== null && Number.isInteger(n) && ok(n) ? n : fallback
  }
  const gradient = get('grad')
  const tab = get('tab')
  return {
    session: get('session') ?? '',
    lens: get('lens') ?? '',
    legacy: get('legacy') === '1',
    layer: int('layer', 0, n => n >= 0),
    zoom: int('zoom', DEFAULT_VIEW.zoom, isZoom) as Zoom,
    color: get('color') || DEFAULT_VIEW.color,
    color2: get('color2') || DEFAULT_VIEW.color2,
    gradient: gradient && gradient in GRADIENT_SCHEMES ? gradient as GradientScheme : DEFAULT_VIEW.gradient,
    rank: int('rank', DEFAULT_VIEW.rank, n => n >= 1 && n <= 4),
    top: get('top') === 'all' ? null : int('top', DEFAULT_VIEW.top ?? 10, n => n > 0),
    sel: get('sel') ?? '',
    tab: tab === 'output' || tab === 'trajectories' ? tab : 'members',
  }
}

// Only what differs from the defaults goes into the URL, so links stay short.
export function viewQuery(view: ViewState): URLSearchParams {
  const out = new URLSearchParams()
  const put = (key: string, value: string, fallback: string) => { if (value !== fallback) out.set(key, value) }
  const show = (top: number | null) => (top === null ? 'all' : String(top))
  put('session', view.session, DEFAULT_VIEW.session)
  put('lens', view.lens, DEFAULT_VIEW.lens)
  if (view.legacy) out.set('legacy', '1')
  put('layer', String(view.layer), String(DEFAULT_VIEW.layer))
  put('zoom', String(view.zoom), String(DEFAULT_VIEW.zoom))
  put('color', view.color, DEFAULT_VIEW.color)
  put('color2', view.color2, DEFAULT_VIEW.color2)
  put('grad', view.gradient, DEFAULT_VIEW.gradient)
  put('rank', String(view.rank), String(DEFAULT_VIEW.rank))
  put('top', show(view.top), show(DEFAULT_VIEW.top))
  put('sel', view.sel, DEFAULT_VIEW.sel)
  put('tab', view.tab, DEFAULT_VIEW.tab)
  return out
}

export type UpdateView = (patch: Partial<ViewState>, options?: { replace?: boolean }) => void

// The view and a setter that merges a patch into the URL. The setter reads the address bar at call
// time, so consecutive or late updates (a MUD message, a finished job) compose instead of
// overwriting each other. Discrete changes add a history entry; pass `replace` for continuous ones.
export function useViewState(): [ViewState, UpdateView] {
  const { search } = useLocation()
  const navigate = useNavigate()
  const view = useMemo(() => parseView(new URLSearchParams(search)), [search])
  const update = useCallback<UpdateView>((patch, options) => {
    const current = parseView(new URLSearchParams(window.location.search))
    navigate({ search: `?${viewQuery({ ...current, ...patch })}` }, { replace: options?.replace ?? false })
  }, [navigate])
  return [view, update]
}
