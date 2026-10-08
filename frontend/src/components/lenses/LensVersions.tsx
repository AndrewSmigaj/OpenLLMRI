// A built lens's k, layer by layer, beside each layer's suggestions (elbow, silhouette, the
// tree's clear levels). Changing any k cuts the saved trees again as a new draft version, with no
// refit; Save freezes a version with its keywords.
import { useEffect, useState } from 'react'
import { apiClient } from '../../api/client'
import type { KSuggestion, LensSummary } from '../../types/lens'
import { heldoutBest } from '../../utils/validation'

interface LensVersionsProps {
  session: string
  lens: LensSummary
  disabled: boolean
  onChanged: () => void
}

const cell = 'px-1 py-0.5 text-center tabular-nums'
// Mirrors the backend's rule: the finest clear level, else the silhouette's k
const byMethod = (s: KSuggestion, method: string) =>
  method === 'levels' ? (s.levels.length ? Math.max(...s.levels) : s.silhouette) : method === 'elbow' ? s.elbow : s.silhouette

export default function LensVersions({ session, lens, disabled, onChanged }: LensVersionsProps) {
  const [suggestions, setSuggestions] = useState<Record<string, KSuggestion> | null>(null)
  const [layers, setLayers] = useState<number[]>([])
  const [ks, setKs] = useState<number[]>(lens.k_per_layer ?? [])
  const [keywords, setKeywords] = useState('')
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let current = true
    apiClient.getLens(session, lens.name, false)
      .then(detail => {
        if (!current) return
        setLayers(detail.layers)
        setSuggestions(detail.manifest?.suggestions ?? {})
      })
      .catch(err => { if (current) setError(err instanceof Error ? err.message : String(err)) })
    return () => { current = false }
  }, [session, lens.name])

  // Once validated, each layer's k that classified held-out data best (selection-biased)
  const [heldout, setHeldout] = useState<Record<string, number> | null>(null)
  useEffect(() => {
    if (!lens.validation) return
    let current = true
    apiClient.getLensValidation(session, lens.name)
      .then(found => { if (current) setHeldout(heldoutBest(found)) })
      .catch(() => undefined)
    return () => { current = false }
  }, [session, lens.name, lens.validation])

  const act = async (work: () => Promise<unknown>) => {
    setBusy(true); setError(null)
    try { await work(); onChanged() } catch (err) { setError(err instanceof Error ? err.message : String(err)) }
    finally { setBusy(false) }
  }
  const changed = ks.some((k, i) => k !== lens.k_per_layer?.[i])
  const saved = lens.state === 'saved'

  if (error && !suggestions) return <p className="text-xs text-red-600">{error}</p>
  if (!suggestions) return <p className="text-xs text-gray-500">Loading the suggestions…</p>
  // Each row: its name, what it shows at a layer, and the k it gives that layer
  const fromSuggestion = (show: (s: KSuggestion) => string, method: string) =>
    [(l: number) => (suggestions[String(l)] ? show(suggestions[String(l)]) : ''),
     (l: number) => byMethod(suggestions[String(l)], method)] as const
  const rows: [string, (l: number) => string, (l: number) => number | undefined][] = [
    ['elbow', ...fromSuggestion(s => String(s.elbow), 'elbow')],
    ['silhouette', ...fromSuggestion(s => String(s.silhouette), 'silhouette')],
    ['levels', ...fromSuggestion(s => s.levels.join(' ') || '–', 'levels')],
    ...(heldout ? [['held-out best', (l: number) => String(heldout[String(l)] ?? ''),
      (l: number) => heldout[String(l)]] as [string, (l: number) => string, (l: number) => number | undefined]] : []),
  ]
  return (
    <div className="space-y-2 pt-2 border-t border-gray-100">
      <div className="overflow-x-auto">
        <table className="text-[11px]">
          <thead>
            <tr className="text-gray-500">
              <th className="pr-2 text-left font-normal">layer</th>
              {layers.map(l => <th key={l} className={`${cell} font-normal`}>{l}</th>)}
            </tr>
          </thead>
          <tbody>
            {rows.map(([method, show, pick]) => (
              <tr key={method} className="text-gray-600">
                <td className="pr-2 whitespace-nowrap">
                  <button disabled={disabled} className="hover:underline text-blue-700 disabled:text-gray-500"
                    title={method === 'held-out best' ? "Take every layer's best held-out k (chosen on the held-out data, so selection-biased)"
                      : `Take every layer's ${method} suggestion`}
                    onClick={() => setKs(layers.map((l, i) => pick(l) ?? ks[i]))}>{method}</button>
                </td>
                {layers.map(l => <td key={l} className={cell}>{show(l)}</td>)}
              </tr>
            ))}
            <tr>
              <td className="pr-2 font-medium text-gray-800">k</td>
              {layers.map((l, i) => (
                <td key={l} className="px-0.5">
                  <input type="number" min={1} max={50} value={ks[i] ?? ''} disabled={disabled}
                    onChange={e => setKs(old => old.map((k, j) => (j === i ? Number(e.target.value) || 1 : k)))}
                    className={`w-9 px-0.5 py-0.5 text-[11px] text-center border rounded ${ks[i] !== lens.k_per_layer?.[i]
                      ? 'border-blue-400 bg-blue-50' : 'border-gray-300'}`} />
                </td>
              ))}
            </tr>
          </tbody>
        </table>
      </div>
      <div className="flex flex-wrap items-center gap-3 text-xs">
        <button disabled={disabled || busy || !changed}
          onClick={() => act(() => apiClient.newLensVersion(session, lens.name, { k_per_layer: ks }))}
          className="px-2 py-1 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-300">
          Cut a new version with these k
        </button>
        {changed && <button onClick={() => setKs(lens.k_per_layer ?? [])} className="text-gray-600 hover:underline">reset</button>}
        <span className="text-gray-300">|</span>
        {saved ? (
          <span className="text-green-700">{lens.current} is saved</span>
        ) : (
          <>
            <input value={keywords} onChange={e => setKeywords(e.target.value)} disabled={disabled || busy}
              placeholder="keywords, comma separated" className="px-1.5 py-0.5 border border-gray-300 rounded w-56" />
            <button disabled={disabled || busy || changed || !lens.current}
              title={changed ? 'Cut the new version first, or reset' : 'Freeze this version and copy its records into the repo'}
              onClick={() => act(() => apiClient.saveLensVersion(session, lens.name, lens.current ?? '',
                keywords.split(',').map(w => w.trim()).filter(Boolean)))}
              className="px-2 py-1 rounded border border-green-600 text-green-700 hover:bg-green-50 disabled:border-gray-300 disabled:text-gray-400">
              Save {lens.current}
            </button>
          </>
        )}
      </div>
      {error && <p className="text-xs text-red-600">{error}</p>}
    </div>
  )
}
