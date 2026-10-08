// Build: make a lens from a form, then see the capture's lenses, newest builds and legacy schemas
// alike. A built lens's k can be changed layer by layer (a new version) and saved. A finished
// build opens in Layers.
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { apiClient } from '../api/client'
import type { LensMethods, LensOptions, LensSummary } from '../types/lens'
import { useViewState, viewQuery } from '../hooks/useViewState'
import { lensAsSchema } from '../utils/lensAsSchema'
import SchemaSummary from '../components/analysis/SchemaSummary'
import LensForm from '../components/lenses/LensForm'
import LensReport from '../components/lenses/LensReport'
import AnalystStatus from '../components/lenses/AnalystStatus'
import LensVersions from '../components/lenses/LensVersions'
import LensBadges from '../components/lenses/LensBadges'
import LensValidation from '../components/lenses/LensValidation'
import MassMeanForm from '../components/lenses/MassMeanForm'
import MassMeanDetails from '../components/lenses/MassMeanDetails'
import MassMeanResults from '../components/lenses/MassMeanResults'
import { useShell } from '../components/shell/shellContext'

export default function BuildWorkspace() {
  const [view] = useViewState()
  const { room, events } = useShell()
  const visitor = room?.role === 'visitor' // visitors only look
  const navigate = useNavigate()
  const [lenses, setLenses] = useState<LensSummary[] | null>(null)
  const [options, setOptions] = useState<LensOptions | null>(null)
  const [methods, setMethods] = useState<LensMethods | null>(null)
  const [problem, setProblem] = useState<string | null>(null)
  const [reload, setReload] = useState(0)
  const [open, setOpen] = useState<string | null>(null) // the lens whose k table is shown
  const [results, setResults] = useState<string | null>(null) // the lens whose validation is shown
  const [report, setReport] = useState<string | null>(null) // the lens whose LLM report is shown

  useEffect(() => {
    apiClient.getLensMethods().then(setMethods).catch(err => setProblem(String(err)))
  }, [])

  useEffect(() => {
    if (!view.session) return
    let current = true
    setOptions(null)
    apiClient.getLensOptions(view.session)
      .then(found => { if (current) setOptions(found) })
      .catch(err => { if (current) setProblem(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [view.session])

  useEffect(() => {
    if (!view.session) return
    let current = true
    apiClient.listLenses(view.session)
      .then(found => { if (current) setLenses(found) })
      .catch(() => { if (current) setLenses([]) })
    return () => { current = false }
  }, [view.session, events.lensRevision, reload])

  if (!view.session) {
    return <div className="m-4 text-xs text-slate-700">Choose a capture in the top bar to build a lens on it.</div>
  }
  const show = (name: string, legacy: boolean) =>
    navigate({ pathname: '/layers', search: `?${viewQuery({ ...view, lens: name, legacy, sel: '', layer: 0 })}` })
  return (
    <div className="h-full overflow-y-auto p-3 space-y-3">
      {problem && <p className="text-xs text-red-600">{problem}</p>}
      {options && methods
        ? <LensForm key={view.session} session={view.session} options={options} methods={methods} disabled={visitor}
            takenNames={(lenses ?? []).map(l => l.name)} onBuilt={name => show(name, false)} />
        : !problem && <p className="text-xs text-gray-500">Reading the capture…</p>}
      {options && (
        <MassMeanForm key={`mm:${view.session}`} session={view.session} options={options} disabled={visitor}
          takenNames={(lenses ?? []).map(l => l.name)} onBuilt={() => setReload(r => r + 1)} />
      )}
      <h2 className="text-sm font-semibold text-gray-900">Lenses on this capture</h2>
      {lenses && <AnalystStatus session={view.session} disabled={visitor}
        lens={(lenses.find(l => !l.legacy && l.kind === 'umap' && l.name === view.lens)
          ?? lenses.find(l => !l.legacy && l.kind === 'umap'))?.name ?? null} />}
      {lenses === null && <p className="text-xs text-gray-500">Loading…</p>}
      {lenses?.length === 0 && <p className="text-xs text-gray-500">None yet.</p>}
      {lenses?.map(lens => (
        <div key={`${lens.legacy}:${lens.name}`} className="bg-white border border-gray-200 rounded p-2">
          <div className="flex items-start gap-3">
            <div className="flex-1 min-w-0">
              {lens.legacy
                ? <div className="text-xs"><span className="font-mono">{lens.name}</span>
                    <span className="ml-2 text-[10px] text-gray-500">legacy schema · {lens.n_items ?? '?'} items</span></div>
                : lens.kind === 'mass_mean'
                  ? <div className="text-xs"><span className="font-mono">{lens.name}</span>
                      <span className="ml-2 text-[10px] text-gray-500">mass-mean: {lens.contrast?.label_a} at −1, {lens.contrast?.label_b} at +1 ·
                        {' '}{lens.n_items ?? '?'} items · token position {lens.site?.token_position}</span></div>
                  : <SchemaSummary schema={lensAsSchema(lens)} />}
              {!lens.legacy && lens.kind !== 'mass_mean' && (
                <div className="text-[10px] text-gray-500 mt-0.5">
                  {lens.current} {lens.state ?? 'draft'} · {lens.versions?.length ?? 1} version(s) · built{' '}
                  {lens.created_at?.slice(0, 16).replace('T', ' ')} by {lens.created_by}
                </div>
              )}
              {!lens.legacy && (
                <div className="mt-1">
                  <LensBadges session={view.session} lens={lens} disabled={visitor} onValidated={() => setReload(r => r + 1)} />
                </div>
              )}
            </div>
            {!lens.legacy && lens.validation && (
              <button onClick={() => setResults(o => (o === lens.name ? null : lens.name))}
                className="px-2 py-1 text-xs rounded border border-gray-300 text-gray-700 hover:bg-gray-50">
                {lens.kind === 'mass_mean' ? 'results' : 'validation'} {results === lens.name ? '▴' : '▾'}
              </button>
            )}
            {!lens.legacy && lens.kind !== 'mass_mean' && (
              <button onClick={() => setReport(o => (o === lens.name ? null : lens.name))} aria-label={`Report on ${lens.name}`}
                className="px-2 py-1 text-xs rounded border border-violet-300 text-violet-800 hover:bg-violet-50">
                report {report === lens.name ? '▴' : '▾'}
              </button>
            )}
            {!lens.legacy && lens.kind !== 'mass_mean' && (
              <button onClick={() => setOpen(o => (o === lens.name ? null : lens.name))}
                className="px-2 py-1 text-xs rounded border border-gray-300 text-gray-700 hover:bg-gray-50">
                k per layer {open === lens.name ? '▴' : '▾'}
              </button>
            )}
            {lens.kind !== 'mass_mean' && (
              <button onClick={() => show(lens.name, lens.legacy)} disabled={visitor}
                className="px-2 py-1 text-xs rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">Open in Layers</button>
            )}
          </div>
          {results === lens.name && !lens.legacy && lens.validation && (lens.kind === 'mass_mean'
            ? <><MassMeanResults session={view.session} lens={lens} />
                <MassMeanDetails session={view.session} lens={lens} disabled={visitor} /></>
            : <LensValidation session={view.session} lens={lens} />)}
          {report === lens.name && !lens.legacy && (
            <div className="mt-2"><LensReport session={view.session} lens={lens.name} cardId="lens"
              label="Report on this lens" disabled={visitor} /></div>
          )}
          {open === lens.name && !lens.legacy && (
            <LensVersions key={`${lens.name}:${lens.current}`} session={view.session} lens={lens} disabled={visitor}
              onChanged={() => setReload(r => r + 1)} />
          )}
        </div>
      ))}
    </div>
  )
}
